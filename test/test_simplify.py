import unittest
from nose.plugins.attrib import attr

from ..simplify import *


ident = lambda x: x

lt  = lambda n: Pred(lambda x: x <  n, name="lt(" + str(n) + ")")
eq  = lambda n: Pred(lambda x: x == n, name="eq(" + str(n) + ")")
gt  = lambda n: Pred(lambda x: x >  n, name="gt(" + str(n) + ")")


class Test_defaultPreds (unittest.TestCase):

    def test_trueIfGivenTrue (self):
        self.assertEqual(true(True), True)

    def test_trueIfGivenFalse (self):
        self.assertEqual(true(False), True)

    def test_trueIsNamedCorrectly (self):
        self.assertEqual(str(true), "true")

    def test_falseIfGivenTrue (self):
        self.assertEqual(false(True), False)

    def test_falseIfGivenFalse (self):
        self.assertEqual(false(False), False)

    def test_falseIsNamedCorrectly (self):
        self.assertEqual(str(false), "false")


class Test_simplify (unittest.TestCase):

    def test_simplestForm (self):
        self.assertEqual(simplify(lt(5)), lt(5))

    def test_notNotXEqualsX (self):
        self.assertEqual(simplify(~~lt(5)), lt(5))

    def test_notNotNotXEqualsX (self):
        self.assertEqual(simplify(~~~lt(5)), ~lt(5))

    def test_notNotNotNotXEqualsX (self):
        self.assertEqual(simplify(~~~~lt(5)), lt(5))

    def test_xAndNotX (self):
        self.assertEqual(simplify(lt(5) & ~lt(5)), false)

    def test_notXAndX (self):
        self.assertEqual(simplify(~lt(5) & lt(5)), false)

    def test_xOrNotX (self):
        self.assertEqual(simplify(lt(5) | ~lt(5)), true)

    def test_notXOrX (self):
        self.assertEqual(simplify(~lt(5) | lt(5)), true)

    def test_xAndX (self):
        self.assertEqual(simplify(lt(5) & lt(5)), lt(5))

    def test_xOrX (self):
        self.assertEqual(simplify(lt(5) | lt(5)), lt(5))

    def test_xAndNotNotX (self):
        self.assertEqual(simplify(lt(5) & ~~lt(5)), lt(5))

