import re


from pred import Pred


class Accessor:

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
                   , *args, **kwargs # TODO are these tested?
                   )

    def equals (self, val):
        return Pred(lambda s: self(s) == val, name="(== " + str(val) + ")")


class StringAccessor (Accessor):

    def __call__ (self, *args):
        result = self._accFunc(*args)
        if not isinstance(result, str):
            try:
                raise TypeError("StringAccessor accessed non-string object: " + str(result))
            except:
                # supposedly str can fail (https://stackoverflow.com/a/4857604/955926)
                raise TypeError("StringAccessor accessed non-string object")
        return result

    def contains (self, string):
        name = "contains(\"" + string + "\")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda s: string in self(s), name=name)

    def startswith (self, string):
        name = "startswith(\"" + string + "\")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda s: self(s).startswith(string), name=name)

    def endswith (self, string):
        name = "endswith(\"" + string + "\")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda s: self(s).endswith(string), name=name)

    def matches (self, pattern):
        name = "matches(\"" + pattern + "\")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda s: re.match(pattern, self(s)), name=name)


class NumAccessor (Accessor):

    def __call__ (self, *args):
        result = self._accFunc(*args)
        if not (isinstance(result, int) or isinstance(result, float)):
            try:
                raise TypeError("NumAccessor accessed non-num object: " + str(result))
            except:
                # supposedly str can fail (https://stackoverflow.com/a/4857604/955926)
                raise TypeError("NumAccessor accessed non-num object")
        return result


    def lt (self, n):
        name = "lt(" + str(n) + ")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda i: self(i) < n, name=name)

    def lte (self, n):
        name = "lte(" + str(n) + ")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda i: self(i) <= n, name=name)

    def eq (self, n):
        name = "eq(" + str(n) + ")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda i: self(i) == n, name=name)

    def gte (self, n):
        name = "gte(" + str(n) + ")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda i: self(i) >= n, name=name)

    def gt (self, n):
        name = "gt(" + str(n) + ")"
        if self._name:
            name = self._name + "." + name
        return Pred(lambda i: self(i) > n, name=name)

