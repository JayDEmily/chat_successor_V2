# Governance review — public MCP-native branch

**Reviewed:** public baseline `820aa20c6643c0ed30177459a685a4a6ee56de79`, 22 November 2026. No nested AGENTS or override files found in the tracked baseline. The review covers repository governance and active entry/operating instructions, not an audit of every historical fixture or every external installed configuration.

## OpenAI guidance

- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md): Codex discovers applicable global/repository/directory instruction files in order. Keep root instructions durable and local instructions scoped.
- [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans): use a linked living plan for complex work, independently verifiable milestones, progress, discoveries, decision log and retrospective. The recipe is archived; its planning convention is still useful, not a current model/API guarantee.
- [Iterating development workflows](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex): AGENTS and roadmap ownership should be distinct; additional GOALS/PROMPTS/harness files are optional, not mandatory. No additional duplicate governing file is justified here.

The repository's explicit precedence is in [AGENTS.md](../AGENTS.md). This is an adapted project convention, not a claim that a normal ChatGPT thread automatically loads Codex files.

## Conflict and ambiguity register

| Baseline source | Finding | Resolution on new branch |
| --- | --- | --- |
| AGENTS.md | Existing approach/Chrome reuse and named old plan conflicted with the owner's new direction; authority ordering and historic evidence status implicit. | Root instructions require applicable owner scope, accepted ADR, plan, progress, assignment; no extension dependency or legacy advancement. |
| ADR 0001 | Generic re-entry/invariants still relevant, but old UI implementation and trailers alone do not establish a new MCP identity contract. | Retain compatible requirements; decide protocol through M02; no silent migration. |
| ADR 0002 | Requires existing Windows/Chrome controller and prior gate order, with broad bounded installation authority. | Preserve historical text; ADR 0003 expressly supersedes conflicting mechanisms/sequencing only for this branch. No transfer of install/Send authority. |
| PROJECT_MANAGEMENT.md | Hard-coded legacy branch, L12 next and old native UI qualification steps. | Rename/replace as root PLANS.md; retain exact old plan at pinned public revision. New milestone order and explicit acceptance. |
| PROGRESS.md | Top-level active L12 pointer and historic next instructions could redirect new workers. | New current checkpoint; historical entries remain as historical observations, not active tasks. |
| README.md | Existing Chrome/mobile launcher examples read as current new-branch instructions. | New active orientation and explicit legacy-only section. |
| docs/PROJECT_INSTRUCTIONS.md | Uninstalled draft names the private repository and original launch workflow. | Label historical, not active/installed; do not copy into new Project settings. |
| plugins/chat-succession/skills/start-chat-succession/SKILL.md / agents/openai.yaml | Legacy launcher procedure and explicit plugin invocation; new development is not ready for that entry path. | Source-only applicability warning in skill; YAML unchanged; installed plugin untouched. |
| integration/README.md | Chrome commands and operator procedures could be mistaken for development assignments. | Mark legacy operational reference; no runtime invocation on the MCP branch. |
| docs/astra-succession/README.md, finish-chat-succession.md and earlier leaves/specs/plans | Earlier trials contain their own ordering, quotas and next steps; historical references to old plan would break after rename. | Mark old plan as historical and pin references. Older trial limits/assignments do not direct the new branch. |
| Imported Astra evidence and historical reviews/fixture instructions | Different gate namespaces, permissions and candidate revisions. | Evidence only; preserve prior artefacts; no automatic gate carry-forward or transfer of work authority. |

Additional distinctions: owner standing work authority is not blanket permission for production or live cross-project actions; a Git record can be durable without being true; acceptance requires direct evidence and independent reviewer role. An exact current-model name is not a substitute for reviewer independence. Legacy held runs and other repositories are not migration targets.

## Verification boundary

This change is documentation only. Verify diff whitespace, active local document links and exact public branch/candidate readback. No application code, executable test behavior, runtime, installed plugin, credential, service, tunnel or live conversation changes are within this governance assignment. M01 is the next investigation, not an implementation or release gate.
