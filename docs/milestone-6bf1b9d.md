# Work Register

## Scope

This document owns the remaining deliverables for ansible-provision on master.
All surviving work is assigned to the Milestone section. Each detail states the
result still needed, the available evidence and the condition for completion.
Completed and retired work is available through the prior-state commit in History.

Out of scope: new product acceptance, new runtime execution and live GitHub changes.

Release line: master
Milestone index: 6bf1b9d
Canonical path: `docs/milestone-6bf1b9d.md`
Canonical branch or ref: master
Git upstream: origin/master
Remote tracker: jeonghanlee/ansible-provision, GitHub milestone Backlog

Next session entry point: M7 evidence accounting. Open `work/issue-54-reporting-body.md` and compare the three unpublished reporting criteria listed in M7 with the last published record. Then compare M4's five stopped-collector calls and the completed six-case independence matrix with the remaining #54 conditions before selecting another runtime check.

Remaining work: 7 milestones. Status tally: 2 Blocked, 2 Deferred, 1 Open and 2 Not started. Two external gates are Open. Backlog contains no unassigned work. M6 is Ready for planning and execution authorization.

Accepted ETL scheduler, journal recording and buffer functionality remains
supported by its recorded evidence. The outstanding tooling work concerns its
own completion criteria. Historical raw inputs that cannot be obtained retain
their recorded unknown or Incomplete outcomes.

## Milestone

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Provisioning | M1 | Finish Archiver distribution and source-build acceptance | Milestone | Blocked | No | G1, D1 | Both acquisition paths meet the retained installation and idempotency contract against the delivered baseline; [detail](#m1---finish-archiver-distribution-and-source-build-acceptance) |
| Provisioning | M2 | Complete SQLite installation on the existing server | Milestone | Blocked | No | G2, D1 | Actual server installation, SQLite, IOC retrieval, restart and reapply checks pass; [detail](#m2---complete-sqlite-installation-on-the-existing-server) |
| EPICS | M3 | Unify the EPICS-env release selector | Milestone | Deferred | No | D2 | Both roles and provenance use the effective selected release, including overrides; [detail](#m3---unify-the-epics-env-release-selector) |
| Tools | M4 | Resolve final-record coverage after normal shutdown | Milestone | Open | No | D1, D4 | The final-record requirement has a precise evidence boundary and every required refusal has actual evidence or an explicit disposition; [detail](#m4---resolve-final-record-coverage-after-normal-shutdown) |
| Tools | M5 | Verify collection during source-store deletion | Milestone | Deferred | No | D3, D4 | Actual deletion overlaps collection, native sizes and status are preserved, and retained-output evaluation agrees; [detail](#m5---verify-collection-during-source-store-deletion) |
| Tools | M6 | Verify accumulation, restart and live measurement overlap | Milestone | Not started | Yes | D1, D4 | Remaining real measurement regressions have process-bound inputs, observed request intervals and native outcomes; [detail](#m6---verify-accumulation-restart-and-live-measurement-overlap) |
| Tools | M7 | Reconcile ETL tooling evidence and close the consolidated issue | Milestone | Not started | No | M4, M5, M6, D1, D4, D5 | Every surviving #54 criterion has evidence or a dated disposition, published content agrees, and closure is verified; [detail](#m7---reconcile-etl-tooling-evidence-and-close-the-consolidated-issue) |
| Gate | G1 | Deliver the Archiver middleware baseline | External gate | Open | No | | cloud-provision delivers its middleware baseline and provisionable verification environment; [detail](#g1---deliver-the-archiver-middleware-baseline) |
| Gate | G2 | Prepare and approve the existing server | External gate | Open | No | | Server owner confirms the proxy settings and installation approval; [detail](#g2---prepare-and-approve-the-existing-server) |

### Decisions

| ID | Decision | Decision Date |
| --- | --- | --- |
| D1 | Reset the canonical document from the committed prior state and assign all surviving work to Milestone. Consolidate the collection, evaluation and issue-tracking summaries into one issue-finalization deliverable. Determine remaining work from completion criteria and actual evidence. | 2026-11-26 |
| D2 | Defer release-selector unification after changing both existing role selectors to EPICS-env 1.5.0. A later accepted implementation plan selects the variable and provenance changes. | 2026-11-09 |
| D3 | Defer live source-store deletion-overlap verification for later selection of a bounded real case. | 2026-11-11 |
| D4 | Use retained actual evidence first and bounded real execution for missing claims. Preserve original tools, outcomes and accepted functionality. Record missing coverage and native Failed or Incomplete outcomes explicitly. | 2026-10-24 |
| D5 | Retire requirements that depend on unavailable historical journals or complete original full-day inputs. Preserve unknown historical coverage and the original outcomes. Available measurement reconciliation and the remaining live regressions retain their completion criteria. | 2026-11-26 |

### Milestone Details

#### M1 - Finish Archiver distribution and source-build acceptance

Origin: 6bf1b9d / M1
Identity History: none
GitHub Issue: none
Status: Blocked

##### Summary

Finish the original whole-assembly acceptance for both Archiver acquisition
paths. The `archiver` distribution-install operator and species still need to
be implemented. The source-build and standalone operator results are already
recorded. Whole-assembly acceptance remains outstanding for both paths.

##### Scope

OpenJDK 21 with the distribution JAVA_HOME, shared Tomcat 9.0.121, MariaDB,
Archiver WARs, group `mid`, user `mid-srv`, site overrides and idempotent reapply.
The `archiver` and `archiver-dev` species layer on `common` + `epics`. The
source-build path uses the Maven Wrapper's Maven 3.9.9 without a separately
installed Maven package. Existing component results are reused at their
recorded versions.

Out of scope: Phoebus, the combined middleware species and site-specific values.

##### Completion Criteria

- [ ] The distribution-install species installs the complete declared stack.
- [ ] The source-build species meets the same stack and service contract.
- [ ] Both species resolve through the normal Make and inventory entry points.
- [ ] Version values use override keys with neutral public defaults; internal endpoints remain in site configuration.
- [ ] Reapply with identical inputs is idempotent and required baseline delivery is complete.

##### Dependencies And Decisions

- G1 is Open. Resume as In progress after its external baseline is complete.
- The accepted scope was narrowed to Archiver Appliance on 2026-10-21.
- The resolved database-schema prerequisite and completed operator work are retained evidence.

##### Implementation Plan

Plan Status: accepted
Plan Acceptance: 2026-10-21 for both Archiver acquisition paths, preserving the earlier accepted operator increments.
Implementation Authorization: earlier operator increments are recorded in History; final whole-assembly execution awaits G1 and its concrete target.
Superseded Plan Artifacts: historical Phoebus and combined-middleware requirements.

1. Confirm the delivered baseline and existing implementation against the two acquisition paths.
2. Implement the `archiver` distribution WAR installation operator and species. Register them in `configure/RELEASE` and add the species group in `inventory/lab.ini`. Retain the `common` + `epics` base and the accepted Rocky 8.10 and Debian 13 scope.
3. Reuse the recorded Java, Tomcat, MariaDB and source-build checks. Run the outstanding structure and integrated installation/reapply checks after the distribution path is available.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Structure | After implementation, resolve and syntax-check both species and confirm their inventory and Make entries. | Control host | Required operators and both acquisition paths resolve. |
| T2 | Integration | Apply each species, inspect the declared stack, then reapply identical inputs. | Baseline-matching appliance environment | Full installation and idempotency contract passes. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Prior-state checkpoint | Control host | Pending | Original whole-assembly structure criterion remains unrun in the retained record. |
| T2 | Prior-state checkpoint | Both acquisition paths | Pending | Standalone and source-build results exist. Whole-assembly acceptance for both paths remains outstanding. |

##### Closure Evidence

Await G1, implementation of the distribution path, and the two outstanding
checks. The prior-state document retains the operator increments, their actual
results and source commits.

#### M2 - Complete SQLite installation on the existing server

Origin: 6bf1b9d / M2
Identity History: none
GitHub Issue: none
Status: Blocked

##### Summary

Apply `archiver_server_sqlite` to the existing general Rocky Linux 8.10 server
and complete the server-specific acceptance checks. The assembly and its local
and disposable-environment checks already have recorded results.

##### Scope

Use the existing server's sudo policy and owner-managed proxy settings. Verify
the installed SQLite appliance through the actual assembly, IOC and retrieval
paths, restart and same-input reapply.

Out of scope: proxy configuration ownership, account access changes and MariaDB removal.

##### Completion Criteria

- [x] Local assembly contract and the optional proxy-check role have recorded passing checks.
- [ ] The assembly installs on the existing server after G2 completes.
- [ ] SQLite contains `PVTypeInfo`, `PVAliases`, `ArchivePVRequests` and `ExternalDataServers`, and the service account can access them.
- [ ] Four JVMs run, the appliance becomes ready, and a health run triggered by its timer succeeds.
- [ ] Three changing numeric IOC PVs are collected and retrieved, with new data after restart.
- [ ] Same-pin reapply succeeds without installation drift.

##### Dependencies And Decisions

- G2 is Open. Resume as In progress after server preparation and installation approval.
- The 2026-10-11 accepted assembly removes the proxy readiness gate and keeps the optional role available.
- The separate completed three-PV installation VM result is available as prior evidence.

##### Implementation Plan

Plan Status: accepted
Plan Acceptance: 2026-10-10, amended on 2026-10-11 to remove proxy-check wiring from the assembly.
Implementation Authorization: local implementation and disposable checks were authorized and executed; existing-server installation awaits G2.
Superseded Plan Artifacts: the earlier proxy-gated assembly design.

1. Confirm the original server and owner-approved inputs when G2 completes.
2. Apply the unchanged server assembly through its normal entry point.
3. Run installation, retrieval, restart and reapply acceptance on that server.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Existing prerequisite evidence | Reuse the recorded assembly and optional proxy-check results. | Retained real records | Existing implementation coverage is identified. |
| T2 | Installation | Apply the server assembly with the owner's proxy settings. | Existing server | Installation succeeds at the selected pins. |
| T3 | Functional acceptance | Inspect tables, processes and readiness, verify a successful timer-triggered health run, query three real IOC PVs, restart and reapply. | Existing server | Every declared server acceptance condition passes. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-10-11 | Controller and dedicated Rocky/Debian guests | Passed within the recorded scope | Assembly checks 10/10, optional role cases 21/21 on Rocky and 7/7 on Debian. Complete original records are in History. |
| T2 | Not run | Existing server | Pending | Requires G2. |
| T3 | Not run | Existing server | Pending | Requires G2 and the actual installation. |

##### Closure Evidence

The existing-server installation and functional checks remain outstanding.

#### M3 - Unify the EPICS-env release selector

Origin: 6bf1b9d / M3
Identity History: none
GitHub Issue: none
Status: Deferred

##### Summary

The `epics` and `epics_build` roles currently select the release through
`epics_env_version` and `epics_env_tag`. Unify selection and verify that provenance
records the effective value, including an inventory or extra-vars override.

##### Scope

Select one variable and its location, update both role readers and provenance,
and update their documentation. Retain tag selection for `epics`, tag-first and
branch-fallback selection for `epics_build`, and standalone role usability.

Out of scope: site modules, the EPICS Base selector and another repository's bake implementation.

##### Completion Criteria

- [ ] One override changes the release used by both roles.
- [ ] Provenance records the effective release with and without an override.
- [ ] Every species playbook passes its syntax check.

##### Dependencies And Decisions

- D2 defers this implementation. A new accepted plan selects the variable and readers.

##### Implementation Plan

Plan Status: draft
Plan Acceptance: none
Implementation Authorization: none
Superseded Plan Artifacts: none

1. Inventory both selectors, role readers, provenance and documentation.
2. Select the common variable and preserve supported source-ref behavior.
3. Apply the selected change and verify its actual consumers.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Static | Syntax-check every species playbook. | Control host | All selected playbooks pass. |
| T2 | Integration | Apply both roles with defaults and an override and read actual provenance. | Dedicated suitable environment | Effective release and recorded release agree. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Control host | Pending | Unification is deferred. |
| T2 | Not run | Dedicated environment | Pending | Unification is deferred. |

##### Closure Evidence

Deferred under D2.

#### M4 - Resolve final-record coverage after normal shutdown

Origin: 6bf1b9d / M4
Identity History: none
GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
Status: Open

##### Summary

The real 7200-second shortened observation passed. Five stopped-collector calls
produced the declared outcomes and restored original application-log bytes and
inodes. Whole-component completion is unresolved because the meaning of
"missing final record" has not been settled against that measured coverage.

##### Scope

Final application-file capture, invocation/PID/file identity, refusal of changed
input, repeated terminal refusal and replay. The remaining action establishes
which loss claim the existing completion criterion actually requires.

Out of scope: another full-day producer and changes to accepted ETL functionality.

##### Completion Criteria

- [x] Actual final/post-stop capture retains all required application-file bytes with the original invocation, PID, inode and prefix identity.
- [ ] A changed invocation, wrong PID, truncation or missing final record refuses complete evidence.
- [x] Repeated terminal invocation dispatches no second stop and leaves original evidence unchanged; real replay reproduces the result.

##### Dependencies And Decisions

- Open condition: determine whether the final-record requirement concerns independently captured bytes, incomplete trailing bytes or a complete event lost before any independent capture.
- The existing collector compares receipt-backed bytes and source identity. An uncaptured event requires an independent expectation before its absence can be established.
- M7 owns reconciliation with the existing issue text. Record the resulting scope decision before selecting another case.

##### Implementation Plan

Plan Status: accepted
Plan Acceptance: 2026-11-26 for one real 7200-second observation and five stopped-collector calls.
Implementation Authorization: that bounded execution completed; the open final-record completion boundary requires a recorded decision.
Superseded Plan Artifacts: the historical draft's already executed identity and partial-record cases.

1. Compare the retained five case inputs and native outcomes with the original completion criterion.
2. State the exact required record and independent evidence for any remaining absence claim.
3. Resolve completion from that evidence or record the explicit scope disposition.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Normal finish | Actual shortened observation, final capture and normal stop. | Dedicated Rocky 8.10/systemd 239 appliance | Native Passed and successful same-boot stop. |
| T2 | Stopped collector | One intact call and four isolated changed-input calls through installed collect.py. | Same stopped appliance and genuine pre-stop receipts | Intact status 0, four intended refusals with status 1, exact restoration. |
| T3 | Repeated request and replay | Reuse actual repeated-finish refusal and independent frozen replay. | Retained actual terminal inputs | No second stop, original bytes preserved and seven artifacts reproduced. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | 2026-11-27T02:23:33.698127+00:00 | Dedicated actual appliance | Passed | Observation elapsed 7200.000315512001 monotonic seconds. Native terminal Passed, stop status 0 in 11.2835461020004 seconds, no terminal errors. |
| T2 | 2026-11-27T02:23:53.275417+00:00 | Same stopped appliance | Five declared outcomes verified | Intact status 0. Changed invocation, wrong PID, receipt-backed truncation and incomplete final record each return 1 with the intended journal diagnostic. Each case verifies restored bytes and inode. |
| T3 | 2026-11-19T22:21:46.335638+00:00 | Isolated retained-input run and independent recipient | Passed within the declared replay scope | Repeated finish status 1, no child stop, seven byte-identical replay artifacts, preservation of 63900 copied input and 448 JDK members. |

The private archive is
`work/etl-shared-vm-preparation-20261126/receipts/100-preserve-native-evidence/stdout`.
Its complete 572-member record is
`work/etl-shared-vm-preparation-20261126/native-evidence-members.json`.
The archive contains the genuine checkpoint, original logs, all five case
inputs, native streams, errors and restoration records. Repeated-request
replay is in `work/m41-repeated-replay-20261119/result.json`.
The provider recorded the dedicated VM shut off at 2026-11-27T02:26:18.304443+00:00,
with its disk and evidence retained.

##### Closure Evidence

Five case outcomes are verified. A complete event removed before any independent
capture was outside those five calls. The final-record criterion remains open
pending its scope/evidence disposition.

#### M5 - Verify collection during source-store deletion

Origin: 6bf1b9d / M5
Identity History: none
GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
Status: Deferred

##### Summary

Observe real file removal while the shipped collector measures store size,
then verify the saved native result through its real reader. Existing retained
parser checks supply narrower evidence.

##### Scope

Actual collector measurement, independently observed removal overlap, surviving
size, native status, unrelated command failures and frozen-result evaluation.

Out of scope: storage-failure product tests and accepted observation data.

##### Completion Criteria

- [ ] Real source-file removal overlaps native collection and independent records establish the overlap.
- [ ] Actual surviving sizes and command status are preserved, including unrelated command failures.
- [ ] Actual collected output and frozen retained-input evaluation agree.

##### Dependencies And Decisions

- D3 retains the dated deferral until a bounded live case is selected.
- D4 requires real native commands and actual inputs for the selected claim.

##### Implementation Plan

Plan Status: draft
Plan Acceptance: none
Implementation Authorization: none for the live case
Superseded Plan Artifacts: none

1. Select a disposable source-store target and the unchanged collector entry point.
2. Declare the independent overlap measurement, native streams, status and restoration.
3. Bind a finite execution limit to the target, run the selected case and freeze the output.
4. Re-evaluate the actual saved output through the shipped reader.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Real collection | Run native measurement during independently observed file removal. | Dedicated disposable store | Actual overlap, measured size and native status are retained. |
| T2 | Retained result | Run the shipped reader on the frozen actual command output and its failure controls. | Isolated retained copies | Native result agrees and unrelated failures remain visible. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Not run | Dedicated store | Pending | Live overlap remains unexecuted. |
| T2 | Prior-state checkpoint | Historical retained command output | Partial | Existing parser consumption does not establish T1 or its actual-output replay. |

##### Closure Evidence

All three live/result criteria remain outstanding.

#### M6 - Verify accumulation, restart and live measurement overlap

Origin: 6bf1b9d / M6
Identity History: none
GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
Status: Not started

##### Summary

Complete the real measurement regressions still outstanding after retained
reporting, query-bound verification and retained pass-overlap checks.

##### Scope

Accumulation, process restart and any required live request/pass-completion
overlap. Each measurement binds its process lifetime, time bounds, units,
actual workload and original input identity.

Out of scope: recovery of unavailable historical raw populations and repeated product acceptance.

##### Completion Criteria

- [ ] Bounded real accumulation has independently identified input, interval and native output.
- [ ] A real process restart is reflected in process/lifetime-bound measurements and saved evidence.
- [ ] Required live request/pass overlap has actual request and pass-completion boundaries.
- [ ] Retained-input and bounded real measurement regressions agree on their declared claims, preserving unresolved coverage.

##### Dependencies And Decisions

- D1 carries this unstarted live scope into the current Milestone.
- D4 selects retained evidence before another bounded live case.
- D5 leaves unavailable historical totals, populations, query bounds and complete OOM coverage explicitly unknown.

##### Implementation Plan

Plan Status: draft
Plan Acceptance: none for the remaining live cases
Implementation Authorization: retained-report, query-bound and retained-overlap work is complete; live accumulation/restart cases await a concrete accepted plan
Superseded Plan Artifacts: completed retained-report and query-bound preparation steps.

1. Compare the retained regression coverage with the live claims above.
2. Select only an uncovered claim and declare actual inputs, exposure, process identity and finite bounds.
3. Execute the native measurement and retain original streams before evaluation.
4. Compare frozen actual inputs/results with the declared expectation.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Accumulation | Observe actual bounded input and native counters/sizes over the declared interval. | Selected real target | Measurements reconcile with their observed input and interval. |
| T2 | Restart | Record actual old/new process identities and native measurements across restart. | Selected real target | Process lifetime changes are represented correctly. |
| T3 | Request overlap | Independently record real request and pass intervals, then evaluate frozen output. | Selected real target and retained copies | Overlap is explicit and native result handling preserves actual failures. |

##### Verification Results

The earlier retained report and its verification are
`work/m43-measurements-20261110/report.json` and
`work/m43-measurements-20261110/verification.json`. They cover eight JVM groups,
the available freshness query bounds and visibility request/response times.
Historical visibility query bounds remain unknown.

The later default/absent run retains query start/end and request/response times
for 260967 freshness queries and 1734 visibility attempts within its observation
window. Read the native files under
`work/m38-default-20261116/absent/recipient-input/state/raw/` and the window in
`work/m38-default-20261116/absent/recipient-input/state/observation.json`.

The query-bound correction and five retained-input overlap cases are recorded
in the prior-state document. Those results cover their measured inputs.
The live accumulation, restart and remaining live-overlap cells above are Pending.

##### Closure Evidence

The remaining live measurement regressions have no completed execution record.

#### M7 - Reconcile ETL tooling evidence and close the consolidated issue

Origin: 6bf1b9d / M7
Identity History: none
GitHub Issue: #54, https://github.com/jeonghanlee/ansible-provision/issues/54
Status: Not started

##### Summary

Maintain one completion account for the consolidated ETL tooling issue.
Collection, evaluation and group coordination use the same child evidence.
This deliverable reconciles each issue requirement with that evidence and
verifies publication and final closure.

##### Scope

The existing #54 criterion set, its verification/retirement decisions, remaining
M4/M5/M6 results and final issue state. This includes resolving residual
interruption, timeout and worker-failure prose against the accepted completed
independence criteria before any additional execution is selected.
Final disposition of the bounded lifecycle and six-case independence results
also belongs here. Their retained technical results do not establish closure
of an unselected full draft; the reset itself supplies no such closure.

Out of scope: duplicate execution of child checks and unavailable historical input reconstruction.

##### Completion Criteria

- [ ] Every #54 condition has identified actual evidence, an explicit remaining claim or a dated retirement.
- [ ] Completed independence, fault, lifecycle, reporting and preservation results are accounted for at their actual scope.
- [ ] M4, M5 and M6 completion/disposition agrees with their evidence and the corresponding issue criteria.
- [ ] Source identity, unsuccessful original outcomes and accepted product results remain traceable.
- [ ] Published issue content matches the canonical results and its final closed state is read back.

##### Dependencies And Decisions

- M4, M5 and M6 determine final issue completion. Evidence accounting can proceed before those conditions close.
- D1 consolidates the repeated collection/evaluation/group tracking under this deliverable.
- D4 governs bounded completion. D5 records retirement of unavailable-original requirements.
- Git and GitHub mutations use their separately delegated operations.

##### Implementation Plan

Plan Status: accepted
Plan Acceptance: 2026-10-24 for retained evidence first and bounded completion, continued by the 2026-11-26 reset instruction.
Implementation Authorization: canonical document reset and evidence accounting; live issue changes retain their operation-specific authorization
Superseded Plan Artifacts: repeated collection-parent, evaluation-parent and group accounting lists.

1. Open the retained reporting draft below and compare the three unpublished reporting criteria with the last published record. Use those records and the retained results to account for each #54 criterion once.
2. Resolve stale open descriptions where completed evidence already satisfies the actual criteria.
3. Record M4's completed five calls and its precise unresolved final-record boundary.
4. Derive technical completion from M4/M5/M6 evidence or explicit disposition.
5. Prepare the complete issue update, apply under issue delegation and read back content and final state.

##### Test Plan

| Label | Layer | Method | Environment | Expected Result |
| --- | --- | --- | --- | --- |
| T1 | Evidence accounting | Compare original criterion texts, actual recorded results and dated dispositions. | Current and historical source records | Each criterion has one explained state and an evidence locator. |
| T2 | Publication | Compare prepared and actual issue body, metadata and check states. | GitHub readback | Exact intended content is published. |
| T3 | Closure | Read issue state after its completion conditions are established. | GitHub readback | Actual final state matches the approved disposition. |

##### Verification Results

| Label | Observed At | Environment | Result | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Prior-state checkpoint | Canonical records and retained receipts | Partial | The historical 81-condition issue account had 60 verified, nine retired and 12 unmet criteria before incorporating the latest collector execution. These counts include repeated parent/group conditions. |
| T2 | 2026-11-26T23:29:18.195067+00:00 | Last retained GitHub readback | Prior publication verified | #54 had 57 verified, nine retired and 15 unmet conditions. Its body SHA256 was 2ce80e0156f154ee92c2e42497c2429f4177b2bfe35a491cbd608f4082198d8c. Three verified reporting criteria await publication. |
| T3 | Not run | GitHub | Pending | #54 was Open at its last retained readback. |

The retained reporting draft is `work/issue-54-reporting-body.md` (SHA256
`8038c6af56e4d819dbdb6c9f990ab8fb94759e03bb05f25b6860bf93f35794cd`). It
accounts for 60 verified criteria. The three verified criteria awaiting
publication are the numerical reporting criterion from source issue #35 and
criteria 1 and 2 from source issue #48. The prior-state document in History
records the draft and last published comparison under `Track ETL test tooling`,
in `GitHub Projection`.

The completed six-case independence matrix and five checked component criteria
are in the committed prior-state record. Actual default-case results are in
`work/m38-default-20261116/absent/verification-case.json`,
`work/m38-t56-fresh-20261119/failing/recipient/result.json` and
`work/m38-t6-20261123/changed/recipient/result.json`.
Normal-finish and independent-recipient results retain the original native
Incomplete outcome for the default/failing case.

The journal normal-stop, later direct read, repeated request and command-error
criteria have recorded passing bounded results in commits `b8d70e8` and
`9277cb0`, with issue accounting in
`work/m47-retirement-20261110/publication.json`.
Completed scope and optional/unexecuted coverage are retained in History.

##### Closure Evidence

Issue #54 remains open for the explicit remaining claims and publication.

#### G1 - Deliver the Archiver middleware baseline

Origin: 6bf1b9d / G1
GitHub Issue: none
Status: Open

##### Summary

The cloud-provision owner supplies the operator/species definition, middleware
package baseline and provisionable verification environment used by M1.

Responsible party: cloud-provision owner.
Affected work: M1.

##### Completion Criteria

- The provider merges the declared system OpenJDK 21, shared Tomcat 9.0.121 and MariaDB baseline and makes its verification environment provisionable.
- Its integration/publication status is confirmed against M1's actual accepted contract.

##### Verification Results

Completed baseline delivery is not recorded in the retained evidence. Confirm
the provider's merge and verification-environment provisionability before
clearing G1. M1's original whole-assembly acceptance remains unverified in the
retained source record.

##### Closure Evidence

External baseline delivery remains Open.

#### G2 - Prepare and approve the existing server

Origin: 6bf1b9d / G2
GitHub Issue: none
Status: Open

##### Summary

The existing server's owner prepares the proxy environment, DNF and Maven
settings and approves appliance installation on that server.

Responsible party: existing-server configuration owner.
Affected work: M2.

##### Completion Criteria

- Required proxy configuration and Maven settings are present on the server.
- Installation approval is recorded with its date.

##### Verification Results

The retained record contains no completed server-preparation/approval condition.

##### Closure Evidence

Existing-server preparation and installation approval remain Open.

## Backlog

### Work

| Group | ID | Work unit | Type | Status | Ready | Deps | Done when / Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Backlog Details

No unassigned work.

## History

| Reset Date | Prior State Commit |
| --- | --- |
| 2026-11-26 | 6bf1b9d11ed404dc6307f5a83acd4b4f263239c2 |
