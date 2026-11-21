import sys,unittest
from pathlib import Path
root=Path("/tmp/ltm-independent-8d27-WTfufe/repo")
sys.path[:0]=[str(root/"vnext"),str(root/"vnext/tests")]
exclude={"test_hosted_mcp_w","test_verified_dialogue_t"}
mods=sorted(p.stem for p in (root/"vnext/tests").glob("test_*.py") if p.stem not in exclude)
from test_hosted_mcp_w import TestStageWSemanticGate
special="test_freeze_registration_preserved_and_old_u_private_audit_untouched"
stage=[f"test_hosted_mcp_w.TestStageWSemanticGate.{n}" for n in unittest.defaultTestLoader.getTestCaseNames(TestStageWSemanticGate) if n!=special]
print("BASE_MODULES",len(mods),"STAGE_W_SYNTHETIC",len(stage),flush=True)
tests=unittest.defaultTestLoader.loadTestsFromNames(mods+stage)
result=unittest.TextTestRunner(verbosity=1).run(tests)
print(f"SUMMARY tests={result.testsRun} failures={len(result.failures)} errors={len(result.errors)} skipped={len(result.skipped)}",flush=True)
if result.testsRun!=285 or not result.wasSuccessful() or result.skipped: sys.exit(1)
