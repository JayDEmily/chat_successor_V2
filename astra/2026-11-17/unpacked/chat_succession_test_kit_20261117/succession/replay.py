"""Replay synthetic event fixtures and record observable model actions."""
from dataclasses import asdict
from pathlib import Path
import argparse
import json
import tempfile

from .core import Config, Controller, RepoView, Response, SemanticVerdict, Status
from .mock import FakeBrowser


def replay_case(case):
    cfg = Config(**case["config"])
    controller = Controller(cfg, case.get("initial_chat_id", "c1"))
    browser = FakeBrowser(cfg.project, controller.state.current_chat_id)
    trace = []
    with tempfile.TemporaryDirectory(prefix="succession-replay-") as tmp:
        state_path = Path(tmp) / "controller.json"
        for index, event in enumerate(case["events"], 1):
            kind = event["kind"]
            action = None
            reason = ""
            before = controller.unique_count
            if kind == "response":
                response = Response(
                    chat_id=event.get("chat_id", controller.state.current_chat_id),
                    response_id=event["response_id"],
                    text=event["text"], complete=event.get("complete", True),
                    role=event.get("role", "assistant"),
                    project=event.get("project", cfg.project),
                )
                repo = None
                if "repo" in event:
                    values = dict(repo=cfg.repo, branch=cfg.branch,
                                  last_chat_id=controller.state.current_chat_id,
                                  programme_complete=False, next_task="Continue next slice")
                    values.update(event["repo"])
                    repo = RepoView(**values)
                semantic = None
                if "semantic" in event:
                    values = dict(event["semantic"])
                    values["status"] = Status(values["status"])
                    semantic = SemanticVerdict(**values)
                decision = controller.consume(response, repo, semantic)
                action, reason = decision.action.value, decision.reason
                controller.save(state_path)
            elif kind == "dispatch":
                browser.perform(controller, state_path,
                                actual_project=event.get("project"),
                                editable_text=event.get("editable_text", ""),
                                fault=event.get("fault"))
            elif kind == "restart":
                controller = Controller.load(state_path)
            elif kind == "reconcile":
                send = browser.sends[-1]
                decision = controller.confirm(controller.state.pending.action_id,
                                              send["chat_id"], send["project"])
                action, reason = decision.action.value, decision.reason
                controller.save(state_path)
            elif kind == "not_sent":
                controller.confirm_not_sent(controller.state.pending.action_id, event["reason"])
                controller.save(state_path)
            elif kind == "resume":
                controller.resume_after_owner()
                controller.save(state_path)
            elif kind == "pause":
                decision = controller.pause(event.get("reason", "Owner pause"))
                action, reason = decision.action.value, decision.reason
                controller.save(state_path)
            else:
                raise ValueError(f"Unknown synthetic event: {kind}")
            row = {
                "case_id": case["id"], "event": index, "kind": kind,
                "action": action, "reason": reason, "count_before": before,
                "count": controller.unique_count, "current_chat": controller.state.current_chat_id,
                "sends": len(browser.sends), "opens": browser.opens,
                "pending_phase": controller.state.pending.phase if controller.state.pending else None,
                "halted": controller.state.halted is not None,
                "mode": "OFFLINE_SYNTHETIC",
            }
            for key, expected in event.get("expect", {}).items():
                if row[key] != expected:
                    raise AssertionError(f"{case['id']} event {index}: {key}: {row[key]!r} != {expected!r}")
            trace.append(row)
    return {"id": case["id"], "outcome": "PASS", "mode": "OFFLINE_SYNTHETIC",
            "trace": trace, "fake_sends": browser.sends}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    cases = json.loads(args.fixtures.read_text(encoding="utf-8"))
    result = [replay_case(case) for case in cases]
    text = json.dumps(result, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
