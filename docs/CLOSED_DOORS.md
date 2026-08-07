# Closed Doors

## Scope

This document records examined candidates that the owner deliberately leaves
unchanged. It is not an active work register.

| Date | Verdict | Candidate | Premise | Evidence | Carrying commit |
| --- | --- | --- | --- | --- | --- |
| 2026-07-31 | Keep | A recorder manifest field injected before `recorded_at=` can be absorbed by the application-record shape glob. | The behavior predates the M.13 selector work and changing it would expand the accepted scope. | M.13 detail in `docs/milestone-0082a56.md`; prior evidence in `docs/MILESTONES.md`; commits `75f16c3` and `ca2a9de` leave it unchanged. | 0082a56 |
