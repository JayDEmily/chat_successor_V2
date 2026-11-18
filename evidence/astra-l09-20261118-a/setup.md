# L09 — scoped lost-acknowledgement fault-hook preparation

Repository: JayDEmily/chat_successor
Branch: work/astra-succession-implementation-20261118
Entry: L01–L08 live outcomes published, L09 live case NOT_RUN.

## Exact test-only seam

The existing WindowsUIA and PowerShell UIA adapter remain the single Send actor. Only a deliberately supplied environment variable on the L09 controller CLI process changes behaviour:

- `ASTRA_L09_FAULT=before_click`: after the controller has saved pending phase `sending`, WindowsUIA validates the saved pending action and prepared target, then throws **before invoking UIA Send**. This is test-injection evidence of no click, not a live lost acknowledgement.
- `ASTRA_L09_FAULT=after_click`: WindowsUIA passes `-L09Fault after_click` to the existing PowerShell Send operation. The adapter executes its **one** Enter/Send, then deliberately throws before observing/returning the posted message. The controller records uncertainty and must reconcile read-only; do not automatically retry.
- Unset `ASTRA_L09_FAULT` for normal operation. The reference Controller state machine, statuses, pending transition and count logic remain unchanged.

The current CLI already supports `reconcile` for positive posted-message readback. The reference Controller's `confirm_not_sent` explicitly rearms only after a reasoned positive no-send observation. The before-click hook supplies that positive no-invocation evidence; no automatic rearm is implemented.

## Verification performed

- `python3 -m unittest discover -s integration/tests -v`: **22/22 PASS** including four focused L09 fault-hook tests.
- Imported Astra reference `python3 run_offline.py --out /tmp/chat-successor-l09-offline-20261118`: **119/119 PASS**.
- Windows PowerShell parser on `integration/uia_adapter.ps1`: **zero parser errors**.
- These are offline tests and static syntax checks. **No live browser Send, ChatGPT conversation creation, controller activation or L09 recovery observation occurred in this preparation.**

## Next authorised L09 live actions

Seed a fresh L09 test-only fixture and private state, without overwriting previous run states. Exercise the published L09 sequence using the existing single controller:

1. A saved `sending` state followed by `before_click` injection: observe hold and no Send; restart; explicitly rearm only with positive before-click evidence.
2. A successor `after_click` fault: restart and reconcile exact posted message and distinct saved Project chat ID once; unresolved delivery stays held.
3. A same-chat continuation `after_click` fault: restart and reconcile exact continuation in the same saved ID, without double-posting or incrementing chat count.

Record actual UI evidence, controller state and any interventions. Keep cumulative L09 result `NOT_RUN` until the real live variants are independently observed. Do not launch a second controller or Send actor.
