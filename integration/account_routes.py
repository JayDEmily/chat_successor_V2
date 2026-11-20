"""Explicit non-secret account/installation binding for ADR 0002.

An installed backend opts in by placing account-routing-required in its
canonical native installation directory, with account_routes.json beside it.
Legacy installations continue only until that opt-in deployment. New bound
runs never adopt an unverified legacy journal or an ambient Chrome profile.
"""
from __future__ import annotations

import hashlib
import json
import ntpath
from pathlib import Path
import re
import subprocess

_ACCOUNT = re.compile(r"[a-z][a-z0-9-]{1,39}\Z")
_APP_ID = re.compile(r"[A-Za-z0-9_.-]{1,128}")
_ROUTE_FIELDS = {"install_root", "profile_path", "chrome_app_id", "plugin_id", "backend_commit"}


def _reject_duplicate_json_keys(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("Conflicting duplicate account route key")
        value[key] = item
    return value


def require_route(install_root: Path, account_key: str | None) -> dict | None:
    base = install_root.resolve()
    marker = base / "account-routing-required"
    if not marker.exists():
        if account_key is not None:
            raise ValueError("Account route key specified but no verified route installation exists")
        return None  # legacy, pre-migration installation
    if not isinstance(account_key, str) or not _ACCOUNT.fullmatch(account_key):
        raise ValueError("A verified account route key is required before any browser effect")
    path = base / "account_routes.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"),
                         object_pairs_hook=_reject_duplicate_json_keys)
    except (OSError, ValueError) as exc:
        raise ValueError("Account routes are unavailable or malformed") from exc
    if not isinstance(raw, dict) or raw.get("schema") != 1 or not isinstance(raw.get("accounts"), dict):
        raise ValueError("Unsupported account route document")
    # A single signed-in Chrome profile cannot independently represent two
    # distinct ChatGPT accounts. Reject ambiguous sibling routes before any
    # login/browser operation, including Windows case/slash variants.
    seen_profiles = set()
    seen_window_ids = set()
    seen_plugins = set()
    for sibling_key, sibling in raw["accounts"].items():
        if (not isinstance(sibling_key, str) or not _ACCOUNT.fullmatch(sibling_key)
                or not isinstance(sibling, dict)
                or set(sibling) != _ROUTE_FIELDS
                or any(not isinstance(value, str) or not value.strip() for value in sibling.values())
                or not _APP_ID.fullmatch(sibling["chrome_app_id"])
                or not re.fullmatch(r"[A-Za-z0-9_-]{8,128}", sibling["plugin_id"])
                or not re.fullmatch(r"[0-9a-f]{40}", sibling["backend_commit"])):
            raise ValueError("Invalid account route sibling entry")
        profile_key = ntpath.normcase(ntpath.normpath(sibling["profile_path"])).casefold()
        if profile_key in seen_profiles:
            raise ValueError("Conflicting account routes share one Chrome profile")
        if sibling["chrome_app_id"].casefold() in seen_window_ids or sibling["plugin_id"] in seen_plugins:
            raise ValueError("Conflicting account routes share a Chrome window identity or plugin")
        seen_profiles.add(profile_key)
        seen_window_ids.add(sibling["chrome_app_id"].casefold())
        seen_plugins.add(sibling["plugin_id"])
    entry = raw["accounts"].get(account_key)
    if not isinstance(entry, dict):
        raise ValueError("Unknown account route; refusing implicit fallback")
    if not Path(entry["install_root"]).is_absolute():
        raise ValueError("Account installation root must be absolute")
    try:
        selected_root = Path(entry["install_root"]).resolve(strict=False)
    except (OSError, ValueError) as exc:
        raise ValueError("Invalid native account installation root") from exc
    if selected_root != base:
        raise ValueError("Account route has a different native installation root")
    profile = entry["profile_path"]
    if not ntpath.isabs(profile) and not Path(profile).is_absolute():
        raise ValueError("Account Chrome profile path must be absolute")
    receipt = hashlib.sha256(json.dumps(
        {"account_key": account_key, **entry}, sort_keys=True,
        separators=(",", ":")).encode()).hexdigest()
    return {"account_key": account_key, "profile_path": profile,
            "chrome_app_id": entry["chrome_app_id"],
            "install_root": str(base), "backend_commit": entry["backend_commit"],
            "plugin_id": entry["plugin_id"], "route_receipt": receipt}


def verify_backend(route: dict | None) -> None:
    if route is None:
        return
    root = Path(__file__).resolve().parents[1]
    git = ["git", "-C", str(root)]
    try:
        head = subprocess.run([*git, "rev-parse", "--verify", "HEAD^{commit}"],
                              capture_output=True, text=True, check=True, timeout=10).stdout.strip()
        if head != route["backend_commit"]:
            raise ValueError("The running backend differs from the verified account route")
        subprocess.run([*git, "diff", "--quiet", "HEAD", "--", "integration",
                        "astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/succession"],
                       capture_output=True, check=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError("The running backend checkout could not be verified") from exc


def verify_saved_binding(cfg: dict, route: dict | None) -> bool:
    """Never allow a bound account to silently adopt legacy run state."""
    if route is None:
        if cfg.get("account_key"):
            raise ValueError("An account-bound run cannot use the legacy default route")
        return True
    for key, cfg_key in (("account_key", "account_key"),
                         ("profile_path", "chrome_profile_path"),
                         ("chrome_app_id", "chrome_app_id"),
                         ("install_root", "install_root"),
                         ("backend_commit", "route_backend_commit"),
                         ("plugin_id", "route_plugin_id"),
                         ("route_receipt", "route_receipt")):
        if cfg.get(cfg_key) != route[key]:
            raise ValueError("Saved account route unverified; preserve the run and hold")
    return True


def bound_config_fields(route: dict) -> dict:
    return {"account_key": route["account_key"],
            "chrome_profile_path": route["profile_path"],
            "chrome_app_id": route["chrome_app_id"],
            "install_root": route["install_root"],
            "route_backend_commit": route["backend_commit"],
            "route_plugin_id": route["plugin_id"],
            "route_receipt": route["route_receipt"]}
