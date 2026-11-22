# Contested Crown contracts — Victoria 3 1.15.0

Reviewed on 5 November 2026 against game build `26453692`, core manifest
`7727600027425614094`, and CMF `1.67.1 + sb-1.15.0-r1`. The
[current fixture](zulu_contested_crown_contracts_1_15_0.json) replaces active test
use of the [preserved 1.14.5 fixture](zulu_contested_crown_contracts_1_14_5.json).
No claimant gameplay scripts changed in this review.

Six of 24 native source contracts changed. The other 18 hashes, all 16 pinned
defines and the CMF movement-value file still match the earlier fixture. Only
the six reviewed native hashes were refreshed; this is not a whole-file repin
of unrelated governance laws or callbacks. Exact old native bodies are not
retained here, so the review establishes the current interface and its relation
to SB rather than claiming a complete old/new implementation diff.

| Changed contract | Review and disposition |
| --- | --- |
| `law_monarchy` and `law_social_monarchy` in [native governance laws](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/laws/00_governance_principles.txt>) | Both complete definitions were read. Their modifier blocks still exactly match SB's independent temporary laws. Native enactment, imposition, country-specific activation and deactivation rules are inherited by the ordinary native laws, not copied into the deliberately restricted claimant demands. Social Monarchy's Poland gate is outside the Zulu controller. |
| `on_revolution_start` and `on_civil_war_won` in [native callbacks](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt>) | Country root, uprising `scope:target`, and the documented end-before-winner ordering remain. Native start delegates movement-type/target bookkeeping and country-specific handlers; winner handling includes anti-monarchist AI status, abolition, French/Springtime/pan-nationalist branches and cleanup. SB's hooks remain additive and identify the exact claimant movement/war. See the runtime limitation below. |
| `gg_korea.2` in [native Korea events](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/events/soi_events/00_ep1_korea_events.txt>) | The current example adds **0.50**, not the historical report's `1`, to a saved existing civil war. It also protects the event portrait temporarily and cleans up afterwards. This remains an example of the fractional progress interface. SB's own `+1` is its authored advance-to-war decision; it is not asserted to equal Korea's current balance value. |
| [Political movement documentation](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/political_movements/political_movements.md>) | Reviewed the complete interface. `can_pressure_interest_group` and `interest_group_can_join` use IG roots; revolution `possible`, `weight` and `target_fraction_of_states` retain movement context. `state_weight` remains a geographical weight. The optional `forced_tags` interface does not require a claimant migration. Agitator support still does not promise commander or battalion allocation. |

The retained CMF [movement-value hooks](../../../Community%20Mod%20Framework/common/script_values/00_mog_plp_movement_values.txt)
still supply neutral state-weight and incorporation multipliers of `1`. Its
[mainland pop-support trigger](../../../Community%20Mod%20Framework/common/scripted_triggers/00_mog_plp_triggers.txt)
remains `always = yes`. Neither replaces SB's coalition selection or guarantees
the native allocation of forces.

## Verification limits

The focused claimant suite checks current hashes and defines, modifier parity,
and shipped claimant scripts with supplied native callback inputs. It does not
run the engine's complete callback pipeline, allocate native armies or establish
callback execution order relative to additive hooks. Earlier 1.14.5 binary
observations remain historical evidence, not a 1.15 engine certification.

`python3 -B -m unittest tests.test_zulu_contested_crown` passed all **78 tests**
after selecting the reviewed current fixture. The historical fixture is
byte-unchanged, all local evidence links resolve, and the scoped diff check is
clean.

DP must still test both winners under Monarchy and Social Monarchy, including
the restored governance law, native `anti_monarchist_revolution` cleanup,
`ai_gendarme_revolutionary_regime_var` and absence of an unintended abolition JE.
Native `country_has_monarchy_law` recognises the two ordinary royal laws, not
SB's independent contested demands; the native start/winner branches therefore
need explicit observation alongside SB's restoration. This is a runtime gate,
not a demonstrated new regression or authorisation to change the controller.

Existing claimant release gates remain: exact conflict identity, both winners,
third-party characters, cancellation, succession, save/load, and meaningful,
repeatable military advantage from stronger coalition backing. Source checks
do not discharge those gates.
