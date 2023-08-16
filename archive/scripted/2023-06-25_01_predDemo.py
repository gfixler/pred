from pprint import pprint
import sys
sys.path.insert(0, "C:/msys64/home/gfixler/code/pred")

import pred
from pred.pred import Pred
from pred.accessor import Accessor as Acc
from pred.accessor import NumAccessor as NumAcc
from pred.accessor import StringAccessor as StrAcc
from pred.simplify import simplify


# a simple predicate
nodeExists = Pred(cmds.objExists)
# example use
nodeExists("testCube")
# example cube
cmds.polyCube(name="testCube")

# a predicate-creating function
attrExists = lambda a: Pred(lambda n: cmds.attributeQuery(a, node=n, exists=True))
# example use
attrExists("translateX")("testCube")

# a number accessor-creating function
numAttr = lambda a: NumAcc(lambda n: cmds.getAttr(n + "." + a))
# example use
numAttr("translateX")("testCube")
numAttr("translateX")("persp")

# as above, but with names
nodeExists = Pred(
    cmds.objExists,
    name = "nodeExists"
)
attrExists = lambda a: Pred(
    lambda n: cmds.attributeQuery(a, node=n, exists=True),
    name = "attrExists(\"" + a + "\")"
)
numAttr = lambda a: NumAcc(
    lambda n: cmds.getAttr(n + "." + a),
    name = "numAttr(\"" + a + "\")"
)

# pretty printing
nodeExists.pprint()
attrExists("scaleY").pprint()
# accessors do not have pretty-printing (yet?)

# named num accessors
tx = numAttr("tx")
ty = numAttr("ty")
tz = numAttr("tz")

# example use
tx("persp")

# num accessors have pred-making methods
tx.gt(0)

# example use
tx.lt(0)("persp")
tx.gt(0)("persp")

# accessor preds are also nameable
txIsNeg = tx.lt(0)
txIsPos = tx.gte(0)

# example use
txIsNeg("persp")
txIsPos("persp")

# pretty-printing accessor-created predicates
txIsNeg.pprint()
txIsPos.pprint()

# predicates compose (via bool alg)
p = tx.gte(2) & tx.lte(9)
# example use
p("testCube")
# move test cube
cmds.setAttr("testCube.tx", 7)

# composed predicates also pretty-print
p.pprint()

# predicates as validators
pprint(p.validate("testCube"))

# const True/False helper functions
const = lambda x: lambda _: x
# example use
const(42)("whatever") # 42
const(42)([1, 2, 3]) # 42
const(42)(37) # 42
const("foo")(False) # "foo"

# True/False constants
true = Pred(const(True), name="true")
false = Pred(const(False), name="false")
# example use
true("foo")
false("bar")

# impossible predicate
p = false & true
p.pprint()
# example use (always (constantly) False)
p(42)
pprint(p.validate(42))

# AND vs SEQ
p = false >> true
p.pprint()
# SEQ will short circuit
pprint(p.validate(42))

# a quick note on associativity
p = attrExists("tx") &  attrExists("ty") & attrExists("tz")
p = attrExists("tx") & (attrExists("ty") & attrExists("tz"))
p.pprint()

# predicates can answer very complex questions
p = nodeExists >> ( (attrExists("tx") >> (tx.lt(2) | tx.gt(9)))
                  & (attrExists("ty") >>  ty.eq(3))
                  & (attrExists("tz") >> ~tz.eq(7))
                  )
p.pprint()
# example use
p("testCube")
pprint(p.validate("testCube"))
# fix it
cmds.setAttr("testCube.t", 1, 3, 9)

# validation pretty-printing
def pprintValidation (v, indent=0):
    op = v["op"]
    ref = v["ref"]
    result = "PASS" if v["result"] else "FAIL" if "result" in v else "untested"
    if op == "PRED":
        print("  " * indent + str(ref), "(" + result + ")")
    else:
        print("  " * indent + op, "(" + result + ")")
    if op in ["AND", "OR", "SEQ"]:
        pprintValidation(v["left"], indent=indent+1)
        pprintValidation(v["right"], indent=indent+1)
    else:
        if "pred" in v:
            pprintValidation(v["pred"], indent=indent+1)

# raw data
pprint(p.validate("testCube"))
# validate looks like pretty Pred
p.pprint()
# pretty validation
pprintValidation(p.validate("testCube"))


# validation report in a UI
def pprintValidation (v, indent=0):
    op = v["op"]
    ref = v["ref"]
    col = ((0.4, 1, 0.4) if v["result"] else (1, 0.4, 0.4)) if "result" in v else (0.2, 0.2, 0.2)
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
    cmds.text(label="        " * indent)
    if op == "PRED":
        line = str(ref)
        cmds.text(label=line, backgroundColor=col)
    else:
        line = op
        cmds.text(label=line, backgroundColor=col)
        print()
    cmds.setParent("..")
    if op in ["AND", "OR", "SEQ"]:
        pprintValidation(v["left"], indent=indent+1)
        pprintValidation(v["right"], indent=indent+1)
    else:
        if "pred" in v:
            pprintValidation(v["pred"], indent=indent+1)

cmds.window()
cmds.showWindow()
cmds.columnLayout()
pprintValidation(p.validate("testCube"))

propIs = lambda v, p: nodeExists >> (attrExists(p) >> numAttr(p).eq(v))
p = propIs(180, "rz")
p.pprint()


gfixlerLOS = """
cdrive|C:
    home|msys64/home/gfixler
COD_GAME_DRIVE|Q:
    t9|t9
        t9tools|tools
            mobutools|motionbuilder
                atb|ATB
                xanimExp|Lib/cod_tools_core/xanimExporter
                    xanimExpPy|xanimExporter.py
"""

import mpath
mpaths = mpath.fromLayoutStr("gfixler", gfixlerLOS)
mpaths.home.extend("docs/pokedex.json")
pokedexPath = mpaths.home.extend("docs/pokedex.json")
type(pokedexPath)
pokedexPath.exists()
pokedex = pokedexPath.loadJSON()
pmons = pokedex["pokemon"]



pmons[0]

getKey = lambda k: lambda d: d[k]
getKey("name")(pmons[0])

name = StrAcc(getKey("name"), name="name")
idn = NumAcc(getKey("id"), name="idn")

name(pmons[0])
idn(pmons[0])

p = name.startswith("Z")
q = idn.gte(10) & idn.lte(30)
p = (q & name.startswith("P")) | name.equals("Cubone")
p = ((idn.gt(5) & idn.lt(9)) & ~idn.eq(7)) | name.startswith("B")

gt = lambda n: Pred(lambda x: x > n, name="gt(" + str(n) + ")")

p.pprint()

p(pmons[0])
list(filter(p, pmons))
list(map(name, filter(p, pmons)))

both = lambda f: lambda g: lambda x: (f(x), g(x))

list(map(both(idn)(name), filter(p, pmons)))

list(map(both(idn)(name), filter(~p, pmons)))

parseValidation(p.validate(pmons[0]))

q = ~~~idn.gt(3)
q.pprint()
simplify(q).pprint()

list(map(name, filter(name.matches("^[^AEIOU][aeiou][^aeiou][aeiou][^aeiou][aeiou][^aeiou][aeiou][^aeiou]$"), pmons)))
list(map(name, filter(name.matches("^[AEIOU][^aeiou][aeiou][^aeiou][aeiou][^aeiou][aeiou][^aeiou]$"), pmons)))

idn.pred(lambda x: x == 1)(pmons[0])

comp2 = lambda f: lambda g: lambda x: f(g(x))
nth = lambda n: lambda xs: xs[n]
eq = lambda y: lambda x: x == y
nth(2)("awesome")

p = name.pred(comp2(eq("e"))(nth(2)), name="eq(\"e\") . nth(2)") | name.equals("Cubone")
p.pprint()


meshHasMat = lambda mat: lambda mesh: (matExists(mat) & meshExists(mesh)) >> matOnMesh(mat, mesh)

scn = mayaSceneAccessor()
meshHasMat = lambda mat: lambda mesh: (scn.has(mat) & scn.has(mesh)) >> scn.ob(mesh).hasMat(mat)


p.ast()



exists = Pred(cmds.objExists, name="exists")
hasProp = lambda p: Pred(lambda n: cmds.attributeQuery(p, node=n, exists=True), name="hasProp(" + repr(p) + ")")
propValIs = lambda v: lambda p: Pred(lambda n: cmds.getAttr(n + "." + p) == v, name="propValIs(" + str(v) + ")(" + str(p) + ")")

r = exists >> hasProp("scaleX") >> propValIs(2)("scaleX")
r.pprint()

obPropValIs = lambda v: lambda p: exists >> hasProp(p) >> propValIs(v)(p)

r = obPropValIs(1)("scaleX")
r.pprint()
r._op
r("persp")
parseValidation(r.validate("persp"))



class MayaSceneAccessor (Acc):

    time = NumAcc(lambda _: cmds.currentTime(query=True))

    def __init__ (self, *args):
        pass

    def __call__ (self, *args):
        try:
            import maya.cmds
            return True
        except:
            return False



scn = MayaSceneAccessor()
q = scn.time.gte(3) & name.startswith("B")
q(pmons[0])
pprint(q.validate(pmons[0]))


