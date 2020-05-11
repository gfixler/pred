class Pred (object):

    def __init__ (self, pred=None):
        self._op = "PRED"
        self._pred = pred

    def __call__ (self, x):
        if self._op == "PRED":
            return self._pred(x)
        elif self._op == "AND":
            return self._left(x) and self._right(x)
        elif self._op == "OR":
            return self._left(x) or self._right(x)
        elif self._op == "NOT":
            return not self._right(x)

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

    def __neg__ (self):
        p = Pred()
        p._op = "NOT"
        p._right = self
        return p

