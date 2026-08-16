# Closed Doors

## Scope

This document records examined candidates that the owner deliberately leaves
unchanged. It is not an active work register.

| Date | Verdict | Candidate | Premise | Evidence | Carrying commit |
| --- | --- | --- | --- | --- | --- |
| 2026-07-31 | Keep | A recorder manifest field injected before `recorded_at=` can be absorbed by the application-record shape glob. | The behavior predates the selector work and changing it would expand the accepted scope. | Prior canonical detail in `git show a519802:docs/milestone-0082a56.md`; prior evidence in `docs/MILESTONES.md`; commits `75f16c3` and `ca2a9de` leave it unchanged. | a519802 |
| 2026-08-16 | Keep | Ansible default SSH ControlMaster reuse across a destroyed-and-recreated testbed VM at a reused address. | ControlPersist=60s reaps the idle master well before a multi-minute VM recreate completes, so no stale master survives to be reused; the natural operating path is safe, and an `[ssh_connection]` mitigation would only guard an unrealistic sub-60s recreate. | Real destroy-recreate on rocky8 `.100`, 2026-08-16: the master was already reaped before destroy; the recreate reconnect reached the fresh VM (`up 2 min`, `rc=0`) through a new master. GitHub #10. | 9770c22 |
