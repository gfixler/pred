"""
This script is a test bed for my composable filters concept.
"""

class Pred (object):

    """
    Pred takes a predicate function, i.e. a function that takes one argument,
    and returns a boolean that answers some True/False question about it.

    Don't use the "dunder" (double underscore) methods defined on this class,
    like __and__; instead use the operators they define, like &. Composition
    through these few boolean operations are the core purpose of this class.

    Example comparison functions:

        lt  = lambda n: lambda x: x <  n
        lte = lambda n: lambda x: x <= n
        eq  = lambda n: lambda x: x == n
        gte = lambda n: lambda x: x >= n
        gt  = lambda n: lambda x: x >  n

    Turned into functions that return predicates of one argument:

        isLT  = lambda n: Pred( lt(n))
        isLTE = lambda n: Pred(lte(n))
        isEq  = lambda n: Pred( eq(n))
        isGTE = lambda n: Pred(gte(n))
        isGT  = lambda n: Pred( gt(n))

    Predicates are composable via & (AND) and | (OR):

        # decide if x is (<2) OR (>6) or (==4)
        (isLT(2) | isGT(6) | isEq(4)).run(x)

    Predicates are negatable via - (negation):

        # True only if x is NOT equal to 3
        (-isEq(3)).run(x)

        # note: dot notation binds tighter than negation, sadly,
        #       so you'll have to group it with parentheses

    Predicates map:

        # convert [0-9] to bools; 2, 3, 7, and 8 are True
        map((isGT(1) & isLT(4) | isGT(6) & isLT(9)).run, xrange(10))

        # note: precedence matters, e.g. & binds tighter than |

    Predicates filter:

        # keep the numbers (<=2) OR (>6), but NOT 9
        filter((isLTE(2) | isGT(6) & -isEq(9)).run, xrange(10))

    Predicates are first class:

        # you can assign them to variables
        isValidWeekdayNum = isGTE(1) & isLTE(7)
        if (-isValidWeekdayNum).run(8):
            # will raise, 8 is invalid
            raise RuntimeError, "invalid weekday number"

        # you can also pass them to and return them from functions

    Predicates "fuse"

        A common way of filtering is filtering by one thing, then filtering the
        results by another thing, etc. This visits values more than once, and
        likely creates several intermediate lists in memory. It's inefficient,
        and unnecessary.

        Another option is to custom code filters, by writing functions that
        manually do all of the things you want, and giving them each a name.
        This is untenable after only a few filters exist, as the number of
        combinations of things you might possibly need, or even just be curious
        about, explodes.

        Composition of base predicates into more complex predicates, and even
        composition of composed predicates gets around the issues listed above.
        Values are visited once, and all of the predicates in the composition
        are run internally, and the results combined in boolean fashion, with
        no intermediate structures (this is called "fusion"), and no need to
        write a la carte solutions. Just glue a few pieces together, when
        needed. If it turns out to be useful, give it a name. """

    def __init__ (self, pred):
        self.pred = pred
        self.run  = pred # a comfy alias

    def __and__ (self, other):
        return Pred(lambda x: self.run(x) and other.run(x))

    def __or__ (self, other):
        return Pred(lambda x: self.run(x) or other.run(x))

    def __neg__ (self):
        return Pred(lambda x: not self.run(x))

