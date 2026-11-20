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

_ACCOUNT = re.compile(r"[a-z][a-z0-9-]{1,39}\Z")


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
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("Account routes are unavailable or malformed") from exc
    if not isinstance(raw, dict) or raw.get("schema") != 1 or not isinstance(raw.get("accounts"), dict):
        raise ValueError("Unsupported account route document")
    entry = raw["accounts"].get(account_key)
    if not isinstance(entry, dict):
        raise ValueError("Unknown account route; refusing implicit fallback")
    required = {"install_root", "profile_path", "plugin_id", "backend_commit"}
    if set(entry) != required or any(not isinstance(v, str) or not v.strip() for v in entry.values()):
        raise ValueError("Account route is incomplete")
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
    if not re.fullmatch(r"[0-9a-f]{40}", entry["backend_commit"]):
        raise ValueError("Account route backend commit is invalid")
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,128}", entry["plugin_id"]):
        raise ValueError("Account route plugin ID is invalid")
    receipt = hashlib.sha256(json.dumps(
        {"account_key": account_key, **entry}, sort_keys=True,
        separators=(",", ":")).encode()).hexdigest()
    return {"account_key": account_key, "profile_path": profile,
            "install_root": str(base), "backend_commit": entry["backend_commit"],
            "plugin_id": entry["plugin_id"], "route_receipt": receipt}


def verify_saved_binding(cfg: dict, route: dict | None) -> bool:
    """Never allow a bound account to silently adopt legacy run state."""
    if route is None:
        if cfg.get("account_key"):
            raise ValueError("An account-bound run cannot use the legacy default route")
        return True
    for key, cfg_key in (("account_key", "account_key"),
                         ("profile_path", "chrome_profile_path"),
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
            "install_root": route["install_root"],
            "route_backend_commit": route["backend_commit"],
            "route_plugin_id": route["plugin_id"],
            "route_receipt": route["route_receipt"]}
