import sys
import uuid
import copy
import re

from six import with_metaclass

from .exception import *
from .statement import Statement
from .config import GRAPH_VARIABLE


_PREDICATES = {}
MODULE = sys.modules[__name__]


class LinkList(object):
    top = None
    bottom = None

    def add(self, link):
        self.bottom.next = link
        self.bottom = link

        return self

    def remove(self, link, drop_after=False):
        next = None
        token = self.top

        while token:
            if link == token:
                if drop_after:
                    token.bottom = None
                    break
                else:
                    token.bottom = token.next.next if token.next else None

            token = token.next

        return self

    def can_use(self, prev, link):
        return True

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        token = self.top
        prev = token
        tokens = []
        variable = ''

        """
        prepare the gremlin string
            use the token's concat value only if the preceeding token is
            not Raw or an empty string (this happens when the graph variable
            is set to ''
        """
        while token:
            string = str(token)

            if len(tokens) and token.concat and self.can_use(prev, token):
                if type(prev) == GraphVariable:
                    append = len(tokens[-1]) > 0
                else:
                    append = True

                if append:
                    tokens.append(token.concat)

            tokens.append(string)

            prev = token
            token = token.next

        return '{}{}'.format(variable, ''.join(tokens))


class Link(object):
    next = None


class Param(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Gremlin(LinkList):
    PARAM_PREFIX = 'GPY_PARAM'

    def __init__(self, graph_variable=GRAPH_VARIABLE, parent=None):
        self.gv = graph_variable
        self.top = GraphVariable(self, graph_variable)
        self._gremlins = []
        self.parent = None

        self.reset()

        if parent:
            self.set_parent_gremlin(parent)

    def reset(self):
        if self.parent:
            self.parent.reset()

        for gremlin in self._gremlins:
            gremlin.reset()

        self.parent = None
        self.bottom = self.top
        self.bound_params = {}
        self.bound_param = str(uuid.uuid4())[-5:]
        self.bound_count = 0
        self.top.next = None
        self.return_var = None
        self._gremlins = []

        return self.set_graph_variable(self.gv)

    @property
    def stack_bound_params(self):
        parent = self.parent
        params = copy.deepcopy(self.bound_params)

        while parent:
            params.update(parent.stack_bound_params)
            parent = parent.parent

        return params

    def can_use(self, prev, link):
        return type(prev) is not Raw

    def __unicode__(self):
        string = super(Gremlin, self).__unicode__()
        variable = ''

        if self.return_var is not None:
            variable = '{} = '.format(self.return_var)

        return '{}{}'.format(variable, string)

    def __getattr__(self, attr):
        attr = Attribute(self, attr)

        return self.add_token(attr)

    def __call__(self, *args):
        func_name = str(self.bottom)

        if len(args) and issubclass(type(args[-1]), Predicate):
            func = UnboudFunction(self, func_name, *args)
        elif func_name in _PREDICATES.keys() and hasattr(MODULE, func_name):
            pred = getattr(MODULE, func_name)(*args, gremlin=self)
            func = pred.bottom
        else:
            func = Function(self, func_name, *args)

        self.bottom.next = func

        return self.remove_token(self.bottom).add_token(func)

    def __getitem__(self, val):
        # TODO: clean this up
        if type(val) is not slice:
            val = val if type(val) is list or type(val) is tuple else [val]

            try:
                start = val[0]
            except Exception as e:
                start = None

            try:
                end = val[1]
            except Exception as e:
                end = None

            try:
                step = val[2]
            except Exception as e:
                step = None

            val = slice(start, end, step)
        index = Index(self, val)

        return self.add_token(index)

    def set_parent_gremlin(self, gremlin):
        self.parent = gremlin

        self._gremlins.append(gremlin)
        gremlin.bind_params(self.bound_params)

        return self.bind_params(gremlin.bound_params)

    def bind_params(self, params=None):
        if params is None:
            params = []

        if isinstance(params, dict):
            for name, value in params.items():
                self.bind_param(value, name)
        else:
            for value in params:
                self.bind_param(value)

        return self.bound_params

    def bind_param(self, value, name=None):
        self.bound_count += 1

        if isinstance(value, Param):
            name = value.name
            value = value.value
        elif not name and value in self.stack_bound_params.values():
            for n, v in self.bound_params.items():
                if v == value:
                    name = n
                    break
        elif not name and value in self.stack_bound_params.keys():
            for n, v in self.bound_params.items():
                if n == value:
                    name = n
                    value = v
                    break

        if name is None:
            name = '{}_{}_{}'.format(self.PARAM_PREFIX, self.bound_param,
                                     self.bound_count)

        self.bound_params[name] = value

        if self.parent is not None:
            self.parent.bind_param(value, name)

        return (name, value)

    def range(self, start, end):
        return self.func_raw_unbound('range', *(start, end))

    def unbound(self, function, *args):
        unbound = UnboudFunction(self, function, *args)

        return self.add_token(unbound)

    def func(self, function, *args):
        func = Function(self, function, *args)

        return self.add_token(func)

    def func_raw(self, function, *args):
        func_raw = FunctionRaw(self, function, *args)

        return self.add_token(func_raw)

    def func_raw_unbound(self, function, *args):
        func_raw = UnboudFunctionRaw(self, function, *args)

        return self.add_token(func_raw)

    def close(self, value, *args):
        if args:
            close = ClosureArguments(self, value, *args)
        else:
            close = Closure(self, value)

        return self.add_token(close)

    def raw(self, value):
        raw = Raw(self, value)

        return self.add_token(raw)

    def add_token(self, token):
        self.bottom.next = token
        self.bottom = token

        return self

    def remove_token(self, remove):
        token = self.top

        while token:
            if token.next == remove:
                token.next = token.next.next
                break

            token = token.next

        return self

    def set_ret_variable(self, return_var=None):
        self.return_var = return_var

        return self

    def set_graph_variable(self, graph_variable='g'):
        if not graph_variable:
            graph_variable = ''

        self.top.value = graph_variable

        return self

    def apply_statement(self, statement):
        statement.set_gremlin(self).build()

        return self


class _Tokenable(object):

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return self.value

    def apply_statement(self, statement):
        if hasattr(statement, 'gremlin') == False:
            statement.set_gremlin(Gremlin())

        statement.gremlin.set_parent_gremlin(self.gremlin)

        return statement

    def fix_value(self, value):
        if isinstance(value, Param):
            return self.gremlin.bind_param(value)[0]
        elif isinstance(value, Token):
            return value
        elif isinstance(value, Predicate):
            value.gremlin = Gremlin(self.gremlin.gv)
            value.set_parent_gremlin(self.gremlin)

            return str(value)
        elif isinstance(value, (list, tuple)):
            value = [self.fix_value(a) for a in value]

            return value if isinstance(value, list) else tuple(value)
        elif issubclass(type(value), Statement):
            self.apply_statement(value)
            return str(value)
        elif isinstance(value, Gremlin):
            value.set_parent_gremlin(self.gremlin)

            return str(value)
        else:
            return value


class Token(Link, _Tokenable):
    next = None
    value = None
    args = []
    concat = ''

    def __init__(self, gremlin, value, *args):
        self.gremlin = gremlin
        self.value = self.fix_value(value)
        self.args = list(args)


class GraphVariable(Token):

    def __unicode__(self):
        if self.value == '':
            self.concat = ''

        return self.value


class Attribute(Token):
    concat = '.'


class Function(Token):
    """
    class used to create a Gremlin function
    it assumes that the last argument passed to the function is the only thing
    that will be bound
    if you need more than the last argument bound, you can do:

        g = Gremlin()
        value1 = g.bind_param('value1')[0]
        value2 = g.bind_param('value2')[0]
        g.functionName('not_bound', value1, value2, ...)
    """
    concat = '.'

    def __unicode__(self):
        params = []

        if len(self.args):
            for arg in self.args:
                if issubclass(type(arg), Statement):
                    self.apply_statment(arg)

                    params.append(str(arg))
                elif issubclass(type(arg), Gremlin):
                    arg.set_parent_gremlin(self.gremlin)

                    params.append(str(arg))
                elif isinstance(arg, Param):
                    params.append(self.gremlin.bind_param(arg)[0])
                else:
                    params.append(self.gremlin.bind_param(arg)[0])

        return '{}({})'.format(self.value, ', '.join(params))


class FunctionRaw(Function):
    concat = ''


class UnboudFunction(Token):
    concat = '.'

    def __unicode__(self):
        args = [self.fix_value(a) for a in self.args]

        return '{}({})'.format(self.value, ', '.join(args))


class UnboudFunctionRaw(UnboudFunction):
    concat = ''


class Index(Token):

    def __unicode__(self):
        if self.value.stop is not None:
            index = '[{}..{}]'.format(self.value.start, self.value.stop)
        else:
            index = '[{}]'.format(self.value.start)

        return index


class Closure(Token):

    def __unicode__(self):
        if issubclass(type(self.value), Statement):
            self.gremlin.apply_statment(self.value)

            self.value = str(self.gremlin)
        elif issubclass(type(self.value), Gremlin):
            self.value.set_parent_gremlin(self.gremlin)

        return '{%s}' % str(self.value)


class ClosureArguments(Token):

    def __unicode__(self):
        if issubclass(type(bound), Statement):
            self.gremlin.apply_statment(self.value)

            self.value = str(self.gremlin)
        elif issubclass(type(self.value), Gremlin):
            self.value.set_parent_gremlin(self.gremlin)

        return '{{} -> {}}'.format(','.join(self.args), str(self.value))


class Raw(Token):

    def __unicode__(self):
        if issubclass(type(self.value), Statement):
            self.apply_statement(self.value)

            self.value = str(self.value)
        elif issubclass(type(self.value), Gremlin):
            self.value.set_parent_gremlin(self.gremlin)

        return str(self.value)


class _MetaPredicate(type):

    def __new__(cls, name, bases, attrs):
        cls = super(_MetaPredicate, cls).__new__(cls, name, bases, attrs)
        _PREDICATES[name] = cls

        return cls


class Predicate(with_metaclass(_MetaPredicate, Gremlin)):

    def __init__(self, *args, **kwargs):
        gremlin = kwargs.get('gremlin', None)
        super(Predicate, self).__init__(None, gremlin)

        self.args = args
        self.func(self._function, *args)

    @property
    def _function(self, *args):
        return str(self.__class__.__name__)


class p(Predicate):
    pass


class pp(Predicate):
    pass


class eq(Predicate):
    pass


class neq(Predicate):
    pass


class lt(Predicate):
    pass


class lte(Predicate):
    pass


class gt(Predicate):
    pass


class gte(Predicate):
    pass


class inside(Predicate):
    pass


class NOT(Predicate):
    """Allows for easy use of 'not' in steps"""

    @property
    def _function(self, *args):
        return 'not'


class outside(Predicate):
    pass


class between(Predicate):
    pass


class within(Predicate):
    pass


class without(Predicate):
    pass


class IS(Predicate):
    """Allows for easy use of 'is' in steps"""

    @property
    def _function(self, *args):
        return 'is'


class select(Predicate):
    """Allows for easy use of select steps"""
    pass


class AS(Predicate):
    """Allows for easy use of as in steps"""

    @property
    def _function(self, *args):
        return 'as'


class AND(Predicate):
    """Allows for easy use of and in steps"""

    @property
    def _function(self, *args):
        return 'and'


class IN(Predicate):
    """Allows for easy use of 'in' in steps"""

    @property
    def _function(self, *args):
        return 'in'


def _(method, *args):
    """method used to create predicates dynamically"""
    kls = type(method, (Predicate,), {})

    return kls(*args)


class Anon(object):
    """class used to create new Gremlin instances every time an anonymous
    traversal is started with the __"""

    def __init__(self):
        pass

    def __getattr__(self, attr):
        gremlin = Gremlin('__')

        getattr(gremlin, attr)

        return gremlin


__ = Anon()
