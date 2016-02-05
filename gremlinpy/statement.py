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
        if_condition = UnboudFunctionRaw(gremlin, 'if', self.if_condition)

        gremlin.set_graph_variable('').add_token(if_condition)
        gremlin.close(self.if_body)

        #build all of the elif statements
        for i, condition in enumerate(self.elif_condition):
            body = self.elif_body[i]
            elif_condition = UnboudFunctionRaw(gremlin, 'elseif', condition)

            gremlin.add_token(elif_condition).close(body)

        #build else statement
        if self.else_body is not None:
            else_condition = Raw(gremlin, 'else')

            gremlin.add_token(else_condition).close(self.else_body)

        return self


class GetEdge(Statement):
    bound_in_id = 'V_IN_ID'
    bound_out_id = 'V_OUT_ID'
    bound_label = 'EDGE_LABEL_NAME'
    bound_entity = 'EDGE_ENTITY'
    directions = {
        'both': 'bothE',
        'in': 'inE',
        'out': 'outE'}
    vertex_directions = {
        'in': 'inV',
        'out': 'outV'}

    def __init__(self, out_v_id, in_v_id, label, direction='both', \
                 bind_ids=True):
        if direction not in self.directions:
            error = 'The direction must be: ' + \
                ', '.join(self.directions.keys())
            raise ValueError(error)
        other = 'in'

        if direction != 'both':
            other = 'in' if direction == 'out' else 'out'

        self.out_v_id = out_v_id
        self.in_v_id = in_v_id
        self.label = label
        self.bind_ids = bind_ids
        self.direction = self.directions[direction]
        self.vertex_direction = self.vertex_directions[other]

    def build(self):
        if self.bind_ids:
            out_id = self.gremlin.bind_param(self.out_v_id, self.bound_out_id)
            in_id = self.gremlin.bind_param(self.in_v_id, self.bound_in_id)
        else:
            out_id = [self.out_v_id]
            in_id = [self.in_v_id]

        label = self.gremlin.bind_param(self.label, self.bound_label)
        back = self.gremlin.bind_param(self.bound_entity.lower(),
                                       self.bound_entity)

        self.gremlin.V(out_id[0])
        getattr(self.gremlin, self.direction)(self.label)
        self.gremlin.AS(back[0]).func(self.vertex_direction)
        self.gremlin.hasId(in_id[0]).select(back[0])
