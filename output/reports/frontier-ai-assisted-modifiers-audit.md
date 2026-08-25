# Frontier AI-Assisted Modifiers Audit

**Project:** Spes Bona - A Southern Africa Flavour Pack

**Audit date:** 23 August 2026

**Method:** Static audit of modifier definitions, event routing, scripted effects, on-actions, game-rule gates, and random weights. No game launch was performed.

## Executive summary

The current system is not controller-neutral. It contains separate anti-player variants, AI-AI outcome dice, deterministic military force floors, and several material assistance packages that are not modifiers at all. Several assists also bypass the Frontier AI game rule.

The audit identified 19 active war or recruitment modifier keys relevant to AI assistance, plus the noncombat `sb_zulu_ai_dynasty_authority` modifier.

The most important findings are:

1. The live Laager package is still the old extreme implementation. It does not match the later proposed package of +50% kill rate, +75% recovery, and +10% defence.
2. Human-AI and AI-AI assistance is not unified. Swazi and Basotho have stronger player-specific variants, while MTB, ZPB, Xhosa, and Blood River contain additional controller-specific handling.
3. The Disabled Frontier AI setting does not suppress every assistance route.
4. Force-floor building creation, free units, free pops, treasury injections, and forced mobilization materially compound the visible modifiers.
5. The Strict-Historical description promises full Swazi aid against ZUL, but the live Zulu-Swazi story route remains probabilistic.

Percentages below translate script values such as `0.50` to +50%. Training and conscription fields ending in `_add` are flat additions, not multipliers.

## 1. Live modifier packages

| Modifier | Current effects | Normal duration |
|---|---|---:|
| `sb_laager_defence` | +1000 training; -100% battle casualties; +75% recovery; +125% kill rate; -100% supply consumption; +50% organization gain | 12 months; 15 at Blood River |
| `sb_swazi_frontier_muster` | +25% organization gain; +50% army offence; +50% army defence; +100% recovery; +100% training; +50% subsistence output | 24 months |
| `sb_swazi_frontier_muster_vs_player` | +50% organization gain; +20% army offence; +75% army defence; +100% recovery; +100% training | 24 months |
| `sb_zulu_swazi_frontier_disarray` | -50% offence; -50% defence; +50% subsistence output | 12 months |
| `sb_klip_river_zulu_muster` | +10% offence, defence, and organization gain | 12 months |
| `sb_blood_river_zulu_no_relief` | -35% offence and defence | 9 months Dynamic; 15 Strict |
| `sb_blood_river_zulu_relief_mobilization` | +15% offence and defence; +10% organization gain | 12 months |
| `sb_zpb_civil_war_player_trn_support` | +500 training; +5% offence and defence | 12 months |
| `sb_bst_scripted_frontier_edge` | +1000 training; +25% offence and defence; +25% morale recovery; +50% recovery and kill rate; -25% morale loss; +25% morale damage | 12 months |
| `sb_bst_gun_war_defensive_muster` | +25% defence | 24 months |
| `sb_bst_gun_war_defensive_muster_vs_player` | +50% defence | 24 months |
| `sb_ora_scripted_frontier_edge` | +5% offence and defence | 12 months |
| `sb_ora_scripted_annex_war_overreach` | -10% offence | 12 months |
| `sb_bst_scripted_frontier_major_edge` | +20% offence; -90% supply consumption | 12 months |
| `sb_bst_scripted_thaba_bosiu` | -90% supply consumption | 12 months |
| `sb_frontier_levy_reconstitution` | +1000 training | Rolling 3 months |
| `sb_amabutho_levy_reconstitution` | +2500 training | Rolling 3 months |
| `sb_xhosa_native_warbands` | +0.50 state conscription rate | Permanent |
| `sb_native_conscription_MTB_player` | +2.5 state conscription rate; +2000 training; +50% offence; +150% defence | Permanent |
| `sb_zulu_ai_dynasty_authority` | +200 authority | While the Zulu dynasty country is AI and has the JE |

### Laager discrepancy

The live `sb_laager_defence` has no defence bonus. Instead, it provides casualty and supply immunity, +125% kill rate, +50% organization gain, and +1000 training in addition to the agreed +75% recovery component. It therefore remains the strongest single balance intervention in the package.

## 2. Dynamic-Historical dated AI-AI wars

Dynamic-Historical is the default game-rule setting. The probabilities below are conditional on the dated war meeting its prerequisites and being scheduled.

| AI-AI conflict | Dynamic modifier result |
|---|---|
| ORA-PHL return war, from 1840 | 80%: ORA receives Laager and Frontier Commando Advantage. 20%: Laager alone. Per-key probability: Laager 100%; ORA edge 80%. |
| ORA-BST return war, from mid-1847 | 80% ORA Laager; 20% BST Prepared Mountain Defense. The branches are mutually exclusive. |
| BST-TRN annexation war, from 1850 | 80% BST Prepared Mountain Defense; 20% TRN Laager. |
| BST-ZPB annexation war, from 1855 | 80% BST Prepared Mountain Defense; 20% ZPB Laager. |
| ORA-BST annexation war, from 1858, when BST does not hold Vrystaat | 60% BST Thaba Bosiu plus ORA Overreach; 20% BST Major Edge plus ORA Overreach; 20% ORA Laager. Per-key: Overreach 80%; Thaba Bosiu 60%; Major Edge 20%; Laager 20%. |
| Same annexation war, but BST already holds Vrystaat | 20% ORA Laager; 80% no modifier. The first two random branches still roll, but their internal ownership condition applies nothing. |

The first four events are scheduled behind AI-only gates, but their hidden events do not revalidate controller status when they fire 14 days later. A controller change within that window can technically cause an ostensibly AI-AI package to be applied after a country becomes player-controlled. The later ORA-BST annexation event does revalidate.

## 3. Blood River

### Dynamic AI-AI result

| Roll | Result |
|---:|---|
| 30% | ZUL receives no combat modifier and ORA is prevented from receiving Laager. ZUL instead gains +20 dynastic stability and +10 firearms progress. |
| 70% | ZUL receives -35% offence and defence for 9 months, while ORA receives Laager for 15 months. |

The 70% branch therefore simultaneously weakens ZUL and grants ORA the extreme Laager package.

### Controller-specific result

- AI ZUL receives War Readiness with 100% probability if either ORA or any living TRN is player-controlled. The TRN test does not require player TRN to be involved in the play.
- Player ZUL against AI ORA causes ORA to receive Laager with 100% probability.
- If TRN is player-controlled but ORA remains AI, ZUL can receive War Readiness while ORA also receives Laager. Assistance is then present on both sides.
- These controller-specific branches execute before the Dynamic AI-AI die and are not gated by the Frontier AI setting.

## 4. Swazi assistance

### Generic diplomatic plays

- If any player is an enemy of target SWZ, SWZ receives `sb_swazi_frontier_muster_vs_player` with 100% probability.
- In an AI-AI play not marked as the Zulu story war, SWZ receives standard `sb_swazi_frontier_muster` with 100% probability.
- Either muster route also gives SWZ 10,000 pounds.
- Neither generic route checks the Frontier AI game rule.

The two muster variants use different cooldown variables. If an AI-AI play first grants the standard muster and a player later joins against SWZ, the anti-player modifier can stack with it. The combined visible effects are +125% defence, +70% offence, +75% organization gain, +200% recovery, +200% training, and +50% subsistence output before force-floor assistance.

### Zulu-Swazi story war

When both ZUL and SWZ are AI, a successful contextual roll applies standard Swazi Muster and Zulu Disarray together.

| Prior Zulu outcome | AI chance to attack | Modifier chance if attacking | Overall chance from event |
|---|---:|---:|---:|
| Won Blood River | 80% | 20% | 16% |
| Lost Blood River | 100% | 80% | 80% |
| Honourable Natal deal | 20% | 60% | 12% |
| Guns sent south | 50% | 40% | 20% |
| No recognized context | 50% | 100% | 50% |

Player ZUL attacking AI SWZ instead triggers the stronger anti-player muster with 100% probability.

Strict-Historical uses the same contextual rolls. Because Strict AI-AI Blood River normally records a Zulu defeat, the resulting Swazi package is 80%, not the full defensive aid stated by the current game-rule description.

## 5. Basotho Gun War

- Player CAP launches the Gun War against AI BST: +50% BST defence for 24 months, with 100% probability.
- AI CAP launches against AI BST: a 66:33 weighted roll for +25% BST defence or nothing. The exact modifier probability is 66/99, or 66.67%.
- AI CAP has a separate 75% chance to choose the war option. From the arrival of the disarmament event, the unconditional probability of the standard modifier is therefore exactly 50%.
- Disabled suppresses the two Gun War defensive modifiers.
- Dynamic and Strict use the same probabilities.

BST also receives universal force-floor assistance. In the player-Cape case, the live package can therefore combine +50% defence, +1000 training, and the construction of missing military-building levels.

## 6. Universal AI force floors

Under Dynamic or Strict, every involved AI ZUL, SWZ, GZA, or BST has its military buildings restored to a scripted floor when a play starts, a participant joins, war begins, and during monthly wartime pulses.

| AI country | Barracks floor | Conscription-centre floor | Training modifier |
|---|---:|---:|---:|
| ZUL | 4 | 20 | +2500 |
| GZA | 4 | 14 | +2500 |
| SWZ | 1 | 4 | +2500 |
| BST | 1 | 14 | +1000 |

Probability is 100% whenever the country is eligible, regardless of whether its opponent is player or AI. The 3-month training modifier is refreshed during the conflict. The created building levels are permanent: conflict cleanup removes the training modifier but does not remove buildings.

## 7. Deterministic anti-player routes

| Player situation | AI recipient | Assistance | Probability |
|---|---|---|---:|
| CAP player accepts its opening event | XHO | Permanent +0.50 state conscription rate | 100% |
| ORA player at startup | MTB | Permanent +2.5 conscription, +2000 training, +50% offence, +150% defence | 100% |
| A player is an enemy of target SWZ | SWZ | Stronger anti-player Swazi Muster plus 10,000 pounds | 100% |
| Player ZUL at Blood River | AI ORA | Laager plus material relief | 100% |
| Player ORA or living player TRN at Blood River | AI ZUL | +15% offence and defence; +10% organization | 100% |
| CAP player chooses the Gun War | AI BST | +50% defence | 100% |
| TRN player opens the ZPB crackdown | ZPB | +500 training and +5% offence and defence | 100% |

## 8. Klip River rolls

These rolls use the same assistance modifiers but are neither AI-gated nor game-rule-gated. They apply equally to player and AI countries.

When the secession play starts:

- If ZUL has the scripted advantage - honourable Dingane plus a Zulu East Transvaal state - there is a 70% chance that KLR receives Laager while ZUL simultaneously receives its +10% muster.
- Without the advantage, the paired chance is 30%.
- The two modifiers are always awarded together.

For a punitive expedition:

- With the Zulu advantage: 60% ZUL muster.
- Without the advantage: 0%.

There is no single overall probability from the beginning of the Klip River chain because the preceding NAL, ZUL, and ORA AI-choice weights vary with relations, firearms, dynasty state, and territorial control.

## 9. Non-modifier assistance that compounds combat strength

The following effects are excluded from modifier probabilities but materially change battlefield strength:

- Swazi Muster grants 10,000 pounds.
- Player-ZUL Blood River can grant ORA one dragoon, 500 Boer officers, 5,500 Boer soldiers, 15,000 Sotho slaves, and enough barracks to reach level 5.
- AI TRN automatically joins the Blood River play, and Dynamic AI ORA is forcibly mobilized and committed to the Natal front.
- The 20% BST branch in the Dynamic ORA-BST return war creates 15,000 soldiers, 10,000 labourers, and 2,500 officers, and adds +50 firearms progress.
- Player-TRN ZPB crackdown grants ZPB 10,000 pounds, one line-infantry unit, and one dragoon.
- Force-floor building construction is permanent.
- Klip River County receives one dragoon, one irregular unit, and extensive population staging. This is story setup rather than controller-specific assistance, but it compounds the subsequent modifier roll.
- The separate AI Economy Helpers setting creates milestone buildings. It does not apply combat modifiers.

## 10. Game-rule coverage and defects

### Dynamic-Historical

Dynamic enables dated AI frontier wars, the AI-AI Blood River die, force-floor restoration, Gun War defence, and the Zulu-Swazi AI contextual roll. It does not control all player-specific assistance.

### Strict-Historical

Strict retains deterministic historical packages, removes several Dynamic outcome branches, and makes AI-AI Blood River apply both Zulu unpreparedness and ORA Laager. However, the Zulu-Swazi roll remains probabilistic despite localization stating that Swazi receive full aid.

### Disabled

Disabled reliably suppresses dated AI frontier wars, force-floor restoration, Gun War defence, and the AI-AI Zulu-Swazi contextual modifier roll. It does not suppress:

- generic Swazi target musters;
- player-facing Blood River packages;
- the remaining ORA Blood River Laager path in AI-AI play;
- Xhosa Warbands against player CAP;
- MTB Host against player ORA;
- ZPB assistance against player TRN;
- Klip River modifier rolls;
- Zulu AI authority.

The current Disabled description therefore overstates its effective scope.

## 11. Dormant definitions

The following definitions should not be counted as live assistance because the repository has no active addition path for them:

- `sb_native_conscription_MTB`
- `sb_trek_ai_mobilization`
- `sb_iron_age_natives`
- `sb_iron_age_weaponry`
- `sb_potgieter_relief`

`sb_iron_age_natives` is especially notable because its nearby comment calls it an active MTB tuning hook even though nothing applies it. `sb_trek_ai_mobilization` has removal logic but no corresponding addition site.

## 12. Overall assessment

The strongest balance problems are not merely the random probabilities. They are the magnitude and compounding of deterministic packages:

1. Laager grants casualty and supply immunity plus +125% kill rate.
2. Swazi anti-player assistance combines a very large tactical modifier, 10,000 pounds, and the universal force floor.
3. Player-ORA MTB receives a permanent +150% defence package.
4. Player-CAP Basotho can combine +50% defence with a 14-conscription-centre floor.
5. The 70% Dynamic Blood River loss branch applies a large penalty to ZUL and the full Laager package to ORA simultaneously.
6. The system remains explicitly controller-dependent despite the stated design direction that human-AI and AI-AI packages should be unified.

## Source map

- `common/game_rules/sb_game_rules.txt:1`
- `common/scripted_triggers/sb_game_rule_triggers.txt:1`
- `common/static_modifiers/sb_modifiers.txt:349`
- `common/static_modifiers/sb_conscription_modifiers.txt:1`
- `events/sb_frontier_ai_wars_events.txt:33`
- `events/sb_natal_crisis_events.txt:83`
- `events/sb_swazi_frontier_events.txt:70`
- `events/sb_bst_frontier_events.txt:350`
- `common/on_actions/sb_diplomatic_play_on_action_handlers.txt:1`
- `common/scripted_effects/sb_swazi_effects.txt:13`
- `common/scripted_effects/sb_bst_effects.txt:21`
- `common/scripted_effects/sb_natalia_effects.txt:319`
- `common/scripted_effects/sb_frontier_force_effects.txt:53`
- `common/script_values/sb_frontier_force_values.txt:1`
- `common/scripted_effects/sb_klip_river_county_effects.txt:259`
- `common/scripted_effects/sb_treaty_effects.txt:1274`
- `events/sb_cape_events.txt:38`
- `common/on_actions/sb_startup_on_action_handlers.txt:385`
- `common/scripted_effects/sb_zulu_dynasty_effects.txt:13`
