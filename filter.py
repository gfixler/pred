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


true = Pred(lambda _: True, name="True")
false = Pred(lambda _: False, name="False")

def simplify_notNot (pred):
    if pred._op == "NOT" and pred._pred._op == "NOT":
        return (simplify(pred._pred._pred), True)
    return (pred, False)

def simplify_xAndNotX (pred):
    if pred._op == "AND":
        if pred._left._op == "NOT" and simplify(pred._right) == simplify(pred._left._pred):
            return (false, True)
        elif pred._right._op == "NOT" and simplify(pred._left) == simplify(pred._right._pred):
            return (false, True)
    return (pred, False)

def simplify_xOrNotX (pred):
    if pred._op == "OR":
        if pred._left._op == "NOT" and simplify(pred._right) == simplify(pred._left._pred):
            return (true, True)
        elif pred._right._op == "NOT" and simplify(pred._left) == simplify(pred._right._pred):
            return (true, True)
    return (pred, False)

def simplify_xAndOrX (pred):
    if pred._op in ["AND", "OR"]:
        simpleLeft = simplify(pred._left)
        if simpleLeft == simplify(pred._right):
            return (simpleLeft, True)
    return (pred, False)

def simplify (pred):
    simplifiers = [ simplify_notNot
                  , simplify_xAndNotX
                  , simplify_xOrNotX
                  , simplify_xAndOrX
                  ]
    for simplifier in simplifiers:
        (result, status) = simplifier(pred)
        if status:
            return result
    return pred

