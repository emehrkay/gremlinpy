## 3.8.0

Added:
* A `copy` method on `gremlinpy.Gremlin`, `gremlinpy.Token`, and `gremlinpy.Predicate` instances that copies over the current query into a new object chain.

## 3.7.0

Added:
* Predicates for 'from', 'to', and 'or' -- https://github.com/emehrkay/gremlinpy/pull/5

## 3.6.1

Fixed:
* Issue where a predicate object followed a predicate object and it didn't convert the Gremlin representation of second predicate correctly.

## 3.6.0

Added:
* NOT 'not' predicate

Changed:
* All args passed to all functions are bound instead of only the last one.
* If a Param object is passed to Gremlinpy.bind_param the remaining checks for the name/value are not run.

## 3.5.0

Added:
* Added Not predicate as NOT

## 3.4.4

Fixed:
* Error with binding params of parent Gremlin instances overwriting params inherited from children -- https://github.com/emehrkay/gremlinpy/pull/4

## 3.4.3

Fixed:
* Error with binding params of parent Gremlin instances overwriting params inherited from children -- https://github.com/emehrkay/gremlinpy/issues/2

## 3.4.2

Fixed:
* Error with GetEdge Statement regarding direction of other edge. It now takes into account which direction the statement is attempting to check.

## 3.4.1

Fixed:
* Error with install procedure. Moved version number outside of gremlinpy.__init__.py

## 3.4.0.1

Added:
* simple test runner to setup.py

## 3.4.0

Added:
* six dependency
* Python 2.7 support

## 3.3.0

Added:
* _ function that allows you to dynamically create predicates. _('myPredicate', arg, arg2, ...argN)

Changed:
* Predicates are no longer forced to lower case. If there needs to be a different representation for the predidate, overwrite the _function method

Fixed:
* There was an error in type checking for Functions' arguments regarding Gremlin instances (fixed in a few other places too).

## 3.2.2

Changed:
* Predicates now back to binding arguments.

Fixed:
* When defining a parent gremlin object, the current parameters are bound up the chain
* Fixed the GetEdge statement

Removed:
* A bunch of newly added predicates: out, outE, outV, in, inE, inV, both, bothE, bothV -- they were deemed unnecessary

## 3.2.1

Changed:
* Added new predicates: out, outE, outV, in, inE, inV, both, bothE, bothV

## 3.2.0

Fixed:
* Predicates now work correctly

Changed:
* When manually adding a token via gremlin.add_token the arguments for the token itself previously required them to be wrapped in a list. This was confusing and caused pain within the tiny library. I removed this in favor of *args and since the lib is in its infancy, this will not cause a version change.
* Made AS (which evals to as()) a predicate because its arguments should not be bound when called.
* Predicates now nolonger bind parameters. They utilitze UnboundFunction under the hood.

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
