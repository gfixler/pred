from .pred import Pred

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

