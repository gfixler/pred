import unittest
from nose.plugins.attrib import attr

import tempfile

from ..accessor import Accessor, StringAccessor, NumAccessor


ident = lambda x: x
const = lambda x: lambda _: x


class Test_Accessor (unittest.TestCase):

    def test_acceptsAndUsesAccessFunction (self):
        self.assertEqual(Accessor(ident)("foo"), "foo")

    def test_canNameAccessors (self):
        accr = Accessor(const(True), name="const(True)")
        # HACK law of demeter violation
        self.assertEqual(accr._name, "const(True)")

    def test_strWorksOnNamedAccessors (self):
        accr = Accessor(ident, name="ident")
        self.assertEqual(str(accr), "ident")

    def test_strYieldsFunctionStrOnUnnamedAccessors (self):
        accr = Accessor(ident)
        # HACK law of demeter violation
        self.assertEqual(str(accr), str(accr._accFunc))

    def test_canCreatePred (self):
        pred = Accessor(ident).pred(lambda s: len(s) == 7)
        self.assertTrue(pred("testing"))

    def test_strComposesStrNamesOfNamedAccessorAndPred (self):
        accr = Accessor(ident, name="ident")
        pred = accr.pred(const(True), name="const(True)")
        self.assertEqual(str(pred), "const(True) . ident")

    def test_strComposesStrNameOfNamedAcessorWithFunctionStrOfUnnamedPred (self):
        accr = Accessor(ident, name="ident")
        p = const(True)
        pred = accr.pred(p)
        # HACK law of demeter violation
        self.assertEqual(str(pred),  str(p) + " . ident")

    def test_strComposesUnnamedAccessorFunctionStrWithStrOfNamedPred (self):
        accr = Accessor(ident)
        pred = accr.pred(const(False), name="const(False)")
        # HACK law of demeter violation
        self.assertEqual(str(pred), "const(False) . " + str(accr._accFunc))

    def test_strComposesFunctionStrsOnUnnamedAccessorAndPred (self):
        accr = Accessor(ident)
        p = const(True)
        pred = accr.pred(p)
        # HACK law of demeter violation
        self.assertEqual(str(pred), str(p) + " . " + str(accr._accFunc))

    def test_canCreateEqualsPred (self):
        accr = StringAccessor(lambda d: d["key"])
        data = {"key": "value"}
        self.assertTrue(accr.equals("value")(data))
        self.assertFalse(accr.equals("random")(data))

    def test_equalsPredIsNamedCorrectly (self):
        accr = StringAccessor(lambda d: d["key"])
        self.assertEqual(str(accr.equals("\"key\"")), "(== \"key\")")

    def test_canMakeDictKeyAccessor (self):
        data = {"a": 3, "b": 42, "c": 7}
        self.assertEqual(Accessor(lambda d: d["b"])(data), 42)


class Test_StringAccessor (unittest.TestCase):

    def setUp (self):
        self.data = {"name": "Bob"}
        self.name = StringAccessor(lambda d: d["name"])
        self.namedName = StringAccessor(lambda d: d["name"], name="name")

    def test_identityOnStringWorks (self):
        self.assertEqual(StringAccessor(ident)("bar"), "bar")

    def test_identityOnNonStringRaises (self):
        self.assertRaises(TypeError, lambda: StringAccessor(ident)(42))

    def test_canCreateContainsPred (self):
        self.assertTrue(self.name.contains("o")(self.data))
        self.assertFalse(self.name.contains("e")(self.data))

    def test_containsPredIsNamedCorrectly (self):
        self.assertEqual(str(self.name.contains("o")), "contains(\"o\")")

    def test_containsPredCombinesWithExistingNameCorrectly (self):
        self.assertEqual(str(self.namedName.contains("o")), "name.contains(\"o\")")

    def test_canCreateStartswithPred (self):
        self.assertTrue(self.name.startswith("B")(self.data))
        self.assertFalse(self.name.startswith("A")(self.data))

    def test_startswithPredIsNamedCorrectly (self):
        self.assertEqual(str(self.name.startswith("B")), "startswith(\"B\")")

    def test_startswithPredCombinesWithExistingNameCorrectly (self):
        self.assertEqual(str(self.namedName.startswith("o")), "name.startswith(\"o\")")

    def test_canCreateEndswithPred (self):
        self.assertTrue(self.name.endswith("b")(self.data))
        self.assertFalse(self.name.endswith("e")(self.data))

    def test_endswithPredIsNamedCorrectly (self):
        self.assertEqual(str(self.name.endswith("b")), "endswith(\"b\")")

    def test_endswithPredCombinesWithExistingNameCorrectly (self):
        self.assertEqual(str(self.namedName.endswith("o")), "name.endswith(\"o\")")

    def test_canCreateMatchesPred (self):
        self.assertTrue(self.name.matches(".*\d\d-\d\d.*")({"name": "blue_23-42_hike"}))
        self.assertFalse(self.name.matches(".*\d\d-\d\d.*")({"name": "ab-cd"}))

    def test_matchesPredIsNamedCorrectly (self):
        self.assertEqual(str(self.name.matches(".*\d\d-\d\d.*")), "matches(\".*\d\d-\d\d.*\")")

    def test_matchesPredCombinesWithExistingNameCorrectly (self):
        self.assertEqual(str(self.namedName.matches("o")), "name.matches(\"o\")")


class Test_NumAccessor (unittest.TestCase):

    def test_identityOnIntsWorks (self):
        self.assertEqual(NumAccessor(ident)(7), 7)

    def test_identityOnFloatsWorks (self):
        self.assertEqual(NumAccessor(ident)(7.0), 7.0)

    def test_identityOnNonNumsRaises (self):
        self.assertRaises(TypeError, lambda: NumAccessor(ident)("foo"))

    def test_ltOnInt (self):
        p = NumAccessor(ident).lt(4)
        self.assertTrue(p(3))
        self.assertFalse(p(4))

    def test_ltIsNamedCorrectly (self):
        p = NumAccessor(ident).lt(4)
        self.assertEqual(str(p), "lt(4)")

    def test_ltCombinesWithExistingNameCorrectly (self):
        p = NumAccessor(ident, name="id").lt(4)
        self.assertEqual(str(p), "id.lt(4)")

    def test_lteOnInt (self):
        p = NumAccessor(ident).lte(4)
        self.assertTrue(p(3))
        self.assertTrue(p(4))
        self.assertFalse(p(5))

    def test_lteIsNamedCorrectly (self):
        p = NumAccessor(ident).lte(4)
        self.assertEqual(str(p), "lte(4)")

    def test_lteCombinesWithExistingNameCorrectly (self):
        p = NumAccessor(ident, name="id").lte(4)
        self.assertEqual(str(p), "id.lte(4)")

    def test_eqOnInt (self):
        p = NumAccessor(ident).eq(4)
        self.assertTrue(p(4))
        self.assertFalse(p(3))

    def test_eqIsNamedCorrectly (self):
        p = NumAccessor(ident).eq(4)
        self.assertEqual(str(p), "eq(4)")

    def test_eqCombinesWithExistingNameCorrectly (self):
        p = NumAccessor(ident, name="id").eq(4)
        self.assertEqual(str(p), "id.eq(4)")

    def test_gteOnInt (self):
        p = NumAccessor(ident).gte(4)
        self.assertFalse(p(3))
        self.assertTrue(p(4))
        self.assertTrue(p(5))

    def test_gteIsNamedCorrectly (self):
        p = NumAccessor(ident).gte(4)
        self.assertEqual(str(p), "gte(4)")

    def test_gteCombinesWithExistingNameCorrectly (self):
        p = NumAccessor(ident, name="id").gte(4)
        self.assertEqual(str(p), "id.gte(4)")

    def test_gtOnInt (self):
        p = NumAccessor(ident).gt(4)
        self.assertTrue(p(5))
        self.assertFalse(p(4))

    def test_gtIsNamedCorrectly (self):
        p = NumAccessor(ident).gt(4)
        self.assertEqual(str(p), "gt(4)")

    def test_gtCombinesWithExistingNameCorrectly (self):
        p = NumAccessor(ident, name="id").gt(4)
        self.assertEqual(str(p), "id.gt(4)")

