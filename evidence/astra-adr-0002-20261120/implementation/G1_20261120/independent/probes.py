"""Reproduce independent G1 findings using only temporary state and stubbed UIA."""

from pathlib import Path
import json
import sys
from unittest.mock import Mock, patch

candidate = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(candidate / "integration"), str(candidate / "integration/tests")]

from account_routes import require_route
from launch_project import launch_request
from repo_reader import GitHandoffReader, STORY_REPO
from runner import Submitted, cycle, initialise, inspect_state
from succession.core import Action, Config, Controller, Response
from test_a2_l02_routes import ADR2RouteTests, PROJECT, URL
from test_l09_faults import L09AdapterFaultTests
from test_owner_reentry import ReentryTests
from test_story_run import CHATS, StoryTests, git
from windows_backend import WindowsUIA


def bad_backend():
    fixture = ADR2RouteTests()
    fixture.setUp()
    try:
        wrong_sha = "0" * 40
        fixture.routes["accounts"]["shoco"]["backend_commit"] = wrong_sha
        (fixture.base / "account_routes.json").write_text(
            json.dumps(fixture.routes), encoding="utf-8")
        calls = []
        composer = {
            "project": PROJECT, "observed_url": URL, "current_chat_id": None,
            "private_window_handle": 55, "editable_text": "", "attachments_present": False,
        }

        def fake_adapter(_browser, mode, **_kwargs):
            calls.append(mode)
            if mode == "Prepare":
                return composer
            if mode == "Send":
                return {"posted_message_observed": False}
            raise AssertionError(mode)

        with patch.object(WindowsUIA, "_invoke", fake_adapter), \
                patch.object(GitHandoffReader, "published_tip", return_value="a" * 40), \
                patch("launch_project.wsl", return_value="a" * 40 + "\trefs/heads/work/active"), \
                patch("launch_project.provision_reader", return_value="/tmp/offline-fixture"), \
                patch("launch_story.start_controller") as start:
            preflight = launch_request(fixture.file, fixture.base, check_only=True, account_key="shoco")
            try:
                launch_request(fixture.file, fixture.base, account_key="shoco")
            except RuntimeError as exc:
                hold = str(exc)
            else:
                hold = None
            start.assert_not_called()

        invalid_id = json.loads(fixture.file.read_text(encoding="utf-8"))
        invalid_id.update(operation="new", job_id="a" * 32)
        fixture.file.write_text(json.dumps(invalid_id), encoding="utf-8")
        with patch("launch_project.resolve_project") as resolve:
            try:
                launch_request(fixture.file, fixture.base, account_key="shoco")
            except ValueError as exc:
                invalid_id_hold = str(exc)
            else:
                invalid_id_hold = None
            resolve.assert_not_called()

        return {
            "declared_backend_is_all_zero": require_route(
                fixture.base, "shoco")["backend_commit"] == wrong_sha,
            "preflight_event": preflight["event"],
            "mock_adapter_modes": calls,
            "bootstrap_intents": len(list(fixture.base.rglob("bootstrap-intent.json"))),
            "hold_after_unverified_mock_submission": hold,
            "invalid_32_character_job_id_control": invalid_id_hold,
        }
    finally:
        fixture.doCleanups()


def publication():
    fixture = StoryTests()
    fixture.setUp()
    try:
        cfg = Config("g-p-abc123", "example-org/fixture", "main", 3)
        state = fixture.root / "generic-controller.json"
        controller = initialise(state, cfg, CHATS[0])
        reader = GitHandoffReader(fixture.root / "reader", cfg.repo, "main")
        reader._verify_origin = Mock()  # The disposable bare remote is local.
        browser = Mock()
        browser.observe.return_value = Response(
            CHATS[0], "turn-first", "CHAT_STATUS: TASK_COMPLETE", project=cfg.project)
        fixture.publish_handoff(CHATS[1], "Next")
        with fixture.assertLogs(level="WARNING"):
            wrong = cycle(controller, browser, reader, "demo", state)
        generic_wrong_consumed = list(Controller.load(state).state.consumed_responses)
        fixture.publish_handoff(CHATS[0], "Next")
        commit = git(fixture.writer, "rev-parse", "HEAD")
        controller.resume_after_owner()
        controller.save(state)
        with fixture.assertLogs(level="INFO") as correct_logs:
            correct = cycle(controller, browser, reader, "demo", state, defer_dispatch=True)
        browser.send_once.assert_not_called()

        legacy_state = fixture.root / "story-controller.json"
        story = initialise(legacy_state, Config(cfg.project, STORY_REPO, "main", 4), CHATS[0])
        fixture.publish(0, chat_id=CHATS[1])
        with fixture.assertLogs(level="INFO") as stale_logs:
            stale = cycle(story, browser, fixture.reader, "story", legacy_state)
        browser.send_once.assert_not_called()
        return {
            "generic_wrong_worker_action": wrong.value,
            "generic_wrong_worker_consumed": generic_wrong_consumed,
            "generic_repair_action": correct.value,
            "generic_repair_exact_sha_in_verified_and_adopted_logs": all(
                any(term in row and f"sha={commit}" in row and "ref=refs/heads/main" in row
                    for row in correct_logs.output)
                for term in ("publication_receipt_verified", "publication_receipt_adopted")),
            "generic_repair_logged_sha": commit,
            "status_publication_commit_after_verified_adoption": inspect_state(state)["publication_commit"],
            "legacy_story_wrong_worker_action": stale.value,
            "legacy_story_wrong_worker_response_consumed": bool(
                Controller.load(legacy_state).state.consumed_responses),
            "legacy_story_wrong_worker_labelled_identity_match": any(
                "result=IDENTITY_MATCH" in row for row in stale_logs.output),
            "legacy_story_wrong_worker_labelled_adopted": any(
                "publication_receipt_adopted" in row for row in stale_logs.output),
        }
    finally:
        fixture.doCleanups()


def provisional_successor():
    fixture = L09AdapterFaultTests()
    fixture.setUp()
    try:
        action, _ = fixture.stage_sending(Action.LAUNCH_SUCCESSOR)
        fixture.c.uncertain(action.action_id)
        fixture.c.save(fixture.path)
        controller = Controller.load(fixture.path)
        # Same provisional slug fed to the native URL parser by native-probes.ps1.
        fixture.w._invoke = Mock(return_value={
            "project": fixture.cfg.project, "chat_id": "local-chatgpt",
            "submitted_text": action.message, "posted_message_observed": True,
        })
        receipt = fixture.w.reconcile_readonly()
        decision = controller.confirm(action.action_id, receipt.chat_id, receipt.project,
                                      message_observed=receipt.posted_message_observed)
        return {"action": decision.action.value, "count": controller.unique_count,
                "pending_preserved": controller.state.pending is not None,
                "mock_adapter_modes": [call.args[0] for call in fixture.w._invoke.call_args_list]}
    finally:
        fixture.doCleanups()


def missing_owner_context():
    fixture = ReentryTests()
    fixture.setUp()
    try:
        fixture.resume(owner_context=fixture.context)
        controller = Controller.load(fixture.state)
        action = controller.state.pending
        owner_file = fixture.state.with_name(f"owner-{action.owner_request_id}.json")
        owner_file.unlink()  # Delete the synthetic input in this temporary fixture only.
        fixture.browser.send_once.return_value = Submitted(
            controller.config.project, controller.state.current_chat_id, action.message, True)
        outcome = cycle(controller, fixture.browser, fixture.reader, "c" * 24, fixture.state)
        return {
            "input_exists_at_dispatch": owner_file.exists(),
            "mock_send_invocations": fixture.browser.send_once.call_count,
            "outcome": outcome.value,
            "count": Controller.load(fixture.state).unique_count,
        }
    finally:
        fixture.doCleanups()


if __name__ == "__main__":
    print(json.dumps({
        "R01_R02_wrong_backend": bad_backend(),
        "R04_S02_publication": publication(),
        "S06_provisional_successor": provisional_successor(),
        "O05_missing_owner_context": missing_owner_context(),
    }, indent=2))
