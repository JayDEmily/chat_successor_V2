"""M04 offline preflight rehearsal, NOT a live MCP server or identity provider.

Uses ephemeral RSA test keys, dummy issuers/accounts, synthetic saved receipts,
a disposable local Git remote and a local SQL invocation journal. It cannot
listen, connect a plugin, launch a chat, or qualify native metadata. The
accepted M03 Proof remains the only succession controller.
"""
import hashlib
import hmac
import os
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mcp_native_poc import Action, Auth, Delivery, Preflight, Proof, Rejected, Route, digest

ISSUER = "https://issuer.example.invalid"
AUDIENCE = "https://resource.example.invalid/mcp"
OAUTH_SUB = "offline-owner"
SCOPE = "succession:trial"
C1 = "11111111-1111-1111-1111-111111111111"
C2 = "22222222-2222-2222-2222-222222222222"
BRANCH = "work/m04-fixture"
BASE = "0" * 40
LIMIT = 8
TOOLS = ("register_worker", "report_worker")


class BudgetHold(RuntimeError):
    pass


class Budget:
    """Offline reservation-before-handler rehearsal; never reset on reopen.

    Separate committed rows for attempt and outcome. An unresolved attempt
    blocks further execution, even after reconnect. This uses local SQLite
    transaction semantics, not the M03 journal's filesystem fault guarantees.
    """
    def __init__(self, path, *, create=False):
        self.path = Path(path)
        if create:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
        self.db = sqlite3.connect(self.path.resolve().as_uri() + "?mode=rw",
                                  uri=True, isolation_level=None, timeout=5)
        try:
            self.db.execute("PRAGMA synchronous=FULL")
            if create:
                self.db.executescript("""
                BEGIN IMMEDIATE;
                CREATE TABLE attempts(n INTEGER PRIMARY KEY CHECK(n BETWEEN 1 AND 8),
                                      tool TEXT NOT NULL);
                CREATE TABLE outcomes(n INTEGER PRIMARY KEY REFERENCES attempts(n),
                                      result TEXT NOT NULL
                                      CHECK(result IN ('registered','received','duplicate',
                                                       'hold','conflict','rejected')));
                COMMIT;
                """)
            self.db.execute("PRAGMA foreign_keys=ON")
            if self.db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise BudgetHold("Counter integrity failure")
            self._validate()
        except BaseException:
            self.close()
            raise

    def _validate(self):
        rows = self.db.execute(
            "SELECT a.n,o.result FROM attempts a LEFT JOIN outcomes o USING(n) ORDER BY a.n"
        ).fetchall()
        if [r[0] for r in rows] != list(range(1, len(rows) + 1)) or len(rows) > LIMIT:
            raise BudgetHold("Counter sequence invalid")
        if self.db.execute("PRAGMA foreign_key_check").fetchall():
            raise BudgetHold("Counter reference invalid")
        if any(result is None for _, result in rows[:-1]):
            raise BudgetHold("Unresolved earlier attempt")
        return rows

    def reserve(self, tool):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            rows = self._validate()
            if rows and rows[-1][1] is None:
                raise BudgetHold("Unknown invocation outcome: no retry")
            if len(rows) == LIMIT:
                raise BudgetHold("Eight-call quota exhausted")
            n = len(rows) + 1
            self.db.execute("INSERT INTO attempts VALUES(?,?)",
                            (n, tool if type(tool) is str and tool in TOOLS else "invalid"))
            self.db.execute("COMMIT")
            return n
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def finish(self, n, result):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            rows = self._validate()
            if not rows or rows[-1] != (n, None):
                raise BudgetHold("No matching pending invocation")
            self.db.execute("INSERT INTO outcomes VALUES(?,?)", (n, result))
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def rows(self):
        return self._validate()

    def close(self):
        self.db.close()


class LocalVerifier:
    """Offline verifier of signed test tokens, not OAuth flow qualification."""
    def __init__(self, public_key, correlation_key):
        self.public_key = public_key
        self.correlation_key = correlation_key

    def opaque(self, label, value):
        if type(value) is not str or not value or len(value) > 1024 or not value.strip():
            raise Rejected("Missing/invalid synthetic metadata")
        return hmac.new(self.correlation_key, (label + ":" + value).encode("utf-8"),
                        hashlib.sha256).hexdigest()

    def context(self, token, metadata, route):
        try:
            claims = jwt.decode(token, self.public_key, algorithms=["RS256"],
                                issuer=ISSUER, audience=AUDIENCE,
                                options={"require": ["iss", "aud", "sub", "iat", "exp", "nbf", "scope"],
                                         "strict_aud": True})
        except (jwt.PyJWTError, ValueError, TypeError):
            raise Rejected("Invalid test credential") from None
        if (claims["sub"] != OAUTH_SUB or claims["scope"] != SCOPE
                or any(type(claims[x]) is not int for x in ("iat", "nbf", "exp"))):
            raise Rejected("Wrong test credential scope/subject")
        if type(metadata) is not dict:
            raise Rejected("Missing synthetic host metadata")
        return Auth(route.principal, route.run_id, route.account_key,
                    self.opaque("session", metadata.get("openai/session")),
                    self.opaque("subject", metadata.get("openai/subject")))


def invoke(budget, proofs, verifier, tool, body, credential, separate_metadata):
    """Count all attempts before validation; leave unknown exceptions pending."""
    n = budget.reserve(tool)
    try:
        if (type(tool) is not str or tool not in TOOLS or type(body) is not dict
                or type(body.get("run_id")) is not str or body["run_id"] not in proofs):
            raise Rejected("Unknown fixture route or tool")
        proof = proofs[body["run_id"]]
        auth = verifier.context(credential, separate_metadata, proof.route)
        if tool == "register_worker":
            if body["run_id"] == "fixture-b":
                a = proofs["fixture-a"].active["registration"]
                if not a or a["session"] == auth.session or a["subject"] != auth.subject:
                    raise Rejected("Second fixture session/subject mismatch")
            result = proof.register_worker(body, auth)
            label = "registered"
        else:
            result = proof.report_worker(body, auth)
            label = result
    except Rejected:
        result = label = "rejected"
    budget.finish(n, label)
    return result


def git(*args, cwd=None):
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               GIT_TERMINAL_PROMPT="0")
    return subprocess.check_output(["git", "-c", "core.hooksPath=/dev/null",
                                    "-c", "commit.gpgsign=false", *args],
                                   cwd=cwd, env=env, text=True,
                                   stderr=subprocess.STDOUT).strip()


def local_publication(root):
    """Create/read a local bare Git fixture; no GitHub or network operations."""
    remote = root / "remote.git"
    work = root / "writer"
    git("init", "--bare", str(remote))
    git("init", "-b", BRANCH, str(work))
    def commit(message):
        git("-c", "user.name=Offline fixture", "-c", "user.email=fixture@example.invalid",
            "commit", "-m", message, cwd=work)
        return git("rev-parse", "HEAD", cwd=work)
    (work / "payload.txt").write_text("base\n")
    git("add", "payload.txt", cwd=work)
    base = commit("Synthetic base")
    (work / "payload.txt").write_text("completed fixture\n")
    git("add", "payload.txt", cwd=work)
    tip = commit("Synthetic publication\n\nChat-Succession-Run: fixture-b\n"
                 f"Chat-ID: {C2}\nChat-Succession-Next: FINISHED")
    git("push", str(remote), f"HEAD:refs/heads/{BRANCH}", cwd=work)
    # Independent read from bare remote, not the claim or the working tree.
    assert git("--git-dir", str(remote), "rev-parse", f"refs/heads/{BRANCH}") == tip
    git("--git-dir", str(remote), "merge-base", "--is-ancestor", base, tip)
    assert git("--git-dir", str(remote), "show", f"{tip}:payload.txt") == "completed fixture"
    for key, expected in [("Chat-Succession-Run", "fixture-b"), ("Chat-ID", C2),
                          ("Chat-Succession-Next", "FINISHED")]:
        assert git("--git-dir", str(remote), "show", "-s",
                   f"--format=%(trailers:key={key},valueonly)", tip) == expected
    return base, tip


class PreflightRehearsal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.signing = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.other = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cs-m04-offline-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.key = secrets.token_bytes(32)
        self.verifier = LocalVerifier(self.signing.public_key(), self.key)
        self.ma = {"openai/session": "offline-A", "openai/subject": "offline-subject"}
        self.mb = {"openai/session": "offline-B", "openai/subject": "offline-subject"}
        self.proofs = {}
        self.dispatch = {}
        self.budget = Budget(self.root / "quota.sqlite", create=True)
        self.addCleanup(self.cleanup)

    def cleanup(self):
        for p in self.proofs.values():
            p.close()
        self.budget.close()

    def mint(self, key=None, omit=None, **overrides):
        now = int(time.time())
        claims = dict(iss=ISSUER, aud=AUDIENCE, sub=OAUTH_SUB, scope=SCOPE,
                      iat=now-10, nbf=now-10, exp=now+300) | overrides
        if omit:
            del claims[omit]
        return jwt.encode(claims, key or self.signing, algorithm="RS256")

    def make(self, run_id, base=BASE):
        route = Route(run_id, "fixture-principal", "fixture-account", "fixture-project",
                      "example/fixture", BRANCH, base, 1, action_cap=1)
        proof = Proof(self.root / run_id, route, clock=lambda: 100.)
        dispatch = proof.reserve()
        self.proofs[run_id] = proof
        self.dispatch[run_id] = dispatch
        self.assertEqual(proof.begin_attempt(dispatch, Preflight(
            route.account_key, route.project_id, None, True, True, None)), Action.WAIT)

    def reg(self, run):
        d = self.dispatch[run]
        return dict(schema_version=1, run_id=run, action_id=d.action_id,
                    challenge=d.challenge)

    def report(self, run, status="NEED_MORE_TIME", commit=None):
        return dict(schema_version=1, run_id=run, action_id=self.dispatch[run].action_id,
                    status=status, publication_sha=commit,
                    publication_branch=BRANCH if commit else None)

    def call(self, tool, body, token, meta):
        return invoke(self.budget, self.proofs, self.verifier, tool, body, token, meta)

    def bind_synthetic(self, run, token, meta, cid):
        p, d = self.proofs[run], self.dispatch[run]
        auth = self.verifier.context(token, meta, p.route)
        self.assertEqual(p.admit_delivery(Delivery(
            run, d.action_id, p.route.account_key, p.route.project_id, cid,
            digest(d.prompt), auth.principal, auth.session, auth.subject, True)), Action.WAIT)

    def test_N01_N08_bounded_rehearsal(self):
        base, tip = local_publication(self.root)
        self.make("fixture-a", base)
        self.make("fixture-b", base)
        token = self.mint()
        a, b = self.proofs["fixture-a"], self.proofs["fixture-b"]
        r1 = self.call(TOOLS[0], self.reg("fixture-a"), token, self.ma)
        self.assertEqual(r1, {"receipt": self.dispatch["fixture-a"].action_id, "bound": False})
        self.assertEqual(a.count, 0)
        self.assertEqual(self.call(TOOLS[0], self.reg("fixture-a"), token, self.ma), r1)
        self.bind_synthetic("fixture-a", token, self.ma, C1)
        self.assertEqual(self.call(TOOLS[1], self.report("fixture-a"), token, self.ma), "received")
        self.assertEqual(self.call(TOOLS[1], self.report("fixture-a"), token, self.ma), "duplicate")
        self.assertEqual(self.call(TOOLS[0], self.reg("fixture-a"), token, self.mb), "rejected")
        self.assertFalse(self.call(TOOLS[0], self.reg("fixture-b"), token, self.mb)["bound"])
        self.assertNotEqual(a.active["registration"]["session"], b.active["registration"]["session"])
        self.assertEqual(a.active["registration"]["subject"], b.active["registration"]["subject"])
        self.bind_synthetic("fixture-b", token, self.mb, C2)
        # N07 chooses an incompatible status/publication tuple; it must not
        # consume the only immutable report slot with a wrong but valid SHA.
        self.assertEqual(self.call(TOOLS[1], self.report("fixture-b", "ERROR", tip),
                                   token, self.mb), "rejected")
        self.assertIsNone(b.active["report"])
        # Local reconnect simulation: reopen quota store and both proof stores.
        self.budget.close()
        self.budget = Budget(self.root / "quota.sqlite")
        for name,p in list(self.proofs.items()):
            p.close()
            self.proofs[name] = Proof(self.root / name, clock=lambda:100.)
        self.verifier = LocalVerifier(self.signing.public_key(), self.key)
        b = self.proofs["fixture-b"]
        self.assertEqual(self.call(TOOLS[1], self.report("fixture-b", "TASK_COMPLETE", tip),
                                   token, self.mb), "received")
        self.assertEqual([r[1] for r in self.budget.rows()],
                         ["registered","registered","received","duplicate",
                          "rejected","registered","rejected","received"])
        with self.assertRaises(BudgetHold):
            self.call(TOOLS[1], self.report("fixture-b", "TASK_COMPLETE", tip),
                      token, self.mb)
        for p in self.proofs.values():
            self.assertFalse(p.active["consumed"])
            self.assertIsNone(p.core.state.pending)
            self.assertEqual(p.count, 1)  # synthetic fixture only
            for f in p.path.iterdir():
                if f.name.startswith(("ledger","intent")):
                    self.assertNotIn(token, f.read_text())
                    self.assertNotIn("offline-subject", f.read_text())
                    self.assertNotIn("offline-A", f.read_text())
                    self.assertNotIn("offline-B", f.read_text())
        self.assertEqual(b.active["report"]["sha"], tip)

    def test_invalid_signed_credentials_counted(self):
        self.make("fixture-a")
        now = int(time.time())
        cases = [None, self.mint(key=self.other),
                 self.mint(iss="https://wrong.example.invalid"),
                 self.mint(aud="https://wrong.example.invalid"),
                 self.mint(sub="wrong"), self.mint(scope="wrong"),
                 self.mint(exp=now-1), self.mint(nbf=now+100)]
        for credential in cases:
            self.assertEqual(self.call(TOOLS[0], self.reg("fixture-a"),
                                       credential, self.ma), "rejected")
        self.assertEqual(self.budget.rows(), [(i, "rejected") for i in range(1,9)])
        self.assertIsNone(self.proofs["fixture-a"].active["registration"])

    def test_missing_claim_metadata_and_body_injection(self):
        self.make("fixture-a")
        token = self.mint()
        for credential, meta, body in [
            (self.mint(omit="exp"), self.ma, self.reg("fixture-a")),
            (self.mint(omit="scope"), self.ma, self.reg("fixture-a")),
            (token, None, self.reg("fixture-a")),
            (token, {"openai/session":"A"}, self.reg("fixture-a")),
            (token, {"openai/subject":"subject"}, self.reg("fixture-a")),
            (token, dict(self.ma, **{"openai/session":True}), self.reg("fixture-a")),
            (token, self.ma, self.reg("fixture-a") | {"principal":"fixture-principal"}),
            (token, self.ma, self.reg("fixture-a") | {"schema_version":True}),
        ]:
            self.assertEqual(self.call(TOOLS[0], body, credential, meta), "rejected")
        self.assertEqual(len(self.budget.rows()), 8)
        self.assertIsNone(self.proofs["fixture-a"].active["registration"])

    def test_distinct_session_same_subject(self):
        self.make("fixture-a")
        self.make("fixture-b")
        token = self.mint()
        self.call(TOOLS[0], self.reg("fixture-a"), token, self.ma)
        for meta in (self.ma, dict(self.mb, **{"openai/subject":"different"})):
            self.assertEqual(self.call(TOOLS[0], self.reg("fixture-b"), token, meta), "rejected")
        self.assertIsNone(self.proofs["fixture-b"].active["registration"])
        self.assertFalse(self.call(TOOLS[0], self.reg("fixture-b"), token, self.mb)["bound"])

    def test_pending_slot_survives_reconnect_and_competing_store(self):
        self.assertEqual(self.budget.reserve(TOOLS[0]), 1)
        other = Budget(self.root / "quota.sqlite")
        try:
            with self.assertRaises(BudgetHold):
                other.reserve(TOOLS[1])
        finally:
            other.close()
        self.budget.close()
        self.budget = Budget(self.root / "quota.sqlite")
        self.assertEqual(self.budget.rows(), [(1,None)])
        with self.assertRaises(BudgetHold):
            self.budget.reserve(TOOLS[0])

    def test_actual_process_exit_after_quota_reservation(self):
        path = self.root / "crash.sqlite"
        init = Budget(path, create=True)
        init.close()
        pid = os.fork()
        if not pid:
            try:
                worker = Budget(path)
                worker.reserve(TOOLS[0])
                os._exit(70)
            except BaseException:
                os._exit(71)
        _, status = os.waitpid(pid, 0)
        self.assertEqual(os.waitstatus_to_exitcode(status), 70)
        recovered = Budget(path)
        try:
            self.assertEqual(recovered.rows(), [(1,None)])
            with self.assertRaises(BudgetHold):
                recovered.reserve(TOOLS[0])
        finally:
            recovered.close()

    def test_unexpected_handler_failure_consumes_slot_and_holds(self):
        self.make("fixture-a")
        with patch.object(self.proofs["fixture-a"], "register_worker",
                          side_effect=OSError("injected failure")):
            with self.assertRaises(OSError):
                self.call(TOOLS[0], self.reg("fixture-a"), self.mint(), self.ma)
        self.assertEqual(self.budget.rows(), [(1,None)])
        self.budget.close()
        self.budget = Budget(self.root / "quota.sqlite")
        with self.assertRaises(BudgetHold):
            self.call(TOOLS[0], self.reg("fixture-a"), self.mint(), self.ma)
        self.assertIsNone(self.proofs["fixture-a"].active["registration"])

    def test_missing_counter_not_recreated(self):
        path = self.root / "missing.sqlite"
        with self.assertRaises(sqlite3.OperationalError):
            Budget(path)
        self.assertFalse(path.exists())
        with self.assertRaises(FileExistsError):
            Budget(self.root / "quota.sqlite", create=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
