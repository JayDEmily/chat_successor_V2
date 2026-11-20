"""ADR 0002 L02 account/installation and read-only status regression tests."""
from __future__ import annotations
from pathlib import Path
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from account_routes import require_route, bound_config_fields
from cli import create_dependencies, load_config
from launch_project import launch_request, matching_runs
from runner import initialise, inspect_state
from succession.core import Config, Controller

PROJECT="g-p-abc123"
REPO="example-org/ordinary-project"
BRANCH="work/active"
URL=f"https://chatgpt.com/g/{PROJECT}/project"
SHA="a"*40


class ADR2RouteTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base=Path(tmp.name)/"Native Windows Root"
        self.base.mkdir()
        self.file=Path(tmp.name)/"request.json"
        self.file.write_text(json.dumps({"repo":REPO,"branch":BRANCH,
            "project_name":"Mock Project","project_url":URL}),encoding="utf-8")
        self.routes={
            "schema":1,
            "accounts":{
                "shoco":{"install_root":str(self.base.resolve()),
                         "profile_path":"C:\\Users\\james\\Chrome\\Profile 11",
                         "chrome_app_id":"Chrome.ShocoTest",
                         "plugin_id":"plugin_shoco_0001","backend_commit":SHA},
                "james-student":{"install_root":str(self.base.resolve()),
                         "profile_path":"C:\\Users\\james\\Chrome\\Profile 13",
                         "chrome_app_id":"Chrome.JamesTest",
                         "plugin_id":"plugin_james_0001","backend_commit":"b"*40},
            }}
        (self.base/"account_routes.json").write_text(json.dumps(self.routes),encoding="utf-8")
        (self.base/"account-routing-required").write_text("ADR2 L02\\n",encoding="ascii")

    def route(self,key="shoco"):
        return require_route(self.base,key)

    def test_r01_selects_exact_shoco_route_and_profile(self):
        s=self.route()
        j=self.route("james-student")
        self.assertNotEqual(s["profile_path"],j["profile_path"])
        self.assertNotEqual(s["route_receipt"],j["route_receipt"])
        self.assertEqual(s["account_key"],"shoco")
        with patch("account_routes.subprocess.run", return_value=Mock(stdout=SHA)), \
             patch("launch_project.wsl",return_value=f"{SHA}\trefs/heads/{BRANCH}"), \
             patch("launch_project.WindowsUIA") as browser:
            browser.return_value._invoke.return_value={
                "project":PROJECT,"observed_url":URL,"current_chat_id":None,
                "private_window_handle":55,"editable_text":"","attachments_present":False}
            result=launch_request(self.file,self.base,check_only=True,account_key="shoco")
            self.assertEqual(result["event"],"preflight_passed")
            self.assertEqual(browser.call_args.kwargs["profile_path"],s["profile_path"])
            self.assertEqual(browser.call_args.kwargs["chrome_app_id"],s["chrome_app_id"])

    def test_wrong_backend_sha_holds_before_preflight_or_start(self):
        before = self.file.read_bytes()
        with patch("account_routes.subprocess.run", return_value=Mock(stdout="0" * 40)), \
             patch("launch_project.WindowsUIA") as browser, patch("launch_project.wsl") as git:
            for check_only in (False, True):
                with self.assertRaisesRegex(ValueError, "backend differs"):
                    launch_request(self.file, self.base, check_only=check_only, account_key="shoco")
            browser.assert_not_called()
            git.assert_not_called()
        self.assertFalse((self.base / "Runs").exists())
        self.assertEqual(self.file.read_bytes(), before)

    def test_r02_ambiguous_route_blocks_before_any_project_or_git(self):
        for key in [None,"unknown","shoco!","SHOCO"]:
            with self.subTest(key=key),patch("launch_project.resolve_project") as project, \
                    patch("launch_project.wsl") as git:
                with self.assertRaises(ValueError):
                    launch_request(self.file,self.base,account_key=key)
                project.assert_not_called()
                git.assert_not_called()

    def test_r02_wrong_route_root_blocks_without_project_side_effects(self):
        raw=json.loads((self.base/"account_routes.json").read_text())
        raw["accounts"]["shoco"]["install_root"]=str(self.base.parent)
        (self.base/"account_routes.json").write_text(json.dumps(raw))
        with patch("launch_project.resolve_project") as project:
            with self.assertRaisesRegex(ValueError,"different native"):
                launch_request(self.file,self.base,account_key="shoco")
            project.assert_not_called()

    def test_r02_relative_install_root_rejected(self):
        raw=json.loads((self.base/"account_routes.json").read_text())
        raw["accounts"]["shoco"]["install_root"]="relative/path"
        (self.base/"account_routes.json").write_text(json.dumps(raw))
        with self.assertRaisesRegex(ValueError,"must be absolute"):
            self.route()

    def test_r04_incomplete_saved_binding_rejected(self):
        cfgpath=self._stage_saved_run("c"*24)
        raw=json.loads(cfgpath.read_text())
        del raw["account_key"]
        cfgpath.write_text(json.dumps(raw))
        with self.assertRaisesRegex(ValueError,"Incomplete saved account route"):
            load_config(cfgpath)

    def test_r02_non_absolute_profile_rejected(self):
        raw=json.loads((self.base/"account_routes.json").read_text())
        raw["accounts"]["shoco"]["profile_path"]="Profile 11"
        (self.base/"account_routes.json").write_text(json.dumps(raw))
        with self.assertRaisesRegex(ValueError,"absolute"):
            self.route()

    def _stage_saved_run(self,runid,account="shoco",legacy=False):
        cfgpath=self.base/"Runs"/runid/"config.json"
        cfgpath.parent.mkdir(parents=True,exist_ok=True)
        cfg={"project":PROJECT,"project_name":"Mock Project","project_url":URL,
             "repo":REPO,"branch":BRANCH,"repo_dir_wsl":"/tmp/bare.git",
             "run_id":runid,"max_unique_chats":2,"workflow":"generic_handoff"}
        # Use workflow constant, not a guessed string.
        from repo_reader import HANDOFF_WORKFLOW
        cfg["workflow"]=HANDOFF_WORKFLOW
        if not legacy:
            cfg.update(bound_config_fields(self.route(account)))
        cfgpath.write_text(json.dumps(cfg),encoding="utf-8")
        return cfgpath

    def test_r03_distinct_accounts_namespace_same_project_without_adoption(self):
        self._stage_saved_run("c"*24,"shoco")
        self._stage_saved_run("d"*24,"james-student")
        sh=matching_runs(self.base/"Runs",PROJECT,REPO,self.route("shoco"))
        ja=matching_runs(self.base/"Runs",PROJECT,REPO,self.route("james-student"))
        self.assertEqual(set(sh),{"c"*24})
        self.assertEqual(set(ja),{"d"*24})

    def test_r04_unbound_legacy_run_hold_without_mutation(self):
        cfg=self._stage_saved_run("c"*24,legacy=True)
        before=cfg.read_bytes()
        with self.assertRaisesRegex(ValueError,"unverified"):
            matching_runs(self.base/"Runs",PROJECT,REPO,self.route())
        self.assertEqual(cfg.read_bytes(),before)

    def test_r04_same_account_different_profile_receipt_hold(self):
        cfg=self._stage_saved_run("c"*24)
        data=json.loads(cfg.read_text())
        data["chrome_profile_path"]="C:\\wrong\\profile"
        cfg.write_text(json.dumps(data))
        before=cfg.read_bytes()
        with self.assertRaisesRegex(ValueError,"unverified"):
            matching_runs(self.base/"Runs",PROJECT,REPO,self.route())
        self.assertEqual(before,cfg.read_bytes())

    def test_r03_new_job_id_generated_once_from_stable_private_request(self):
        request=json.loads(self.file.read_text())
        request["operation"]="new"
        self.file.write_text(json.dumps(request))
        with patch("account_routes.subprocess.run",return_value=Mock(stdout=SHA)), \
                patch("launch_project.resolve_project",return_value=(PROJECT,"Mock Project",URL)), \
                patch("launch_project.provision_reader",return_value="/tmp/mock-repo"), \
                patch("launch_project.launch",return_value={"event":"controller_started"}) as launch:
            first=launch_request(self.file,self.base,account_key="shoco")
            second=launch_request(self.file,self.base,account_key="shoco")
            self.assertEqual(first["run_id"],second["run_id"])
            self.assertEqual(len(first["run_id"]),24)
            self.assertEqual(second["event"],"existing_run")
            self.assertEqual(launch.call_count,1)
            cfg=load_config(self.base/"Runs"/first["run_id"]/"config.json")
            self.assertEqual(cfg["account_key"],"shoco")

    def test_r01_child_dependency_validates_account_route_and_root(self):
        path=self._stage_saved_run("c"*24)
        state=path.with_name("controller.json")
        cfg=load_config(path)
        with patch("account_routes.subprocess.run",return_value=Mock(stdout=SHA)):
            browser,reader=create_dependencies(cfg,state)
        self.assertEqual(browser.profile_path,self.route()["profile_path"])
        self.assertEqual(browser.chrome_app_id,self.route()["chrome_app_id"])
        with self.assertRaisesRegex(ValueError,"native installation"):
            create_dependencies(cfg,self.base/"Other"/"controller.json")

    def test_r04_pause_status_reports_request_distinct_from_acknowledgement(self):
        cfgpath=self._stage_saved_run("c"*24)
        state=cfgpath.with_name("controller.json")
        cfg=Config(PROJECT,REPO,BRANCH,2)
        c=initialise(state,cfg,"worker-first")
        marker=state.with_suffix(".pause")
        marker.write_text("pause generation test")
        first=inspect_state(state)
        self.assertTrue(first["pause_requested"])
        self.assertFalse(first["pause_acknowledged"])
        self.assertEqual(first["account_key"],"shoco")
        c.pause("Operator pause requested")
        c.save(state)
        second=inspect_state(state)
        self.assertTrue(second["pause_acknowledged"])
        self.assertEqual(second["unique_chat_count"],1)
        self.assertTrue(marker.exists())

    def test_r02_child_browser_profile_overrides_ambient_profile(self):
        path=self._stage_saved_run("c"*24)
        cfg=load_config(path)
        with patch("account_routes.subprocess.run",return_value=Mock(stdout=SHA)):
            b,_=create_dependencies(cfg,path.with_name("controller.json"))
        with patch("windows_backend.subprocess.run",return_value=Mock(returncode=0,stdout='{"ready": false}')) as runner:
            self.assertEqual(b._invoke("Observe",ChatId="test-worker"),{"ready":False})
            self.assertEqual(runner.call_args.kwargs["env"]["CHAT_SUCCESSION_CHROME_PROFILE_PATH"],
                             self.route()["profile_path"])
            cmd = runner.call_args.args[0]
            self.assertEqual(cmd[cmd.index("-ChromeAppId") + 1], self.route()["chrome_app_id"])

    def test_r04_unbound_legacy_direct_cli_holds_without_browser(self):
        cfgpath=self._stage_saved_run("c"*24,legacy=True)
        cfg=load_config(cfgpath)
        with patch("cli.WindowsUIA") as browser:
            with self.assertRaisesRegex(ValueError,"Unbound legacy run"):
                create_dependencies(cfg,cfgpath.with_name("controller.json"))
            browser.assert_not_called()

    def test_r03_project_display_rename_keeps_same_bound_run(self):
        cfgpath=self._stage_saved_run("c"*24)
        cfg=json.loads(cfgpath.read_text())
        cfg["project_name"]="Renamed Display Only"
        cfgpath.write_text(json.dumps(cfg))
        matches=matching_runs(self.base/"Runs",PROJECT,REPO,self.route())
        self.assertEqual(set(matches),{"c"*24})
        self.assertEqual(matches["c"*24][1]["run_stage"],"configured")

    def test_r02_no_account_key_on_bound_launch_holds(self):
        with patch("launch_project.resolve_project") as project:
            with self.assertRaisesRegex(ValueError,"account route key"):
                launch_request(self.file,self.base)
            project.assert_not_called()


if __name__ == "__main__":
    unittest.main()
