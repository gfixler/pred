class Pred (object):

    def __init__ (self, pred):
        self.pred = pred
        self.run  = pred # a comfy alias

    def __and__ (self, other):
        return Pred(lambda x: self.run(x) and other.run(x))

    def __or__ (self, other):
        return Pred(lambda x: self.run(x) or other.run(x))

    def __neg__ (self):
        return Pred(lambda x: not self.run(x))

