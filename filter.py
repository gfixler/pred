class Pred (object):

    def __init__ (self, pred=None):
        self._op = "PRED"
        self._pred = pred

    def __call__ (self, x):
        if   self._op == "PRED": return self._pred(x)
        elif self._op == "AND":  return self._left(x) and self._right(x)
        elif self._op == "OR":   return self._left(x) or self._right(x)
        elif self._op == "NOT":  return not self._pred(x)

    def __and__ (self, other):
        p = Pred()
        p._op = "AND"
        p._left = self
        p._right = other
        return p

    def __or__ (self, other):
        p = Pred()
        p._op = "OR"
        p._left = self
        p._right = other
        return p

    def __invert__ (self):
        p = Pred()
        p._op = "NOT"
        p._pred = self
        return p

    def ast (self):
        if self._op == "PRED":
            return ("PRED", self._pred)
        elif self._op == "AND":
            return ("AND", (self._left.ast(), self._right.ast()))
        elif self._op == "OR":
            return ("OR", (self._left.ast(), self._right.ast()))
        elif self._op == "NOT":
            return ("NOT", self._pred.ast())

    def __str__ (self):
        if self._op == "PRED":
            return str(self._pred)
        elif self._op == "NOT":
            return "~" + str(self._pred)
        elif self._op == "AND":
            return str(self._left) + " & " + str(self._right)
        elif self._op == "OR":
            return str(self._left) + " | " + str(self._right)

