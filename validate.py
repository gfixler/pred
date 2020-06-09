class Validator (object):

    def __init__ (self, pred, fix):
        self._pred = pred
        self._fix = fix

    def __call__ (self, x):
        if self._pred(x):
            return {"status": "PASSED"}
        else:
            if self._fix:
                try:
                    self._fix(x)
                except Exception as e:
                    return {"status": "FIXRAISED", "error": e}
                if self._pred(x):
                    return {"status": "FIXED"}
                else:
                    return {"status": "UNFIXED"}
            else:
                return {"status": "UNFIXABLE"}

