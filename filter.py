"""
This script is a test bed for my composable filters concept.
"""

# example
lt  = lambda n: lambda x: x <  n
lte = lambda n: lambda x: x <= n
eq  = lambda n: lambda x: x == n
gte = lambda n: lambda x: x >= n
gt  = lambda n: lambda x: x >  n

isLT = lambda n: Pred(lt(n))
isEq = lambda n: Pred(eq(n))
isGT = lambda n: Pred(gt(n))


class Pred (object):

    def __init__ (self, pred):
        self.pred = pred
        self.run  = pred # a comfy alias

    def __and__ (self, other):
        return Pred(lambda x: self.run(x) and other.run(x))

    def __or__ (self, other):
        return Pred(lambda x: self.run(x) or other.run(x))


"""
# examples of composition, usage

# compose filters
(isLT(2) | isGT(6) | isEq(4)).run(3)

# map composed filters
map((isLT(2) | isGT(6) | isEq(4)).run, xrange(10))

# filter with composed filters
filter((isLT(2) | isGT(6) | isEq(4)).run, xrange(10))
"""

