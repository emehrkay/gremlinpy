import unittest
from gremlinpy.statement import Statement, Conditional, GetEdge
from gremlinpy.gremlin import Gremlin


def get_dict_key(dict, value):
    for k, v in dict.items():
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

        string = str(g)
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

        string = str(g)
        params = g.bound_params
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

        string = str(g)
        params = g.bound_params
        arg_1 = get_dict_key(params, one)
        arg_2 = get_dict_key(params, two)
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

        string = str(g)
        params = g.bound_params
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

        string = str(g)
        params = g.bound_params
        expected = 'g.will_be_rawg.inner_statement'

        self.assertTrue(string == expected)
        self.assertTrue(len(params) == 0)


class PackagedStatementTests(unittest.TestCase):

    def test_can_make_conditional_statement(self):
        g = Gremlin()
        c = Conditional()
        cond = '1 == 2'
        body = 'nope'
        else_c = 'one doesnt equal two'

        c.set_if(cond, body)
        c.set_else(else_c)
        g.apply_statement(c)

        string = str(g)
        params = g.bound_params
        expected = 'if(%s){%s}else{%s}' % (cond, body, else_c)

        self.assertTrue(string == expected)
        self.assertTrue(len(params) == 0)

    def test_can_make_conditional_statement_with_elseif(self):
        g = Gremlin()
        c = Conditional()
        cond = '1 == 2'
        body = 'nope'
        else_i = '2 == 2'
        else_b = 'two does equal 2'
        else_c = 'one doesnt equal two'

        c.set_if(cond, body)
        c.set_elif(else_i, else_b)
        c.set_else(else_c)
        g.apply_statement(c)

        string = str(g)
        params = g.bound_params
        expected = 'if(%s){%s}elseif(%s){%s}else{%s}' % (cond,
                                                         body,
                                                         else_i,
                                                         else_b, else_c)

        self.assertTrue(string == expected)
        self.assertTrue(len(params) == 0)

    def test_can_make_conditional_statement_with_two_elseif(self):
        g = Gremlin()
        c = Conditional()
        cond = '1 == 2'
        body = 'nope'
        else_i = '2 == 2'
        else_b = 'two does equal 2'
        else_i2 = '20 == 20'
        else_b2 = 'already caught above'
        else_c = 'one doesnt equal two'

        c.set_if(cond, body)
        c.set_elif(else_i, else_b)
        c.set_elif(else_i2, else_b2)
        c.set_else(else_c)
        g.apply_statement(c)

        string = str(g)
        params = g.bound_params
        exp = (cond, body, else_i, else_b, else_i2, else_b2, else_c)
        expected = 'if(%s){%s}elseif(%s){%s}elseif(%s){%s}else{%s}' % exp

        self.assertTrue(string == expected)
        self.assertTrue(len(params) == 0)

    def test_can_make_get_edge_statement_both_direction(self):
        out_id = 1
        in_id = 9
        label = 'knows'
        g = Gremlin()
        e = GetEdge(out_id, in_id, label)

        g.apply_statement(e)

        string = str(g)
        params = g.bound_params
        oid = get_dict_key(params, out_id)
        iid = get_dict_key(params, in_id)
        label_b = get_dict_key(params, label)
        as_b = e.bound_entity
        bound = (oid, label_b, as_b, iid, as_b)
        expected = 'g.V(%s).bothE(%s).as(%s).inV().hasId(%s).select(%s)' % \
            bound

        self.assertEqual(expected, string)

    def test_can_make_get_edge_statement_in_direction(self):
        out_id = 1
        in_id = 9
        label = 'knows'
        g = Gremlin()
        e = GetEdge(out_id, in_id, label, 'in')

        g.apply_statement(e)

        string = str(g)
        params = g.bound_params
        oid = get_dict_key(params, out_id)
        iid = get_dict_key(params, in_id)
        label_b = get_dict_key(params, label)
        as_b = e.bound_entity
        bound = (oid, label_b, as_b, iid, as_b)
        expected = 'g.V(%s).inE(%s).as(%s).outV().hasId(%s).select(%s)' % \
            bound

        self.assertEqual(expected, string)

    def test_can_make_get_edge_statement_out_direction(self):
        out_id = 1
        in_id = 9
        label = 'knows'
        g = Gremlin()
        e = GetEdge(out_id, in_id, label, 'out')

        g.apply_statement(e)

        string = str(g)
        params = g.bound_params
        oid = get_dict_key(params, out_id)
        iid = get_dict_key(params, in_id)
        label_b = get_dict_key(params, label)
        as_b = e.bound_entity
        bound = (oid, label_b, as_b, iid, as_b)
        expected = 'g.V(%s).outE(%s).as(%s).inV().hasId(%s).select(%s)' % \
            bound

        self.assertEqual(expected, string)


if __name__ == '__main__':
    unittest.main()
