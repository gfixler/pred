import maya.cmds as cmds

# STANDARD FUNCTIONS AND COMBINATORS
const = lambda x: lambda _: x

# SIMPLE MAYA QUERY/SET EXPRESSIONS; WE'LL LIFT THESE INTO PREDS BELOW
nodeExists = lambda n: cmds.objExists(n)

parentIs = lambda p: lambda x: cmds.listRelatives(x, parent=True) == [p] # could/will be a Pred
parentTo = lambda p: lambda x: cmds.parent(x, p)

getPos = lambda x: tuple(cmds.xform(x, query=True, translation=True))
posIs = lambda p: lambda x: getPos(x) == p # could/will be a Pred
setPos = lambda (x, y, z): lambda n: cmds.move(x, y, z, n, localSpace=True)

# IMPURE PRED MAKERS OF 1 AND 2 ARGS (WRAPS PREDS TO IGNORE FINAL PRED INPUT)
# (the optional g=const hoops jumped through here, while clever, are upsetting to me)
# (I also really don't like these names)
ipred1 = lambda f, g=const({}): lambda x: Pred(lambda _: f(x), **g(x))
ipred2 = lambda f, g=const(const({})): lambda x: lambda y: Pred(lambda _: f(x)(y), **g(x)(y))

# USE CASES FOR 1 AND 2 ARG IMPURE PREDICATE MAKERS
# (these names are awful, just terrible)
ipredNodeExists = ipred1(nodeExists, lambda x: {"name": "ipred1(nodeExists)(\"" + x + "\")"})
ipredParentIs = ipred2(parentIs, lambda x: lambda y: {"name": "ipred2(parentIs)(\"" + x + "\")(\"" + y + "\")"})
"""
# EXAMPLE USES OF ABOVE I[MPURE]PREDS (TRY .pprint() ON EACH)
ipredNodeExists("pSphere1") # pred that ignores input and just checks if pSphere1 exists
ipredParentIs("pSphere1")("pCube1") # pred that ignores input, and just checks that pSphere1 is parent of pCube1
# (parentIs and posIs should probably have been Preds from the start, but this let me flesh out the zany ipred idea)
"""

# HELPERS; MERGINGS OF PREDS WITH THEIR OBVIOUS FIXES
ensureParentIs = lambda p: Pred(parentIs(p), fix=parentTo(p), name="parentIs(\"" + p + "\")")
ensurePosIs = lambda p: Pred(posIs(p), fix=setPos(p), name="posIs(" + str(p) + ")")

# TEST RUN OF ABOVE TOYS
# create test subjects
cmds.polySphere("pSphere1")
cmds.polyCube("pCube1")
# this entire predicate [below] has pCube1 as its input, and checks/fixes things about it
# use of >> (SEQ = sequential AND) everywhere, as each thing has the thing to its left as a prerequisite
# note that all pos things here are [default] local space, i.e. ultimately re: the cube's position under the sphere
p = ipredNodeExists("pSphere1") >> Pred(nodeExists, name="nodeExists") >> ensureParentIs("pSphere1") >> ensurePosIs((1,2,3))
p.pprint() # shows off all the naming gynmastics above
p("pCube1") # should be false until after validate is run
p.validate("pCube1") # should actually parent cube under sphere, and move it in local space (i.e. runs all fixes)

