# Victoria 3 1.14.0 Open Beta 1 Runtime Matrix

Certification status: **not runtime-certified**. Every case below is unrun and remains `Engine pending`.

Runtime identity:

- Victoria 3 `1.14.0` Open Beta 1, runtime release identifier `release/1.14.x`
- Steam build `25081502`
- Steam branch `1.14-openbeta`
- core depot manifest `3868129321396195520`
- Spes Bona `0.20.0`
- Community Mod Framework `1.66.0`, commit `807c32ff42b75714a3a0e090c0db3357b5e46ed7`
- official CMF asset SHA-256 `79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b`

`Docs/compatibility/1_13_11_runtime_matrix.md` is preserved unchanged as historical evidence. None of its observations, and no stale log from that target, can pass an OB1 row.

## Evidence protocol

Before each run:

1. Recheck the installed Steam branch, build, and core depot manifest. Stop if the rolling beta no longer matches the identity above; do not test a later beta as OB1.
2. Confirm the enabled mod versions and exact load order. Use a fresh OB1 campaign unless a row explicitly asks for a save created earlier in the same OB1 test sequence.
3. Rotate `~/Documents/Paradox Interactive/Victoria 3/logs/error.log`, `debug.log`, and `game.log`. Do not append evidence to a pre-OB1 session.
4. Record the exact launch command or launcher action, UTC start/end timestamps, save name and checksum/load order, observed result, and SHA-256 of every retained log in the evidence ledger below.

A static test cannot pass a runtime row. An unrun row stays `Engine pending`. Any observed contract failure is `Fail — blocker`; it must not be relabelled pending. A row becomes `Pass` only when its acceptance condition and evidence record are complete.

## Carried-forward engine cases

These cases remain relevant from the historical matrix and receive new OB1 IDs.

| ID | Former ID | Scenario | Acceptance condition | Status |
|---|---|---|---|---|
| `OB1-CF-01` | `RV-01` | Cold-launch a fresh 1836 game with CMF 1.66.0 and SB 0.20.0, then save and reload. | The process identifies the exact OB1 build; no new parser, missing-scope, stale-JE, duplicate Situation-widget, or save/reload error appears. | Engine pending |
| `OB1-CF-02` | `RV-02` | Open Bechuanaland, inspect `com_container`, save/reload, replace an actor, then resolve or invalidate the story. | Exactly one `sb_bechuanaland_corridor_state` exists while active; scopes, lists, score, drift, JE handles, and title boxes survive reload; no container remains after terminal cleanup. | Engine pending |
| `OB1-CF-03` | `RV-03` | Exercise every Warren/Caprivi direct and proxy route, support/neutrality choice, back-down, white peace, negotiated peace, and mixed enforcement. | Intended participants and each scripted goal appear once; no self-transfer, invalid transfer, early terminal result, stranded phase, stale lease, or duplicate settlement occurs. | Engine pending |
| `OB1-CF-04` | `RV-04` | Establish, disband, and re-establish the Mozambique Company and a generic prestige-good company. | Vanilla HQ/assets remain valid, SB MZQ cleanup runs once, and Vanilla restores the eligible prestige-good JE once. | Engine pending |
| `OB1-CF-05` | `RV-05` | Inherit a hosted treaty port through revolution and conquest; test honour and revoke. | One inheritance prompt appears, the agreement follows the chosen outcome, and the treaty port reconnects to the correct market without SB duplication. | Engine pending |
| `OB1-CF-06` | `RV-06` | Test Cultural Supremacy with owned and unowned primary-culture homelands and neighbouring insurrectionary movements. | Radicalism retains all upstream scope fixes while CAP exclusions remain intact under CMF 1.66.0. | Engine pending |
| `OB1-CF-07` | `RV-07` | Open Stake Colonial Claim with and without sufficient interest. | The action is unavailable without the required interest and never opens an empty target picker. | Engine pending |
| `OB1-CF-08` | `RV-08` | Inspect country selection/history for XHO, CAP, and the retired XHG/XHR/XHT tags. | Retired tags are absent, XHO remains valid, and John Philip is created only through CAP's authoritative template. | Engine pending |
| `OB1-CF-09` | `RV-09` | Use SB-modified starting fleets for recruitment, embarkation, invasion, cancellation, rerouting, transfer, retrofit, and repair. | OB1 naval-network, pathfinding, transport, and Supply Ship rules work; no uncrewed mission, destroyed reroute, stuck repair, or 99% invasion occurs. | Engine pending |
| `OB1-CF-10` | `RV-10` | Run Tiger and review fresh `error.log`, `debug.log`, and `game.log`. | No new SB-authored error remains. External diagnostics and Tiger's currently incomplete 1.14 schema coverage are recorded with exact evidence rather than silently ignored. | Engine pending |
| `OB1-CF-11` | `RV-11` | Take the Pink Map decision before BC, while BC is active, and after invalid, British, Boer, exact-zero, and SWA outcomes. | The decision is disabled only while BC is active; pre-BC and invalid routes grant all three claims, Boer/zero grants Kazembe and Zambia, and British/SWA routes reach the recorded arbiter. Later BC rewards never duplicate a pre-BC basin package. | Engine pending |
| `OB1-CF-12` | `RV-12` | Resolve British and SWA Pink Map arbitration through outright acceptance, favour, rejection/back-down, and defiance, including a held event whose arbiter disappears. | Dynamic names and tooltips render; acceptance transfers the intended claim package, the favour transaction targets the saved arbiter, defiance preserves competing claims with the authored relation/aggression effects, and a missing arbiter falls back cleanly. | Engine pending |
| `OB1-CF-13` | `RV-13` | Let MZQ colonize a basin target, then form IBE from POR before and during the Pink Map lifecycle; save and reload both states. | Subject colonization enables the decision, claims remain on POR/IBE rather than MZQ, tag formation preserves pending state and claims, and no stale arbiter or hostility marker survives JE closure. | Engine pending |

## OB1 startup, parser, and UI

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-START-01` | Cold-launch the exact target with SB 0.20.0 and CMF 1.66.0; open the relevant journal, situation, diplomacy, treaty, and naval panels. | No SB/CMF database, parser, scope, missing-texture, duplicate-key, treaty, container, or GUI error appears; situations and progress bars render. | Engine pending |

## War timers, final predicates, and launch identity

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-WAR-01` | In a multi-goal territorial story war, timer-enforce one goal while the war continues; save/reload with its pending marker; flip the territory, flip it back, and end the war. | No terminal event, annexation, union, or story cleanup fires early. The final owner predicate selects one result exactly once after war end. | Engine pending |
| `OB1-WAR-02` | In Xhosa War 7, enforce `colonization_rights`, inspect the treaty/article, enforce the `break_enforced_treaties` mirror, save/reload, and end the war. | The final resolver follows the live treaty/article predicate; repeated or reversed enforcement causes no early or duplicate terminal outcome. | Engine pending |
| `OB1-WAR-03` | In ordinary Griqualand `.252` and `.253` routes, timer-enforce and reverse each safe Vanilla territorial goal while WBL is aligned with one side. Hold every assent-required claim/proxy objective occupied beyond 100 progress. Resolve return-only, revoke-only, and neither settlements. | Safe territorial mirrors remain in the same war; assent-required objectives never self-enforce; closure reconciles territory before applying each recorded claim removal. | Engine pending |
| `OB1-WAR-04` | Test a normal two-demand Griqualand settlement only while the counter-goal holder survives outside the transferred state. | Both accepted records are applied once in callback-independent order, with final territory first and claim removal second. | Engine pending |
| `OB1-WAR-05` | In CAP-refusal `.025` and hardline `.253`, attempt to let ordinary one-state WBL press its counter-demand while losing Griqualand West; then give synthetic WBL another state and repeat. | The UI/engine rejects the last-state dual with `WAR_PEACE_ANNEXED_COUNTRY_CANT_PRESS_WARGOALS`; the surviving-WBL synthetic dual records its counter before transfer and resolves once. | Engine pending |
| `OB1-WAR-06` | Use the non-hardline live-ORA-as-TRN-subject route. Add CAP's counter across holders and close each accepted-demand combination. | `can_add_for_other_country` permits the proxy counter; the durable record targets ORA's legal claim, not a fictitious TRN claim. | Engine pending |
| `OB1-WAR-07` | In both Natal and Martinus, occupy both opposing `sb_story_humiliation` objectives for at least 25 weeks. Resolve with initiator-only, target-only, neither, and both demands accepted. | Neither goal timer-enforces. The shared 0/1/2 truth table chooses one side, white-peace cleanup, or mutual stand-down exactly once; the dual grants no exclusive victory, annexation, or union. | Engine pending |
| `OB1-WAR-08` | Back down once as initiator and once as target before war in Natal, Martinus, Klip River, Gaza–Zulu, Swazi–Zulu, and Great Trek routes. Force each scripted launch to fail while an unrelated/old same-type play exists. | The exact non-backing side enters the route's terminal resolver immediately; no state waits for `on_war_end`; no goal/backer is added to the unrelated play; residual launch leases follow the documented retry or neutral-cleanup path. | Engine pending |
| `OB1-WAR-09` | Repeat capitulation, negotiated peace, and white peace across Natal crisis, British–Zulu annexation/handoff, Gaza–Zulu, Klip River, Martinus, Kimberley, Xhosa/frontier wars, Swazi/Zulu, Great Trek, BST, NRP boundary, and every Bechuanaland route including Warren and CAP–SGO total war. | Every dispatch requires its play type, exact primary participants, and saved authored-play identity. Timer callbacks are nonterminal, unambiguous final subject/owner predicates own the result, and each route resolves idempotently without unrelated-war cleanup. | Engine pending |

## Sequential `sb_griqualand_west.254`

The approved route is a two-stage three-party struggle. It does not restore the retired dead play and does not launch three simultaneous plays.

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-GQ-00` | Cold-load the database and traverse Griqualand presentation after retirement of `dp_sb_griqualand_revoke_claim`. | No definition, handler, localisation, missing-key, or UI residue refers to the dead play; no replacement launcher exists. | Engine pending |
| `OB1-GQ-01` | Start `.254` in hardline and non-hardline variants with direct ORA, live ORA as a TRN subject, and federated TRN. | Phase A creates exactly one orientation-correct CAP–Boer claim play and no WBL play. Hardline CAP initiates with no new GBR backer; otherwise the Boer side initiates and GBR backs CAP. The durable legal claim owner/party identities are correct. | Engine pending |
| `OB1-GQ-02` | During Phase A, occupy both claim objectives beyond 100; test both back-down directions, capitulation, and 0/1/2 accepted-demand closes. | Assent-required records do not timer-enforce. The close resolver records the non-backing side where applicable, mutates claims only once at close, then recomputes the live legal claims. | Engine pending |
| `OB1-GQ-03` | Save/reload during Phase A and during the one-day gap after Phase A. Close with exactly one legal claimant. | Global generation/phase/accepted state and refreshable party links survive. Exactly one `.261` and at most one Phase-B play are scheduled; `.260` cannot finalize in the gap. | Engine pending |
| `OB1-GQ-04` | Close Phase A once with both claims revoked, and once through a zero-demand white peace with both claims surviving while independent WBL owns Griqualand West. | Each route finalizes once with no Phase B and no invented winner. The white peace preserves both CAP and Boer claims plus WBL ownership. | Engine pending |
| `OB1-GQ-05` | Kill or invalidate each participant in turn; kill the prior `.261` host; let a Phase-A play escalate to war; then remove an exact acknowledged play without a normal close callback. | Loss of an obsolete claimant does not cancel a valid sole winner. Missing required winner/leader, newly subject WBL, or changed state owner takes the documented fallback. The elected monthly coordinator rebuilds state, never mistakes escalation for disappearance, and requeues `.261` only when required. | Engine pending |
| `OB1-GQ-06` | Enter Phase B with CAP, direct ORA, subject-ORA proxy, and federated TRN as sole winner in separate runs. | Exactly one fresh claimant-to-independent-WBL owner play appears. In the proxy, TRN is goal holder/leader, ORA joins its side and remains legal claimant/beneficiary, and no second TRN or ORA-held Vanilla return goal appears. | Engine pending |
| `OB1-GQ-07` | In Phase B, flip and reverse the ordinary return-state mirror; prove the ORA proxy has no timer enforcement; resolve return-only, revoke-only, zero-demand, forbidden one-state-WBL dual, and legal surviving-WBL synthetic dual. | Final ownership reconciles before WBL's accepted claim record. Zero demands change nothing without a prior timer result. The one-state dual is rejected; the synthetic dual records before transfer. Kimberley finalizes once. | Engine pending |
| `OB1-GQ-08` | Force a valid Phase-B creation failure, observe the seven-day bounded retry and fallback, save/reload, and exercise every terminal cleanup path. | One retry occurs, then fallback makes no scripted transfer. `.261` never re-grants/normalizes claims. Container, global phase/generation/accepted/retry flags, all leases, pending `.261`, independent-route marker, and hardline flag clear exactly once. | Engine pending |

## Subject restoration and revolutions

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-SUB-01` | For Vanilla dominion and each of the four self-directing SB types, start Independence and timer-enforce it; exercise capitulation and mirror restoration. | The mirror restores the exact former relationship, `side_switch = on_capitulation` behaves correctly, and no missing-goal error appears. | Engine pending |
| `OB1-SUB-02` | For Boer presidential union, Boer confederal partner, and Zulu chiefdoms, use third-party Liberate Subject and an overlord revolution. | Each exact custom relation is restored; the three locked types are forced into the overlord revolution and remain unable to start their own play. | Engine pending |
| `OB1-SUB-03` | Check revolution alignment and ordinary overlord-war participation across all seven SB types plus the Vanilla dominion override. | Only the exact three locked SB types are forced into the revolution; the four self-directing types are not. Both SB dominion variants still do not auto-join ordinary overlord wars. | Engine pending |

## Regional AI incorporation

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-AI-01` | For AI NAL, test recognized and colonial branches; full and split Zululand; above/below 100,000 population; adjacent/nonadjacent ownership; and with/without an authored story request. | Code-valid, affordable `STATE_ZULULAND` is selected under both caller branches without the bypassed content gates. A player NAL and wrong owner/tag/state retain OB1 behavior. | Engine pending |
| `OB1-AI-02` | Exercise NAL request/start/complete, owner loss and reacquisition, the one-day `.130` race, silent generic incorporation, completion replay protection, and save/reload. | Owner loss clears transient leases synchronously; stale `.130` is cleanup-only; an unfinished authored route can retry; the durable completed marker prevents replay; generic incorporation shows no story-specific conquest prose. | Engine pending |
| `OB1-AI-03` | Give AI CAP unincorporated Bechuanaland and Griqualand West under both ordinary and colonial/company caller branches. | Each code-valid, affordable state receives the authored priority and is selected/completed sequentially; the helper does not promise simultaneous commands or bypass engine affordability. | Engine pending |
| `OB1-AI-04` | Give AI ORA unincorporated Drakensberg; repeat with player, wrong-tag, wrong-owner, and unrelated-state controls. | AI ORA selects code-valid, affordable Drakensberg. Every negative control retains the byte-faithful OB1 path. | Engine pending |

## Map, pathfinding, and naval network

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-MAP-01` | Cold-load a fresh game on the structured merged spline, save, and reload. | No map, spline, travel-network, port-node, or save corruption appears. | Engine pending |
| `OB1-MAP-02` | Build/use rail and move HQ/front forces across Natal and Zululand. | SB's split-state anchors and OB1 pathfinding route correctly across both states. | Engine pending |
| `OB1-MAP-03` | At every changed Southern African port, recruit, crew, supply, embark, invade, cancel, reroute, transfer, retrofit, and repair. | Every port, including `STATE_LOURENCO_MARQUES.port = x54CDC5`, reaches a connected naval node and completes each operation without a stuck or invalid mission. | Engine pending |
| `OB1-MAP-04` | Spot-check OB1's Scania and French Low Countries/Picardy routes. | The structured merge retains the upstream geometry/anchor corrections outside SB's region. | Engine pending |

## AI, economy, treaty, and global ideology smoke

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-SMOKE-01` | Run observer cases for NAL incorporation, MZQ company/colonial incorporation, Boer and CAP construction, and partially employed buildings. Inspect state-value reasons and investment-pool use. | No SB override suppresses OB1 state-value reasons, construction budgeting, investment-pool use, or stable wage behavior. | Engine pending |
| `OB1-SMOKE-02` | In the ORA–ZUL route, create an unrelated goods transfer first, then the exact small-arms transfer; repeat with dead/missing ZUL. | Only a live, direction-correct `goods_transfer` with `input_goods = g:small_arms` deduplicates the authored firearms treaty. | Engine pending |
| `OB1-SMOKE-03` | Exercise CAP-only, ABY-only, both-qualified, neither-qualified, and prior-war-sequence frontier-war candidates. | Each event selects only a candidate satisfying the same technology and sequence predicate as its outer trigger; an unqualified ABY is never preferred. | Engine pending |
| `OB1-SMOKE-04` | With ship-transfer entitlement active, let AI offer an obsolete ship, inspect price/spam behavior, and combine the article with an SB compact before renewal/cleanup. If entitlement is unavailable, record that fact without passing the row. | OB1 ship transfer works and no broad SB matcher silently removes an unrelated mixed treaty article. Any observed matcher failure blocks release and remains registered under `OB1-01`. | Engine pending |
| `OB1-IDEO-01` | Start fresh ORA and TRN cases after Vanilla's global Landowners setup change. | Each receives the intended Landowners ideology; no SB shadow restores the superseded generic non-monarchy setup. | Engine pending |

## Names, assets, naval UI, and DLC controls

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-UI-01` | Exercise BIC's evaluated-actor name transition, SAF custom names, the Zulu chiefdom pact, Bechuanaland custom plays, and the registered TRN/Lourenço Marques/German Namibia naming gaps. | BIC evaluates `scope:actor`; SAF remains SB-authored; the chiefdom pact renders `puppet_15.dds`; no raw Bechuanaland key appears. Naming gaps are observed and recorded without changing their design. | Engine pending |
| `OB1-UI-02` | Open the ship panel and naval mission information throughout fleet operations. | OB1 naval UI and messages render without an SB-authored GUI or localisation error. | Engine pending |
| `OB1-UI-03` | Disable the relevant DLC and launch all seven exact image calls: `sb_klip_river_county.010` (`ep1_redcoats`); `sb_nam.140` (`votp_french_algeria`); `sb_natal_crisis.110` (`votp_gunboat_diplomacy`); `sb_natal_crisis.115` (`ep1_transfer_of_authority`); `sb_natal_interwar.005` (`ip4_colonial_exploitation_going_well`); `sb_natal_interwar.030` (`ep1_transfer_of_authority`); and `sb_pink_map.040` (`ep1_printing_press`). | Each image result and fresh error-log evidence is recorded. Do not replace DP-selected art from an all-DLC static guess; any missing asset remains an open finding until designed. | Engine pending |

## Multiplayer

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `OB1-MP-01` | With two clients, host and join once using Steam as the default backend and load identical SB/CMF checksums. If two clients are unavailable, record the limitation and leave the row pending. | Both clients join and load the same campaign without an SB/CMF checksum or backend error. Static tests alone cannot pass this row. | Engine pending |

## Run evidence ledger

Add one ledger row for every executed matrix ID. Keep raw rotated logs or a durable evidence path beside the hashes. A grouped run may cover multiple IDs only when each scenario and result is individually identifiable.

| Matrix ID(s) | UTC start/end | Exact launch command or launcher action; save; mod load order/checksum | Installed build/branch/depot and CMF identity | `error.log` / `debug.log` / `game.log` SHA-256 | Result and evidence path |
|---|---|---|---|---|---|
| — | — (not run) | — | — | — | All rows remain `Engine pending`. |
