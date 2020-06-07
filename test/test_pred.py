import unittest
from nose.plugins.attrib import attr

from ..pred import *


ident = lambda x: x

lt  = lambda n: Pred(lambda x: x <  n, name="lt(" + str(n) + ")")
eq  = lambda n: Pred(lambda x: x == n, name="eq(" + str(n) + ")")
gt  = lambda n: Pred(lambda x: x >  n, name="gt(" + str(n) + ")")


class Test_Pred (unittest.TestCase):

    def test_canCallIdentityPredicate (self):
        self.assertTrue(Pred(ident)(True))

    def test_eq_actuallyEqual (self):
        self.assertEquals(lt(5), lt(5))

    def test_eq_AND (self):
        self.assertEquals(lt(5) & gt(3), lt(5) & gt(3))

    def test_eq_OR (self):
        self.assertEquals(lt(5) | gt(3), lt(5) | gt(3))

    def test_eq_NOT (self):
        self.assertEquals(~lt(5), ~lt(5))

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

    def test_str_PRED_unnamed (self):
        self.assertTrue(str(Pred(ident)).startswith("<function <lambda> at"))

    def test_str_PRED_named (self):
        self.assertEquals(str(Pred(ident, name="id")), "id")

    def test_str_NOT_unnamed (self):
        self.assertTrue(str(~Pred(ident)).startswith("~<function <lambda> at"))

    def test_str_NOT_named (self):
        self.assertEquals(str(~Pred(ident, name="id")), "~id")

    def test_str_AND_named (self):
        self.assertEquals(str(gt(3) & lt(5)), "gt(3) & lt(5)")

    def test_str_OR_named (self):
        self.assertEquals(str(gt(3) | lt(5)), "gt(3) | lt(5)")

    def test_str_AndOrNot_unparenthesizedOr (self):
        self.assertEquals(str(gt(3) | lt(5) & ~eq(7)), "gt(3) | lt(5) & ~eq(7)")

    def test_str_AndOrNot_parenthesizedOr (self):
        self.assertEquals(str((gt(3) | lt(5)) & ~eq(7)), "(gt(3) | lt(5)) & ~eq(7)")

    def test_ast_returnsOpPredPair (self):
        (op, ast) = gt(3).ast()
        self.assertEquals(op, "PRED")
        self.assertEquals(type(ast), Pred)

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

    def test_pformat_onePred (self):
        p = lt(3)
        self.assertEquals(p.pformat(), "lt(3)")

    def test_pformat_onePred_customIndent (self):
        p = lt(3)
        self.assertEquals(p.pformat(indent=5), "lt(3)")

    def test_pformat_andOfTwoPreds (self):
        p = lt(7) & gt(3)
        self.assertEquals(p.pformat(), "AND\n  lt(7)\n  gt(3)")

    def test_pformat_andOfTwoPreds_customIndent (self):
        p = lt(7) & gt(3)
        self.assertEquals(p.pformat(indent=5), "AND\n     lt(7)\n     gt(3)")

    def test_pformat_orOfTwoPreds (self):
        p = lt(5) | eq(9)
        self.assertEquals(p.pformat(), "OR\n  lt(5)\n  eq(9)")

    def test_pformat_orOfTwoPreds_customIndent (self):
        p = lt(5) | eq(9)
        self.assertEquals(p.pformat(indent=3), "OR\n   lt(5)\n   eq(9)")

    def test_pformat_notPred (self):
        p = ~eq(4)
        self.assertEquals(p.pformat(), "NOT\n  eq(4)")

    def test_pformat_notPred_customIndent (self):
        p = ~eq(4)
        self.assertEquals(p.pformat(indent=7), "NOT\n       eq(4)")

