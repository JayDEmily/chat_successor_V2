I’ll inspect the archive and compare the intended workflow with the live-project evidence, then produce a gated implementation plan focused on generic entry into the methodology—not a rowing-specific patch.The baseline tests pass again, but they don’t cover the missing transition: repeating a launch returns the hold, and the existing resume command restarts observation without giving the worker a new instruction. The code also treats a changed branch as a new run. I’m shaping the plan around those gaps while leaving project-specific decisions to the reasoning model.The plan now has five implementation leaves and three gates. It keeps project-state reasoning in the model and limits the new mechanics to run selection, scoped owner-input delivery, and verified checkpoint-branch changes. It also includes the whitespace finding, explicit evidence limits, and regression cases beyond Rowing.**[Download the implementation plan (.md)](sandbox:/mnt/data/Chat_Succession_Generic_Entry_Plan_2026-11-19.md)**

The key finding is a missing **re-entry path**: resuming the controller restarts observation but does not itself give an idle, blocked worker a new instruction. Changing branches can also create a separate run instead of continuing the existing one.

The plan has **five leaves and three gates**, covering:
- State-aware entry into the methodology, without hard-coding project workflows.
- Contextual approval delivered to the verified existing worker.
- Authorized checkpoint-branch changes without resetting the run.
- Preservation of the existing controller, three statuses and duplicate-Send protections.

I independently reran the **35 integration tests and 119 reference tests**; all passed. Additional probes reproduced the gaps. The plan distinguishes those results from live behavior still requiring verification and addresses the whitespace finding without attributing an unproven cause.

[Download the verification evidence and reproducible probes](sandbox:/mnt/data/Chat_Succession_Review_Evidence_2026-11-19.zip)