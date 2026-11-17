import json
from pathlib import Path
import unittest
from succession.core import interpret, SemanticVerdict, Status
from succession.composer import ComposerObservation, classify_composer
from succession.replay import replay_case

ROOT = Path(__file__).resolve().parents[1]

class ParserFixtures(unittest.TestCase):
    pass

def parser_test(case):
    def test(self):
        semantic = None
        if "semantic" in case:
            raw = dict(case["semantic"])
            raw["status"] = Status(raw["status"])
            semantic = SemanticVerdict(**raw)
        result = interpret(case["text"], case["complete"], semantic)
        self.assertEqual(result.status.value if result.status else None, case["expected_status"])
        self.assertEqual(result.basis, case["expected_basis"])
    return test

for case in json.loads((ROOT / "fixtures/parser_cases.json").read_text()):
    setattr(ParserFixtures, "test_" + case["id"], parser_test(case))


class ComposerFixtures(unittest.TestCase):
    pass

def composer_test(case):
    def test(self):
        result = classify_composer(ComposerObservation(**case["observation"]))
        self.assertEqual(result.value, case["expected"])
    return test

for case in json.loads((ROOT / "fixtures/composer_cases.json").read_text()):
    setattr(ComposerFixtures, "test_" + case["id"], composer_test(case))


class SequenceFixtures(unittest.TestCase):
    pass

def sequence_test(case):
    def test(self):
        result = replay_case(case)
        self.assertEqual(result["outcome"], "PASS")
    return test

for case in json.loads((ROOT / "fixtures/sequence_cases.json").read_text()):
    setattr(SequenceFixtures, "test_" + case["id"], sequence_test(case))
