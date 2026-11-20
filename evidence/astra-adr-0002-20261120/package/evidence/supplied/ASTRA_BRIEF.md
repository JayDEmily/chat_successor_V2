# Brief for Astra

Propose a new ADR for Chat Succession and return an ordered set of implementation leaves and acceptance gates. Start from the original ADR, the 0.4.3 source, the prior fixture runs, and the exact pause checkpoint. Use the verified behavior as a baseline and explain which parts of the current Windows, Chrome, and Desktop Commander path should be kept or simplified. [Original ADR](source/docs/adr/0001-generic-entry-and-re-entry.md) · [Pause evidence](evidence/pause-2026-11-20/LIVE_PAUSE.md)

## Owner workflow

- The owner creates the ChatGPT Project folder and the GitHub repository for each project before starting a run. The project provides its existing work record and publication rules. The owner identifies the exact Project, repository, and published branch when the context leaves them ambiguous.
- James Student and Shoco belong to the same owner. Both have authorised GitHub and PC access. Each private plugin belongs to its account and must route to the matching signed-in Chrome profile. The account switch is part of release and recovery verification.
- The owner can select Chat Succession from an iPhone Project chat to start a new run. The request chat stays outside the desktop worker count. Include both a fresh start and a scoped approval delivered once to the already saved worker, then verify the published Git receipt before a successor starts.
- An owner pause must survive restart and block new controller Sends. Resume the same saved worker and cap. Test a closed or displaced view, a genuinely stale view with a newer completed response, and a pending or uncertain Send. Reconcile the existing action before any retry.

## Acceptance design

Use Cat and Dog and Bird and Pig, or comparably small fixtures, for repeatable acceptance. Include one ordinary finish and one run that reaches its worker cap with an eligible next assignment. Keep each run's worker cap separate from the number of concurrently running instances.

Start with two overlapping runs and a pause/restart in one while the other continues. Then increase concurrency in steps on the same PC until measured latency, resource use, or reliability shows the practical limit. Define window and run identity, the shared contention points, and the evidence for safe isolation and exactly-once handoffs. The design should support more runs as capacity allows.

For each leaf and gate, name the prerequisite, expected outcome, exact checks and evidence, and what happens on a hold or failed check. Separate earlier verified results from acceptance still needed on Shoco 0.4.3. Finish with the simplest operator procedure for starting, pausing, resuming, and checking a run.
