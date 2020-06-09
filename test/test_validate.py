import unittest
from nose.plugins.attrib import attr

from ..validate import *


ident = lambda x: x
const = lambda x: lambda _: x


class Test_Validator (unittest.TestCase):

    def test_simplePredNoFix_passing (self):
        vdtr = const(True)
        fixr = None
        v = Validator(vdtr, fixr)
        self.assertEquals(v(42), {"status": "PASSED"})

    def test_simplePredBadFix_unfixed (self):
        vdtr = const(False)
        fixr = ident
        v = Validator(vdtr, fixr)
        self.assertEquals(v(42), {"status": "UNFIXED"})

    def test_simplePredNoFix_unfixable (self):
        vdtr = const(False)
        fixr = None
        v = Validator(vdtr, fixr)
        self.assertEquals(v(42), {"status": "UNFIXABLE"})

    def test_simplePredNoFix_fixed (self):
        """
        Trying to write this test made it obvious that fixing things via
        validator may often be about mutating (global?) state.
        """
        global globalvar
        globalvar = 3
        def vdtr (_):
            global globalvar
            return globalvar == 42
        def fixr (_):
            global globalvar
            globalvar = 42
        v = Validator(vdtr, fixr)
        self.assertEquals(v(3), {"status": "FIXED"})

    def test_handlesFixThatRaises (self):
        """
        If the fix raises, it's caught, and the error is returned under the
        "error" key. The Exception instance returned will have (among other
        things), a useful "message" property.
        """
        def fixThatRaises (_):
            raise RuntimeError, "Fix blew up the world."
        vdtr = const(False)
        fixr = fixThatRaises
        v = Validator(vdtr, fixr)
        result = v(42)
        self.assertEquals("FIXRAISED", result["status"])

