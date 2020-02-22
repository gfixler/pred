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

        Consider this line of code:

            filter(f, filter(g, xs))

        We have some xs, and we're first filtering them by some function, g,
        and then we're taking the result, and filtering it again by some
        function, f. In many languages, this would create an intermediate list
        to hold the results of the g filtering, which would then be passed to
        the f filtering. If we could instead 'fuse' f and g, by composing them
        together into a new function, we could give that function to filter,
        and traverse the list only once. This is how the composed predicates
        work here.

    Thoughts...

        We talked about how many systems can't fuse, and thus traverse
        structures many times, creating intermediate structures in between, and
        how this class helps avoid that.

        Another option for composed filters is to custom code filters, by
        writing functions that manually do all of the things you want, and
        giving them each a name. This is untenable after only a few filters
        exist, as the number of combinations of things you might possibly need,
        or even just be curious about, explodes.

        A third option is to create a domain specific language (DSL) around
        your filtering needs, and then write a parser that can turn queries in
        that language into code. This is a big undertaking, and requires a lot
        of micromanaging of the parser, tests, debugging, etc., to get working,
        and keep working as needs change.

        Composition of base predicates into more complex predicates, and even
        composition of composed predicates gets around the issues listed above.
        Values are visited once, and all of the predicates in the composition
        are run internally, and the results combined in boolean fashion, with
        no intermediate structures (this is called "fusion").

        There's no need to write a ton of a la carte solutions. Just glue a few
        premade pieces together, as and when needed. If it turns out to be
        useful, give it a name. It's also to create new predicates. They're
        just functions that return a boolean.

        There's also no interoperation to consider. Everything is separate,
        composable pieces, each being simple to create in isolation, and
        automatically usable with every other piece.

        Finally, the code needed to make this work is simple to test, easy to
        reason about, and vanishingly small.
        """

    def __init__ (self, pred):
        self.pred = pred
        self.run  = pred # a comfy alias

    def __and__ (self, other):
        return Pred(lambda x: self.run(x) and other.run(x))

    def __or__ (self, other):
        return Pred(lambda x: self.run(x) or other.run(x))

    def __neg__ (self):
        return Pred(lambda x: not self.run(x))

