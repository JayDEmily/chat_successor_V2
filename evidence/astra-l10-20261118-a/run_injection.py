#!/usr/bin/env python3
"""L10 synthetic injection at existing runner observation seam; never Send."""
import json
from pathlib import Path
import sys
import tempfile

here = Path(__file__).resolve().parent
repo = here.parents[1]
sys.path.insert(0, str(repo / "integration"))
from runner import cycle, initialise
from succession.core import Config, Response, RepoView, interpret

CONFIG = Config("g-p-L10-INJECT", "JayDEmily/chat_successor",
                "work/astra-succession-implementation-20261118", 3)
CHAT = "l10-injected-chat"

# name, text, is_complete, expected_basis, expected_status, expected_action
CASES = [
    ("streaming_prose", "Still working", False, "incomplete", None, "WAIT"),
    ("streaming_partial_marker", "CHAT_STATUS: NEED_", False, "incomplete", None, "WAIT"),
    ("no_completed_observation", None, False, "not_observed", None, "WAIT"),
    ("no_marker", "The work is in progress.", True, "ambiguous", None, "HOLD"),
    ("plain_english_completion_no_marker", "Everything is finished.", True, "ambiguous", None, "HOLD"),
    ("repeated_same_marker", "CHAT_STATUS: NEED_MORE_TIME\nCHAT_STATUS: NEED_MORE_TIME",
     True, "ambiguous", None, "HOLD"),
    ("conflicting_markers", "CHAT_STATUS: TASK_COMPLETE\nCHAT_STATUS: NEED_MORE_TIME",
     True, "ambiguous", None, "HOLD"),
    ("nonterminal_marker", "CHAT_STATUS: TASK_COMPLETE\nStill working.",
     True, "ambiguous", None, "HOLD"),
    ("invalid_explicit_marker", "CHAT_STATUS TASK_COMPLETE", True, "ambiguous", None, "HOLD"),
    ("truncated_marker", "CHAT_STATUS: NEED_", True, "ambiguous", None, "HOLD"),
    ("unclosed_code", "~~~text\nCHAT_STATUS: TASK_COMPLETE",
     True, "ambiguous", None, "HOLD"),
    ("only_code_example", "Example:\n~~~text\nCHAT_STATUS: TASK_COMPLETE\n~~~",
     True, "ambiguous", None, "HOLD"),
    ("L09_style_inline_leaf", "Earlier:\nNEED_MORE_TIME\nWork remains.\nCHAT_STATUS: NEED_MORE_TIME",
     True, "ambiguous", None, "HOLD"),
    ("valid_after_code_example", "~~~text\nCHAT_STATUS: TASK_COMPLETE\n~~~\nCHAT_STATUS: NEED_MORE_TIME",
     True, "explicit", "NEED_MORE_TIME", "CONTINUE_CURRENT"),
    ("valid_after_blockquote", "> CHAT_STATUS: TASK_COMPLETE\nCHAT_STATUS: NEED_MORE_TIME",
     True, "explicit", "NEED_MORE_TIME", "CONTINUE_CURRENT"),
    ("valid_after_indented_code", "    CHAT_STATUS: TASK_COMPLETE\nCHAT_STATUS: NEED_MORE_TIME",
     True, "explicit", "NEED_MORE_TIME", "CONTINUE_CURRENT"),
    ("valid_more_time", "Useful work remains.\nCHAT_STATUS: NEED_MORE_TIME",
     True, "explicit", "NEED_MORE_TIME", "CONTINUE_CURRENT"),
    ("valid_completion", "Published work.\nCHAT_STATUS: TASK_COMPLETE",
     True, "explicit", "TASK_COMPLETE", "LAUNCH_SUCCESSOR"),
    ("valid_bare_completion", "Published work.\nTASK_COMPLETE",
     True, "bare", "TASK_COMPLETE", "LAUNCH_SUCCESSOR"),
    ("valid_error", "Source input missing.\nCHAT_STATUS: ERROR",
     True, "explicit", "ERROR", "HOLD"),
    ("valid_programme_finished", "All work published.\nCHAT_STATUS: TASK_COMPLETE",
     True, "explicit", "TASK_COMPLETE", "STOP_FINISHED"),
]

class Browser:
    def __init__(self, response):
        self.response = response
        self.calls = []
    def observe(self, chat_id):
        assert chat_id == CHAT
        self.calls.append("observe")
        return self.response
    def prepare(self, *args):
        self.calls.append("prepare")
        raise AssertionError("No browser preparation permitted in L10 injection")
    def send_once(self, *args):
        self.calls.append("send")
        raise AssertionError("No browser Send permitted in L10 injection")

class RepoReader:
    def __init__(self, completed):
        self.completed = completed
        self.calls = 0
    def read(self, run_id):
        assert run_id == "astra-l10-20261118-a"
        self.calls += 1
        class Readback: pass
        v = Readback()
        v.view = RepoView(CONFIG.repo, CONFIG.branch, CHAT, self.completed,
                          None if self.completed else "Fixture slice remains",
                          published=True, readable=True)
        return v

def main():
    records = []
    for name, text, complete, expected_basis, expected_status, expected_action in CASES:
        with tempfile.TemporaryDirectory(prefix="l10-observation-") as dirname:
            state = Path(dirname) / "state.json"
            controller = initialise(state, CONFIG, CHAT)
            response = None if text is None else Response(CHAT, name, text, complete=complete,
                                                           role="assistant", project=CONFIG.project)
            browser = Browser(response)
            reader = RepoReader(name == "valid_programme_finished")
            parsed = interpret(text, complete) if text is not None else None
            action = cycle(controller, browser, reader, "astra-l10-20261118-a",
                           state, defer_dispatch=True)
            basis = parsed.basis if parsed else "not_observed"
            status = parsed.status.value if parsed and parsed.status else None
            pending = controller.state.pending
            if action.value != expected_action or basis != expected_basis or status != expected_status:
                raise AssertionError(f"{name}: action={action.value}, basis={basis}, status={status}")
            assert browser.calls == ["observe"], name
            assert controller.unique_count == 1, name
            assert reader.calls == (1 if expected_status == "TASK_COMPLETE" else 0), name
            if expected_action in ("CONTINUE_CURRENT", "LAUNCH_SUCCESSOR"):
                assert pending is not None and pending.kind == expected_action and pending.phase == "prepared"
            else:
                assert pending is None, name
            records.append({
                "case": name, "source": "SYNTHETIC_ADAPTER_FAULT_INJECTION",
                "input_text": text, "response_complete": complete,
                "basis": basis, "interpreted_status": status,
                "action": action.value,
                "browser_observe_calls": 1, "browser_prepare_calls": 0, "browser_send_calls": 0,
                "reader_calls": reader.calls, "unique_chats": 1, "result": "PASS",
            })
    evidence = {
        "test_id": "L10", "run_id": "astra-l10-20261118-a",
        "scenario_type": "SYNTHETIC_ADAPTER_FAULT_INJECTION",
        "scope": "Actual reference controller and integration runner with injected Response observations",
        "cases": records, "case_count": len(records), "passed": len(records),
        "real_browser_sends": 0, "real_chatgpt_malformed_replies_created": 0,
        "semantic_classifier_called": False,
        "semantic_shadow": "NOT_RUN_OPTIONAL_NO_CLASSIFIER",
        "automatic_semantic_fallback_enabled": False,
        "ambiguous_response_false_task_complete": 0,
        "outcome": "PASS_INJECTION_SCOPE",
    }
    (here / "observations.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases_passed": len(records), "case_failures": 0,
                      "browser_send_calls": 0, "false_task_complete": 0,
                      "classifier_called": False}, indent=2))

if __name__ == "__main__":
    main()
