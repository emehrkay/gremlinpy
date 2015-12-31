## 3.1.2

Fixed:
* Get edge built-in statement

## 3.1.1

Fixed:
* Bug where Gremlin.stack\_bound_params was not redefining the parent variable causing an infinite loop. 

## 3.1.0

Added:
* Parameter value caching. The system will attempt to utilize previously defined parameters for newly bound values when that value has been bound before.

## 3.0.0

Added:
* Skipped 3 version numbers just to align with the TinkerPop version. TinerPop2 support is in the gremlinpy 2.X.X release.
* Predicate support. This allows simple gremlinpy strings to be built utiling some keywords defined in the TinkerPop3 library as predicates.
* Python3 support
