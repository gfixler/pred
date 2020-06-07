inParens = lambda x: "(" + str(x) + ")"


class Pred (object):

    def __init__ (self, pred=None, name=None):
        self._op = "PRED"
        self._pred = pred
        self._name = name if name else str(pred)

    def __call__ (self, x):
        if   self._op == "PRED": return self._pred(x)
        elif self._op == "AND":  return self._left(x) and self._right(x)
        elif self._op == "OR":   return self._left(x) or self._right(x)
        elif self._op == "NOT":  return not self._pred(x)

    def __eq__ (self, other):
        if self._op != other._op:
            return False
        if self._op == "PRED":
            return self._name == other._name
        elif self._op == "NOT":
            return self._pred == other._pred
        elif self._op in ["AND", "OR"]:
            return self._left == other._left and self._right == other._right

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

    def __str__ (self):
        if self._op == "PRED":
            return self._name
        elif self._op == "NOT":
            fn = inParens if self._pred._op in ["AND", "OR"] else str
            return "~" + fn(self._pred)
        elif self._op == "AND":
            leftfn = inParens if self._left._op == "OR" else str
            rightfn = inParens if self._right._op == "OR" else str
            return leftfn(self._left) + " & " + rightfn(self._right)
        elif self._op == "OR":
            return str(self._left) + " | " + str(self._right)

    def ast (self):
        if self._op == "PRED":
            return ("PRED", self)
        elif self._op == "AND":
            return ("AND", (self._left.ast(), self._right.ast()))
        elif self._op == "OR":
            return ("OR", (self._left.ast(), self._right.ast()))
        elif self._op == "NOT":
            return ("NOT", self._pred.ast())

    def pformat (self, indent=2, indLev=0, *args, **kwargs):
        ind = " " * indent * indLev
        if self._op == "PRED":
            return ind + str(self)
        if self._op == "AND":
            left = self._left.pformat(indent=indent, indLev=indLev+1)
            right = self._right.pformat(indent=indent, indLev=indLev+1)
            return "\n".join([ind + "AND", left, right])
        if self._op == "OR":
            left = self._left.pformat(indent=indent, indLev=indLev+1)
            right = self._right.pformat(indent=indent, indLev=indLev+1)
            return "\n".join([ind + "OR", left, right])
        if self._op == "NOT":
            p = self._pred.pformat(indent=indent, indLev=indLev+1)
            return '\n'.join([ind + "NOT", p])

    def pprint (self, *args, **kwargs):
        print self.pformat(*args, **kwargs)

