import unittest
from nose.plugins.attrib import attr

from ..simplify import *


ident = lambda x: x

lt  = lambda n: Pred(lambda x: x <  n, name="(<" + str(n) + ")")
eq  = lambda n: Pred(lambda x: x == n, name="(==" + str(n) + ")")
gt  = lambda n: Pred(lambda x: x >  n, name="(>" + str(n) + ")")


class Test_simplify (unittest.TestCase):

    def test_simplestForm (self):
        self.assertEquals(simplify(lt(5)), lt(5))

    def test_notNotXEqualsX (self):
        self.assertEquals(simplify(~~lt(5)), lt(5))

    def test_notNotNotXEqualsX (self):
        self.assertEquals(simplify(~~~lt(5)), ~lt(5))

    def test_notNotNotNotXEqualsX (self):
        self.assertEquals(simplify(~~~~lt(5)), lt(5))

    def test_xAndNotX (self):
        self.assertEquals(simplify(lt(5) & ~lt(5)), false)

    def test_notXAndX (self):
        self.assertEquals(simplify(~lt(5) & lt(5)), false)

    def test_xOrNotX (self):
        self.assertEquals(simplify(lt(5) | ~lt(5)), true)

    def test_notXOrX (self):
        self.assertEquals(simplify(~lt(5) | lt(5)), true)

    def test_xAndX (self):
        self.assertEquals(simplify(lt(5) & lt(5)), lt(5))

    def test_xOrX (self):
        self.assertEquals(simplify(lt(5) | lt(5)), lt(5))

    def test_xAndNotNotX (self):
        self.assertEquals(simplify(lt(5) & ~~lt(5)), lt(5))

