import unittest
from random import randrange
from gremlinpy.gremlin import Gremlin, Function, UnboudFunction

def get_dict_key(dict, value):
    for k, v in dict.iteritems():
        if v == value:
            return k
    
    return None
    
class GremlinTests(unittest.TestCase):
    def test_gremlin_instance(self):
        g = Gremlin()
        
        self.assertTrue(type(g) == Gremlin)
        
    def test_can_drop_graph_variable(self):
        g = Gremlin().set_graph_variable('')
        
        self.assertTrue(str(g) == '')

    def test_can_change_graph_variable(self):
        g = Gremlin().set_graph_variable('x')
        
        self.assertTrue(str(g) == 'x')
        
    def test_can_add_one_attribute(self):
        g        = Gremlin().a
        expected = 'g.a'

        self.assertTrue(str(g) == expected)
        
    def test_can_add_one_attribute_and_drop_graph_variable(self):
        g        = Gremlin().a.set_graph_variable('')
        expected = 'a'

        self.assertTrue(str(g) == expected)
        
    def test_can_add_two_attributes(self):
        g        = Gremlin().a.b
        expected = 'g.a.b'

        self.assertTrue(str(g) == expected)
        
    def test_can_add_random_attributes(self):
        g   = Gremlin()
        exp = ['g']

        for x in range(1, randrange(5, 22)):
            getattr(g, str(x))
            exp.append(str(x))
            
        expected = '.'.join(exp)

        self.assertTrue(str(g) == expected)
        
    def test_can_add_random_attributes_drop_graph_variable(self):
        g   = Gremlin().set_graph_variable('')
        exp = []

        for x in range(1, randrange(5, 22)):
            getattr(g, str(x))
            exp.append(str(x))
            
        expected = '.'.join(exp)

        self.assertTrue(str(g) == expected)
        
    def test_can_add_return_variable(self):
        g = Gremlin()
        v = 'ret_var'
        
        g.set_ret_variable(v).function()
        
        expected = '%s = g.function()' % v
        script = str(g)
        
        self.assertEquals(expected, script)
        
    def test_can_add_and_remove_return_variable(self):
        g = Gremlin()
        v = 'ret_var'
        
        g.set_ret_variable(v).function().set_ret_variable(None)
        
        expected = 'g.function()'
        script = str(g)
        
        self.assertEquals(expected, script)
        
    def test_can_add_functon(self):
        g = Gremlin().function()
        e = 'g.function()'
        
        self.assertEquals(str(g), e)
        self.assertEquals(len(g.bound_params), 0)
        
    def test_can_add_unbound_function(self):
        g = Gremlin().unbound('mark')
        e = 'g.mark()'
        
        self.assertEquals(str(g), e)
        self.assertEquals(len(g.bound_params), 0)
        
    def test_can_add_raw_function(self):
        g = Gremlin().func_raw('mark')
        e = 'gmark()'
        
        self.assertEquals(str(g), e)
        self.assertEquals(len(g.bound_params), 0)
        
    def test_can_add_functon_one_arg(self):
        g           = Gremlin().function('arg')
        string      = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected    = 'g.function(%s)' % bind

        self.assertTrue(string == expected)
        self.assertTrue(len(g.bound_params) == 1)
        
    def test_can_add_unbound_functon_one_arg(self):
        g        = Gremlin().unbound('function', 'arg')
        string   = str(g)
        expected = 'g.function(arg)'
        
        self.assertEquals(string, expected)
        self.assertEquals(len(g.bound_params), 0)
        
    def test_can_add_raw_functon_one_arg(self):
        g        = Gremlin().func_raw('function', 'arg')
        string   = str(g)

        bind, value = g.bound_params.copy().popitem()
        expected = 'gfunction(%s)' % bind

        self.assertEquals(string, expected)
        self.assertEquals(len(g.bound_params), 1)
        
    def test_can_add_functon_two_args(self):
        g           = Gremlin().function('one', 'two')
        string      = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected    = 'g.function(one, %s)' % bind

        self.assertTrue(string == expected)
        self.assertTrue(len(g.bound_params) == 1) 
    
    def test_can_add_unbound_functon_two_args(self):
        g        = Gremlin().unbound('function', 'arg', 'two')
        string   = str(g)
        expected = 'g.function(arg, two)'
        
        self.assertEquals(string, expected)
        self.assertEquals(len(g.bound_params), 0)
        
    def test_can_add_raw_functon_two_args(self):
        g        = Gremlin().func_raw('function', 'arg', 'two')
        string   = str(g)

        bind, value = g.bound_params.copy().popitem()
        expected = 'gfunction(arg, %s)' % bind

        self.assertEquals(string, expected)
        self.assertEquals(len(g.bound_params), 1)
        
    def test_can_add_functon_three_args(self):
        g           = Gremlin().function('one', 'two', 'three')
        string      = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected    = 'g.function(one, two, %s)' % bind

        self.assertTrue(string == expected)
        self.assertTrue(len(g.bound_params) == 1)
    
    def test_can_add_functon_manually_bind_one_arg(self):
        g     = Gremlin()
        bound = g.bind_param('arg')
        
        g.function(bound[0])
        
        string      = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected    = 'g.function(%s)' % bind

        self.assertTrue(string == expected)
        self.assertTrue(bind == bound[0])
        self.assertTrue(value == bound[1])
        self.assertTrue(len(g.bound_params) == 1)
    
    def test_can_add_functon_manually_bind_two_args(self):
        g      = Gremlin()
        bound  = g.bind_param('arg')
        bound2 = g.bind_param('arg2')
        
        g.function(bound[0], bound2[0])
        
        string   = str(g)
        expected = 'g.function(%s, %s)' % (bound[0], bound2[0])

        self.assertTrue(string == expected)
        self.assertTrue(len(g.bound_params) == 2)
        
    def test_can_add_function_with_arg_before_attribute(self):
        g = Gremlin()
        
        g.function('val').a
        
        string      = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected    = 'g.function(%s).a' % bind

        self.assertTrue(string == expected)
        self.assertTrue(len(g.bound_params) == 1)
        
    def test_can_add_function_with_arg_after_attribute(self):
        g = Gremlin()
        
        g.a.function('val')
        
        string      = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected    = 'g.a.function(%s)' % bind

        self.assertTrue(string == expected)
        self.assertTrue(len(g.bound_params) == 1)
        
    def test_can_add_function_with_arg_after_attribute_drop_graph_var(self):
        g = Gremlin().set_graph_variable('')
        
        g.a.function('val')
        
        string      = str(g)
        bind, value = g.bound_params.copy().popitem()
        expected    = 'a.function(%s)' % bind
        
        self.assertTrue(string == expected)
        self.assertTrue(len(g.bound_params) == 1)
        
    def test_can_add_function_where_no_params_are_bound(self):
        g = Gremlin()
        
        g.unbound('func', 'val1', 'val2')
        
        expected = 'g.func(val1, val2)'
        
        self.assertTrue(str(g) == expected)
        self.assertTrue(len(g.bound_params) == 0)
        
    def test_can_add_function_where_no_params_are_bound_and_func_with_bound_params(self):
        g = Gremlin()
        
        g.unbound('func', 'val1', 'val2').isbound('hello')
        
        s        = str(g)
        params   = g.bound_params
        hello    = get_dict_key(params, 'hello')
        expected = 'g.func(val1, val2).isbound(%s)' % hello

        self.assertTrue(str(g) == expected)
        self.assertTrue(len(g.bound_params) == 1)
        
    def test_can_add_function_with_closure(self):
        g = Gremlin()
        
        g.condition('x').close('body')
        
        s        = str(g)
        params   = g.bound_params
        x        = get_dict_key(params, 'x')
        expected = 'g.condition(%s){body}' % x
        
        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 1)
        
    def test_can_add_an_index_with_single_value(self):
        g = Gremlin()
        
        g.func()[1]
        
        s = str(g)
        expected = 'g.func()[1]'
        
        self.assertTrue(s == expected)
    
    def test_can_add_an_index_with_range(self):
        g = Gremlin()
        
        g.func()[1:2]
        
        s = str(g)
        expected = 'g.func()[1..2]'
        
        self.assertTrue(s == expected)
        
    def test_can_add_an_index_after_closure(self):
        g = Gremlin()
        
        g.condition('x').close('body')[12:44]
        
        s        = str(g)
        params   = g.bound_params
        x        = get_dict_key(params, 'x')
        expected = 'g.condition(%s){body}[12..44]' % x
        
        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 1)
        
    def test_can_add_raw_after_function(self):
        g = Gremlin()
        r = '--raw-text--'
        
        g.func().raw(r)
        
        s        = str(g)
        params   = g.bound_params
        expected = 'g.func()%s' % r
        
        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 0)
        
    def test_can_add_raw_drop_graph_variable(self):
        g = Gremlin()
        r = '--raw-text--'
        
        g.raw(r).set_graph_variable('')
        
        s        = str(g)
        params   = g.bound_params
        expected = '%s' % r
        
        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 0)
        
    def test_can_add_raw_between_functions(self):
        g = Gremlin()
        r = '--raw-text--'
        a = 'arg'
        
        g.func().raw(r).func2(a)
        
        s        = str(g)
        params   = g.bound_params
        arg      = get_dict_key(params, a)
        expected = 'g.func()%sfunc2(%s)' % (r, arg)
        
        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 1)
        
    def test_can_add_raw_after_closure(self):
        g = Gremlin()
        r = '--raw-text--'
        c = '[[[]]]'
        
        g.func().close(c).raw(r)
        
        s        = str(g)
        params   = g.bound_params
        expected = 'g.func(){%s}%s' % (c, r)
        
        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 0)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_with_args(self):
        g = Gremlin();
        init = Function(g, '__init__', ['arg'])

        g.add_token(init)
        
        s        = str(g)
        params   = g.bound_params
        arg      = get_dict_key(params, 'arg')
        expected = 'g.__init__(%s)' % arg
        
        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 1)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_with_args_after_other_calls(self):
        g = Gremlin();
        args = ['arg', 'LOOK', 'AT']
        init = Function(g, '__init__', [args[0]])

        g.look(args[1]).at(args[2]).close('--this--').add_token(init)
        
        s        = str(g)
        params   = g.bound_params
        arg      = get_dict_key(params, args[0])
        look     = get_dict_key(params, args[1])
        at       = get_dict_key(params, args[2])
        expected = 'g.look(%s).at(%s){--this--}.__init__(%s)' % (look, at, arg)

        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 3)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_without_args(self):
        g = Gremlin();
        unbound = ['arg', '2']
        init = UnboudFunction(g, '__init__', unbound)

        g.add_token(init)
        
        s        = str(g)
        params   = g.bound_params
        expected = 'g.__init__(%s, %s)' % (unbound[0], unbound[1])

        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 0)

    def test_can_add_a_reserved_word_as_apart_of_the_query_as_function_without_args_after_other_calls(self):
        g = Gremlin();
        unbound = ['arg', '2']
        arg = 'some_arg'
        init = UnboudFunction(g, '__init__', unbound)
        
        g.someFunc(arg).add_token(init)
        
        s        = str(g)
        params   = g.bound_params
        expected = 'g.someFunc(%s).__init__(%s, %s)' % (get_dict_key(params, arg), unbound[0], unbound[1])

        self.assertTrue(s == expected)
        self.assertTrue(len(params) == 1)


class GremlinInjectionTests(unittest.TestCase):
    def test_can_nest_gremlin(self):
        g = Gremlin()
        n = Gremlin()
        
        g.nest(n.nested())
        
        expected = 'g.nest(g.nested())'
        string   = str(g)
        params   = g.bound_params
        
        self.assertTrue(expected == string)
        self.assertTrue(len(params) == 0)
        
    def test_can_nest_double_nest_gremlin(self):
        g = Gremlin()
        n = Gremlin()
        d = Gremlin()
        
        g.nest(n.nested(d.deep()))
        
        expected = 'g.nest(g.nested(g.deep()))'
        string   = str(g)
        params   = g.bound_params
        
        self.assertTrue(expected == string)
        self.assertTrue(len(params) == 0)
        
    def test_can_nest_with_bound_params(self):
        g = Gremlin()
        d = {'name': 'parent'}
        n = Gremlin()
        p = {'prop': 'child'}
        
        n.set_graph_variable('').setSubProp('prop', p['prop'])
        g.func('name', d['name']).nest(n)
        
        string   = str(g)
        params   = g.bound_params
        name     = get_dict_key(params, 'parent')
        child    = get_dict_key(params, 'child')
        expected = 'g.func(name, %s).nest(setSubProp(prop, %s))' % (name, child)

        self.assertTrue(expected == string)
        self.assertTrue(len(params) == 2)


if __name__ == '__main__':
    unittest.main()
