inParens = lambda x: "(" + str(x) + ")"


class Pred (object):

    def __init__ (self, pred=None, name=None, fix=None, typeCon=None):
        self._op = "PRED"
        self._pred = pred
        self._name = name if name else str(pred)
        if callable(fix):
            self._fix = fix
        if type(typeCon) == list:
            self._typeCon = sorted(typeCon)
        else:
            self._typeCon = typeCon

    def __call__ (self, x):
        if self._typeCon:
            typeSpec, typePred = self._typeCon
            if not typePred(x):
                if isinstance(typeSpec, list):
                    typesStr = " or ".join(map(str, typeSpec))
                    raise TypeError, "Pred requires " + typesStr + "; received " + str(type(x))
                else:
                    raise TypeError, "Pred requires " + str(typeSpec) + "; received " + str(type(x))
        if   self._op == "PRED": return self._pred(x)
        elif self._op == "AND":  return self._left(x) and self._right(x)
        elif self._op == "SEQ":  return self._left(x) and self._right(x)
        elif self._op == "OR":   return self._left(x) or self._right(x)
        elif self._op == "NOT":  return not self._pred(x)

    def __eq__ (self, other):
        if self._op != other._op:
            return False
        if self._op == "PRED":
            return self._name == other._name
        elif self._op == "NOT":
            return self._pred == other._pred
        elif self._op in ["AND", "OR", "SEQ"]:
            return self._left == other._left and self._right == other._right

    def __and__ (self, other):
        if self._typeCon:
            selfSpec, _ = self._typeCon
            if other._typeCon:
                otherSpec, _ = other._typeCon
                if selfSpec != otherSpec:
                    raise TypeError, "Cannot AND " + str(selfSpec) + " Pred with " + str(otherSpec) + " Pred"
        p = Pred()
        p._op = "AND"
        p._left = self
        p._right = other
        p._name = str(p)
        p._typeCon = self._typeCon
        return p

    def __rshift__ (self, other):
        if self._typeCon:
            selfSpec, _ = self._typeCon
            if other._typeCon:
                otherSpec, _ = other._typeCon
                if selfSpec != otherSpec:
                    raise TypeError, "Cannot SEQ " + str(selfSpec) + " Pred with " + str(otherSpec) + " Pred"
        p = Pred()
        p._op = "SEQ"
        p._left = self
        p._right = other
        p._name = str(p)
        return p

    def __or__ (self, other):
        if self._typeCon:
            selfSpec, _ = self._typeCon
            if other._typeCon:
                otherSpec, _ = other._typeCon
                if selfSpec != otherSpec:
                    raise TypeError, "Cannot OR " + str(selfSpec) + " Pred with " + str(otherSpec) + " Pred"
        p = Pred()
        p._op = "OR"
        p._left = self
        p._right = other
        p._name = str(p)
        return p

    def __invert__ (self):
        p = Pred()
        p._op = "NOT"
        p._pred = self
        p._name = str(p)
        return p

    def __str__ (self):
        if self._op == "PRED":
            return self._name
        elif self._op == "NOT":
            fn = inParens if self._pred._op in ["AND", "SEQ", "OR"] else str
            return "~" + fn(self._pred)
        elif self._op == "AND":
            leftfn = inParens if self._left._op == "OR" else str
            rightfn = inParens if self._right._op == "OR" else str
            return leftfn(self._left) + " & " + rightfn(self._right)
        elif self._op == "SEQ":
            leftfn = inParens if self._left._op == "OR" else str
            rightfn = inParens if self._right._op == "OR" else str
            return leftfn(self._left) + " >> " + rightfn(self._right)
        elif self._op == "OR":
            return str(self._left) + " | " + str(self._right)

    def ast (self):
        if self._op == "PRED":
            return ("PRED", self)
        elif self._op == "AND":
            return ("AND", (self._left.ast(), self._right.ast()))
        elif self._op == "SEQ":
            return ("SEQ", (self._left.ast(), self._right.ast()))
        elif self._op == "OR":
            return ("OR", (self._left.ast(), self._right.ast()))
        elif self._op == "NOT":
            return ("NOT", self._pred.ast())

    def validate (self, x, noSolve=False):
        if noSolve:
            if self._op == "PRED":
                return {"ref": self, "op": "PRED"}
            elif self._op in ["AND", "OR", "SEQ"]:
                return {"ref": self, "op": self._op, left:self._left.validate(x, noSolve=True), right:self._right.validate(x, noSolve=True)}
            elif self._op == "NOT":
                return {"ref": self, "op": "NOT", left:self._pred.validate(x, noSolve=True)}

        if self._op == "PRED":
            result = self._pred(x)
            if result:
                return {"ref": self, "op": "PRED", "result": True}
            else:
                if hasattr(self, "_fix"):
                    self._fix(x)
                    result = self._pred(x)
                    if result:
                        return {"ref": self, "op": "PRED", "result": True, "status": "FIXED"}
                    else:
                        return {"ref": self, "op": "PRED", "result": False, "status": "UNFIXED"}
                else:
                    return {"ref": self, "op": "PRED", "result": False}
        elif self._op == "AND":
            left = self._left.validate(x)
            right = self._right.validate(x)
            result = left["result"] and right["result"]
            if result:
                return {"ref": self, "op": "AND", "left": left, "right": right, "result": True}
            else:
                return {"ref": self, "op": "AND", "left": left, "right": right, "result": False}
        elif self._op == "OR":
            left = self._left.validate(x)
            right = self._right.validate(x)
            result = left["result"] or right["result"]
            if result:
                return {"ref": self, "op": "OR", "left": left, "right": right, "result": True}
            else:
                return {"ref": self, "op": "OR", "left": left, "right": right, "result": False}
        elif self._op == "NOT":
            pred = self._pred.validate(x)
            result = not pred["result"]
            if result:
                return {"ref": self, "op": "NOT", "pred": pred, "result": True}
            else:
                return {"ref": self, "op": "NOT", "pred": pred, "result": False}
        elif self._op == "SEQ":
            left = self._left.validate(x)
            if not left["result"]:
                right = self._right.validate(x, noSolve=True)
                return {"ref": self, "op": "SEQ", "left": left, "right": right, "result": False}
            right = self._right.validate(x)
            result = left["result"] and right["result"]
            if result:
                return {"ref": self, "op": "SEQ", "left": left, "right": right, "result": True}
            else:
                return {"ref": self, "op": "SEQ", "left": left, "right": right, "result": False}

    def pformat (self, indent=2, indLev=0, *args, **kwargs):
        ind = " " * indent * indLev
        if self._op == "PRED":
            return ind + str(self)
        if self._op == "AND":
            left = self._left.pformat(indent=indent, indLev=indLev+1)
            right = self._right.pformat(indent=indent, indLev=indLev+1)
            return "\n".join([ind + "AND", left, right])
        if self._op == "SEQ":
            left = self._left.pformat(indent=indent, indLev=indLev+1)
            right = self._right.pformat(indent=indent, indLev=indLev+1)
            return "\n".join([ind + "SEQ", left, right])
        if self._op == "OR":
            left = self._left.pformat(indent=indent, indLev=indLev+1)
            right = self._right.pformat(indent=indent, indLev=indLev+1)
            return "\n".join([ind + "OR", left, right])
        if self._op == "NOT":
            p = self._pred.pformat(indent=indent, indLev=indLev+1)
            return '\n'.join([ind + "NOT", p])

    def pprint (self, *args, **kwargs):
        print self.pformat(*args, **kwargs)

