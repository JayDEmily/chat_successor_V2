# Astra ADR 0002 — independent review intake

- **Source:** Shoko Google Drive, [Astra Response — Chat Succession — 20 November 2026, 13:09 AEDT](https://drive.google.com/file/d/1IGaka15BSgbueBm7ax-_7YukPnG4AIqt/view?usp=drivesdk).
- **Google Drive object size:** 2,286,051 bytes.
- **Original returned archive SHA-256:** `8fcb94cd24b954c6f31b37a636fcb346dac1d48c1e7b647713fae664ff6a15c2`.
- **Original input archive SHA-256:** `473876c6b0fffa1f55ef68ad9da62bda0e949295808f899d502edd68ab5f3945`.
- **Reviewed GitHub source:** `283e6c17bf3359c203a362fd6593563480eeea5f`.
- **Runtime/plugin candidate baseline:** `2c29406b1c43904c5ead79064fe7856971e0aa2e`, 0.4.3.
- **Disposition:** **Received and preserved as a proposed independent review.** ADR 0002 remains pending owner decision, and no implementation or live acceptance is implied.

## Navigating the complete evidence

- [Verbatim return archive](Astra-Response-20261120-1309-AEDT.tar.gz) — original 2,286,051-byte object.
- [Package overview](package/README.md).
- [Proposed ADR 0002](package/docs/adr/0002-account-bound-resumable-runs.md) and [ordered implementation plan](package/docs/IMPLEMENTATION_PLAN.md).
- [Ten implementation leaves](package/docs/leaves/), [seven gates](package/acceptance/GATES.md), [41 case register](package/acceptance/cases.csv) and [operator quickstart](package/operator/QUICKSTART.md).
- [Independent evidence review](package/evidence/EVIDENCE_REVIEW.md), [source index](package/evidence/SOURCE_INDEX.md), [verification report](package/verification/README.md), [verification files](package/verification/).
- [Astra's original input archive](package/original/Chat-Succession-Astra-Handoff-2026-11-20.tar.gz), plus selected supplied source and history evidence.

The extracted `package/` is the complete archive content, not a rewritten interpretation. Its `MANIFEST.sha256` independently verifies **94/94** included payload files; the manifest itself is the 95th file. The outer returned archive is stored separately, leaving package integrity checks unchanged.

The review reports **63 integration and 119 reference offline tests passing**, plus 9 baseline characterisations and 13 archived fixtures. These are Astra's recorded offline outcomes, **not a new authenticated Windows/iPhone acceptance run**. No account-run was resumed, and no release was deployed as part of this GitHub intake.

The supplied package includes Windows CRLF files (including CSV and log evidence). The scoped `.gitattributes` permits ordinary Git whitespace checks without rewriting or normalising the manifest-verified bytes.
