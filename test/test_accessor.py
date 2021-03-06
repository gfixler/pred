import unittest
from nose.plugins.attrib import attr

import tempfile

from ..accessor import Accessor, StringAccessor, NumAccessor, PathAccessor


ident = lambda x: x


class Test_Accessor (unittest.TestCase):

    def test_acceptsAndUsesAccessFunction (self):
        self.assertEquals(Accessor(ident)("foo"), "foo")

    def test_canCreatePred (self):
        pred = Accessor(ident).pred(lambda s: len(s) == 7)
        self.assertTrue(pred("testing"))

    def test_canNamePreds (self):
        pred = Accessor(ident).pred(lambda x: lambda _: x, name="id")
        self.assertEquals(str(pred), "id")

    def test_canCreateEqualsPred (self):
        accr = StringAccessor(lambda d: d["key"])
        data = {"key": "value"}
        self.assertTrue(accr.equals("value")(data))
        self.assertFalse(accr.equals("random")(data))

    def test_equalsPredIsNamedCorrectly (self):
        accr = StringAccessor(lambda d: d["key"])
        self.assertEquals(str(accr.equals("\"key\"")), "(== \"key\")")

    def test_canMakeDictKeyAccessor (self):
        data = {"a": 3, "b": 42, "c": 7}
        self.assertEquals(Accessor(lambda d: d["b"])(data), 42)


class Test_StringAccessor (unittest.TestCase):

    def setUp (self):
        self.data = {"name": "Bob"}
        self.name = StringAccessor(lambda d: d["name"])

    def test_identityOnStringWorks (self):
        self.assertEquals(StringAccessor(ident)("bar"), "bar")

    def test_identityOnNonStringRaises (self):
        self.assertRaises(TypeError, lambda: StringAccessor(ident)(42))

    def test_canCreateContainsPred (self):
        self.assertTrue(self.name.contains("o")(self.data))
        self.assertFalse(self.name.contains("e")(self.data))

    def test_containsPredIsNamedCorrectly (self):
        self.assertEquals(str(self.name.contains("o")), "contains(\"o\")")

    def test_canCreateStartswithPred (self):
        self.assertTrue(self.name.startswith("B")(self.data))
        self.assertFalse(self.name.startswith("A")(self.data))

    def test_startswithPredIsNamedCorrectly (self):
        self.assertEquals(str(self.name.startswith("B")), "startswith(\"B\")")

    def test_canCreateEndswithPred (self):
        self.assertTrue(self.name.endswith("b")(self.data))
        self.assertFalse(self.name.endswith("e")(self.data))

    def test_endswithPredIsNamedCorrectly (self):
        self.assertEquals(str(self.name.endswith("b")), "endswith(\"b\")")

    def test_canCreateMatchesPred (self):
        self.assertTrue(self.name.matches(".*\d\d-\d\d.*")({"name": "blue_23-42_hike"}))
        self.assertFalse(self.name.matches(".*\d\d-\d\d.*")({"name": "ab-cd"}))

    def test_matchesPredIsNamedCorrectly (self):
        self.assertEquals(str(self.name.matches(".*\d\d-\d\d.*")), "matches(\".*\d\d-\d\d.*\")")


class Test_NumAccessor (unittest.TestCase):

    def test_identityOnIntsWorks (self):
        self.assertEquals(NumAccessor(ident)(7), 7)

    def test_identityOnFloatsWorks (self):
        self.assertEquals(NumAccessor(ident)(7.0), 7.0)

    def test_identityOnNonNumsRaises (self):
        self.assertRaises(TypeError, lambda: NumAccessor(ident)("foo"))

    def test_ltOnInt (self):
        p = NumAccessor(ident).lt(4)
        self.assertTrue(p(3))
        self.assertFalse(p(4))

    def test_ltIsNamedCorrectly (self):
        p = NumAccessor(ident).lt(4)
        self.assertEquals(str(p), "lt(4)")

    def test_lteOnInt (self):
        p = NumAccessor(ident).lte(4)
        self.assertTrue(p(3))
        self.assertTrue(p(4))
        self.assertFalse(p(5))

    def test_lteIsNamedCorrectly (self):
        p = NumAccessor(ident).lte(4)
        self.assertEquals(str(p), "lte(4)")

    def test_eqOnInt (self):
        p = NumAccessor(ident).eq(4)
        self.assertTrue(p(4))
        self.assertFalse(p(3))

    def test_eqIsNamedCorrectly (self):
        p = NumAccessor(ident).eq(4)
        self.assertEquals(str(p), "eq(4)")

    def test_gteOnInt (self):
        p = NumAccessor(ident).gte(4)
        self.assertFalse(p(3))
        self.assertTrue(p(4))
        self.assertTrue(p(5))

    def test_gteIsNamedCorrectly (self):
        p = NumAccessor(ident).gte(4)
        self.assertEquals(str(p), "gte(4)")

    def test_gtOnInt (self):
        p = NumAccessor(ident).gt(4)
        self.assertTrue(p(5))
        self.assertFalse(p(4))

    def test_gtIsNamedCorrectly (self):
        p = NumAccessor(ident).gt(4)
        self.assertEquals(str(p), "gt(4)")


class Test_PathAccessor (unittest.TestCase):

    def setUp (self):
        self.path = tempfile.gettempdir() + "/testFile.txt"
        self.payload = "testing"
        with open(self.path, "w") as f:
            f.write(self.payload)
        self.data = {"filepath": self.path}
        self.accpath = PathAccessor(lambda d: d["filepath"])
        self.result = self.accpath(self.data)

    def test_canAccessPath (self):
        self.assertEquals(self.result, self.path)

    def test_canCheckPathExistence (self):
        self.assertTrue(self.result.exists())

    def test_canReadFromFileAtAccessedPath (self):
        with open(self.result) as f:
            result = f.read()
        self.assertEquals(result, self.payload)

