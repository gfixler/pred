import unittest
from nose.plugins.attrib import attr

from ..validate import *


ident = lambda x: x
const = lambda x: lambda _: x


class Test_Validator (unittest.TestCase):

    def test_simplePredNoFix_passing (self):
        name = "yay"
        desc = "Any value would pass this."
        vdtr = const(True)
        fixr = None
        v = Validator(name, desc, vdtr, fixr)
        self.assertEquals(v(42), {"name": name, "descrip": desc, "status": "PASSED"})

    def test_simplePredBadFix_unfixed (self):
        name = "uhoh"
        desc = "No value would pass this."
        vdtr = const(False)
        fixr = ident
        v = Validator(name, desc, vdtr, fixr)
        self.assertEquals(v(42), {"name": name, "descrip": desc, "status": "UNFIXED"})

    def test_simplePredNoFix_unfixable (self):
        name = "giveup"
        desc = "Any value fails, and we have no fix."
        vdtr = const(False)
        fixr = None
        v = Validator(name, desc, vdtr, fixr)
        self.assertEquals(v(42), {"name": name, "descrip": desc, "status": "UNFIXABLE"})

    def test_simplePredNoFix_fixed (self):
        """
        Trying to write this test made it obvious that fixing things via
        validator may often be about mutating (global?) state.
        """
        global globalvar
        globalvar = 3
        name = "Actual fix to an incorrect, global var."
        desc = "not so bad"
        def vdtr (_):
            global globalvar
            return globalvar == 42
        def fixr (_):
            global globalvar
            globalvar = 42
        v = Validator(name, desc, vdtr, fixr)
        self.assertEquals(v(3), {"name": name, "descrip": desc, "status": "FIXED"})

