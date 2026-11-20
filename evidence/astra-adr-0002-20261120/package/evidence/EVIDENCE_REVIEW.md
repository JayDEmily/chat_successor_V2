# Evidence review and pause disposition

**Review date: 20 November 2026.** Source IDs resolve in the [source index](SOURCE_INDEX.md).

## Verdict

The evidence supports retaining the existing architecture and narrowing the next increment to explicit account routing, existing-action identity, safe view recovery, observable pause/re-entry, and measured multi-run acceptance. It does **not** support declaring Shoco 0.4.3 fully accepted, automatic stale reload proven, or more than two concurrent runs qualified.

This delivery proposes work; it does not deploy it. Original source and all existing repositories remain unchanged. No live environment was accessed.

## Evidence labels

- **VERIFIED_LOCAL:** directly reproduced from supplied bytes, executable offline checks or bundled Git objects in this sandbox.
- **STATIC_FINDING:** behavior/limitation visible in the supplied implementation; where possible characterized with mocked boundaries.
- **ARCHIVED_LIVE:** earlier live observation reported in supplied records, sometimes corroborated by Git objects. Not a fresh live rerun.
- **UNVERIFIED:** a claim or desired result not established by the supplied evidence.
- **PROPOSED:** a design or acceptance requirement in ADR 0002; not an implemented capability.

Checksums establish integrity against the supplied manifest. Git fsck establishes local object consistency. Neither certifies who wrote a narrative, the current remote state, or a real browser's exactly-once behavior.

## 1. Exact paused pair — do not bootstrap replacements

Pause requested **20 November 2026, 08:49:10 Sydney (UTC+11)**, equivalent to **19 November 2026, 21:49:10 UTC**. The saved snapshot was read at **20 November 2026, 08:55:18 Sydney**. It reports both pause markers present, both controllers halted with `Operator pause requested`, zero trial-controller processes, and no pending Send in either run. These are **ARCHIVED_LIVE**, not an observation of the PC now. [S04/S05]

| Field | Rowing | SolidWorks |
| --- | --- | --- |
| Run | `b401f984a1927f6979067d07` | `271867d56ebd3443a4b40fa6` |
| Project | Project A Test | Project B Test |
| Repository | `JayDEmily/rowing2026` | `JayDEmily/sw_v1` |
| Saved worker labels / current | `ROWING-1`, `ROWING-2` / `ROWING-2` | `SOLIDWORKS-1` / `SOLIDWORKS-1` |
| Count / immutable cap | 2 / 2 | 1 / 2 |
| Entry branch | `work/bio2-golden-yaml-24-integrated-workstation-20261119` | `work/sw2021-full-source-library-20261119` |
| Effective branch in journal | `work/chat-succession-audit-rowing-20261119` | Still the entry branch |
| Last consumed status | `TASK_COMPLETE` from the first worker; not a terminal cycle for worker two | None |
| Confirmed automatic successors | One | None |
| First captured Git receipt | `acbf989ffefed1771f9fd9d08261bdb9d2e4bce0` | `b6579ae8dc308ad4912ede85530056d53566bc8a` |
| At pause | Worker two in progress; no pending action | Completion reply/publication saved, but controller had not consumed it; no pending action |

The post-pause Rowing commit `1eadc9d8b5486aecf13b312a0d02737b3cf8a35f` is reported at **20 November 2026, 08:55:28 Sydney**, with the second worker/run and `FINISHED`, one verification line on top of `acbf989`. That commit time is later than the pause-journal readback above; it is a separate publication capture, not evidence that the journal consumed it. No terminal Rowing cycle is recorded. A pause of the controller does not cancel an already-running ChatGPT worker or revoke already-authorized publication. [S04/S05]

The Rowing and SolidWorks repositories themselves are **not** bundled. Their commit hashes, one-file diffs, run/worker matches, unchanged original refs, and post-pause publication are supported here by the supplied readback JSON and narrative only. The stable redacted worker labels cannot be independently rejoined to private saved IDs without the owner's journal. Do not present these as newly fetched GitHub findings.

**Only after an explicit owner release:** inspect the exact journals/markers and original actions first. For Rowing, verify the saved second worker's completed response and current effective-branch receipt before recording `STOP_FINISHED`; being at cap two alone is not a completed-job verdict. For SolidWorks, consume the saved first worker's completion and any verified branch locator/receipt before allowing at most one successor; only a verified second receipt with eligible remaining work warrants `STOP_CAP`. A changed remote tip, missing journal, unverified worker or uncertain action must hold. This review supplies no authorization to run either workload. [S10–S13]

## 2. Independently verified offline results

| Finding | Evidence and limitation |
| --- | --- |
| 295/295 root-manifest entries match; 296 regular files including the manifest | V01. No omitted/unlisted payloads. Original archive preserved exactly. |
| All 268 exported source files agree with the pinned Git revision | V03/V04: 10 byte-identical; 258 differ only by CRLF/LF. Do not call the whole export byte-identical to Git blobs. |
| Runtime/controller/plugin paths have no Git diff from `2c29406…` to `283e6c1…` | V04. Establishes code content agreement, not installed runtime selection. |
| All four 0.4.3 ZIP files equal exported plugin bytes | V05. Does not prove either private plugin was installed from those bytes. |
| Six bundles restore and pass fsck | V03. Main 10 refs/157 commits; Cat/Dog 3/11; Bird/Pig 3/10; four-turn story 5/7; approval 4/9; rotation 4/5. Ref equality is to supplied TSVs, not a new remote query. |
| 63 integration and 119 reference tests pass without skips | V02. Browser/Windows boundaries are simulated. Reference seeded traces are part of tests, not extra live trials. |
| 13 archived workload fixtures validate | V06. Includes D at 1/5, E at 3/5, and cap fixture at 2/3. A valid partial fixture is not a completed run. |
| All 15 A/B/F event commits contain matching worker IDs and slice counts | V03. Corroborates the published fixture chain; not independent replay of their unattended browser transport. |
| Fresh Shoco approval branch is a clean staged seed | V06: `b91b00fe75be2ca011eac1ad1cc0d668ffd8d8bf`, `codex/g2-iphone-approval-shoco-20261120`, no `NOTES.md`. This says nothing about subsequent remote changes. |

The retained Windows default-code-page failure is real evidence of a failed attempt. The later captured UTF-8 pass does not erase it. Our rerun uses UTF-8; PowerShell was unavailable and was not executed. [S16/V02]

## 3. Earlier live behavior worth carrying forward — with qualifications

| Earlier result | Evidence level / conclusion |
| --- | --- |
| Astra A/B/F: five saved workers each, four automatic successors each, terminal finish | ARCHIVED_LIVE with V03 fixture corroboration. Historical bounded G0–G4 only. Assisted initial setup remains disclosed; C was assisted, D/E interrupted, L14/30-chat exercise not run. [S08] |
| Four-turn My Cat and Dog launch from iPhone | ARCHIVED_LIVE with bundled four-commit parent chain, one `STORY.md` line each and four distinct `Chat-ID` trailers independently read. This special story reader is not the later generic three-trailer protocol. [S09/S13/V06] |
| Earlier generic Cat/Dog and Bird/Pig overlap | ARCHIVED_LIVE: separate Projects/journals/readers; 3m09s simultaneous controllers; four distinct workers in total, not four concurrent runs. Final Git artifacts corroborate the two stories. [S07/V06] |
| Bird/Pig cap-two replay | ARCHIVED_LIVE: two same-chat continuations, pause/restart, operator-assisted stale reload, then `STOP_CAP`. Bundled final `e940ee5…` leaves “Review the two published lines” eligible. Not an automatic stale-reload pass. [S06/V06] |
| Earlier James Student iPhone scoped approval | ARCHIVED_LIVE: request-chat approval to original worker once, one automatic successor, two workers and `STOP_FINISHED`; identical request replay reported no new action. Bundled `cba9880…` → `1590c45…` verifies two-line artifact and run/chat trailers. Phone channel and exact Send count still rely on the archived records. [S07/V06] |
| Branch rotation | ARCHIVED_LIVE with bundled `58eecd7…` → `ddff243…`: original run and cap retained; new authorized checkpoint verified before successor. UTF-8/observation assistance preceded completion. [S07/V06] |
| Concurrent window-creation mutex | ARCHIVED_LIVE: two near-simultaneous inspections first produced an ambiguous window; both succeeded after the scoped session mutex. This is not a >2 capacity measurement. [S07/S12] |
| Shoco route and displaced view | ARCHIVED_LIVE: wrapper routed Shoco connector to candidate and Shoko Chrome Profile 11; Rowing view restoration at 08:38:08 Sydney preserved its worker/count while SolidWorks continued. Closed historical-worker reopening and its unchanged journal were a separate no-Send probe. [S04/S06] |

The initial approval and rotation attempts on `main` / `work/checklist` entered uncertain successor holds with provisional `local-chatgpt` addresses. Later successful runs do not retroactively reconcile those original actions. Preserve their independent run records. [S07/V06]

## 4. Static findings and newly reproduced limitations

| ID | Finding | Interpretation and smallest response |
| --- | --- | --- |
| F01 | The route is supplied by wrapper/environment; `load_config` accepts no account/profile binding fields. Matching runs uses Project ID and normalized repo. P07 reproduces rejection of proposed fields. | STATIC_FINDING. Not evidence of a past misroute. Persist an owner-verified account/profile binding and validate it on start/re-entry/recovery. Keep old run IDs/journals. Do not fall through to another account when routing is unresolved. [S03/S10/S11/V07] |
| F02 | `send_once` checks persisted sending/message and target handle/source/kind, but not target `action_id`; `reconcile_readonly` likewise checks source/kind only. Some target writes contain action IDs, others do not. P08 reaches a mocked Send with a deliberately different target action ID. | VERIFIED_LOCAL characterization + STATIC_FINDING. No real wrong Send was demonstrated. Extend the existing target record/checks for every action, including continuations and recovery; an old handle is not sufficient identity. [S12/V07] |
| F03 | `inspect_state` omits the separate pause marker. P09 returns `halted: null` immediately after a marker is created but before acknowledgement. | VERIFIED_LOCAL. The marker still blocks later dispatch; this is a status/operability gap, not proof that pause is ignored. Display requested versus acknowledged pause separately. [S11/V07] |
| F04 | `ObserveReentry` can classify a worker as `advanced` because it is streaming or has a later user turn. | STATIC_FINDING. This safely avoids a duplicate controller input, but does not itself prove the specific owner approval was delivered or authorized. Report observation-only continuation separately from a verified approval receipt. [S10/S12] |
| F05 | Stale detection is elapsed-progress based (120 s) with a 300 s per-worker probe interval; both are process memory and restart resets the timers. | STATIC_FINDING. Preserve these conservative defaults; time alone must never authorize reload or Send. `refreshed` means reload invoked, not that the next response has been consumed. [S12] |
| F06 | Window discovery scans accessible Chrome top-level windows; account/profile is not a predicate in `Find-TargetWindows`. Handles can become unusable as views move or close. | STATIC_FINDING. Bind view provenance to the verified route and recheck URL/Project/chat/document; hold ambiguous views rather than guessing a tab. [S12] |
| F07 | Job/run IDs are exactly 24 lowercase alphanumerics, not an arbitrary GUID string; owner request IDs are 24–64. | VERIFIED_LOCAL P06 and captured pre-Send failures. Generate a stable valid internal job ID once; do not burden the owner with identifier formatting. [S04/S10/V07] |

P01–P05 additionally reproduce cap/finish precedence, same-chat continuation at the cap, pause blocking and count-once adoption after an uncertain restart. These are offline assertions, not fresh browser evidence.

## 5. Claims that remain unverified

1. **Shoco 0.4.3 iPhone fresh start and scoped approval:** staged only; no phone start or approval on `b91b00f…`. Earlier James Student evidence cannot satisfy this.
2. **Successful automatic stale recovery when a newer completed response truly exists:** the Shoco comparisons returned `waiting`. The later SolidWorks fresh response was not consumed before pause.
3. **Terminal closeout of the paused desktop pair:** no Rowing terminal cycle and no SolidWorks successor recorded at checkpoint.
4. **Current installed James Student release and a safe account round-trip:** private plugins are account-specific; the wrapper's retained default points to a different checkout. Verify both bindings; do not infer symmetric 0.4.3 deployment.
5. **Concurrency above two or a practical PC limit:** no such measurements are supplied. Four total saved workers in a pair is not four concurrent controllers.
6. **Cause of the fresh-composer timeout or malformed UIA JSON:** memory pressure was observed, but causation was not established. Do not prescribe global Chrome shutdown or a replacement automation stack from that observation.
7. **Whether the earlier ordinary Rowing approval reached the registered worker, or who produced its whitespace diagnostics/concurrent edits:** the supplied evidence explicitly leaves these unresolved.
8. **General unlimited “exactly once” browser delivery, complete power-loss durability, or arbitrary workload correctness:** not established. The supported pattern is single attempt, durable uncertainty, positive readback and count-once adoption; inability to reconcile is a hold, not permission to resend.

## 6. Next decision

Adopt or amend ADR 0002, then implement its small deltas in order. Run the remaining acceptance on the exact installed candidate/account combination. If any source is changed, record a new pinned candidate and release identity; a patched successor release is not proof that unchanged Shoco 0.4.3 passed. Retain all failures and interventions alongside the positive results.
