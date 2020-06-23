import unittest
from nose.plugins.attrib import attr

from ..pred import *


ident = lambda x: x

lt  = lambda n: Pred(lambda x: x < n, name="lt(" + str(n) + ")")
lte  = lambda n: Pred(lambda x: x <= n, name="lte(" + str(n) + ")")
eq  = lambda n: Pred(lambda x: x == n, name="eq(" + str(n) + ")")
gte  = lambda n: Pred(lambda x: x >= n, name="gte(" + str(n) + ")")
gt  = lambda n: Pred(lambda x: x > n, name="gt(" + str(n) + ")")


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

    def test_canSEQPredicates_bothTrue (self):
        p = gt(3) >> lt(5)
        self.assertEquals(p(4), True)

    def test_canSEQPredicates_firstFails (self):
        p = gt(3) >> lt(5)
        self.assertEquals(p(7), False)

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

    def test_canSeqAndORAndNOTPredicates (self):
        # p = ((gt(0) & lt(4)) | (gt(5) & lt(9))) & ~(eq(2) | eq(7)) # confusing version
        betwen0and4 = gt(0) >> lt(4)
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

    def test_str_SEQ_named (self):
        self.assertEquals(str(gt(3) >> lt(5)), "gt(3) >> lt(5)")

    def test_str_OR_named (self):
        self.assertEquals(str(lt(3) | gt(5)), "lt(3) | gt(5)")

    def test_str_AndOrNot_unparenthesizedOr (self):
        self.assertEquals(str(gt(3) | lt(5) & ~eq(7)), "gt(3) | lt(5) & ~eq(7)")

    def test_str_SeqOrNot_unparenthesizedOr (self):
        self.assertEquals(str(gt(3) | lt(5) >> ~eq(7)), "gt(3) | lt(5) >> ~eq(7)")

    def test_str_AndOrNot_parenthesizedOr (self):
        self.assertEquals(str((gt(3) | lt(5)) & ~eq(7)), "(gt(3) | lt(5)) & ~eq(7)")

    def test_str_AndOrNot_parenthesizedOr (self):
        self.assertEquals(str((gt(3) | lt(5)) >> ~eq(7)), "(gt(3) | lt(5)) >> ~eq(7)")

    def test_NOT_namedNameStoredInNameProperty (self):
        self.assertEquals((~Pred(ident, name="id"))._name, "~id")

    def test_AND_namedNameStoredInNameProperty (self):
        self.assertEquals((gt(3) & lt(5))._name, "gt(3) & lt(5)")

    def test_SEQ_namedNameStoredInNameProperty (self):
        self.assertEquals((gt(3) >> lt(5))._name, "gt(3) >> lt(5)")

    def test_OR_namedNameStoredInNameProperty (self):
        self.assertEquals((lt(3) | gt(5))._name, "lt(3) | gt(5)")

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

    def test_ast_SEQ (self):
        (op, erands) = (gt(3) >> lt(5)).ast()
        self.assertEqual(op, "SEQ")
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

    def test_canPassAFixFunction (self):
        data = [1,2,4]
        def fix (x):
            x.append(3)
        p = Pred(lambda x: 3 in x, fix=fix)
        result = p.validate(data)
        self.assertTrue(result["result"])
        self.assertEquals(result["op"], "PRED")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["status"], "FIXED")

    def test_validate_PRED_pass (self):
        p = eq(4)
        result = p.validate(4)
        self.assertEquals(result["op"], "PRED")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

    def test_validate_PRED_fail (self):
        p = eq(4)
        result = p.validate(3)
        self.assertEquals(result["op"], "PRED")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

    def test_validate_PRED_fixFails (self):
        data = {"value": "incorrect"}
        def fix (x):
            x["value"] = "still incorrect"
        p = Pred(lambda x: x["value"] == "correct")
        p._fix = fix
        result = p.validate(data)
        self.assertEquals(result["op"], "PRED")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)
        self.assertEquals(result["status"], "UNFIXED")

    def test_validate_PRED_fixWorks (self):
        data = {"value": "incorrect"}
        def fix (x):
            x["value"] = "correct"
        p = Pred(lambda x: x["value"] == "correct")
        p._fix = fix
        result = p.validate(data)
        self.assertEquals(result["op"], "PRED")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)
        self.assertEquals(result["status"], "FIXED")

    def test_validate_AND_bothFail (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John", name="fname(\"John\")")
        b = Pred(lambda x: x["lname"] == "Johnson", name="lname(\"Johnson\")")
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertFalse("status" in result["right"])

    def test_validate_AND_bothPass (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob", name="fname(\"Bob\")")
        b = Pred(lambda x: x["lname"] == "Smith", name="lname(\"Smith\")")
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_AND_leftFails_noFix (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John", name="fname(\"John\")")
        b = Pred(lambda x: x["lname"] == "Smith", name="lname(\"Smith\")")
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_AND_leftFails_fixFails (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John", name="fname(\"John\")")
        def fix (x):
            x["fname"] = "Bill"
        a._fix = fix
        b = Pred(lambda x: x["lname"] == "Smith", name="lname(\"Smith\")")
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertEquals(result["left"]["status"], "UNFIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_AND_leftFails_fixWorks (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John", name="fname(\"John\")")
        def fix (x):
            x["fname"] = "John"
        a._fix = fix
        b = Pred(lambda x: x["lname"] == "Smith", name="lname(\"Smith\")")
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertEquals(result["left"]["status"], "FIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_AND_rightFails_noFix (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob", name="fname(\"Bob\")")
        b = Pred(lambda x: x["lname"] == "Johnson", name="lname(\"Johnson\")")
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertFalse("status" in result["right"])

    def test_validate_AND_rightFails_fixFails (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob", name="fname(\"Bob\")")
        b = Pred(lambda x: x["lname"] == "Jones", name="lname(\"Smith\")")
        def fix (x):
            x["lname"] = "Johnson"
        b._fix = fix
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertEquals(result["right"]["status"], "UNFIXED")

    def test_validate_AND_rightFails_fixWorks (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob", name="fname(\"Bob\")")
        b = Pred(lambda x: x["lname"] == "Jones", name="lname(\"Smith\")")
        def fix (x):
            x["lname"] = "Jones"
        b._fix = fix
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertEquals(result["right"]["status"], "FIXED")

    def test_validate_AND_bothFail_fixesFail (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John", name="fname(\"John\")")
        def fix (x):
            x["fname"] = "Frank"
        a._fix = fix
        b = Pred(lambda x: x["lname"] == "Johnson", name="lname(\"Johnson\")")
        def fix (x):
            x["lname"] = "Lewis"
        b._fix = fix
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertEquals(result["left"]["status"], "UNFIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertEquals(result["right"]["status"], "UNFIXED")

    def test_validate_AND_bothFail_fixesWork (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John", name="fname(\"John\")")
        def fix (x):
            x["fname"] = "John"
        a._fix = fix
        b = Pred(lambda x: x["lname"] == "Johnson", name="lname(\"Johnson\")")
        def fix (x):
            x["lname"] = "Johnson"
        b._fix = fix
        p = a & b
        result = p.validate(data)
        self.assertEquals(result["op"], "AND")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertEquals(result["left"]["status"], "FIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertEquals(result["right"]["status"], "FIXED")

    def test_validate_OR_bothFail (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x, name="listContains(2)")
        b = Pred(lambda x: 6 in x, name="listContains(6)")
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertFalse("status" in result["right"])

    def test_validate_OR_bothPass (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x, name="listContains(3)")
        b = Pred(lambda x: 8 in x, name="listContains(8)")
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_OR_leftFails_noFix (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x, name="listContains(2)")
        b = Pred(lambda x: 8 in x, name="listContains(8)")
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_OR_leftFails_fixFails (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x, name="listContains(2)")
        def fix (x):
            x.append(4)
        a._fix = fix
        b = Pred(lambda x: 8 in x, name="listContains(8)")
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertEquals(result["left"]["status"], "UNFIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_OR_leftFails_fixWorks (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x, name="listContains(2)")
        def fix (x):
            x.append(2)
        a._fix = fix
        b = Pred(lambda x: 8 in x, name="listContains(8)")
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertEquals(result["left"]["status"], "FIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_OR_rightFails_noFix (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x, name="listContains(3)")
        b = Pred(lambda x: 6 in x, name="listContains(6)")
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertFalse("status" in result["right"])

    def test_validate_OR_rightFails_fixFails (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x, name="listContains(3)")
        b = Pred(lambda x: 6 in x, name="listContains(6)")
        def fix (x):
            x.append(7)
        b._fix = fix
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertEquals(result["right"]["status"], "UNFIXED")

    def test_validate_OR_rightFails_fixWorks (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x, name="listContains(3)")
        b = Pred(lambda x: 7 in x, name="listContains(7)")
        def fix (x):
            x.append(7)
        b._fix = fix
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertEquals(result["right"]["status"], "FIXED")

    def test_validate_OR_bothFail_fixesFail (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x, name="listContains(2)")
        def fix (x):
            x.append(4)
        a._fix = fix
        b = Pred(lambda x: 6 in x, name="listContains(6)")
        def fix (x):
            x.append(7)
        b._fix = fix
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertEquals(result["left"]["status"], "UNFIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertEquals(result["right"]["status"], "UNFIXED")

    def test_validate_OR_bothFail_fixesWork (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x, name="listContains(2)")
        def fix (x):
            x.append(2)
        a._fix = fix
        b = Pred(lambda x: 6 in x, name="listContains(6)")
        def fix (x):
            x.append(6)
        b._fix = fix
        p = a | b
        result = p.validate(data)
        self.assertEquals(result["op"], "OR")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertEquals(result["right"]["status"], "FIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertEquals(result["right"]["status"], "FIXED")

    def test_validate_NOT_fail (self):
        data = {"value": "shouldn't exist"}
        p = ~Pred(lambda x: "value" in x)
        result = p.validate(data)
        self.assertEquals(result["op"], "NOT")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)

    def test_validate_NOT_pass (self):
        data = {"value": "shouldn't exist"}
        p = ~Pred(lambda x: "nonvalue" in x)
        result = p.validate(data)
        self.assertEquals(result["op"], "NOT")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)

    def test_validate_NOT_fixFails (self):
        data = {"value": "shouldn't exist"}
        p = ~Pred(lambda x: "value" in x)
        def fix (x):
            x["nonvalue"] = "not helping"
        p._fix = fix
        result = p.validate(data)
        self.assertEquals(result["op"], "NOT")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)
        self.assertEquals(result["status"], "UNFIXED")

    def test_validate_NOT_fixWorks (self):
        data = {"value": "shouldn't exist"}
        p = ~Pred(lambda x: "value" in x)
        def fix (x):
            del x["value"]
        p._fix = fix
        result = p.validate(data)
        self.assertEquals(result["op"], "NOT")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)
        self.assertEquals(result["status"], "FIXED")

    def test_validate_SEQ_bothFail (self):
        pass

    def test_validate_SEQ_bothPass (self):
        data = {"value": "target"}
        a = Pred(lambda x: "value" in x, name="dictHasKey(\"value\")")
        b = Pred(lambda x: x["value"] == "target", name="key(\"value\").eq(\"target\")")
        p = a >> b
        result = p.validate(data)
        self.assertEquals(result["op"], "SEQ")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)
        self.assertFalse("status" in result)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])

    def test_validate_SEQ_leftFails_noFix (self):
        data = {"wrongvalue": "wrongtarget"}
        a = Pred(lambda x: "value" in x, name="dictHasKey(\"value\")")
        b = Pred(lambda x: x["value"] == "target", name="key(\"value\").eq(\"target\")")
        p = a >> b
        result = p.validate(data)
        self.assertEquals(result["op"], "SEQ")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)
        self.assertFalse("status" in result)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertFalse("result" in result["right"])
        self.assertFalse("status" in result["right"])

    def test_validate_SEQ_leftFails_fixFails (self):
        data = {"wrongvalue": "wrongtarget"}
        a = Pred(lambda x: "value" in x, name="dictHasKey(\"value\")")
        def fix (x):
            x["stillnothelping"] = "useless"
        a._fix = fix
        b = Pred(lambda x: x["value"] == "target", name="key(\"value\").eq(\"target\")")
        p = a >> b
        result = p.validate(data)
        self.assertEquals(result["op"], "SEQ")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)
        self.assertFalse("status" in result)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], False)
        self.assertEquals(result["left"]["status"], "UNFIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertFalse("result" in result["right"])
        self.assertFalse("status" in result["right"])

    def test_validate_SEQ_leftFails_fixWorks (self):
        data = {"wrongvalue": "wrongtarget"}
        a = Pred(lambda x: "value" in x, name="dictHasKey(\"value\")")
        def fix (x):
            x["value"] = "target"
        a._fix = fix
        b = Pred(lambda x: x["value"] == "target", name="key(\"value\").eq(\"target\")")
        p = a >> b
        result = p.validate(data)
        self.assertEquals(result["op"], "SEQ")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)
        self.assertFalse("status" in result)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertEquals(result["left"]["status"], "FIXED")

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertFalse("status" in result["right"])


    def test_validate_SEQ_rightFails_noFix (self):
        data = {"value": "wrongtarget"}
        a = Pred(lambda x: "value" in x, name="dictHasKey(\"value\")")
        b = Pred(lambda x: x["value"] == "target", name="key(\"value\").eq(\"target\")")
        p = a >> b
        result = p.validate(data)
        self.assertEquals(result["op"], "SEQ")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)
        self.assertFalse("status" in result)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertFalse("status" in result["right"])

    def test_validate_SEQ_rightFails_fixFails (self):
        data = {"value": "wrongtarget"}
        a = Pred(lambda x: "value" in x, name="dictHasKey(\"value\")")
        b = Pred(lambda x: x["value"] == "target", name="key(\"value\").eq(\"target\")")
        def fix (x):
            x["value"] = "stillwrongtarget"
        b._fix = fix
        p = a >> b
        result = p.validate(data)
        self.assertEquals(result["op"], "SEQ")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], False)
        self.assertFalse("status" in result)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], False)
        self.assertEquals(result["right"]["status"], "UNFIXED")

    def test_validate_SEQ_rightFails_fixWorks (self):
        data = {"value": "wrongtarget"}
        a = Pred(lambda x: "value" in x, name="dictHasKey(\"value\")")
        b = Pred(lambda x: x["value"] == "target", name="key(\"value\").eq(\"target\")")
        def fix (x):
            x["value"] = "target"
        b._fix = fix
        p = a >> b
        result = p.validate(data)
        self.assertEquals(result["op"], "SEQ")
        self.assertEquals(result["pred"], p)
        self.assertEquals(result["result"], True)
        self.assertFalse("status" in result)

        self.assertEquals(result["left"]["op"], "PRED")
        self.assertEquals(result["left"]["pred"], a)
        self.assertEquals(result["left"]["result"], True)
        self.assertFalse("status" in result["left"])

        self.assertEquals(result["right"]["op"], "PRED")
        self.assertEquals(result["right"]["pred"], b)
        self.assertEquals(result["right"]["result"], True)
        self.assertEquals(result["right"]["status"], "FIXED")

    def test_pformat_onePred (self):
        p = lt(3)
        self.assertEquals(p.pformat(), "lt(3)")

    def test_pformat_onePred_customIndent (self):
        p = lt(3)
        self.assertEquals(p.pformat(indent=5), "lt(3)")

    def test_pformat_ANDOfTwoPreds (self):
        p = lt(7) & gt(3)
        self.assertEquals(p.pformat(), "AND\n  lt(7)\n  gt(3)")

    def test_pformat_SEQOfTwoPreds (self):
        p = lt(7) >> gt(3)
        self.assertEquals(p.pformat(), "SEQ\n  lt(7)\n  gt(3)")

    def test_pformat_ANDOfTwoPreds_customIndent (self):
        p = lt(7) & gt(3)
        self.assertEquals(p.pformat(indent=5), "AND\n     lt(7)\n     gt(3)")

    def test_pformat_SEQOfTwoPreds_customIndent (self):
        p = lt(7) >> gt(3)
        self.assertEquals(p.pformat(indent=5), "SEQ\n     lt(7)\n     gt(3)")

    def test_pformat_OROfTwoPreds (self):
        p = lt(5) | eq(9)
        self.assertEquals(p.pformat(), "OR\n  lt(5)\n  eq(9)")

    def test_pformat_OROfTwoPreds_customIndent (self):
        p = lt(5) | eq(9)
        self.assertEquals(p.pformat(indent=3), "OR\n   lt(5)\n   eq(9)")

    def test_pformat_NOTPred (self):
        p = ~eq(4)
        self.assertEquals(p.pformat(), "NOT\n  eq(4)")

    def test_pformat_NOTPred_customIndent (self):
        p = ~eq(4)
        self.assertEquals(p.pformat(indent=7), "NOT\n       eq(4)")

