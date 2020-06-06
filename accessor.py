import re


from .filter import Pred


class Accessor (object):

    def __init__ (self, accFunc):
        self._accFunc = accFunc

    def __call__ (self, *args):
        return self._accFunc(*args)

    def pred (self, p, *args, **kwargs):
        return Pred(lambda s: p(s), *args, **kwargs)

    def equals (self, string):
        return Pred(lambda s: self(s) == string, name="(== \"" + string + "\")")


class StringAccessor (Accessor):

    def __call__ (self, *args):
        result = self._accFunc(*args)
        if type(result) != str:
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
        return Pred(lambda s: re.match(pattern, s), name="matches(\"" + pattern + "\")")


class NumAccessor (Accessor):

    def __call__ (self, *args):
        result = self._accFunc(*args)
        if type(result) not in [int, float]:
            try:
                raise TypeError, "NumAccessor accessed non-num object: " + str(result)
            except:
                # supposedly str can fail (https://stackoverflow.com/a/4857604/955926)
                raise TypeError, "NumAccessor accessed non-num object"
        return result


    def lt (self, n):
        return Pred(lambda i: i < n, name="(< " + str(n) + ")")

    def lte (self, n):
        return Pred(lambda i: i <= n, name="(<= " + str(n) + ")")

    def eq (self, n):
        return Pred(lambda i: i == n, name="(== " + str(n) + ")")

    def gte (self, n):
        return Pred(lambda i: i >= n, name="(>= " + str(n) + ")")

    def gt (self, n):
        return Pred(lambda i: i > n, name="(> " + str(n) + ")")

