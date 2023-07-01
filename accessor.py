import re


from pred import Pred


class Accessor (object):

    def __init__ (self, accFunc, name=None):
        self._accFunc = accFunc
        self._name = name

    def __call__ (self, *args):
        return self._accFunc(*args)

    def __str__ (self):
        return self._name or str(self._accFunc)

    def pred (self, p, name=None, *args, **kwargs):
        accName = str(self)
        predName = name or str(p)
        compName = predName + " . " + accName
        return Pred( lambda s: p(self(s))
                   , name = compName
                   , *args, **kwargs
                   )

    def equals (self, val):
        return Pred(lambda s: self(s) == val, name="(== " + str(val) + ")")


class StringAccessor (Accessor):

    def __call__ (self, *args):
        result = self._accFunc(*args)
        if not isinstance(result, str):
            try:
                raise TypeError, "StringAccessor accessed non-string object: " + str(result)
            except:
                # supposedly str can fail (https://stackoverflow.com/a/4857604/955926)
                raise TypeError, "StringAccessor accessed non-string object"
        return result

    def contains (self, string):
        return Pred(lambda s: string in self(s), name="contains(\"" + string + "\")")

    def startswith (self, string):
        return Pred(lambda s: self(s).startswith(string), name="startswith(\"" + string + "\")")

    def endswith (self, string):
        return Pred(lambda s: self(s).endswith(string), name="endswith(\"" + string + "\")")

    def matches (self, pattern):
        return Pred(lambda s: re.match(pattern, self(s)), name="matches(\"" + pattern + "\")")


class NumAccessor (Accessor):

    def __call__ (self, *args):
        result = self._accFunc(*args)
        if not (isinstance(result, int) or isinstance(result, float)):
            try:
                raise TypeError, "NumAccessor accessed non-num object: " + str(result)
            except:
                # supposedly str can fail (https://stackoverflow.com/a/4857604/955926)
                raise TypeError, "NumAccessor accessed non-num object"
        return result


    def lt (self, n):
        return Pred(lambda i: self(i) < n, name="lt(" + str(n) + ")")

    def lte (self, n):
        return Pred(lambda i: self(i) <= n, name="lte(" + str(n) + ")")

    def eq (self, n):
        return Pred(lambda i: self(i) == n, name="eq(" + str(n) + ")")

    def gte (self, n):
        return Pred(lambda i: self(i) >= n, name="gte(" + str(n) + ")")

    def gt (self, n):
        return Pred(lambda i: self(i) > n, name="gt(" + str(n) + ")")

