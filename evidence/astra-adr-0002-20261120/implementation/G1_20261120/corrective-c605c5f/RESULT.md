# ADR 0002 conversation readback correction

**Offline checks pass. Independent A2-G1 decision pending.** 20 November 2026 AEDT.

Source `c605c5fafe4d3cfefe4173f04a53ebf0d1943d59`, tree `7bbf56bf60cf0006782dd6fef300a8d9b0217071`, parent `c8a3020d9c3e8bca763be31f81720fe6cfc6a6c2`. This candidate addresses the single native delimiter finding in the [independent review of 9e64211](../independent-9e64211/REPORT.md), which held S01, S05, S06 and O04.

The Windows UIA adapter reads each body within its verified accessibility article. The app's role heading establishes the speaker. Literal footer and role-label text inside the article remains part of the body. Same-chat acknowledgement requires the full exact latest user body immediately after the triggering assistant response. An unknown article or ambiguous role cannot supply a receipt. The live Chrome layout remains an A2-G2 check. [Chromium article mapping](https://chromium.googlesource.com/chromium/src/%2B/refs/heads/main/ui/accessibility/platform/ax_platform_node_win.cc#930)

The synthetic native harness supplies an actual article/heading/descendant model to the adapter functions. It tests all five former delimiter labels inside both user and assistant bodies, exact user-turn positives with browser text outside the articles, the response anchor, and unverified structure. Existing action-ID, scoped input and prose controls still pass. [Native Windows PowerShell output](native-dispatch.log)

| Check | Result |
| --- | --- |
| Windows CPython 3.13.15 integration | [113/113](windows-integration.log) |
| Ubuntu CPython 3.14.4 integration | [113/113](ubuntu-integration.log) |
| Native Windows PowerShell view and profile helpers | [PASS](native-view-profile.log) |
| Native Windows PowerShell legacy view helpers | [PASS](native-legacy-view.log) |
| Reference kit | Unchanged by Git diff. The preceding pin passed [119/119 on Windows](../corrective-9e64211/windows-reference.log) and [119/119 on Ubuntu](../corrective-9e64211/ubuntu-reference.log). |

The [strict independent review](../../../../../docs/astra-succession/adr-0002/G1_STRICT_REVIEW_COMMISSION.md) applies to the new pin. A2-G2–G6 remain NOT_RUN.
