import unittest
from nose.plugins.attrib import attr

from ..accessor import Accessor, StringAccessor


ident = lambda x: x


class Test_Accessor (unittest.TestCase):

    def test_acceptsAndUsesAccessFunction (self):
        self.assertEquals(Accessor(ident)("foo"), "foo")

    def test_canMakeDictKeyAccessor (self):
        data = {"a": 3, "b": 42, "c": 7}
        self.assertEquals(Accessor(lambda d: d["b"])(data), 42)

