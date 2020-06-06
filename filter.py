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

    def __ne__ (self, other):
        return not (self == other)

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

def predFlip (pred):
    if pred._op == "AND":
        return pred._right & pred._left
    if pred._op == "OR":
        return pred._right | pred._left
    return pred

def simplify_NOT (pred):
    if pred._pred._op == "NOT":
        return simplify(pred._pred._pred)
    return pred

def simplify_AND (pred):
    pred._left = simplify(pred._left)
    pred._right = simplify(pred._right)
    if pred._left._op == "NOT" and pred._left._pred == pred._right:
        return false
    elif pred._left == pred._right:
        return pred._left
    elif pred._left == true:
        return pred._right
    elif pred._left == false:
        return false
    elif pred._right._op == "OR" and (pred._left == pred._right._left or pred._left == pred._right._right):
        return pred._left
    return pred

def simplify_OR (pred):
    pred._left = simplify(pred._left)
    pred._right = simplify(pred._right)
    if pred._left._op == "NOT" and pred._left._pred == pred._right:
        return true
    elif pred._right == pred._left:
        return pred._right
    elif pred._left == false:
        return pred._right
    elif pred._left == true:
        return true
    elif pred._left._op == "AND" and pred._right._op == "AND":
        return simplify_distribute(pred._left, pred._right)
    elif pred._right._op == "AND" and (pred._left == pred._right._left or pred._left == pred._right._right):
        return pred._left
    return pred

def simplify_distribute (left, right):
    if left._left == right._left:
        return simplify(left._left & (left._right | right._right))
    if left._left == right._right:
        return simplify(left._left & (left._right | right._left))
    if left._right == right._left:
        return simplify(left._right & (left._left | right._right))
    if left._right == right._right:
        return simplify(left._right & (left._left | right._left))
    return left | right

def simplify_commutative (pred, simplifier):
    result = simplifier(pred)
    if result != pred:
        return result
    result = simplifier(predFlip(pred))
    if result != predFlip(pred):
        return result
    return pred

def simplify (pred):
    if pred._op == "AND":
        return simplify_commutative(pred, simplify_AND)
    elif pred._op == "OR":
        return simplify_commutative(pred, simplify_OR)
    elif pred._op == "NOT":
        return simplify_NOT(pred)
    return pred

