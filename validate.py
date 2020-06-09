class Validator (object):

    def __init__ (self, name, descrip, pred, fix):
        self._name = name
        self._descrip = descrip
        self._pred = pred
        self._fix = fix

    def __call__ (self, x):
        result = { "name": self._name
                 , "descrip": self._descrip
                 , "status": "NOTRUN"
                 }
        if self._pred(x):
            result["status"] = "PASSED"
        else:
            if self._fix:
                self._fix(x)
                if self._pred(x):
                    result["status"] = "FIXED"
                else:
                    result["status"] = "UNFIXED"
            else:
                result["status"] = "UNFIXABLE"
        return result

