#!/usr/bin/env python3
"""L12 controlled delay, session-loss and pause injections; no real browser Send."""
import json
from pathlib import Path
import sys
import tempfile
import time

here = Path(__file__).resolve().parent
repo = here.parents[1]
sys.path.insert(0, str(repo / "integration"))
from runner import Destination, cycle, initialise, inspect_state
from succession.composer import ComposerObservation
from succession.core import Action, Config, Controller, Response

CONFIG = Config("g-p-L12-INJECTION", "JayDEmily/chat_successor",
                "work/astra-succession-implementation-20261118", 3)
CHAT = "l12-injected-chat"
READY = Response(CHAT, "l12-first", "CHAT_STATUS: NEED_MORE_TIME",
                 complete=True, role="assistant", project=CONFIG.project)

class Browser:
    def __init__(self, outcomes=None, fail_prepare=False):
        self.outcomes = list(outcomes if outcomes is not None else [READY])
        self.fail_prepare = fail_prepare
        self.calls = []
    def observe(self, chat_id):
        assert chat_id == CHAT
        self.calls.append("observe")
        if self.outcomes:
            outcome = self.outcomes.pop(0)
        else:
            outcome = None
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
    def prepare(self, kind, chat_id):
        self.calls.append("prepare")
        if self.fail_prepare:
            raise RuntimeError("L12 injected UIA browser session unavailable")
        return Destination(CONFIG.project, CHAT, ComposerObservation(editable_text=""),
                           private_window_handle=1234)
    def send_once(self, *args):
        self.calls.append("send")
        raise AssertionError("L12 must not Send")

class Reader:
    def read(self, run_id):
        raise AssertionError("L12 NEED_MORE_TIME must not read task-completion repo state")

def fresh(path):
    return initialise(path, CONFIG, CHAT)

def result(name, browser, state, **details):
    report = inspect_state(state)
    assert report["unique_chat_count"] == 1
    assert report["current_chat_id"] == CHAT
    assert "send" not in browser.calls
    return {
        "case": name,
        "source": "TEST_ONLY_ADAPTER_AND_STATE_INJECTION",
        "observed_state": report,
        "browser_calls": browser.calls,
        "browser_send_calls": 0,
        "automatic_login_calls": 0,
        "real_chat_created": False,
        "result": "PASS",
        **details
    }

def delayed_observation():
    with tempfile.TemporaryDirectory(prefix="l12-delay-") as td:
        path = Path(td) / "state.json"
        controller = fresh(path)
        browser = Browser([None, None, READY])
        start = time.monotonic()
        first = cycle(controller, browser, Reader(), "l12-injected", path)
        time.sleep(0.06)
        second = cycle(controller, browser, Reader(), "l12-injected", path)
        time.sleep(0.06)
        before_response = inspect_state(path)
        assert first == second == Action.WAIT
        assert before_response["last_status"] is None and before_response["pending_action"] is None
        third = cycle(controller, browser, Reader(), "l12-injected", path,
                      defer_dispatch=True)
        elapsed = int(round((time.monotonic() - start) * 1000))
        assert third == Action.CONTINUE_CURRENT
        assert controller.state.pending.phase == "prepared"
        assert browser.calls == ["observe", "observe", "observe"]
        return result("delayed_incomplete_observation", browser, path,
                      initial_actions=["WAIT", "WAIT"],
                      completed_action=third.value, measured_elapsed_wait_ms=elapsed,
                      production_owner_silence_deadline="NOT_CONFIGURED_BY_THIS_TEST",
                      no_premature_completion=True)

def session_loss():
    with tempfile.TemporaryDirectory(prefix="l12-session-") as td:
        path = Path(td) / "state.json"
        c = fresh(path)
        b = Browser([RuntimeError("Injected missing UIA session"), READY])
        first = cycle(c, b, Reader(), "l12-injected", path)
        assert first == Action.HOLD
        assert "Desktop response observation unavailable" in c.state.halted
        assert c.state.pending is None
        restarted = Controller.load(path)
        assert cycle(restarted, b, Reader(), "l12-injected", path) == Action.HOLD
        assert b.calls == ["observe"]
        restarted.resume_after_owner()
        restarted.save(path)
        again = cycle(restarted, b, Reader(), "l12-injected", path,
                      defer_dispatch=True)
        assert again == Action.CONTINUE_CURRENT
        assert restarted.state.pending.phase == "prepared"
        return result("tool_session_loss_then_repair", b, path,
                      first_action=first.value, held_across_restart=True,
                      repair_action=again.value, no_automatic_login=True)

def owner_pause_idle():
    with tempfile.TemporaryDirectory(prefix="l12-pause-idle-") as td:
        path = Path(td) / "state.json"
        c = fresh(path)
        b = Browser([READY])
        c.pause("Owner pause while idle")
        c.save(path)
        restarted = Controller.load(path)
        assert cycle(restarted, b, Reader(), "l12-injected", path) == Action.HOLD
        assert b.calls == []
        held_state = inspect_state(path)
        assert held_state["last_status"] is None
        assert held_state["pending_action"] is None
        assert held_state["halted"] == "Owner pause while idle"
        restarted.resume_after_owner()
        restarted.save(path)
        permitted = cycle(restarted, b, Reader(), "l12-injected", path,
                          defer_dispatch=True)
        assert permitted == Action.CONTINUE_CURRENT
        return result("owner_pause_while_idle", b, path,
                      held_state=held_state,
                      after_resume_action=permitted.value)

def owner_pause_prepared():
    with tempfile.TemporaryDirectory(prefix="l12-pause-prepared-") as td:
        path = Path(td) / "state.json"
        c = fresh(path)
        b = Browser([READY])
        assert cycle(c, b, Reader(), "l12-injected", path,
                     defer_dispatch=True) == Action.CONTINUE_CURRENT
        assert c.state.pending.phase == "prepared"
        c.pause("Owner pause while prepared")
        c.save(path)
        restarted = Controller.load(path)
        assert cycle(restarted, b, Reader(), "l12-injected", path) == Action.HOLD
        held_state = inspect_state(path)
        assert held_state["pending_action"]["phase"] == "prepared"
        assert held_state["pending_action"]["kind"] == "CONTINUE_CURRENT"
        assert held_state["last_status"] == "NEED_MORE_TIME"
        assert held_state["halted"] == "Owner pause while prepared"
        restarted.resume_after_owner()
        restarted.save(path)
        permitted = cycle(restarted, b, Reader(), "l12-injected", path,
                          defer_dispatch=True)
        assert permitted == Action.CONTINUE_CURRENT
        assert restarted.state.pending.phase == "prepared"
        return result("owner_pause_while_prepared", b, path,
                      held_state=held_state,
                      after_resume_action=permitted.value)

def uncertain_send_readonly_adoption():
    with tempfile.TemporaryDirectory(prefix="l12-inflight-") as td:
        path = Path(td) / "state.json"
        c = fresh(path)
        b = Browser([READY])
        assert cycle(c, b, Reader(), "l12-injected", path,
                     defer_dispatch=True) == Action.CONTINUE_CURRENT
        action_id = c.state.pending.action_id
        c.begin_send(action_id)
        c.save(path)
        c.uncertain(action_id, "L12 injected lost acknowledgement after click")
        c.save(path)
        restarted = Controller.load(path)
        assert restarted.state.pending.phase == "uncertain"
        assert cycle(restarted, b, Reader(), "l12-injected", path) == Action.HOLD
        held = inspect_state(path)
        assert held["pending_action"]["phase"] == "uncertain"
        assert b.calls == ["observe"]
        # The test adapter supplies a *positive* read-only receipt. No new Send.
        decision = restarted.confirm(action_id, CHAT, CONFIG.project,
                                     message_observed=True)
        assert decision.action == Action.WAIT
        restarted.save(path)
        assert restarted.state.pending is None and restarted.unique_count == 1
        return result("uncertain_send_reconciled_no_retry", b, path,
                      previous_hold=held,
                      receipt_source="SYNTHETIC_POSITIVE_READ_ONLY",
                      after_receipt_action=decision.action.value)

def preparation_tool_failure():
    with tempfile.TemporaryDirectory(prefix="l12-prepare-loss-") as td:
        path = Path(td) / "state.json"
        c = fresh(path)
        b = Browser([READY], fail_prepare=True)
        first = cycle(c, b, Reader(), "l12-injected", path)
        assert first == Action.HOLD
        assert c.state.pending.phase == "prepared"
        assert "Desktop prepare did not establish safe target" in c.state.halted
        restarted = Controller.load(path)
        assert cycle(restarted, b, Reader(), "l12-injected", path) == Action.HOLD
        assert b.calls == ["observe", "prepare"]
        b.fail_prepare = False
        restarted.resume_after_owner()
        restarted.save(path)
        prepared = cycle(restarted, b, Reader(), "l12-injected", path,
                         defer_dispatch=True)
        assert prepared == Action.CONTINUE_CURRENT
        assert "send" not in b.calls
        return result("prepare_session_failure_then_repair", b, path,
                      first_action=first.value, retained_pending="prepared",
                      after_repair=prepared.value)

if __name__ == "__main__":
    tests = [delayed_observation, session_loss, owner_pause_idle,
             owner_pause_prepared, uncertain_send_readonly_adoption,
             preparation_tool_failure]
    outcomes = [fn() for fn in tests]
    output = {
        "test_id": "L12", "run_id": "astra-l12-20261118-a",
        "scenario_type": "SYNTHETIC_DELAY_TOOL_LOSS_AND_PAUSE_INJECTION",
        "cases": outcomes, "cases_passed": len(outcomes), "cases_failed": 0,
        "real_browser_sends": 0, "real_browser_login_attempts": 0,
        "real_successor_launches": 0,
        "owner_silence_deadline": "NOT_ESTABLISHED_FOR_PRODUCTION",
        "outcome": "PASS_TEST_INJECTION_SCOPE"
    }
    (here / "observations.json").write_text(json.dumps(output, indent=2) + "\n",
                                            encoding="utf-8")
    print(json.dumps({"cases_passed": len(outcomes), "browser_sends": 0,
                      "real_login_attempts": 0, "outcome": output["outcome"]}, indent=2))
