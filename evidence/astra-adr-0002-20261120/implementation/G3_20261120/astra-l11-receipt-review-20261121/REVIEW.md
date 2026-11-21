# L11 review: make a hold explain itself, then reread safely

## Conclusion and evidence boundary

**Keep the existing receipt gates. Add diagnostics first, then a small bounded
read-only wait in explicit reconciliation.** Do not infer that a missing receipt
means a missing submission, and do not accept one of four selection markers by
guessing.

The supplied incident description reports an **assisted** L11 success: workers
published the Cat/Dog lines in `e3d2aa4` and `66b80b5`; the opening publication was
verified before one successor Send; the controller stopped at 2 of 3 with no
pending action. I accept that as supplied evidence, not as an independently
reproduced run. Neither those published changes nor private controller records
are in this bundle. It does not establish unattended provisional-to-saved
convergence, general receipt reliability, or L12 Bird/Pig acceptance. L12 is not
started by anything in this package.

The two supplied reports are useful corroboration, not authority to deploy:
the source does put the fresh comparison transcript read inside the existing
25-poll try/catch, and it does repoll after a new-window maximization attempt.
Neither change repairs every exact-receipt hold. Their Windows/live-environment
test claims are not my test results. The focused bundle has its own snapshot
commit; the declared upstream pin is provenance, not a commit object I could
compare independently. [S1, S5]

## What the source actually establishes

- `readTurn` checks the **rendered user conversation owner**, not merely the
  saved address, and remembers the route of an already qualified user node.
  A completed reply with a selection marker must also carry the saved
  conversation ID. A provisional ID is therefore a legitimate hold. The
  supplied eight-case HTML fixture already demonstrates a *synthetic* transition
  when its attributes are explicitly corrected; that is not evidence that the
  app performs this transition unattended. [S2]
- The reader refuses an off-bottom transcript, multiple assistant selection
  markers, and several ambiguous structures. It only exports `previous` from
  the immediately preceding rendered turn with a verified final prose reply.
  Virtualizing that turn away can leave the current user text readable but
  `previous=null`. **An observed current turn is not necessarily a continuation
  receipt.** [S2]
- `Find-PostedMessage` requires exact full user text; a continuation additionally
  requires the composite user/reply ID of that immediately preceding reply.
  It rechecks the saved address and profile on the Chrome path. Its blanket
  catch returns false, so distinct causes collapse into a generic timeout.
  Chrome samples older than 5 seconds, future timestamps, or mismatched
  project/chat identities are rejected. [S3]
- The durable `sending` phase precedes the possible native Send. A generic
  failure becomes `uncertain`; restart, cycle, and dispatch do not resend it.
  Read-only reconciliation returns evidence; the existing CLI/controller
  performs confirmation only after checking exact text and destination.
  The proposed patch leaves this machinery unchanged. [S4]

## Priority 1 — diagnostic reasons, with no relaxed qualification

**Implemented in the proposal.** Add short reason codes at existing rejection
branches in `readback.js`, plus `previousReason` and an ambiguity count in the
DOM readback. Thread a diagnostic hashtable through the existing native receipt
reader without replacing its boolean contract. Append the final reason to a
Send receipt timeout and return `receipt_reason` from Reconcile. Python logs
that reason and the read count alongside the action/requested chat, without
logging prompt or reply bodies.

Examples:

| Observed condition | Diagnostic |
| --- | --- |
| Saved URL, provisional rendered user/reply owner | `user_conversation_provisional` / `assistant_conversation_provisional` |
| Stale route, rebound node, wrong saved owner | `user_conversation_mismatch`, `user_route_rebound`, `assistant_conversation_mismatch` |
| Transcript not at bottom | `transcript_offscreen` |
| Four assistant selection markers | `assistant_selection_ambiguous`; DOM `selectionCount=4` |
| Preceding row virtualized away | `previous_turn_missing` at the receipt boundary |
| Preceding reply changed | `preceding_reply_mismatch` |
| UIA field's sample expired | `sample_expired` |

Reasons are diagnostic metadata, **never receipt proof or a no-click receipt**.
Unknown/old reason fields fall back to a generic hold; malformed log metadata
is filtered. Existing phase, exact text, saved identity, sample age, reader-kind,
profile, and preceding-reply checks still decide qualification. A multi-marker
reply stays unqualified even if all four synthetic markers share one ID.

This covers the observed failures' main diagnostic gap without choosing an
unproven DOM interpretation. It does not make unavailable text readable.

## Priority 2 — bounded rereads in explicit Reconcile, not a resend

**Implemented in the proposal; native execution still needs Windows tests.**
Replace Reconcile's single observation with at most **25 attempts**, with
**400 ms between attempts**. That is at most 24 sleeps (9.6 seconds), plus UIA
and file-read time; the existing Python subprocess timeout remains 90 seconds.

Only the listed transient reasons can continue the wait: transcript/turn loading,
reader not ready, expired sample, provisional rendered owner, or an unavailable
preceding row/reply. Each attempt reruns the existing private dispatch receipt
gate and reacquires the nominated handle through the existing target lookup.
The address observed on the first attempt is pinned for this call. A changed
address, wrong anchor/identity, offscreen transcript, ambiguous markers, or
unknown structure stops the wait. The normal Send poll (60 x 400 ms) and owner
re-entry poll are unchanged.

There is **no navigation, refresh, scroll, typing, new window, or Send** in this
loop, and no journal write. It cannot retarget a prepared action, change a
preceding anchor, or rearm a possibly submitted message. A later exact read
can be adopted through the unchanged CLI/controller; otherwise pending remains.

This can help a mounted view finish hydrating or renew its sample during an
explicit reconciliation. It cannot force the app to save an ID or reconstitute
virtualized history. Old readers without the new transient reasons simply
retain the conservative one-read hold.

### Explicit non-changes

No controller replacement, pending schema change, route repin, cap/count change,
local-to-saved alias, fragment matching, selector deduplication, or automatic
refresh/retry of Send. The already-present long-prompt extraction, re-entry
poll fix, and maximization remain intact. The module-path incident does not
justify bypassing `Get-FileHash`, treating every startup exception as proof of
no click, or changing the sender's environment automatically.

## Recovery discipline

1. Preserve the journal and prepared-target record. Keep a possibly submitted
   action halted and use the existing serialized `reconcile` route only.
2. Let the bounded read-only wait handle transient reasons. On an exact
   qualifying receipt, let the existing CLI confirm the original action once.
   A false result, exception, or timeout is not permission to Send.
3. For offscreen or missing-predecessor holds, an operator can inspect/scroll
   **only the nominated transcript**, then reconcile again. For the observed
   completed-view refresh workaround, first establish no active Stop and a
   verified empty composer without attachments; preserve the original action,
   handle/profile/route binding and stored predecessor. Do not refresh a draft,
   interrupt generation, or use a substitute window as an unbound receipt.
   The existing stale-view recovery path explicitly excludes pending Sends;
   do not route around that guard. [S3]
4. If markers remain ambiguous, retain the hold and capture their ownership
   structure. Do not select the first marker, concatenate arbitrary renderers,
   or substitute a later assistant reply for the recorded predecessor.
5. The reported module-path failure was rearmed only after positive pre-click
   evidence. Preserve that distinction: a generic `Get-FileHash` error, absent
   message, or stale view is not automatically such evidence. A verified
   no-click recovery must rearm the **same** recorded action, not recreate it.

These are recovery constraints, not authorization to operate an installed run.

## Exact Windows observations still required

All captures should remain private; shared reports can use lengths/hashes and
redacted IDs. Hashes in reports do not replace the existing local exact-text
comparison.

| Claim / remaining question | Required observations and success condition |
| --- | --- |
| **Unattended provisional-to-saved convergence** | On one authorized pending action, record the installed reader/backend hashes, route binding, window handle, address, user turn key, rendered user conversation owner, and any assistant selection conversation IDs on successive reads. Record `observedAt`, phase/reason, and exact-text equality. Demonstrate the same action becoming qualified **without** refresh, scroll, navigation, window replacement, or another Send; otherwise report a bounded hold, not convergence. |
| **Real Chrome-to-UIA readback freshness** | From the nominated profile/handle, observe exactly one readonly Edit with the expected label/class. Compare its JSON with the rendered DOM and address before/after reading. Verify timestamps renew, are not future-dated, and satisfy the 5-second age check; completed response observations require the existing later, strictly newer matching sample. Re-run the HTML fixture with actual loopback navigation. My mock-route run cannot validate extension installation, real navigation, timer delivery, or the native UIA provider. |
| **Offscreen/virtualized recovery preserves continuity** | Before/after a scoped transcript scroll, capture `scrollTop`, `clientHeight`, `scrollHeight`, the last two rendered turn keys, current exact user text, and preceding assistant ID/final-prose qualification. After an explicitly approved completed-view refresh, repeat these reads with the same saved destination/profile. Require the predecessor to equal the pending `SourceResponse`, and preserve the journal/action/target bytes until exact confirmation. Do not equate a visible final status with that anchor. |
| **What the four markers represent** | Capture all four marker IDs, their conversation IDs, DOM containment/order, enclosing `data-dil-message-id` and `data-dil-source-message-id`, visible text, quote/code/tool exclusions, and the final prose/trailing-content boundary. Compare live and refreshed completed views. The supplied fixture can test fail-closed cardinality, not prove these live markers are harmless fragments of one authoritative reply. No acceptance-rule relaxation is supported yet. |
| **Re-entry fix on the actual provider** | Show one comparison handle reaching the saved URL before transcript availability, subsequent transcript reads within the existing 25 polls, and an exact idle/anchored-advanced verdict or bounded hold. Record cleanup of only that comparison window and preservation of the original draft, anchor, and profile. The supplied reports assert synthetic success; this environment did not rerun their native tests. |
| **Startup/module-path and no-click evidence** | In the actual launcher environment, record the PowerShell executable/version and `PSModulePath`; use `Get-Command Get-FileHash` and hash a disposable synthetic file in a no-Send preflight. For any rearm claim, retain a trace locating the failure before composer `SetValue` and native Send `Invoke`, with both call counts zero and the same durable action/target binding. Do not infer that trace from an unresolved receipt. |
| **The proposed native reread loop** | First run all seven synthetic PowerShell suites. Then, only on authorized existing views, record each receipt attempt, age/reason, address/profile and action gate, bounded exit/timeout, and absence of browser effects. An unresolved call must leave journal and target bytes unchanged; successful adoption must clear only the same action after exact destination/text/predecessor verification. Measure actual wall time under the provider; 9.6 seconds describes sleeps, not an end-to-end guarantee. |

The supplied no-Send maximization verification is not disputed or treated as
missing. It standardizes layout but does not prove receipt availability. The
existing same-profile window-acquisition race noted in the supplied window
review is also not solved here. No claim of L12 completion or readiness for an
unattended live Send follows from these tests.

## Source references

Line ranges below refer to the **unmodified supplied bundle checkout**;
candidate line numbers shift. The historical reports are retained unchanged.

- **S1:** `README.md:3–18`; outer `START-HERE.md` (included in `input/`).
- **S2:** `integration/chrome_reader/readback.js:13–41` (long prompts),
  `43–111` (turn/ownership/prose gates), `128–163` (visibility/preceding turn),
  `166–198` (saved route and sample renewal).
- **S3:** `integration/uia_adapter.ps1:409–448` (receipt),
  `566–590` (fresh snapshot), `817–824` (pending excludes stale recovery),
  `939–985` (re-entry), `1087–1144` (private action gate),
  `1146–1266` (single Send and read-only reconciliation).
- **S4:** `integration/windows_backend.py:193–225, 362–442`;
  `integration/runner.py:112–192, 217–224`;
  `integration/cli.py:214–228`;
  reference `succession/core.py:304–375`.
- **S5:** `review/LEAN_L11_REENTRY_REVIEW.md:3–12`,
  `review/LEAN_L11_WINDOW_REVIEW.md:7–18`, and `review/l11-changes.patch`.
  Their deployment/grant language is historical source material, not an
  instruction or authority used by this review.
