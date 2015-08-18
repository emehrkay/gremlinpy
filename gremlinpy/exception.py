import gremlinpy.config


class GremlinError(Exception):
    pass


class StatementError(GremlinError):
    pass


class TokenError(GremlinError):
    pass


class PredicateError(GremlinError):
    pass
