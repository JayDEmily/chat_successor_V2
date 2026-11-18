# L06 initial setup - 18 November 2026

- Test: L06, repository-only probe rotation after the first worker response and before successor Send.
- Fixture: succession-tests/astra-l06-20261118-a, two slices, initially uncompleted (0/2).
- Seeded with unchanged imported Astra repo_fixture.py init, not a simulated ChatGPT worker.
- A minimal cycle --prepare-only test seam is added to the existing reference-controller integration: persist the prepared handover but do not launch the successor yet. A normal subsequent cycle dispatches the same pending action. No new controller or browser mechanism.
- The probe is NOT rotated at seed. It must change after actual first-worker terminal publication, through the existing rotate-probe tool, with separate Git commit before Send.
- Local test evidence of prepare-only is simulated unit testing, not a live L06 pass.
- Next action: assisted first-worker bootstrap in nominated Project, record its real saved ID and initialise a fresh L06 private controller with cap 3. First worker publishes slice 1; then staged prepare, rotate, dispatch, validate and terminal-stop observation. Do not reuse or reset L05.
