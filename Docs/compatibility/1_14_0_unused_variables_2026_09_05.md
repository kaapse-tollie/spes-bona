# OB1 unused-variable repair — 2026-09-05

The 19 launch warnings reported at 19:03:44 were checked against all mod source references, including localization. None had a reader. Seventeen were redundant state, one represented a useful failure diagnostic, and one needed a real gameplay guard. This supersedes the initial launch report's decision to retain all nineteen.

## Dispositions

| Variable | Repair and retained behavior |
|---|---|
| `sb_zululand_direct_british_administration_var` | Removed. Annexation, province ownership, and the handoff-resolved flag already implement the result. |
| `sb_zululand_crown_led_route_var` | Removed. The live gradual-restoration and settlement-resolved flags, plus the protectorate relationship, still implement this route. |
| `sb_zululand_defection_usuthu_var` | Removed. The balance shift remains; the event's default description already supplies the uSuthu text. |
| `sb_nrp_union_petition_lapsed_var` | Retained and checked by the monthly petition scheduler. A refused or permanently invalid petition must not be queued again after its pending flags are cleared. |
| `sb_nrp_scripted_frontier_setup_var` | Removed. Republic setup still runs and retains its active constitution/setup flags. |
| `sb_griqualand_last_record_claim_target_scope` | Removed. The accepted-side global flags still record the actual claim target used by the resolver. |
| `sb_zululand_boer_patron_scope` | Removed. Current diplomacy and incorporation routes address TRN directly. The earlier design document proposed a stored patron, but no live route read it. The authoritative commitment bar and committed flag remain. |
| `sb_bst_annexation_backdown_rejected_var` | Removed with its diagnostic-only branch. A Boer aggressor backing down still receives no scripted annexation; the separate bound Gun War resolver remains. |
| `sb_griqualand_last_record_holder_scope` | Removed. Exact play binding and the accepted-side flags still control settlement. |
| `sb_zululand_boer_aid_delivered_var` | Removed. Soldier movement, commitment gain, balance shift, and committed-state handling remain. |
| `sb_nrp_boundary_demand_lapsed_var` | Removed. Clearing the pending demand and checking the current territorial/political conditions already cancels the demand. |
| `sb_nrp_zulu_victory_honored_var` | Removed. The victory path still clears the rebellion and boundary-demand state. |
| `sb_natal_zulu_secession_configuration_failed_var` | Replaced with `debug_log`: a surviving launch lease now logs the configuration failure when it occurs, then remains consumed as before. Vanilla OB1 uses this effect in its on-actions. |
| `sb_zululand_exiled_successor_var` | Removed. The heir is still exiled; live royal-house restoration uses its existing character/template selection. |
| `sb_zululand_gbr_scope` | Removed with the otherwise-empty container initialization branch. Live British-authority checks use the country directly. |
| `sb_zulu_generic_war_resolution_recent_var` | Removed. Exact-play terminal handling still awards the existing dynastic-stability effects; this unused 30-day flag never prevented duplicate delivery. |
| `sb_nrp_greater_concession_var` | Removed. Greater/reduced-republic triggers already inspect the territory; setup and boundary scheduling remain. |
| `sb_dinuzulu_ever_created_global_var` | Removed. This flag was never a creation guard. Existing character selection, creation, and succession behavior is unchanged by its removal. |
| `sb_zululand_skirmish_usuthu_var` | Removed. The 50/50 roll and balance effects remain; the event's default description already supplies the uSuthu text. |

## Verification

The new petition regression failed before the scheduler guard was added. All 53 focused settlement/war-route tests then passed. Existing assertions that merely required a diagnostic variable now check the actual cleanup, annexation exclusion, or failure log instead. The validator's stale-symbol check rejects the 18 retired variable names in shipped scripts. No artificial variable reads were added to suppress warnings.

The full run (`tools/validate.py --skip-cmf-sync`) completed 14/16 categories without failure. Its localization check and the matching unit test failed on a concurrent edit to `localization/english/sb_great_trek_l_english.yml:66`: `# ### (DP) REVIEWED ###` is not recognized by the current review-marker parser. That approval annotation was left intact. The unit suite ran 397 tests with this one failure; the variable checks, runtime script contracts, delayed-event lifecycle, and source inventory checks passed. `git diff --check` passed. Full output is retained at `/private/tmp/sb-unused-variable-fix/verification.txt`.

Existing saves need no variable migration: the removed values have no consumers, while an existing petition-lapsed flag now correctly prevents another offer. Restart the game to load the updated scripts and inspect a fresh launch log. A fresh engine launch and a runtime petition-refusal retest have not yet been performed.
