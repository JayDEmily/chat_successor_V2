# ADR 0002 complete transcript verification candidate

**Offline checks pass. Independent A2-G1 decision pending.** 20 November 2026 AEDT.

Source `0b6bfa3e935e713fe2f36afd8da79c2befab9a42`, tree `668194fff116591bb88958276994f32025f24caf`, direct parent `0ac9fe6a0ee7575894dad0eaf8a30997a811fcd2`. The [review of c605c5f](../independent-c605c5f/REPORT.md) verified the literal-body correction and held S01, S05, S06 and O04 because a newer article could be omitted.

The adapter now requires a single active transcript region, enumerates its top-level conversation articles in order, and requires one verified role heading per article. An unverified article invalidates the read instead of allowing an older body or assistant status to control the run. An incomplete streaming transcript waits. The native test rejects older acknowledgements with a trailing unverified article, holds the older assistant status and retains the prior literal-label and exact-body controls. [Native action and transcript test](native-dispatch.log)

- Windows CPython 3.13.15 integration 113/113 and Ubuntu CPython 3.14.4 integration 113/113. Both exited 0 with zero skips, failures or errors. [Windows output](windows-integration.log) · [Ubuntu output](ubuntu-integration.log)
- All three Windows PowerShell helper scripts passed. [Native action and transcript](native-dispatch.log) · [View/profile helpers](native-view-profile.log) · [Legacy view comparisons](native-legacy-view.log)
- The option-free reference kit and plugin source are unchanged by Git diff. The preceding pin's independent review recorded 119/119 on both hosts. [Prior reference evidence](../independent-c605c5f/REPORT.md)

The strict A2-G1 commission applies to this pin. Installed Chrome hierarchy, profile and no-Send preflight remain A2-G2 work. A2-G2–G6 are NOT_RUN.
