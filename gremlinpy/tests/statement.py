import unittest
from gremlinpy.statement import Statement, Conditional, GetEdge, ConnectOnce
from gremlinpy.gremlin import Gremlin


def get_dict_key(dict, value):
    for k, v in dict.iteritems():
        if v == value:
            return k
    
    return None


class StatementTests(unittest.TestCase):
    def test_can_apply_statement(self):
        class statement(Statement):
            def build(self):
                g = self.gremlin
                
                g.random().statement()
                
        s = statement()
        g = Gremlin()
        
        g.apply_statement(s)
        
        string   = str(g)
        expected = 'g.random().statement()'
        
        self.assertTrue(string == expected)
        
    def test_can_apply_statement_with_args(self):
        arg = 'statement_arg'
        
        class statement(Statement):
            def build(self):
                g = self.gremlin
                
                g.statementFunction(arg)
        
        s = statement()
        g = Gremlin()
        
        g.apply_statement(s)
        
        string   = str(g)
        params   = g.bound_params
        expected = 'g.statementFunction(%s)' % get_dict_key(params, arg)
        
        self.assertTrue(string == expected)
        
    def test_can_apply_two_statements_with_args(self):
        one = 'one'
        two = 'two'
        
        class First(Statement):
            def build(self):
                g = self.gremlin
                
                g.first(one)
        
        class Second(Statement):
            def build(self):
                g = self.gremlin
                
                g.second(two)
        
        f = First()
        s = Second()
        g = Gremlin()
        
        g.apply_statement(f).apply_statement(s)
        
        string   = str(g)
        params   = g.bound_params
        arg_1    = get_dict_key(params, one)
        arg_2    = get_dict_key(params, two)
        expected = 'g.first(%s).second(%s)' % (arg_1, arg_2)
        
        self.assertTrue(string == expected)
        

class NestedStatementTests(unittest.TestCase):
    def test_can_nest_one_statement_into_another_via_unbound(self):
        class Outer(Statement):
            def build(self):
                g = self.gremlin
                i = Inner()
                
                g.unbound('outer', i)
        
        class Inner(Statement):
            def build(self):
                g = self.gremlin
                g.inner_statement
        
        g = Gremlin()
        o = Outer()
        
        g.apply_statement(o)
        
        string   = str(g)
        params   = g.bound_params
        expected = 'g.outer(g.inner_statement)'
        
        self.assertTrue(string == expected)
        self.assertTrue(len(params) == 0)
        
    def test_can_nest_one_statement_into_another_via_raw(self):
        class Outer(Statement):
            def build(self):
                g = self.gremlin
                i = Inner()
                
                g.will_be_raw.raw(i)
        
        class Inner(Statement):
            def build(self):
                g = self.gremlin
                g.inner_statement
        
        g = Gremlin()
        o = Outer()
        
        g.apply_statement(o)
        
        string   = str(g)
        params   = g.bound_params
        expected = 'g.will_be_rawg.inner_statement'
        
        self.assertTrue(string == expected)
        self.assertTrue(len(params) == 0)


class PackagedStatementTests(unittest.TestCase):
    def test_can_make_conditional_statement(self):
        pass
    
    def test_can_make_get_edge_statement(self):
        out_id = 1
        in_id  = 9
        label  = 'knows'
        g      = Gremlin()
        e      = GetEdge(out_id, in_id, label)
        
        g.apply_statement(e)
        
        string   = str(g)
        params   = g.bound_params
        oid      = get_dict_key(params, out_id)
        iid      = get_dict_key(params, in_id)
        label_b  = get_dict_key(params, label)
        as_b     = get_dict_key(params, 'vertex')
        bound    = (iid, label_b, as_b, oid, as_b)
        expected = 'g.v(%s).outE(%s).as(%s).inV.retain([g.v(%s)]).back(%s)' % bound
        
        self.assertTrue(expected == string)
        self.assertTrue(len(params) == 4)

    def test_can_make_connect_once_statement(self):
        pass


if __name__ == '__main__':
    unittest.main()