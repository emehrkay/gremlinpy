from random import randrange, random
import unittest

from gremlinpy.gremlin import *
from gremlinpy.gremlin import _


def get_dict_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k

    return None


class GremlinTests(unittest.TestCase):

    def test_gremlin_instance(self):
        g = Gremlin()

        self.assertEqual(type(g), Gremlin)

    def test_can_drop_graph_variable(self):
        g = Gremlin().set_graph_variable('')

        self.assertEqual(str(g), '')

    def test_can_change_graph_variable(self):
        g = Gremlin().set_graph_variable('x')

        self.assertEqual(str(g), 'x')

    def test_can_add_one_attribute(self):
        g = Gremlin().a
        expected = 'g.a'

        self.assertEqual(str(g), expected)

    def test_can_add_one_attribute_and_drop_graph_variable(self):
        g = Gremlin().a.set_graph_variable('')
        expected = 'a'

        self.assertEqual(str(g), expected)

    def test_can_add_two_attributes(self):
        g = Gremlin().a.b
        expected = 'g.a.b'

        self.assertEqual(str(g), expected)

    def test_can_add_random_attributes(self):
        g = Gremlin()
        exp = ['g']

        for x in range(1, randrange(5, 22)):
            getattr(g, str(x))
            exp.append(str(x))

        expected = '.'.join(exp)

        self.assertEqual(str(g), expected)

    def test_can_add_random_attributes_drop_graph_variable(self):
        g = Gremlin().set_graph_variable('')
        exp = []

        for x in range(1, randrange(5, 22)):
            getattr(g, str(x))
            exp.append(str(x))

        expected = '.'.join(exp)

        self.assertEqual(str(g), expected)

    def test_can_add_return_variable(self):
        g = Gremlin()
        v = 'ret_var'

        g.set_ret_variable(v).function()

        expected = '%s = g.function()' % v
        script = str(g)

        self.assertEqual(expected, script)

    def test_can_add_and_remove_return_variable(self):
        g = Gremlin()
        v = 'ret_var'

        g.set_ret_variable(v).function().set_ret_variable(None)

        expected = 'g.function()'
        script = str(g)

        self.assertEqual(expected, script)

    def test_can_add_functon(self):
        g = Gremlin().function()
        e = 'g.function()'

        self.assertEqual(str(g), e)
        self.assertEqual(len(g.bound_params), 0)

    def test_can_add_unbound_function(self):
        g = Gremlin().unbound('mark')
        e = 'g.mark()'

        self.assertEqual(str(g), e)
        self.assertEqual(len(g.bound_params), 0)

    def test_can_add_raw_function(self):
        g = Gremlin().func_raw('mark')
        e = 'gmark()'

        self.assertEqual(str(g), e)
        self.assertEqual(len(g.bound_params), 0)

    def test_can_add_functon_one_arg(self):
        g = Gremlin().function('arg')
        string = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected = 'g.function(%s)' % bind

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 1)

    def test_will_bind_all_params_in_function(self):
        g = Gremlin().some_function('one', 'two', 'three')
        string = str(g)
        params = g.bound_params
        one = get_dict_key(params, 'one')
        two = get_dict_key(params, 'two')
        three = get_dict_key(params, 'three')
        expected = 'g.some_function({}, {}, {})'.format(one, two, three)

        self.assertEqual(3, len(params))
        self.assertEqual(expected, string)

    def test_will_bind_all_params_in_function_with_mixed_manually_bound_args(self):
        g = Gremlin()
        b_one = Param('one', 'one')
        b_two = g.bind_param('two', 'two')

        g.some_function(b_one, b_two[0], 'three')

        string = str(g)
        params = g.bound_params
        one = get_dict_key(params, 'one')
        two = get_dict_key(params, 'two')
        three = get_dict_key(params, 'three')
        expected = 'g.some_function({}, {}, {})'.format(one, two, three)

        self.assertEqual(3, len(params))
        self.assertEqual(expected, string)

    def test_can_add_fuctions_binding_same_value_with_one_bound_param(self):
        val = 'random' + str(random())
        g = Gremlin()
        g.func1(val).func2(val)
        s = str(g)
        params = g.bound_params
        one = get_dict_key(params, val)
        two = get_dict_key(params, val)
        expected = 'g.func1({}).func2({})'.format(one, two)

        self.assertEqual(1, len(params))
        self.assertEqual(expected, s)

    def test_can_add_unbound_functon_one_arg(self):
        g = Gremlin().unbound('function', 'arg')
        string = str(g)
        expected = 'g.function(arg)'

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 0)

    def test_can_add_raw_functon_one_arg(self):
        g = Gremlin().func_raw('function', 'arg')
        string = str(g)

        bind, value = g.bound_params.copy().popitem()
        expected = 'gfunction(%s)' % bind

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 1)

    def test_can_add_functon_two_args(self):
        g = Gremlin().function('one', 'two')
        string = str(g)
        params = g.bound_params
        one = get_dict_key(params, 'one')
        two = get_dict_key(params, 'two')
        expected = 'g.function({}, {})'.format(one, two)

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 2)

    def test_can_add_unbound_functon_two_args(self):
        g = Gremlin().unbound('function', 'arg', 'two')
        string = str(g)
        expected = 'g.function(arg, two)'

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 0)

    def test_can_add_raw_functon_two_args(self):
        g = Gremlin().func_raw('function', 'arg', 'two')
        string = str(g)
        params = g.bound_params
        arg = get_dict_key(params, 'arg')
        two = get_dict_key(params, 'two')
        expected = 'gfunction({}, {})'.format(arg, two)

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 2)

    def test_can_add_functon_three_args(self):
        g = Gremlin().function('one', 'two', 'three')
        string = str(g)
        params = g.bound_params
        one = get_dict_key(params, 'one')
        two = get_dict_key(params, 'two')
        three = get_dict_key(params, 'three')
        expected = 'g.function({}, {}, {})'.format(one, two, three)

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 3)

    def test_can_add_functon_manually_bind_one_arg(self):
        g = Gremlin()
        bound = g.bind_param('arg')

        g.function(bound[0])

        string = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected = 'g.function(%s)' % bind

        self.assertEqual(string, expected)
        self.assertEqual(bind, bound[0])
        self.assertEqual(value, bound[1])
        self.assertEqual(len(g.bound_params), 1)

    def test_can_add_functon_manually_bind_two_args(self):
        g = Gremlin()
        bound = g.bind_param('arg')
        bound2 = g.bind_param('arg2')

        g.function(bound[0], bound2[0])

        string = str(g)
        expected = 'g.function(%s, %s)' % (bound[0], bound2[0])

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 2)

    def test_can_add_function_with_arg_before_attribute(self):
        g = Gremlin()

        g.function('val').a

        string = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected = 'g.function(%s).a' % bind

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 1)

    def test_can_add_function_with_arg_after_attribute(self):
        g = Gremlin()

        g.a.function('val')

        string = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected = 'g.a.function(%s)' % bind

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 1)

    def test_can_add_function_with_arg_after_attribute_drop_graph_var(self):
        g = Gremlin().set_graph_variable('')

        g.a.function('val')

        string = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected = 'a.function(%s)' % bind

        self.assertEqual(string, expected)
        self.assertEqual(len(g.bound_params), 1)

    def test_can_add_function_where_no_params_are_bound(self):
        g = Gremlin()

        g.unbound('function', 'val1', 'val2')

        expected = 'g.function(val1, val2)'

        self.assertEqual(str(g), expected)
        self.assertEqual(len(g.bound_params), 0)

    def test_can_add_function_where_no_params_are_bound_and_func_with_bound_params(self):
        g = Gremlin()

        g.unbound('function', 'val1', 'val2').isbound('hello')

        s = str(g)
        params = g.bound_params
        hello = get_dict_key(params, 'hello')
        expected = 'g.function(val1, val2).isbound(%s)' % hello

        self.assertEqual(s, expected)
        self.assertEqual(len(g.bound_params), 1)

    def test_can_add_function_with_closure(self):
        g = Gremlin()

        g.condition('x').close('body')

        s = str(g)
        params = g.bound_params
        x = get_dict_key(params, 'x')
        expected = 'g.condition(%s){body}' % x

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 1)

    def test_can_add_an_index_with_single_value(self):
        g = Gremlin()

        g.function()[1]

        s = str(g)
        expected = 'g.function()[1]'

        self.assertEqual(s, expected)

    def test_can_add_an_index_with_range(self):
        g = Gremlin()

        g.function()[1:2]

        s = str(g)
        expected = 'g.function()[1..2]'

        self.assertEqual(s, expected)

    def test_can_add_an_index_after_closure(self):
        g = Gremlin()

        g.condition('x').close('body')[12:44]

        s = str(g)
        params = g.bound_params
        x = get_dict_key(params, 'x')
        expected = 'g.condition(%s){body}[12..44]' % x

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 1)

    def test_can_add_raw_after_function(self):
        g = Gremlin()
        r = '--raw-text--'

        g.function().raw(r)

        s = str(g)
        params = g.bound_params
        expected = 'g.function()%s' % r

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 0)

    def test_can_add_raw_drop_graph_variable(self):
        g = Gremlin()
        r = '--raw-text--'

        g.raw(r).set_graph_variable('')

        s = str(g)
        params = g.bound_params
        expected = '%s' % r

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 0)

    def test_can_add_raw_between_functions(self):
        g = Gremlin()
        r = '--raw-text--'
        a = 'arg'

        g.function().raw(r).func2(a)

        s = str(g)
        params = g.bound_params
        arg = get_dict_key(params, a)
        expected = 'g.function()%sfunc2(%s)' % (r, arg)

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 1)

    def test_can_add_raw_after_closure(self):
        g = Gremlin()
        r = '--raw-text--'
        c = '[[[]]]'

        g.function().close(c).raw(r)

        s        = str(g)
        params   = g.bound_params
        expected = 'g.function(){%s}%s' % (c, r)

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 0)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_with_args(self):
        g = Gremlin();
        init = Function(g, '__init__', 'arg')

        g.add_token(init)

        s = str(g)
        params = g.bound_params
        arg = get_dict_key(params, 'arg')
        expected = 'g.__init__(%s)' % arg

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 1)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_with_args_after_other_calls(self):
        g = Gremlin();
        args = ['arg', 'LOOK', 'AT']
        init = Function(g, '__init__', args[0])

        g.look(args[1]).at(args[2]).close('--this--').add_token(init)

        s = str(g)
        params = g.bound_params
        arg = get_dict_key(params, args[0])
        look = get_dict_key(params, args[1])
        at = get_dict_key(params, args[2])
        expected = 'g.look(%s).at(%s){--this--}.__init__(%s)' % (look, at, arg)

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 3)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_without_args(self):
        g = Gremlin();
        unbound = ['arg', '2']
        init = UnboudFunction(g, '__init__', *unbound)

        g.add_token(init)

        s = str(g)
        params = g.bound_params
        expected = 'g.__init__(%s, %s)' % (unbound[0], unbound[1])

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 0)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_without_args_after_other_calls(self):
        g = Gremlin();
        unbound = ['arg', '2']
        arg = 'some_arg'
        init = UnboudFunction(g, '__init__', *unbound)

        g.someFunc(arg).add_token(init)

        s = str(g)
        params = g.bound_params
        expected = 'g.someFunc(%s).__init__(%s, %s)' % (get_dict_key(params, arg), unbound[0], unbound[1])

        self.assertEqual(s, expected)
        self.assertEqual(len(params), 1)


class GremlinInjectionTests(unittest.TestCase):

    def test_can_nest_gremlin(self):
        g = Gremlin()
        n = Gremlin()

        g.nest(n.nested())

        expected = 'g.nest(g.nested())'
        string   = str(g)
        params   = g.bound_params

        self.assertEqual(expected, string)
        self.assertEqual(len(params), 0)

    def test_can_nest_double_nest_gremlin(self):
        g = Gremlin()
        n = Gremlin()
        d = Gremlin()

        g.nest(n.nested(d.deep()))

        expected = 'g.nest(g.nested(g.deep()))'
        string = str(g)
        params = g.bound_params

        self.assertEqual(expected, string)
        self.assertEqual(len(params), 0)

    def test_can_nest_with_bound_params(self):
        g = Gremlin()
        d = {'name': 'parent'}
        n = Gremlin()
        p = {'prop': 'child'}

        n.set_graph_variable('').setSubProp('prop', p['prop'])
        g.function('name', d['name']).nest(n)

        string = str(g)
        params = g.bound_params
        name_field = get_dict_key(params, 'name')
        name = get_dict_key(params, 'parent')
        prop_field = get_dict_key(params, 'prop')
        child = get_dict_key(params, 'child')
        expected = 'g.function(%s, %s).nest(setSubProp(%s, %s))' % (name_field,
            name, prop_field, child)

        self.assertEqual(expected, string)
        self.assertEqual(len(params), 4)

    def test_can_nest_with_unbound_params_of_same_value(self):
        g = Gremlin()
        n = Gremlin()
        d = {'name': str(random()), 'age': str(random())}

        n.set_graph_variable('__').has('name', d['name'])
        n.func('age', d['age'])
        g.function('name', d['name']).nest(n)

        string = str(g)
        params = g.bound_params
        name_field = get_dict_key(params, 'name')
        name = get_dict_key(params, d['name'])
        age = get_dict_key(params, d['age'])
        expected = ("g.function({}, {})"
                    ".nest(__.has({}, {}).age({}))").format(name_field,
                        name, name_field, name, age)

        self.assertEqual(3, len(params))
        self.assertEqual(expected, string)

    def test_can_double_nest_with_unbound_params_of_same_value(self):
        g = Gremlin()
        n = Gremlin()
        nn = Gremlin()
        d = {
            'name_val': str(random()), 
            'age_val': str(random()),
        }

        nn.set_graph_variable('_').func('name', d['name_val'])
        n.set_graph_variable('__').has('name', d['name_val'])
        n.func('age', d['age_val']).nest(nn)
        g.function('name', d['name_val']).nest(n)

        string = str(g)
        params = g.bound_params
        name_field = get_dict_key(params, 'name')
        name_val = get_dict_key(params, d['name_val'])
        age_val = get_dict_key(params, d['age_val'])
        expected = ("g.function({}, {})"
                    ".nest(__.has({}, {}).age({})"
                    ".nest(_.name({})))").format(name_field, name_val,
                        name_field, name_val, age_val, name_val)

        self.assertEqual(3, len(params))
        self.assertEqual(expected, string)


class PredicateTests(unittest.TestCase):

    def test_can_pass_single_predicate_to_function(self):
        arg = str(random())
        g = Gremlin()
        g.function(lt(arg).out())

        string = str(g)
        params = g.bound_params
        argument = get_dict_key(params, arg)
        expected = 'g.function(lt(%s).out())' % (argument)

        self.assertEqual(expected, string)

    def test_can_pass_bound_param_to_predicate(self):
        g = Gremlin()
        val = 'test'+ str(random())
        param = 'param'
        bound = g.bind_param(val, param)
        pred = lt(bound[0], gremlin=g)
        expected = 'lt({})'.format(param)
        actual = str(pred)

        self.assertEqual(expected, actual)

    def test_can_pass_bound_param_to_embedded_predicate(self):
        g = Gremlin()
        val = 'test'+ str(random())
        param = 'param'
        bound = g.bind_param(val, param)
        pred = lt(bound[0], gremlin=g)
        g.function(pred)
        expected = 'g.function(lt({}))'.format(param)
        actual = str(g)

        self.assertEqual(expected, actual)

    def test_can_pass_two_predicates_to_function(self):
        arg = str(random())
        arg2 = '222_' + str(random())
        g = Gremlin()
        g.function(lt(arg).out(), lt(arg2))

        string = str(g)
        params = g.bound_params
        argument = get_dict_key(params, arg)
        argument2 = get_dict_key(params, arg2)
        expected = 'g.function(lt(%s).out(), lt(%s))' % (argument, argument2)

        self.assertEqual(expected, string)

    def test_can_nest_predicates(self):
        arg = str(random())
        arg2 = '222_' + str(random())
        g = Gremlin()
        g.function(lt(arg).out(lt(arg2)))

        string = str(g)
        params = g.bound_params
        argument = get_dict_key(params, arg)
        argument2 = get_dict_key(params, arg2)
        expected = 'g.function(lt(%s).out(lt(%s)))' % (argument, argument2)

        self.assertEqual(expected, string)

    def test_can_create_dynamic_predicate(self):
        ran = 'someFunc'+ str(random())
        pred = _(ran)
        g = Gremlin()
        g.function(pred)

        expected = 'g.function({}())'.format(ran)
        s = str(g)

        self.assertEqual(s, expected)

    def test_can_nest_dynamically_created_predicates(self):
        ran = 'someFunc'+ str(random())
        ran2 = 'outer'+ str(random())
        pred = _(ran)
        pred2 = _(ran2, pred)
        g = Gremlin()
        g.function(pred2)

        expected = 'g.function({}({}()))'.format(ran2, ran)
        s = str(g)

        self.assertEqual(s, expected)

    def test_can_start_anon_traversal(self):
        a = Anon().call()
        g = Gremlin().subAnon(a)

        string = str(g)
        params = g.bound_params
        expected = 'g.subAnon(__.call())'

        self.assertEqual(0, len(params))
        self.assertEqual(expected, string)

    def test_can_handle_problematic_predicates_in_diff_contexes(self):
        g = Gremlin().IN().AND(AS().IS().NOT())
        string = str(g)
        expected = 'g.in().and(as().is().not())'
        params = g.bound_params

        self.assertEqual(0, len(params))
        self.assertEqual(expected, string)


if __name__ == '__main__':
    unittest.main()
