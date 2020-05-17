import unittest
from nose.plugins.attrib import attr

from ..filter import Pred


ident = lambda x: x

lt  = lambda n: Pred(lambda x: x <  n)
eq  = lambda n: Pred(lambda x: x == n)
gt  = lambda n: Pred(lambda x: x >  n)


class Test_Pred (unittest.TestCase):

    def test_canCallIdentityPredicate (self):
        self.assertTrue(Pred(ident)(True))

    def test_canANDPredicates (self):
        self.assertEquals(map(gt(3) & lt(5), [3, 4, 5]), [False, True, False])

    def test_canORPredicates (self):
        self.assertEquals(map(lt(5) | gt(5), [4, 5, 6]), [True, False, True])

    def test_canNOTPredicates (self):
        self.assertEquals(map(~eq(3), [2, 3, 4]), [True, False, True])

    def test_canANDAndORAndNOTPredicates (self):
        # p = ((gt(0) & lt(4)) | (gt(5) & lt(9))) & ~(eq(2) | eq(7)) # confusing version
        betwen0and4 = gt(0) & lt(4)
        betwen5and9 = gt(5) & lt(9)
        not2or7 = ~(eq(2) | eq(7))
        p = (betwen0and4 | betwen5and9) & not2or7
        #             0      1     2      3     4      5      6     7      8     9
        expected = [False, True, False, True, False, False, True, False, True, False]
        self.assertEquals(map(p, range(10)), expected)

    def test_ast_PRED (self):
        (op, erand) = Pred(ident).ast()
        self.assertEquals(op, "PRED")
        self.assertTrue(callable(erand))

    def test_ast_AND (self):
        (op, erands) = (gt(3) & lt(5)).ast()
        self.assertEqual(op, "AND")
        ((lop, lerands), (rop, rerands)) = erands
        self.assertEquals(lop, "PRED")
        self.assertEquals(rop, "PRED")
        self.assertTrue(callable(lerands))
        self.assertTrue(callable(rerands))

    def test_ast_OR (self):
        (op, erands) = (gt(3) & lt(5)).ast()
        self.assertEqual(op, "AND")
        ((lop, lerands), (rop, rerands)) = erands
        self.assertEquals(lop, "PRED")
        self.assertEquals(rop, "PRED")
        self.assertTrue(callable(lerands))
        self.assertTrue(callable(rerands))

    def test_ast_NOT (self):
        (op, erand) = (~Pred(ident)).ast()
        self.assertEquals(op, "NOT")
        (nop, nerands) = erand
        self.assertEquals(nop, "PRED")
        self.assertTrue(callable(nerands))

    def test_str_PRED (self):
        self.assertTrue(str(Pred(ident)).startswith("<function <lambda> at"))

    def test_str_NOT (self):
        self.assertTrue(str(~Pred(ident)).startswith("~<function <lambda> at"))

