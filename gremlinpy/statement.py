import gremlinpy.config
from gremlinpy.exception import GremlinError, StatementError


class Statement(object):

    def set_gremlin(self, gremlin):
        self.gremlin = gremlin

        return self

    def build(self):
        raise NotImplementedError('Gremlinpy statements need a build method')

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        self.build()

        return str(self.gremlin)


class Conditional(Statement):

    def __init__(self):
        self.if_condition = None
        self.if_body = None
        self.else_body = None
        self.elif_condition = []
        self.elif_body = []

    def set_if(self, condition, body):
        self.if_condition = condition
        self.if_body = body

        return self

    def set_elif(self, condition, body):
        self.elif_condition.append(condition)
        self.elif_body.append(body)

        return self

    def set_else(self, body):
        self.else_body = body

        return self

    def build(self):
        from gremlinpy.gremlin import UnboudFunctionRaw, Raw

        gremlin = self.gremlin

        if self.if_condition is None or self.if_body is None:
            error = 'Your statement needs at least both an if clause and body'
            raise StatmentError(error)

        #build the if statement
        if_condition = UnboudFunctionRaw(gremlin, 'if', [self.if_condition])

        gremlin.set_graph_variable('').add_token(if_condition)
        gremlin.close(self.if_body)

        #build all of the elif statements
        for i, condition in enumerate(self.elif_condition):
            body = self.elif_body[i]
            elif_condition = UnboudFunctionRaw(gremlin, 'elseif', [condition])

            gremlin.add_token(elif_condition).close(body)

        #build else statement
        if self.else_body is not None:
            else_condition = Raw(gremlin, 'else')

            gremlin.add_token(else_condition).close(self.else_body)

        return self


class GetEdge(Statement):

    def __init__(self, out_v_id, in_v_id, label, bind_ids=True):
        self.out_v_id = out_v_id
        self.in_v_id = in_v_id
        self.label = label
        self.bind_ids = bind_ids

    def build(self):
        from gremlinpy.gremlin import Function as GF
        
        gremlin = self.gremlin

        if self.bind_ids:
            out = gremlin.bind_param(self.out_v_id, 'V_OUT_ID')
            v_id = gremlin.bind_param(self.in_v_id, 'V_IN_ID')
        else:
            out = [self.out_v_id]
            v_id = [self.in_v_id]

        label = gremlin.bind_param(self.label, 'LABEL')
        back = gremlin.bind_param('vertex', 'VERTEX')
        as_var = gremlin.bind_param('AS_LABEL')
        as_func = GF(gremlin, 'as', [as_var[0]])
        self.gremlin.V(v_id[0]).bothE(label[0]).add_token(as_func).bothV().has('T.id', out[0]).select(as_var[0])
