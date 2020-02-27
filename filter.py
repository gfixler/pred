class Pred (object):

    def __init__ (self, pred):
        self.pred = pred

    def __and__ (self, other):
        return Pred(lambda x: self(x) and other(x))

    def __or__ (self, other):
        return Pred(lambda x: self(x) or other(x))

    def __neg__ (self):
        return Pred(lambda x: not self(x))

    def __call__ (self, *args):
        return self.pred(*args)

