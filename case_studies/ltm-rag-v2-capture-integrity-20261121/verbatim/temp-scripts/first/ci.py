from pathlib import Path
import os, sys, unittest
root=Path("/tmp/ltmragv2_review_fresh_7d8b")
sys.path[:0]=[str(root/"vnext"),str(root/"vnext/tests")]
os.chdir(root)
skip={"test_hosted_mcp_w.py","test_verified_dialogue_t.py"}
suite=unittest.TestSuite()
loader=unittest.defaultTestLoader
modules=[p.stem for p in sorted((root/"vnext/tests").glob("test_*.py")) if p.name not in skip]
for module in modules:
    suite.addTests(loader.loadTestsFromName(module))
from test_hosted_mcp_w import TestStageWSemanticGate
private="test_freeze_registration_preserved_and_old_u_private_audit_untouched"
names=loader.getTestCaseNames(TestStageWSemanticGate)
assert private in names and len(names)-1==13,(len(names),private in names)
for name in names:
    if name!=private:
        suite.addTests(loader.loadTestsFromName("test_hosted_mcp_w.TestStageWSemanticGate."+name))
print("Review CI-equivalent discovery: base_modules="+str(len(modules))+" stage_w="+str(len(names)-1),flush=True)
result=unittest.TextTestRunner(verbosity=1).run(suite)
print("Review CI-equivalent: ran="+str(result.testsRun)+" failures="+str(len(result.failures))+" errors="+str(len(result.errors))+" skipped="+str(len(result.skipped)),flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
