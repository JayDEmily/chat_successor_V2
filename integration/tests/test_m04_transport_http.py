"""Actual localhost MCP SDK transport; never a native ChatGPT claim."""
import asyncio
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time

from mcp import Client
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from m04_transport_probe import Probe,A,B,SHA,BRANCH


async def exercise(port, phase, probe):
    registration,report=probe.registration,probe.report
    async with Client(f"http://127.0.0.1:{port}/mcp") as client:
        tools=(await client.list_tools()).tools
        assert {t.name for t in tools}=={"probe_registration","probe_report"}
        assert all(t.annotations.read_only_hint is False for t in tools)
        a={"openai/session":"synthetic-A","openai/subject":"synthetic-owner"}
        b={"openai/session":"synthetic-B","openai/subject":"synthetic-owner"}
        cases=[("probe_registration",registration(A),a,"registered"),
              ("probe_registration",registration(A),a,"duplicate"),
              ("probe_report",report(A,"NEED_MORE_TIME"),a,"received"),
              ("probe_report",report(A,"NEED_MORE_TIME"),a,"duplicate"),
              ("probe_registration",registration(A),b,"rejected"),
              ("probe_registration",registration(B),b,"registered"),
              ("probe_report",report(B,"ERROR",SHA),b,"rejected"),
              ("probe_report",report(B,"TASK_COMPLETE",SHA),b,"received")]
        for i,(tool,body,meta,expected) in enumerate(cases,1):
            if (phase==1 and i>7) or (phase==2 and i!=8):
                continue
            r=await client.call_tool(tool,{"body":body},meta=meta)
            assert not r.is_error, r
            out=r.structured_content
            assert out["slot"]==i and out["result"]==expected, (i,out)
            assert not any(out[k] for k in ("authenticated_owner","worker_admitted","dispatch_authorized","native_message_attested"))
            print("slot",i,expected,flush=True)
        if phase==2:
            r=await client.call_tool("probe_report",{"body":report(B,"TASK_COMPLETE",SHA)},meta=b)
            assert r.structured_content["result"]=="quota_exhausted"


def run():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/"probe"
        script=Path(__file__).resolve().parents[1]/"m04_transport_probe.py"
        for phase in (1,2):
            with socket.socket() as s:
                s.bind(("127.0.0.1",0))
                port=s.getsockname()[1]
            cmd=[sys.executable,"-B",str(script),"--root",str(root),"--port",str(port)]
            if phase==1:cmd.append("--create")
            p=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            try:
                for _ in range(100):
                    if p.poll() is not None:raise RuntimeError("server stopped")
                    try:
                        with socket.create_connection(("127.0.0.1",port),timeout=.2):break
                    except OSError:time.sleep(.1)
                else:raise RuntimeError("server not ready")
                asyncio.run(exercise(port,phase,Probe(root)))
            finally:
                p.terminate()
                try:_,err=p.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    p.kill();_,err=p.communicate()
                if p.returncode not in (0,-15):print(err[-2000:])
        probe=Probe(root)
        with probe.connect() as db:
            rows=probe.check(db)
            assert len(rows)==8
            assert len({r[3] for r in rows[:4]})==1
            assert len({r[3] for r in rows[4:]})==1
            assert rows[0][3]!=rows[4][3] and len({r[4] for r in rows})==1
            assert "synthetic-owner" not in json.dumps(rows)
        from mcp_native_poc import Proof
        for run in (A,B):
            with Proof(root/run,clock=lambda:100.) as p:
                assert p.count==1 and p.active["report"] and not p.active["consumed"]
                assert p.core.state.pending is None
        print("PASS: actual MCP HTTP 8/8 through accepted synthetic adapter, restart, ninth denied; native calls 0")

def negative():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/"negative"
        probe=Probe(root,create=True)
        # Failed first slot cannot manufacture a positive duplicate.
        assert probe.call("probe_registration",probe.registration(A),None)["result"]=="rejected"
        meta={"openai/session":"A","openai/subject":"S"}
        assert probe.call("probe_registration",probe.registration(A),meta)["result"]=="rejected"
        with probe.connect() as db:
            db.execute("INSERT INTO pending VALUES(3)")
        try: Probe(root)
        except RuntimeError: pass
        else: raise AssertionError("Reopened unresolved call")
        print("PASS: missing metadata, failed prefix, unresolved slot hold")

if __name__=="__main__":
    run()
    negative()
