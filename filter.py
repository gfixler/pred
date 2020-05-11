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
            return ("  " * indent) + str(self._pred) + "\n"
        elif self._op == "AND":
            return ("  " * indent) + "AND\n" + self._left.ast(indent=indent+2) + self._right.ast(indent=indent+2)
        elif self._op == "OR":
            return ("  " * indent) + "OR\n" + self._left.ast(indent=indent+2) + self._right.ast(indent=indent+2)
        elif self._op == "NOT":
            return ("  " * indent) + "NOT\N" + self._right.ast(indent=indent+2)
