class Accessor (object):

    def __init__ (self, accFunc):
        self._accFunc = accFunc

    def __call__ (self, *args):
        return self._accFunc(*args)

