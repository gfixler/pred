import unittest
from nose.plugins.attrib import attr

from ..simplify import *


ident = lambda x: x

lt  = lambda n: Pred(lambda x: x <  n, name="(<" + str(n) + ")")
eq  = lambda n: Pred(lambda x: x == n, name="(==" + str(n) + ")")
gt  = lambda n: Pred(lambda x: x >  n, name="(>" + str(n) + ")")


class Test_Pred (unittest.TestCase):

    def test_simplify_simplestForm (self):
        self.assertEquals(simplify(lt(5)), lt(5))

    def test_simplify_notNotXEqualsX (self):
        self.assertEquals(simplify(~~lt(5)), lt(5))

    def test_simplify_notNotNotXEqualsX (self):
        self.assertEquals(simplify(~~~lt(5)), ~lt(5))

    def test_simplify_notNotNotNotXEqualsX (self):
        self.assertEquals(simplify(~~~~lt(5)), lt(5))

    def test_simplify_xAndNotX (self):
        self.assertEquals(simplify(lt(5) & ~lt(5)), false)

    def test_simplify_notXAndX (self):
        self.assertEquals(simplify(~lt(5) & lt(5)), false)

    def test_simplify_xOrNotX (self):
        self.assertEquals(simplify(lt(5) | ~lt(5)), true)

    def test_simplify_notXOrX (self):
        self.assertEquals(simplify(~lt(5) | lt(5)), true)

    def test_simplify_xAndX (self):
        self.assertEquals(simplify(lt(5) & lt(5)), lt(5))

    def test_simplify_xOrX (self):
        self.assertEquals(simplify(lt(5) | lt(5)), lt(5))

    def test_simplify_xAndNotNotX (self):
        self.assertEquals(simplify(lt(5) & ~~lt(5)), lt(5))

