import json
from pathlib import Path
import random
import tempfile
import unittest

from succession.core import (
    Action, Config, Controller, RepoView, Response, SemanticVerdict, Status, conversation_id,
)
from succession.mock import FakeBrowser

CONFIG = dict(project="project-nominated", repo="JayDEmily/chat_successor",
              branch="test/succession", max_unique_chats=30)


def make(maximum=30):
    c = Controller(Config(**{**CONFIG, "max_unique_chats": maximum}), "c1")
    return c, FakeBrowser(c.config.project)


def response(c, status="TASK_COMPLETE", rid="r1", **kwargs):
    data = dict(chat_id=c.state.current_chat_id, response_id=rid,
                text="Useful progress.\nCHAT_STATUS: " + status, project=c.config.project)
    data.update(kwargs)
    return Response(**data)


def repo(c, **kwargs):
    data = dict(repo=c.config.repo, branch=c.config.branch,
                last_chat_id=c.state.current_chat_id,
                programme_complete=False, next_task="Continue next slice")
    data.update(kwargs)
    return RepoView(**data)


class ControllerTests(unittest.TestCase):
    def test_C01_exactly_three_worker_statuses(self):
        self.assertEqual({s.value for s in Status}, {"NEED_MORE_TIME", "TASK_COMPLETE", "ERROR"})

    def test_C02_config_rejects_invalid_cap(self):
        for invalid in (0, -1, 1.5, True, "30"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                Config(**{**CONFIG, "max_unique_chats": invalid})

    def test_C03_config_requires_single_line_nomination(self):
        for field in ("project", "repo", "branch"):
            for invalid in ("", "  ", "x\ny"):
                with self.subTest(field=field, invalid=invalid), self.assertRaises(ValueError):
                    Config(**{**CONFIG, field: invalid})

    def test_C04_ignore_tools_and_user_messages(self):
        for role in ("tool", "user", "system"):
            c, b = make()
            self.assertEqual(c.consume(response(c, role=role), repo(c)).action, Action.IGNORE)
            self.assertIsNone(c.state.pending)

    def test_C05_ignore_other_chat(self):
        c, b = make()
        self.assertEqual(c.consume(response(c, chat_id="other"), repo(c)).action, Action.IGNORE)
        self.assertEqual(c.unique_count, 1)

    def test_C06_unknown_or_wrong_project_holds(self):
        for project in (None, "other-project"):
            c, b = make()
            self.assertEqual(c.consume(response(c, project=project), repo(c)).action, Action.HOLD)

    def test_C07_stable_response_identity_required(self):
        c, b = make()
        self.assertEqual(c.consume(response(c, response_id=""), repo(c)).action, Action.HOLD)

    def test_C08_missing_repo_state_not_success(self):
        c, b = make()
        self.assertEqual(c.consume(response(c)).action, Action.HOLD)
        self.assertEqual(c.unique_count, 1)

    def test_C09_unpublished_unreadable_and_wrong_bool_hold(self):
        for change in ({"published": False}, {"readable": False}, {"published": "true"},
                       {"programme_complete": "false"}):
            c, b = make()
            self.assertEqual(c.consume(response(c), repo(c, **change)).action, Action.HOLD)

    def test_C10_same_repo_branch_and_current_worker(self):
        for change in ({"repo": "other/repo"}, {"branch": "other"},
                       {"last_chat_id": "older"}, {"last_chat_id": ""}):
            c, b = make()
            self.assertEqual(c.consume(response(c), repo(c, **change)).action, Action.HOLD)

    def test_C11_inconsistent_overall_state_holds(self):
        for change in ({"programme_complete": True}, {"next_task": None}, {"next_task": "  "}):
            c, b = make()
            self.assertEqual(c.consume(response(c), repo(c, **change)).action, Action.HOLD)

    def test_C12_overall_finish_precedes_cap(self):
        c, b = make(1)
        decision = c.consume(response(c), repo(c, programme_complete=True, next_task=None))
        self.assertEqual(decision.action, Action.STOP_FINISHED)
        self.assertIsNone(c.state.pending)

    def test_C13_initial_chat_is_in_cap(self):
        c, b = make(1)
        self.assertEqual(c.unique_count, 1)
        self.assertEqual(c.consume(response(c), repo(c)).action, Action.STOP_CAP)

    def test_C14_thirty_unique_chats_no_thirty_first(self):
        c, b = make(30)
        for n in range(1, 30):
            d = c.consume(response(c, rid=f"r{n}"), repo(c))
            self.assertEqual(d.action, Action.LAUNCH_SUCCESSOR)
            self.assertEqual(c.unique_count, n)  # prepared isn't counted as created
            b.perform(c)
            self.assertEqual(c.unique_count, n + 1)
        self.assertEqual(c.consume(response(c, rid="r30"), repo(c)).action, Action.STOP_CAP)
        self.assertEqual((c.unique_count, b.opens, len(b.sends)), (30, 29, 29))

    def test_C15_same_chat_continuations_do_not_consume_cap(self):
        c, b = make(1)
        for n in range(100):
            self.assertEqual(c.consume(response(c, "NEED_MORE_TIME", f"r{n}")).action,
                             Action.CONTINUE_CURRENT)
            b.perform(c)
        self.assertEqual((c.unique_count, b.opens, len(b.sends)), (1, 0, 100))

    def test_C16_pending_action_serializes_responses(self):
        c, b = make()
        c.consume(response(c, "NEED_MORE_TIME", "r1"))
        later = response(c, "TASK_COMPLETE", "r2")
        self.assertEqual(c.consume(later, repo(c)).action, Action.WAIT)
        b.perform(c)
        self.assertEqual(c.consume(later, repo(c)).action, Action.LAUNCH_SUCCESSOR)

    def test_C17_duplicate_completed_response_after_restart_ignored(self):
        c, b = make()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            r = response(c, "NEED_MORE_TIME")
            c.consume(r)
            b.perform(c, path)
            c = Controller.load(path)
            self.assertEqual(c.consume(r).action, Action.IGNORE)
            self.assertEqual(len(b.sends), 1)

    def test_C18_response_ids_namespaced_by_chat(self):
        c, b = make()
        c.consume(response(c, rid="same"), repo(c))
        b.perform(c)
        self.assertEqual(c.consume(response(c, "NEED_MORE_TIME", "same")).action,
                         Action.CONTINUE_CURRENT)

    def test_C19_new_chat_observation_required(self):
        c, b = make()
        d = c.consume(response(c), repo(c))
        c.begin_send(d.action_id)
        self.assertEqual(c.confirm(d.action_id, "c1", c.config.project).action, Action.HOLD)
        self.assertEqual(c.unique_count, 1)
        self.assertIsNotNone(c.state.pending)

    def test_C20_missing_readback_does_not_count_new_chat(self):
        c, b = make()
        d = c.consume(response(c), repo(c))
        c.begin_send(d.action_id)
        for observation in (False, "false", None):
            self.assertEqual(c.confirm(d.action_id, "c2", c.config.project, observation).action, Action.HOLD)
            self.assertEqual(c.unique_count, 1)

    def test_C21_continuation_must_stay_in_current_chat(self):
        c, b = make()
        d = c.consume(response(c, "NEED_MORE_TIME"))
        c.begin_send(d.action_id)
        self.assertEqual(c.confirm(d.action_id, "c2", c.config.project).action, Action.HOLD)
        self.assertEqual(c.unique_count, 1)

    def test_C22_url_aliases_normalize_one_identity(self):
        a = "https://chatgpt.com/c/chat-uuid?x=1"
        b = "https://chatgpt.com/g/g-p-project-name/c/chat-uuid#turn"
        self.assertEqual(conversation_id(a), conversation_id(b))
        self.assertEqual(conversation_id("chat-uuid"), "chat-uuid")
        with self.assertRaises(ValueError):
            conversation_id("https://chatgpt.com/g/project")

    def test_C23_error_repair_never_resets_count_or_replays_old_event(self):
        c, b = make()
        c.consume(response(c), repo(c))
        b.perform(c)
        r = response(c, "ERROR", "error-turn")
        self.assertEqual(c.consume(r).action, Action.HOLD)
        c.resume_after_owner()
        self.assertEqual(c.unique_count, 2)
        self.assertEqual(c.consume(r).action, Action.IGNORE)
        self.assertEqual(c.consume(response(c, "NEED_MORE_TIME", "new-turn")).action,
                         Action.CONTINUE_CURRENT)

    def test_C24_uncertain_send_cannot_be_automatically_retried(self):
        c, b = make()
        d = c.consume(response(c), repo(c))
        b.perform(c, fault="after_click")
        with self.assertRaises(ValueError):
            c.begin_send(d.action_id)
        with self.assertRaises(ValueError):
            c.resume_after_owner()
        self.assertEqual((c.unique_count, len(b.sends)), (1, 1))

    def test_C25_duplicate_acknowledgement_has_no_effect(self):
        c, b = make()
        d = c.consume(response(c), repo(c))
        receipt = b.perform(c)
        self.assertEqual(c.confirm(d.action_id, receipt.chat_id, receipt.project).action, Action.IGNORE)
        self.assertEqual(c.unique_count, 2)

    def test_C26_wrong_project_observation_halts(self):
        c, b = make()
        d = c.consume(response(c), repo(c))
        c.begin_send(d.action_id)
        self.assertEqual(c.confirm(d.action_id, "c2", "wrong").action, Action.HOLD)
        self.assertEqual(c.unique_count, 1)

    def test_C27_prepared_but_not_attempted_survives_restart(self):
        c, b = make()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            c.consume(response(c), repo(c))
            c.save(path)
            c = Controller.load(path)
            self.assertIsNone(c.state.halted)
            b.perform(c, path)
            self.assertEqual(c.unique_count, 2)

    def test_C28_bad_state_does_not_silently_reset_counter(self):
        c, b = make()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            c.save(path)
            good = path.read_text()
            for change in ("bad-json", "bad-count", "bad-version", "bad-pending"):
                raw = json.loads(good)
                if change == "bad-json":
                    path.write_text("{")
                else:
                    if change == "bad-count":
                        raw["state"]["unique_chat_ids"] = ["c1", "c1"]
                    elif change == "bad-version":
                        raw["version"] = 2
                    else:
                        raw["state"]["pending"] = dict(action_id="x",kind="SEND_ANYWHERE",
                            source_chat_id="c1",response_id="r1",message="x")
                    path.write_text(json.dumps(raw))
                with self.subTest(change=change), self.assertRaises((ValueError, TypeError)):
                    Controller.load(path)

    def test_C29_explicit_status_not_overridden_by_semantic_guess(self):
        c, b = make()
        semantic = SemanticVerdict(Status.TASK_COMPLETE, True, "Deliberately wrong injected guess")
        self.assertEqual(c.consume(response(c, "ERROR"), repo(c), semantic).action, Action.HOLD)
        self.assertEqual(c.state.last_status, "ERROR")

    def test_C30_owner_silence_timeout_pause_does_not_send(self):
        c, b = make()
        c.pause("Response deadline expired; no terminal response observed")
        self.assertEqual(c.consume(response(c), repo(c)).action, Action.HOLD)
        self.assertEqual((c.unique_count, len(b.sends)), (1, 0))

    def test_C31_terminal_states_not_an_error_retry(self):
        for done in (False, True):
            c, b = make(1)
            c.consume(response(c), repo(c, programme_complete=done,
                                        next_task=None if done else "Continue"))
            with self.assertRaises(ValueError):
                c.resume_after_owner()

    def test_C32_model_trace_invariants_300_seeded_runs(self):
        # Independent simple oracle for the core three-branch happy-path contract.
        # 300 runs, variable caps; no files, no browser, no sleeping.
        rng = random.Random(20261117)
        for run in range(300):
            maximum = rng.randrange(1, 31)
            c, b = make(maximum)
            oracle_count = 1
            for turn in range(60):
                status = rng.choices(["NEED_MORE_TIME", "TASK_COMPLETE", "ERROR"],
                                     [6, 4, 1])[0]
                done = rng.random() < 0.1
                r = response(c, status, f"r{turn}")
                view = repo(c, programme_complete=done, next_task=None if done else "More")
                expected = (Action.CONTINUE_CURRENT if status == "NEED_MORE_TIME"
                            else Action.HOLD if status == "ERROR"
                            else Action.STOP_FINISHED if done
                            else Action.STOP_CAP if oracle_count >= maximum
                            else Action.LAUNCH_SUCCESSOR)
                with self.subTest(run=run, turn=turn):
                    d = c.consume(r, view)
                    self.assertEqual(d.action, expected)
                    if expected in (Action.CONTINUE_CURRENT, Action.LAUNCH_SUCCESSOR):
                        before = c.unique_count
                        b.perform(c)
                        oracle_count += int(expected == Action.LAUNCH_SUCCESSOR)
                        self.assertEqual(c.unique_count, oracle_count)
                        self.assertEqual(len(set(c.state.unique_chat_ids)), c.unique_count)
                        self.assertLessEqual(c.unique_count, maximum)
                        self.assertEqual(c.unique_count - before, int(expected == Action.LAUNCH_SUCCESSOR))
                    else:
                        break

    def test_C33_uncertain_semantic_completion_never_launches(self):
        c, b = make()
        r = response(c, text="Maybe finished, maybe not.")
        for flag, reason in ((False, "Cannot distinguish slice from programme"),
                             ("false", "Malformed boolean"), (True, None)):
            c, b = make()
            r = response(c, text="Maybe finished, maybe not.")
            semantic = SemanticVerdict(Status.TASK_COMPLETE, flag, reason)
            self.assertEqual(c.consume(r, repo(c), semantic).action, Action.HOLD)

    def test_C34_rearm_requires_reason_and_possible_attempt(self):
        c, b = make()
        d = c.consume(response(c), repo(c))
        with self.assertRaises(ValueError):
            c.confirm_not_sent(d.action_id, "Not yet attempted")
        c.begin_send(d.action_id)
        with self.assertRaises(ValueError):
            c.confirm_not_sent(d.action_id, "")
        c.uncertain(d.action_id)
        c.confirm_not_sent(d.action_id, "Test trace establishes no click happened")
        b.perform(c)
        self.assertEqual(c.unique_count, 2)

    def test_C35_rejected_empty_saved_chat_id(self):
        c, b = make()
        d = c.consume(response(c), repo(c))
        c.begin_send(d.action_id)
        self.assertEqual(c.confirm(d.action_id, "", c.config.project).action, Action.HOLD)
        self.assertEqual(c.unique_count, 1)

    def test_C36_existing_draft_causes_zero_sends(self):
        c, b = make()
        c.consume(response(c), repo(c))
        b.perform(c, editable_text="Preserve my work")
        self.assertEqual(len(b.sends), 0)
        self.assertEqual(c.unique_count, 1)
        self.assertEqual(c.state.pending.phase, "prepared")
