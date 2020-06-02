import unittest
from nose.plugins.attrib import attr

from ..accessor import Accessor, StringAccessor, IntAccessor, FloatAccessor


ident = lambda x: x


class Test_Accessor (unittest.TestCase):

    def test_acceptsAndUsesAccessFunction (self):
        self.assertEquals(Accessor(ident)("foo"), "foo")

    def test_canCreatePred (self):
        pred = Accessor(ident).pred(lambda s: len(s) == 7)
        self.assertTrue(pred("testing"))

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

    def test_canCreateIsPred (self):
        self.assertTrue(self.name.equals("Bob")(self.data))
        self.assertFalse(self.name.equals("Alice")(self.data))

    def test_canCreateContainsPred (self):
        self.assertTrue(self.name.contains("o")(self.data))
        self.assertFalse(self.name.contains("e")(self.data))

    def test_canCreateStartswithPred (self):
        self.assertTrue(self.name.startswith("B")(self.data))
        self.assertFalse(self.name.startswith("A")(self.data))

    def test_canCreateEndswithPred (self):
        self.assertTrue(self.name.endswith("b")(self.data))
        self.assertFalse(self.name.endswith("e")(self.data))

    def test_canCreateMatchesPred (self):
        self.assertTrue(self.name.matches(".*\d\d-\d\d.*")("blue_23-42_hike"))
        self.assertFalse(self.name.matches(".*\d\d-\d\d.*")("ab-cd"))


class Test_IntAccessor (unittest.TestCase):

    def test_identityOnIntsWorks (self):
        self.assertEquals(IntAccessor(ident)(7), 7)

    def test_identityOnNonIntsRaises (self):
        self.assertRaises(TypeError, lambda: IntAccessor(ident)("foo"))


class Test_FloatAccessor (unittest.TestCase):

    def test_identityOnFloatsWorks (self):
        self.assertEquals(FloatAccessor(ident)(7.0), 7.0)

    def test_identityOnNonFloatsRaises (self):
        self.assertRaises(TypeError, lambda: FloatAccessor(ident)("foo"))

