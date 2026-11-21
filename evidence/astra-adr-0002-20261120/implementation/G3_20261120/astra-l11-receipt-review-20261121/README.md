# Astra — Chat Succession L11 receipt review

Review date: **November 21, 2026**. This is an offline, synthetic-only proposal,
not a deployment or a live acceptance result.

## Contents

- `REVIEW.md` — two prioritized changes, evidence assessment, recovery rules, and
  exact observations still needed on Windows.
- `proposal.patch` — unified diff against the supplied bundle checkout.
- `candidate/` — the **complete focused snapshot**, with the proposal and tests
  already applied. Do not apply the patch to this directory again.
- `TEST_REPORT.md` — actual results and explicit limits.
- `evidence/` — test logs, synthetic DOM readbacks, source hashes, and patch verification.
- `input/` — unchanged supplied bundle and outer request, for reproducibility.
- `SHA256SUMS` — hashes of every other file in this package.

The supplied bundle head is `5f1399a12e09304c76e0a48bce986440a1016782`.
Its README identifies the upstream source as
`36b17092aa5fef09b5ac3747c03e5661be23559c`; that upstream commit object is not
in this focused bundle. No remote repository, account, installed route, or
private run state was accessed or modified.

## Run the portable tests

From `candidate/`:

```sh
python -B -X utf8 -m unittest discover -s integration/tests
```

The eight added Python cases can also be run alone:

```sh
python -B -X utf8 -m unittest discover -s integration/tests -p test_l11_receipt_safety.py -v
```

For the reference tests, change to
`candidate/astra/2026-11-17/unpacked/chat_succession_test_kit_20261117/` and run:

```sh
python -B -X utf8 -m unittest discover -s tests
```

These use synthetic state, mocked native calls, and disposable local Git
fixtures, not a live chat.

## DOM tests

The published loopback HTML entry point remains
`/integration/tests/test_chrome_user_message.html`; it now reports **22** checks.
Serve `candidate/` on loopback and open that path in a disposable browser profile.
No extension installation is required: the supplied fixture stubs the manifest.

An optional runner uses an **already installed** Playwright Python package and
Chromium/Chrome; it never downloads a browser. From `candidate/`:

```sh
python -B integration/tests/run_chrome_fixture.py --chrome /path/to/chromium --report dom-results.json
```

This sandbox disallows browser navigation, so the recorded DOM run instead used:

```sh
python -B integration/tests/run_chrome_fixture.py --chrome /usr/lib/chromium/chromium --mock-route --container-flags --report dom-results.json
```

`--mock-route` explicitly supplies location/history doubles on `about:blank`.
It tests real DOM layout, text extraction, and mutation observation, **not real
address-bar navigation or extension injection**. `--container-flags` is only
for a restricted disposable Linux test renderer, never an existing user profile.

## Windows-only synthetic tests — not run here

From `candidate/`, in Windows PowerShell with its normal module path:

```powershell
Get-ChildItem .\integration\tests\test_*.ps1 | Sort-Object Name | ForEach-Object {
    & powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $_.FullName
    if ($LASTEXITCODE -ne 0) { throw "Synthetic suite failed: $($_.Name)" }
}
```

This includes the six supplied native suites and the new
`test_a2_l11_receipts.ps1`. The new suite extracts the adapter's actual functions
and Reconcile block via its AST; all UIA targets are synthetic. It does not
execute the adapter entry point or acquire a browser window. Passing these
tests is still required before adopting the PowerShell change.

## Apply to a clean copy instead

From this package root:

```sh
git clone -b astra/l11-test-review input/chat-successor.bundle replay
git -C replay apply --check ../proposal.patch
git -C replay apply ../proposal.patch
```

This is a local clone only. See `evidence/patch-verification.txt` for the checked
round trip. Do not repin an uncertain installed run to this candidate. Keep any
possibly submitted action read-only until the existing controller can confirm
its exact posted text, saved destination, and required preceding reply.
