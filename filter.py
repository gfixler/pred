class Pred (object):

    def __init__ (self, pred=None, op="PRED", left=None, right=None):
        self._op = op
        self._pred = pred
        if left:  self._left = left
        if right: self._right = right

    def __call__ (self, x):
        if   self._op == "PRED": return self._pred(x)
        elif self._op == "AND":  return self._left(x) and self._right(x)
        elif self._op == "OR":   return self._left(x) or self._right(x)
        elif self._op == "NOT":  return not self._right(x)

    def __and__ (self, other):
        return Pred(op="AND", left=self, right=other)

    def __or__ (self, other):
        return Pred(op="OR", left=self, right=other)

    def __neg__ (self):
        return Pred(op="NOT", right=self)

    def ast (self, indent=0):
        if self._op == "PRED":
            return ("PRED", [str(self._pred)])
        elif self._op == "AND":
            return ("AND", [self._left.ast(), self._right.ast()])
        elif self._op == "OR":
            return ("OR", [self._left.ast(), self._right.ast()])
        elif self._op == "NOT":
            return ("NOT", [self._right.ast()])

