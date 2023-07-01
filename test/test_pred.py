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
        self.assertEqual(lt(5), lt(5))

    def test_eq_AND (self):
        self.assertEqual(lt(5) & gt(3), lt(5) & gt(3))

    def test_eq_OR (self):
        self.assertEqual(lt(5) | gt(3), lt(5) | gt(3))

    def test_eq_NOT (self):
        self.assertEqual(~lt(5), ~lt(5))

    def test_canANDPredicates (self):
        self.assertEqual(list(map(gt(3) & lt(5), [3, 4, 5])), [False, True, False])

    def test_canSEQPredicates_bothTrue (self):
        p = gt(3) >> lt(5)
        self.assertEqual(p(4), True)

    def test_canSEQPredicates_firstFails (self):
        p = gt(3) >> lt(5)
        self.assertEqual(p(7), False)

    def test_canORPredicates (self):
        self.assertEqual(list(map(lt(5) | gt(5), [4, 5, 6])), [True, False, True])

    def test_canNOTPredicates (self):
        self.assertEqual(list(map(~eq(3), [2, 3, 4])), [True, False, True])

    def test_canANDAndORAndNOTPredicates (self):
        # p = ((gt(0) & lt(4)) | (gt(5) & lt(9))) & ~(eq(2) | eq(7)) # confusing version
        betwen0and4 = gt(0) & lt(4)
        betwen5and9 = gt(5) & lt(9)
        not2or7 = ~(eq(2) | eq(7))
        p = (betwen0and4 | betwen5and9) & not2or7
        #             0      1     2      3     4      5      6     7      8     9
        expected = [False, True, False, True, False, False, True, False, True, False]
        self.assertEqual(list(map(p, range(10))), expected)

    def test_canSeqAndORAndNOTPredicates (self):
        # p = ((gt(0) & lt(4)) | (gt(5) & lt(9))) & ~(eq(2) | eq(7)) # confusing version
        betwen0and4 = gt(0) >> lt(4)
        betwen5and9 = gt(5) & lt(9)
        not2or7 = ~(eq(2) | eq(7))
        p = (betwen0and4 | betwen5and9) & not2or7
        #             0      1     2      3     4      5      6     7      8     9
        expected = [False, True, False, True, False, False, True, False, True, False]
        self.assertEqual(list(map(p, range(10))), expected)

    def test_str_PRED_unnamed (self):
        self.assertTrue(str(Pred(ident)).startswith("<function <lambda> at"))

    def test_str_PRED_named (self):
        self.assertEqual(str(Pred(ident, name="id")), "id")

    def test_str_NOT_unnamed (self):
        self.assertTrue(str(~Pred(ident)).startswith("~<function <lambda> at"))

    def test_str_NOT_named (self):
        self.assertEqual(str(~Pred(ident, name="id")), "~id")

    def test_str_AND_named (self):
        self.assertEqual(str(gt(3) & lt(5)), "gt(3) & lt(5)")

    def test_str_SEQ_named (self):
        self.assertEqual(str(gt(3) >> lt(5)), "gt(3) >> lt(5)")

    def test_str_OR_named (self):
        self.assertEqual(str(lt(3) | gt(5)), "lt(3) | gt(5)")

    def test_str_AndOrNot_unparenthesizedOr (self):
        self.assertEqual(str(gt(3) | lt(5) & ~eq(7)), "gt(3) | lt(5) & ~eq(7)")

    def test_str_SeqOrNot_unparenthesizedOr (self):
        self.assertEqual(str(gt(3) | lt(5) >> ~eq(7)), "gt(3) | lt(5) >> ~eq(7)")

    def test_str_AndOrNot_parenthesizedOr (self):
        self.assertEqual(str((gt(3) | lt(5)) & ~eq(7)), "(gt(3) | lt(5)) & ~eq(7)")

    def test_str_AndOrNot_parenthesizedOr (self):
        self.assertEqual(str((gt(3) | lt(5)) >> ~eq(7)), "(gt(3) | lt(5)) >> ~eq(7)")

    def test_NOT_namedNameStoredInNameProperty (self):
        self.assertEqual((~Pred(ident, name="id"))._name, "~id")

    def test_AND_namedNameStoredInNameProperty (self):
        self.assertEqual((gt(3) & lt(5))._name, "gt(3) & lt(5)")

    def test_SEQ_namedNameStoredInNameProperty (self):
        self.assertEqual((gt(3) >> lt(5))._name, "gt(3) >> lt(5)")

    def test_OR_namedNameStoredInNameProperty (self):
        self.assertEqual((lt(3) | gt(5))._name, "lt(3) | gt(5)")

    def test_typeCon_raisesOnWrongType (self):
        p = Pred(lambda x: x == "foo", typeCon=(str, lambda v: type(v) is str))
        self.assertRaises(TypeError, lambda: p(23))

    def test_typeCon_okayWithCorrectType (self):
        p = Pred(lambda x: x == "foo", typeCon=(str, lambda v: type(v) is str))
        self.assertFalse(p("bar"))

    def test_typeCon_multipleSpecifiedTypes_failCase (self):
        p = Pred(lambda x: x == 42, typeCon=([int, float], lambda v: type(v) in [int, float]))
        self.assertRaises(TypeError, lambda: p("foo"))

    def test_typeCon_multipleSpecifiedTypes_passCase (self):
        p = Pred(lambda x: x == 42, typeCon=([int, float], lambda v: type(v) in [int, float]))
        self.assertTrue(p(42.0))

    def test_typeCon_AND_typesMatch (self):
        p = Pred(lambda x: x > 0, typeCon=(int, lambda v: type(v) == int))
        q = Pred(lambda x: x < 9, typeCon=(int, lambda v: type(v) == int))
        self.assertTrue((p & q)(7))

    def test_typeCon_AND_typesDiffer (self):
        p = Pred(lambda x: x > 0, typeCon=(int, lambda v: type(v) == int))
        q = Pred(lambda x: x == "cat", typeCon=(str, lambda v: type(v) == str))
        self.assertRaises(TypeError, lambda: p & q)

    def test_typeCon_SEQ_typesMatch (self):
        p = Pred(lambda x: x > 0, typeCon=(int, lambda v: type(v) == int))
        q = Pred(lambda x: x < 9, typeCon=(int, lambda v: type(v) == int))
        self.assertTrue((p >> q)(5))

    def test_typeCon_SEQ_typesDiffer (self):
        p = Pred(lambda x: x > 0, typeCon=(int, lambda v: type(v) == int))
        q = Pred(lambda x: x == "cat", typeCon=(str, lambda v: type(v) == str))
        self.assertRaises(TypeError, lambda: p >> q)

    def test_typeCon_OR_typesMatch (self):
        p = Pred(lambda x: x < 3, typeCon=(int, lambda v: type(v) == int))
        q = Pred(lambda x: x > 5, typeCon=(int, lambda v: type(v) == int))
        self.assertTrue((p | q)(7))

    def test_typeCon_OR_typesDiffer (self):
        p = Pred(lambda x: x > 0, typeCon=(int, lambda v: type(v) == int))
        q = Pred(lambda x: x == "cat", typeCon=(str, lambda v: type(v) == str))
        self.assertRaises(TypeError, lambda: p | q)

    def test_ast_returnsOpPredPair (self):
        (op, ast) = gt(3).ast()
        self.assertEqual(op, "PRED")
        self.assertEqual(type(ast), Pred)

    def test_ast_PRED (self):
        (op, erand) = Pred(ident).ast()
        self.assertEqual(op, "PRED")
        self.assertTrue(callable(erand))

    def test_ast_AND (self):
        (op, erands) = (gt(3) & lt(5)).ast()
        self.assertEqual(op, "AND")
        ((lop, lerands), (rop, rerands)) = erands
        self.assertEqual(lop, "PRED")
        self.assertEqual(rop, "PRED")
        self.assertTrue(callable(lerands))
        self.assertTrue(callable(rerands))

    def test_ast_SEQ (self):
        (op, erands) = (gt(3) >> lt(5)).ast()
        self.assertEqual(op, "SEQ")
        ((lop, lerands), (rop, rerands)) = erands
        self.assertEqual(lop, "PRED")
        self.assertEqual(rop, "PRED")
        self.assertTrue(callable(lerands))
        self.assertTrue(callable(rerands))

    def test_ast_OR (self):
        (op, erands) = (gt(3) & lt(5)).ast()
        self.assertEqual(op, "AND")
        ((lop, lerands), (rop, rerands)) = erands
        self.assertEqual(lop, "PRED")
        self.assertEqual(rop, "PRED")
        self.assertTrue(callable(lerands))
        self.assertTrue(callable(rerands))

    def test_ast_NOT (self):
        (op, erand) = (~Pred(ident)).ast()
        self.assertEqual(op, "NOT")
        (nop, nerands) = erand
        self.assertEqual(nop, "PRED")
        self.assertTrue(callable(nerands))

    def test_canPassAFixFunction (self):
        data = [1,2,4]
        def fix (x):
            x.append(3)
        p = Pred(lambda x: 3 in x, fix=fix)
        result = p.validate(data)
        expected = { "op": "PRED"
                   , "ref": p
                   , "result": True
                   , "status": "FIXED"
                   }
        self.assertEqual(result, expected)

    def test_validate_PRED_pass (self):
        p = eq(4)
        result = p.validate(4)
        expected = { "op": "PRED"
                   , "ref": p
                   , "result": True
                   }
        self.assertEqual(result, expected)

    def test_validate_PRED_fail (self):
        p = eq(4)
        result = p.validate(3)
        expected = { "op": "PRED"
                   , "ref": p
                   , "result": False
                   }
        self.assertEqual(result, expected)

    def test_validate_PRED_noSolve_hasNoResult (self):
        p = eq(3)
        result = p.validate(23, noSolve=True)
        expected = { "op": "PRED"
                   , "ref": p
                   }
        self.assertEqual(result, expected)

    def test_validate_NOT_noSolve_hasNoResults (self):
        q = eq(3)
        p = ~q
        result = p.validate(23, noSolve=True)
        expected = { "op": "NOT"
                   , "ref": p
                   , "pred": { "op": "PRED"
                             , "ref": q
                             }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_noSolve_hasNoResults (self):
        a = eq(7)
        b = eq(3)
        p = a & b
        result = p.validate(17, noSolve=True)
        expected = { "op": "AND"
                   , "ref": p
                   , "left": { "op": "PRED"
                             , "ref": a
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_noSolve_hasNoResults (self):
        a = eq(7)
        b = eq(3)
        p = a | b
        result = p.validate(17, noSolve=True)
        expected = { "op": "OR"
                   , "ref": p
                   , "left": { "op": "PRED"
                             , "ref": a
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_PRED_fixFails (self):
        data = {"value": "incorrect"}
        def fix (x):
            x["value"] = "still incorrect"
        p = Pred(lambda x: x["value"] == "correct", fix=fix)
        result = p.validate(data)
        expected = { "op": "PRED"
                   , "ref": p
                   , "result": False
                   , "status": "UNFIXED"
                   }
        self.assertEqual(result, expected)

    def test_validate_PRED_fixWorks (self):
        data = {"value": "incorrect"}
        def fix (x):
            x["value"] = "correct"
        p = Pred(lambda x: x["value"] == "correct", fix=fix)
        result = p.validate(data)
        expected = { "op": "PRED"
                   , "ref": p
                   , "result": True
                   , "status": "FIXED"
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_bothFail (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John")
        b = Pred(lambda x: x["lname"] == "Johnson")
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_bothPass (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob")
        b = Pred(lambda x: x["lname"] == "Smith")
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": p
                             , "result": True
                             }
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_leftFails_noFix (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "John")
        b = Pred(lambda x: x["lname"] == "Smith")
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_leftFails_fixFails (self):
        data = {"fname": "Bob", "lname": "Smith"}
        def fix (x):
            x["fname"] = "Bill"
        a = Pred(lambda x: x["fname"] == "John", fix=fix)
        b = Pred(lambda x: x["lname"] == "Smith")
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             , "status": "UNFIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_leftFails_fixWorks (self):
        data = {"fname": "Bob", "lname": "Smith"}
        def fix (x):
            x["fname"] = "John"
        a = Pred(lambda x: x["fname"] == "John", fix=fix)
        b = Pred(lambda x: x["lname"] == "Smith")
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             , "status": "FIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_rightFails_noFix (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob")
        b = Pred(lambda x: x["lname"] == "Johnson")
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_rightFails_fixFails (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob")
        def fix (x):
            x["lname"] = "Johnson"
        b = Pred(lambda x: x["lname"] == "Jones", fix=fix)
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              , "status": "UNFIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_rightFails_fixWorks (self):
        data = {"fname": "Bob", "lname": "Smith"}
        a = Pred(lambda x: x["fname"] == "Bob")
        def fix (x):
            x["lname"] = "Jones"
        b = Pred(lambda x: x["lname"] == "Jones", fix=fix)
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              , "status": "FIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_bothFail_fixesFail (self):
        data = {"fname": "Bob", "lname": "Smith"}
        def fix (x):
            x["fname"] = "Frank"
        a = Pred(lambda x: x["fname"] == "John", fix=fix)
        def fix (x):
            x["lname"] = "Lewis"
        b = Pred(lambda x: x["lname"] == "Johnson", fix=fix)
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                              , "status": "UNFIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              , "status": "UNFIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_AND_bothFail_fixesWork (self):
        data = {"fname": "Bob", "lname": "Smith"}
        def fix (x):
            x["fname"] = "John"
        a = Pred(lambda x: x["fname"] == "John", fix=fix)
        def fix (x):
            x["lname"] = "Johnson"
        b = Pred(lambda x: x["lname"] == "Johnson", fix=fix)
        p = a & b
        result = p.validate(data)
        expected = { "op": "AND"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             , "status": "FIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              , "status": "FIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_bothFail (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x)
        b = Pred(lambda x: 6 in x)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_bothPass (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x)
        b = Pred(lambda x: 8 in x)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_leftFails_noFix (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 2 in x)
        b = Pred(lambda x: 8 in x)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_leftFails_fixFails (self):
        data = [1,3,8,9]
        def fix (x):
            x.append(4)
        a = Pred(lambda x: 2 in x, fix=fix)
        b = Pred(lambda x: 8 in x)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             , "status": "UNFIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_leftFails_fixWorks (self):
        data = [1,3,8,9]
        def fix (x):
            x.append(2)
        a = Pred(lambda x: 2 in x, fix=fix)
        b = Pred(lambda x: 8 in x)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             , "status": "FIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_rightFails_noFix (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x)
        b = Pred(lambda x: 6 in x)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_rightFails_fixFails (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x)
        def fix (x):
            x.append(7)
        b = Pred(lambda x: 6 in x, fix=fix)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              , "status": "UNFIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_rightFails_fixWorks (self):
        data = [1,3,8,9]
        a = Pred(lambda x: 3 in x)
        def fix (x):
            x.append(7)
        b = Pred(lambda x: 7 in x, fix=fix)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              , "status": "FIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_bothFail_fixesFail (self):
        data = [1,3,8,9]
        def fix (x):
            x.append(4)
        a = Pred(lambda x: 2 in x, fix=fix)
        def fix (x):
            x.append(7)
        b = Pred(lambda x: 6 in x, fix=fix)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             , "status": "UNFIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              , "status": "UNFIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_OR_bothFail_fixesWork (self):
        data = [1,3,8,9]
        def fix (x):
            x.append(2)
        a = Pred(lambda x: 2 in x, fix=fix)
        def fix (x):
            x.append(6)
        b = Pred(lambda x: 6 in x, fix=fix)
        p = a | b
        result = p.validate(data)
        expected = { "op": "OR"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             , "status": "FIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              , "status": "FIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_NOT_fail (self):
        data = {"value": 42}
        p = ~Pred(lambda x: "value" in x)
        result = p.validate(data)
        expected = { "op": "NOT"
                   , "ref": p
                   , "result": False
                   , "pred": { "op": "PRED"
                             , "ref": p._pred
                             , "result": True
                             }
                   }
        self.assertEqual(result, expected)

    def test_validate_NOT_pass (self):
        data = {"value": 42}
        p = ~Pred(lambda x: "nonvalue" in x)
        result = p.validate(data)
        expected = { "op": "NOT"
                   , "ref": p
                   , "result": True
                   , "pred": { "op": "PRED"
                             , "ref": p._pred
                             , "result": False
                             }
                   }
        self.assertEqual(result, expected)

    def test_validate_SEQ_bothPass (self):
        data = {"value": "target"}
        a = Pred(lambda x: "value" in x)
        b = Pred(lambda x: x["value"] == "target")
        p = a >> b
        result = p.validate(data)
        expected = { "op": "SEQ"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_SEQ_leftFails_noFix (self):
        data = {"wrongvalue": "wrongtarget"}
        a = Pred(lambda x: "value" in x)
        b = Pred(lambda x: x["value"] == "target")
        p = a >> b
        result = p.validate(data)
        expected = { "op": "SEQ"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_SEQ_leftFails_fixFails (self):
        data = {"wrongvalue": "wrongtarget"}
        def fix (x):
            x["stillnothelping"] = "useless"
        a = Pred(lambda x: "value" in x, fix=fix)
        b = Pred(lambda x: x["value"] == "target")
        p = a >> b
        result = p.validate(data)
        expected = { "op": "SEQ"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": False
                             , "status": "UNFIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_SEQ_leftFails_fixWorks (self):
        data = {"wrongvalue": "wrongtarget"}
        def fix (x):
            x["value"] = "target"
        a = Pred(lambda x: "value" in x, fix=fix)
        b = Pred(lambda x: x["value"] == "target")
        p = a >> b
        result = p.validate(data)
        expected = { "op": "SEQ"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             , "status": "FIXED"
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_SEQ_rightFails_noFix (self):
        data = {"value": "wrongtarget"}
        a = Pred(lambda x: "value" in x)
        b = Pred(lambda x: x["value"] == "target")
        p = a >> b
        result = p.validate(data)
        expected = { "op": "SEQ"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_SEQ_rightFails_fixFails (self):
        data = {"value": "wrongtarget"}
        a = Pred(lambda x: "value" in x)
        def fix (x):
            x["value"] = "stillwrongtarget"
        b = Pred(lambda x: x["value"] == "target", fix=fix)
        p = a >> b
        result = p.validate(data)
        expected = { "op": "SEQ"
                   , "ref": p
                   , "result": False
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": False
                              , "status": "UNFIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_validate_SEQ_rightFails_fixWorks (self):
        data = {"value": "wrongtarget"}
        a = Pred(lambda x: "value" in x)
        def fix (x):
            x["value"] = "target"
        b = Pred(lambda x: x["value"] == "target", fix=fix)
        p = a >> b
        result = p.validate(data)
        expected = { "op": "SEQ"
                   , "ref": p
                   , "result": True
                   , "left": { "op": "PRED"
                             , "ref": a
                             , "result": True
                             }
                   , "right": { "op": "PRED"
                              , "ref": b
                              , "result": True
                              , "status": "FIXED"
                              }
                   }
        self.assertEqual(result, expected)

    def test_pformat_onePred (self):
        p = lt(3)
        self.assertEqual(p.pformat(), "lt(3)")

    def test_pformat_onePred_customIndent (self):
        p = lt(3)
        self.assertEqual(p.pformat(indent=5), "lt(3)")

    def test_pformat_ANDOfTwoPreds (self):
        p = lt(7) & gt(3)
        self.assertEqual(p.pformat(), "AND\n  lt(7)\n  gt(3)")

    def test_pformat_SEQOfTwoPreds (self):
        p = lt(7) >> gt(3)
        self.assertEqual(p.pformat(), "SEQ\n  lt(7)\n  gt(3)")

    def test_pformat_ANDOfTwoPreds_customIndent (self):
        p = lt(7) & gt(3)
        self.assertEqual(p.pformat(indent=5), "AND\n     lt(7)\n     gt(3)")

    def test_pformat_SEQOfTwoPreds_customIndent (self):
        p = lt(7) >> gt(3)
        self.assertEqual(p.pformat(indent=5), "SEQ\n     lt(7)\n     gt(3)")

    def test_pformat_OROfTwoPreds (self):
        p = lt(5) | eq(9)
        self.assertEqual(p.pformat(), "OR\n  lt(5)\n  eq(9)")

    def test_pformat_OROfTwoPreds_customIndent (self):
        p = lt(5) | eq(9)
        self.assertEqual(p.pformat(indent=3), "OR\n   lt(5)\n   eq(9)")

    def test_pformat_NOTPred (self):
        p = ~eq(4)
        self.assertEqual(p.pformat(), "NOT\n  eq(4)")

    def test_pformat_NOTPred_customIndent (self):
        p = ~eq(4)
        self.assertEqual(p.pformat(indent=7), "NOT\n       eq(4)")

