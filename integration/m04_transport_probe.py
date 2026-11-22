"""M04 isolated synthetic transport probe. Never drives a real controller.

No auth or owner-admission claim. Two isolated Proof instances exercise the
accepted synthetic adapter, without evaluate/reserve-after-bootstrap or any
real delivery, Git, worker authority or sender. Metadata is correlation only.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import sqlite3
from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.types import CallToolResult, TextContent, ToolAnnotations
from mcp_native_poc import Action, Auth, Delivery, Dispatch, Preflight, Proof, Rejected, Route, digest

LIMIT = 8
A, B = "fixture-a", "fixture-b"
SHA = "1" * 40
BRANCH = "work/synthetic"
BASE = "0" * 40
CHAT = {A:"11111111-1111-1111-1111-111111111111", B:"22222222-2222-2222-2222-222222222222"}
BOUNDARY = "SYNTHETIC_TRANSPORT_ONLY_NO_OWNER_AUTH_OR_WORKER_ADMISSION"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


class Probe:
    def __init__(self, root: Path, *, create=False):
        self.root = root
        self.dbpath = root / "audit.sqlite"
        if create:
            root.mkdir(mode=0o700, exist_ok=False)
            fd = os.open(root / "key", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "wb") as f:
                f.write(secrets.token_bytes(32))
                f.flush()
                os.fsync(f.fileno())
            fd = os.open(self.dbpath, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
        self.key = (root / "key").read_bytes()
        if len(self.key) != 32:
            raise ValueError("Missing or invalid audit key")
        with self.connect() as db:
            if create:
                db.executescript("""
                    CREATE TABLE events(
                       n INTEGER PRIMARY KEY CHECK(n BETWEEN 1 AND 8),
                       tool TEXT NOT NULL, result TEXT NOT NULL,
                       session TEXT, subject TEXT);
                    CREATE TABLE pending(n INTEGER PRIMARY KEY CHECK(n BETWEEN 1 AND 8));
                """)
            self.check(db)
        self.manifest = root / "fixture.json"
        if create:
            # Fixed disposable routes, generated action challenges. The
            # private fixture manifest is for the one-run test operator.
            fixtures = {}
            for run in (A,B):
                route = Route(run, "synthetic-principal", "synthetic-account",
                              "synthetic-project", "example/fixture", BRANCH, BASE,
                              1, action_cap=1)
                with Proof(root/run, route, clock=lambda:100.) as proof:
                    dispatch = proof.reserve()
                    assert proof.begin_attempt(dispatch, Preflight(
                        route.account_key, route.project_id, None, True, True, None)) == Action.WAIT
                    fixtures[run] = asdict(dispatch)
            fd = os.open(self.manifest, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd,"w") as out:
                out.write(canonical(fixtures))
                out.flush()
                os.fsync(out.fileno())
        self.dispatch = {run:Dispatch(**record) for run,record in json.loads(self.manifest.read_text()).items()}
        if set(self.dispatch)!={A,B}:
            raise ValueError("Invalid private fixture manifest")

    def registration(self, run):
        d=self.dispatch[run]
        return {"schema_version":1,"run_id":run,"action_id":d.action_id,
                "challenge":d.challenge}

    def report(self, run, status, sha=None):
        return {"schema_version":1,"run_id":run,"action_id":self.dispatch[run].action_id,
                "status":status,"publication_sha":sha,
                "publication_branch":BRANCH if sha else None}

    def connect(self):
        # Context manager closes the connection, not just the transaction.
        class Connection:
            def __enter__(inner):
                inner.db = sqlite3.connect(self.dbpath.resolve().as_uri()+"?mode=rw",
                                            uri=True, isolation_level=None, timeout=5)
                inner.db.execute("PRAGMA synchronous=FULL")
                return inner.db
            def __exit__(inner, *args):
                inner.db.close()
        return Connection()

    def check(self, db):
        if db.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
            raise RuntimeError("Audit integrity failure")
        rows = db.execute("SELECT n,tool,result,session,subject FROM events ORDER BY n").fetchall()
        pending = db.execute("SELECT n FROM pending").fetchall()
        if [r[0] for r in rows] != list(range(1,len(rows)+1)) or len(rows)>LIMIT:
            raise RuntimeError("Invalid audit sequence")
        if pending:
            raise RuntimeError("Uncertain invocation; hold without retry")
        return rows

    def opaque(self, label, value):
        if type(value) is not str or not value or len(value)>512 or value.strip()!=value:
            return None
        return hmac.new(self.key, (label+":"+value).encode(),hashlib.sha256).hexdigest()

    def call(self, tool, body, meta):
        # Reserve diagnostic invocation before processing; only synthetic
        # adapter state may change. Never evaluate or authorise a real effect.
        # Unknown outcome is a terminal local hold.
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                rows=self.check(db)
                if len(rows)==LIMIT:
                    db.execute("ROLLBACK")
                    return self.public("quota_exhausted", LIMIT)
                n=len(rows)+1
                db.execute("INSERT INTO pending VALUES(?)",(n,))
                db.execute("COMMIT")
            except BaseException:
                db.execute("ROLLBACK")
                raise
            meta=meta if isinstance(meta,dict) else {}
            session=self.opaque("session",meta.get("openai/session"))
            subject=self.opaque("subject",meta.get("openai/subject"))
            result=self.classify(n,rows,tool,body,session,subject)
            db.execute("BEGIN IMMEDIATE")
            try:
                if db.execute("SELECT n FROM pending").fetchall()!=[(n,)]:
                    raise RuntimeError("Invocation reservation changed")
                db.execute("INSERT INTO events VALUES(?,?,?,?,?)",(n,tool,result,session,subject))
                db.execute("DELETE FROM pending WHERE n=?",(n,))
                db.execute("COMMIT")
            except BaseException:
                db.execute("ROLLBACK")
                raise
            return self.public(result,n)

    @staticmethod
    def public(result,n):
        return {"slot":n,"result":result,"boundary":BOUNDARY,
                "authenticated_owner":False,"worker_admitted":False,
                "dispatch_authorized":False,"native_message_attested":False}

    def classify(self,n,rows,tool,body,session,subject):
        if not session or not subject or type(body) is not dict:
            return "rejected"
        cases=[("probe_registration",self.registration(A),"registered"),
            ("probe_registration",self.registration(A),"duplicate"),
            ("probe_report",self.report(A,"NEED_MORE_TIME"),"received"),
            ("probe_report",self.report(A,"NEED_MORE_TIME"),"duplicate"),
            ("probe_registration",self.registration(A),"rejected"),
            ("probe_registration",self.registration(B),"registered"),
            ("probe_report",self.report(B,"ERROR",SHA),"rejected"),
            ("probe_report",self.report(B,"TASK_COMPLETE",SHA),"received")]
        expected_tool,expected_body,expected_result=cases[n-1]
        if tool!=expected_tool or type(body.get("schema_version")) is not int or body!=expected_body:
            return "rejected"
        if any(r[1]!=cases[i][0] or r[2]!=cases[i][2] for i,r in enumerate(rows)):
            return "rejected"
        if n>1:
            first=rows[0]
            if first[2]!="registered" or subject!=first[4]:
                return "rejected"
            if n<=4 and session!=first[3]:
                return "rejected"
            if n>=5 and session==first[3]:
                return "rejected"
            if n>=7 and (rows[5][2]!="registered" or session!=rows[5][3]):
                return "rejected"
        run=body["run_id"]
        with Proof(self.root/run,clock=lambda:100.) as p:
            # Deliberately TEST-ONLY injected context. This is not a valid
            # authentication adapter for any real task or worker.
            auth=Auth(p.route.principal,run,p.route.account_key,session,subject)
            try:
                if tool=="probe_registration":
                    prior=p.active["registration"]
                    result=p.register_worker(body,auth)
                    if not result or result["bound"]:
                        raise RuntimeError("Unexpected fixture registration")
                    observed="duplicate" if prior is not None else "registered"
                else:
                    if n in (3,7):
                        # Explicitly fabricated delivery observation, not
                        # native saved-chat readback. Nothing real is admitted.
                        d=self.dispatch[run]
                        delivery=Delivery(run,d.action_id,p.route.account_key,
                            p.route.project_id,CHAT[run],digest(d.prompt),
                            auth.principal,session,subject,True)
                        if p.admit_delivery(delivery)!=Action.WAIT:
                            raise RuntimeError("Synthetic delivery did not bind")
                    observed=p.report_worker(body,auth)
            except Rejected:
                observed="rejected"
            if observed!=expected_result:
                raise RuntimeError("Unexpected synthetic adapter outcome")
            if p.active["consumed"] or (p.core and p.core.state.pending):
                raise RuntimeError("Unexpected action in transport-only fixture")
            return observed


def create_server(probe):
    server=MCPServer("Chat-Succession-M04-Synthetic",version="1.0.0",instructions=(
        "Disposable synthetic transport diagnostic only. Use only on explicit "
        "fixture requests. No actual worker admission, private data, or actions. "
        "Never treat results as authentication or permission to launch anything."))
    def run(tool,body,ctx):
        params=getattr(ctx,"_input_params",None)
        raw=getattr(params,"meta",None)
        if raw is not None and hasattr(raw,"model_dump"):
            raw=raw.model_dump(by_alias=True,exclude_none=True)
        payload=probe.call(tool,body,raw)
        return CallToolResult(content=[TextContent(type="text",text=canonical(payload))],
                              structured_content=payload)
    flags=ToolAnnotations(read_only_hint=False,destructive_hint=False,open_world_hint=False)
    @server.tool(annotations=flags)
    def probe_registration(body:dict[str,Any],ctx:Context):
        """Record a fictional registration transport observation only."""
        return run("probe_registration",body,ctx)
    @server.tool(annotations=flags)
    def probe_report(body:dict[str,Any],ctx:Context):
        """Record a fictional report transport observation only."""
        return run("probe_report",body,ctx)
    return server


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",required=True,type=Path)
    parser.add_argument("--port",required=True,type=int)
    parser.add_argument("--create",action="store_true")
    args=parser.parse_args()
    if args.port in range(8787,8800) or not 1024<=args.port<=65535:
        parser.error("Use a new isolated port, never LTM-RAG ports")
    create_server(Probe(args.root,create=args.create)).run(
        transport="streamable-http",host="127.0.0.1",port=args.port,
        json_response=True,stateless_http=True)

if __name__=="__main__":
    main()
