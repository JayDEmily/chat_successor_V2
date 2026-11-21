"""Independent reproduction of GitHub CI synthetic subset, omitting only two historical evidence modules."""
import pathlib
import sys
import unittest
tests=pathlib.Path("vnext/tests")
modules=sorted(p.stem for p in tests.glob("test_*.py") if p.name not in ("test_hosted_mcp_w.py","test_verified_dialogue_t.py"))
from test_hosted_mcp_w import TestStageWSemanticGate
private="test_freeze_registration_preserved_and_old_u_private_audit_untouched"
w_tests=unittest.defaultTestLoader.getTestCaseNames(TestStageWSemanticGate)
assert private in w_tests, "Missing historical Stage W exclusion"
w=[f"test_hosted_mcp_w.TestStageWSemanticGate.{n}" for n in w_tests if n != private]
assert len(w)==13, (len(w),w)
suite=unittest.defaultTestLoader.loadTestsFromNames(modules+w)
print(f"Modules={len(modules)} StageW={len(w)} cases={suite.countTestCases()}", flush=True)
r=unittest.TextTestRunner(verbosity=1).run(suite)
print(f"CI_EQUIVALENT_RESULT run={r.testsRun} failures={len(r.failures)} errors={len(r.errors)} skipped={len(r.skipped)} success={r.wasSuccessful()}", flush=True)
sys.exit(0 if r.wasSuccessful() else 1)
