# ADR 0002 — L02 route contract and G2 installation handoff

**Status:** L02 implementation candidate, offline checks only. No installed
Windows launcher, private plugin, or real signed-in Chrome profile was changed
by this leaf.

## Opt-in route model

The existing Python controller remains in use; its installed native state
root remains `<native-install>/Requests`, `Runs/<run-id>` and `Locks`.

At the installation step **after A2-G1**:

1. Positively verify the account's signed-in Chrome profile, private
   plugin/binding and exact backend commit and native root. Do not infer
   account identity from a Chrome profile number alone.
2. In the *private native installation root* create `account_routes.json`
   containing two separate account records matching this schema:

```json
{
  "schema": 1,
  "accounts": {
    "shoco": {
      "install_root": "VERIFIED_ABSOLUTE_NATIVE_INSTALL_ROOT",
      "profile_path": "VERIFIED_ABSOLUTE_CHROME_PROFILE_PATH",
      "chrome_app_id": "OBSERVED_CHROME_WINDOW_APP_USER_MODEL_ID",
      "plugin_id": "VERIFIED_PRIVATE_PLUGIN_ID",
      "backend_commit": "VERIFIED_40_CHARACTER_GIT_SHA"
    },
    "james-student": {
      "install_root": "VERIFIED_ABSOLUTE_NATIVE_INSTALL_ROOT",
      "profile_path": "VERIFIED_ABSOLUTE_CHROME_PROFILE_PATH",
      "chrome_app_id": "OBSERVED_CHROME_WINDOW_APP_USER_MODEL_ID",
      "plugin_id": "VERIFIED_PRIVATE_PLUGIN_ID",
      "backend_commit": "VERIFIED_40_CHARACTER_GIT_SHA"
    }
  }
}
```

   These are placeholders. Do not store account credentials, owner-input
   bodies, cookies or tokens in the route file or GitHub.
3. Adapt the existing wrapper's verified account-specific paths to call
   the pinned new backend with `--install-root` and
   `--account-key shoco` or `--account-key james-student`. Preserve
   its former compatible wrapper for rollback.
4. Only **after** the two records are verified, add the
   `account-routing-required` marker in that native root. From this
   point any missing/unknown account route holds before browser activity.
   Do not enable this marker for a live installation until its available
   old-run compatibility and paused actions have been audited.
5. Run no-Send account/profile/root verification, including wrong-account,
   wrong-profile, draft/duplicate-view and missing-login negative cases.
   Confirm the exact install backend/plugins in both ChatGPT accounts.
   A mocked UIA pass is not an authenticated acceptance pass.

The installed wrapper chooses the account key; the user does not need to
supply it. Once bound, controller subprocess UIA invocations explicitly pass
the configured Chrome profile instead of inheriting an arbitrary ambient one.

Set each `chrome_app_id` from a normal Chrome window already verified to use
that account and profile. The native read uses the window handle and
`System.AppUserModel.ID`. Use the existing no-Send setup to confirm the
profile path and signed-in ChatGPT account on the same window before pinning
the ID. Each account must have a distinct profile, window ID and private
plugin. The adapter checks the ID on newly opened and existing windows.
[Chrome profile taskbar identity](https://chromium.googlesource.com/chromium/src.git/%2Bshow/b855dc7a9addbed2a8bc023ae53c2530cfdb9bdd/docs/windows_shortcut_and_taskbar_handling.md)
· [Windows window property API](https://learn.microsoft.com/en-us/windows/desktop/api/shellapi/nf-shellapi-shgetpropertystoreforwindow).

The wrapper must point at the exact Git checkout named by `backend_commit`.
The launcher and controller verify the running checkout's HEAD and tracked
backend source with the local Windows Git executable before browser effects.
Use the implementation commit as the installation pin. The review and
evidence commits can advance separately on the working branch.

## Compatibility

Existing pre-opt-in 0.4.3 installations retain the legacy route until
an account marker is deliberately installed. A legacy run without
account-binding fields is **not** implicitly adopted by a bound account:
the launcher and direct controller CLI hold rather than resetting run ID,
chat count, cap, pending action or pause state.

The selected account, native root, plugin identity, backend revision and
profile are recorded as a non-secret, SHA-256 route receipt in new private
run configuration. A modified or different route cannot restart a bound
run without positive verification. It is a route fingerprint, **not**
a cryptographic guarantee that a browser is signed into a particular
ChatGPT account.

## L02 test boundary and next work

[Raw L02 offline results](../../../evidence/astra-adr-0002-20261120/implementation/L02_20261120/L02_RESULT.md)
cover R01–R04 at mock boundaries, original integration tests and the
119-reference offline kit. A2-G1 still requires L03–L05 and their tests.
A2-G2 is where the route is actually installed and independently verified
against both real signed-in account environments. No Shoko phone success,
worker Send or resumed ordinary-project run is implied here.
