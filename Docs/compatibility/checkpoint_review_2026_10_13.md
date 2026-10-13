# SB 0.20.1 maintenance checkpoint review

Date: 2026-10-13. Reviewed against commit `9f77cac` on `main`.
This checkpoint preserves the September maintenance batch. It is not a release
certification or a rebase to the game currently installed on the development machine.

## Baselines and scope

| Component | Recorded state |
|---|---|
| SB metadata and descriptor | Both `0.20.1`, supported game `1.14.3` |
| Supported game target | Build `25347710`, core manifest `5228357714133991559` |
| Installed game | `1.14.5`, build `25629520`, core manifest `5521822647051867164` |
| Dependency | CMF `1.66.0` + `sb-1.14.3-r1`; installed-tree verification passes |

The review covered the staged dependency patch workflow and rollback, effective
CMF replacements, story-war actor/goal routing, Great Trek and Natal delivery,
Klip River's two-demand settlement, Chiefdoms movement identity and UI, supporting
tests, inventory changes, map repairs, and historical/design records. No additional
confirmed code defect was identified beyond the validation findings below.
Static review does not establish engine behavior.

Review changes are documentation only: correct README claims that validation
installs CMF, that the live dependency is pristine, and that `--latest` is supported;
align the open audit register with the existing 1.14.3 target. No test expectation,
inventory hash, reviewed prose, or gameplay script was changed to conceal a failure.

The September 20 ideology/interest-group/outcome proposals remain design records.
The implemented Chiefdoms contest still uses its ten-year deadline and existing
movement package. This checkpoint does not implement those later proposals.

## Unit-test results

Full discovery was rerun on this tree: **470 tests; 460 passed, 4 failed, 1 errored,
5 skipped**. The four failures and error are unresolved, not engine-pending labels.

| Result | Test | Cause |
|---|---|---|
| FAIL | `test_1_14_3_compatibility.CurrentBetaTests.test_exact_current_build_and_depot_report` | Expects build `25347710`; installed build is `25629520`. |
| FAIL | `test_1_14_naval_network.NavalNetworkTests.test_every_sb_state_port_has_a_connected_ob1_harbor_node` | Fails at the pinned naval-network hash before checking port connectivity. This does not demonstrate a disconnected port. |
| FAIL | `test_natal_zululand_gameplay_contract.NatalZululandGameplayContractTests.test_shepstone_has_a_twenty_five_year_repeal_lock_independent_of_indenture` | Its final assertion rejects the present `je_sb_natal_indenture_program_v2_goal:0` localization key. The failure does not show a broken repeal lock. |
| FAIL | `test_validate.RepositoryValidatorTests.test_repository_manifests_are_current` | DP-reviewed namespace `sb_boer_conventions.141` is missing from the reviewed-localization baseline. Preserve the approved text when reconciling it. |
| ERROR | `test_1_14_3_compatibility.CurrentBetaTests.test_current_manifest_tampering_is_rejected` | Cannot read the no-longer-retained `529341_5228357714133991559.manifest`. The current-target test is not conditional on manifest availability. |

The five skips are deliberate historical checks:

| Test | Missing historical prerequisite |
|---|---|
| `test_1_14_2_compatibility.BetaRebaseTests.test_historical_depot_evidence_rebuilds_when_manifests_retained` | Exact 1.14.0/1.14.2 manifests |
| `test_1_14_2_compatibility.BetaRebaseTests.test_historical_installed_payload_only_on_exact_1_14_2_build` | Installed 1.14.2 payload |
| `test_1_14_depot_delta.DepotDeltaEvidenceTests.test_committed_artifact_rebuilds_from_exact_manifests_when_retained` | Exact retained OB1 comparison manifests |
| `test_1_14_depot_delta.DepotDeltaEvidenceTests.test_decoder_rejects_a_same_size_manifest_with_different_hash` | Exact retained old manifest |
| `test_1_14_depot_delta.DepotDeltaEvidenceTests.test_installed_new_side_matches_manifest_when_ob1_is_present` | Installed OB1 payload |

## Validator and remaining work

The full validator reported **10 PASS, 1 WARN, 1 SKIP, 4 FAIL**. Its failed gates
are unit tests, localization bookkeeping, naval-network hash, and upstream
compatibility. These four gates are distinct from the four unit-test failures.
The synchronizer check was deliberately skipped with `--skip-cmf-sync`; installed
CMF integrity still passed. Tiger was not rerun for this checkpoint.

Local map data, override inventory, on-action routing, symbol checks, runtime
script contracts, delayed-event lifecycle, and release invariants passed.
The warning retains five deferred gates: BC-20, BC-22, CP-07, QUAL-09, SUP-05.

Staging the previously untracked files also exposes whitespace diagnostics that
an unstaged-only `git diff --check` missed: 1,499 across captured validation output,
unified patch context, a pinned CMF payload, the copied Absolutist definition, and
one blank line at the end of `test_usuthu_movement_contest.py`. These are preserved
in this checkpoint; the staged whitespace check is not reported as passing.

The 1.14.5 compatibility report identifies changes requiring semantic review in
AI incorporation and scoring, state-transfer scoring, European formation history,
colonial claims, Highveld/Scramble journal entries, and several containing source
files for interactions, technologies, and Dominion localization. Review those
changes and the naval network before changing the supported target or hashes.
All sixteen Vanilla contracts pinned by the current CMF patch still match the
installed game; that alone does not certify the entire dependency for 1.14.5.

Reconcile the two localization/test-bookkeeping failures explicitly. During the
next rebase, preserve historical report checks while conditioning historical
payload reproduction on retained inputs; current-target checks remain mandatory.

DP retains game launches and engine verification, including CAP deployment,
ORA–BST occupation, Klip River settlement, and Zulu/NRP branches. The ORA–BST
workaround remains on hold. The ZUL war crash mitigation remains unproven.
No game was launched, save migrated, dependency replaced, or engine scenario
certified during this review.

Reproduce the checks from the repository root:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B tools/validate.py --skip-cmf-sync \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/Community Mod Framework'
python3 -B tools/sync_cmf.py --check
git diff --cached --check
```
