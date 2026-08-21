# Spes Bona Audit Register Archive — Resolved Tickets

Closed records moved out of [audit_issue_register.md](audit_issue_register.md) on 2026-08-21. Everything below is implemented and verified; it is kept for provenance only. Open work (deferred gates and the FA audit round) lives in the live register.

## Rebase Resolution

| ID | Resolution | Evidence |
|---|---|---|
| `RB-01` | Cultural Supremacy is rebased from CMF 1.63.0 and reviewed against Vanilla 1.13.11 while retaining only CAP's exclusion. | CMF and Vanilla object hashes are pinned in the override inventory; regression tests cover the retained container/metadata contract. |
| `RB-02` | Descriptor, metadata, build, source paths, hashes, law/movement baselines, and compatibility documents now target 1.13.11 and CMF 1.63.0. The launcher relationship is pinned to `1.63.*`. | `check_override_inventory.py` rejects any target other than 1.13.11/build 24799966, CMF 1.63.0/`bd92022`, or the `1.63.*` launcher dependency range. |
| `RB-03` | Mozambique and De Beers were reviewed against their Vanilla 1.13.11 objects. Player requirements remain Vanilla; only the documented AI incorporation/weight and diamond deltas remain. | Inventory intent and hashes are explicit; SB registers one Mozambique disband handler and leaves Vanilla's prestige-good restoration hook intact. |
| `RB-04` | SB does not shadow or duplicate Vanilla's new treaty-port inheritance on-action. Historical treaty ownership remains an exact-path reviewed surface. | The validator pins `on_treaty_ports_inherited` and rejects any SB use of that hook or `renege_treaty_ports_with`; engine outcomes remain `RV-05`. |
| `RB-05` | Scripted war-goal blocks and subject-transfer packages were structurally audited. Bechuanaland participant lists and enforced-goal state now live in one container. | Validation requires holder, type, and target for every scripted war-goal block and currently finds 82 complete blocks; runtime combinations remain `RV-03`. |
| `RB-06` | Both military-formation exact-path files were reviewed against the unchanged 1.13.11 source baseline without altering intended SB force counts. | Source hashes are pinned; naval recruitment, transport, invasion, retrofit, repair, and rerouting remain `RV-09`. |

## Bechuanaland Container Migration

The active corridor story now has one authoritative container:

- name: `sb_bechuanaland_corridor_state`
- tags: `sb_story sb_bechuanaland_corridor`
- parent: `c:GBR`

It owns actors, influence, cached drift, route and phase state, leases, victory state, enforced goals, CAP's prewar subject type, pending settlement, the Boer network, and British subject targets.

Only the permanent eligibility, story-open, terminal-resolution, and Pink Map terminal-outcome envelope remains global. Country-local cooldowns and temporary modifiers remain country-local. Score changes perform one clamped mutation and one participant broadcast; the singleton monthly pulse calculates drift once.

The corridor is one contextless JE shared by all involved countries. SB projects the container's actor scopes and influence state directly onto that singleton JE, while CMF 1.63's title setters and International Situation widgets provide its presentation. The `1.63.*` launcher dependency makes this API contract explicit. The repository contains no SB journal GUI replacement, no gameplay `every_container` scan, no debug UI, and no release canary. CMF's `com_container` manager is the supported runtime inspector.

Static tests cover creation shape, parent/tags, container-owned shared state, variable lists, singleton-JE projection without global display scopes, and removal of obsolete migration variables. Save/reload and terminal destruction remain `RV-02`.

## Pink Map / Bechuanaland Cross-Content Audit

### BC-25 — Medium / resolved / design and runtime — The Pink Map is routed through the corridor settlement

**Resolution.** The Vanilla Portuguese Colonialism and Pink Map journal entries remain authoritative. A keyed replacement of the Vanilla `pink_map` decision adds only Bechuanaland routing and colonial-network eligibility, while dedicated follow-up events retain Vanilla's three-option arbitration and favour transaction with a dynamically saved British or SWA arbiter.

- A pre-corridor Pink Map grants POR/IBE the full Kazembe, Zambia, and Zambezi package and suppresses only those later BC basin rewards; Botswana settlement rewards remain unchanged.
- The decision remains visible but disabled during an active Corridor Question. Invalid or cancelled outcomes grant the full package; Boer and exact-zero outcomes grant Kazembe and Zambia while preserving the Boer Zambezi claim; British and SWA outcomes request permission from the terminal arbiter.
- BC teardown records one durable terminal outcome plus the actual basin claimant and, where needed, the British or SWA arbiter before destroying the active container. A missing arbiter falls back to direct Portuguese claims.
- Acceptance removes the recorded BC claimant's competing basin claims before granting all three claims to POR/IBE. Defiance preserves both claimants, applies `-50` relations, and gives the arbiter `+25` target aggression only while the Pink Map JE remains active.
- POR/IBE colonial and charter-company subjects, including MZQ, can satisfy the decision's colonization requirement. Pink Map claims remain on POR/IBE; the obsolete MZQ Zambezi-claim redirect is removed.
- A bounded POR/IBE strategy adds six desired naval units, 120 desired supply ships, `1.5` naval construction weight, and Kongo-specific pressure while Kongo retains Northern Angola and either Portuguese Colonialism or the Pink Map remains unresolved.

**Evidence.** `tests/test_pink_map_bechuanaland_integration.py` covers all decision routes, exact-zero handling, claim ownership, MZQ eligibility, arbitration bands, missing arbiters, and temporary hostility. The keyed decision object is pinned to Vanilla 1.13.11 in the override inventory. The complete validator targets Vanilla 1.13.11 and CMF 1.63.0. Engine-only arbitration, held-event, tag-change, and save/reload combinations remain part of the runtime matrix rather than being claimed by static analysis.

## Correctness And Cleanup Resolution

| Tickets | Resolution |
|---|---|
| `GP-20` | Stake Colonial Claim again requires sufficient top-level interest and cannot expose an empty target picker. |
| `GP-21` | Dormant XHG, XHR, and XHT definitions, histories, characters, flags, CoAs, and localisation were removed. XHO remains; CAP owns the sole John Philip template. |
| `SUP-03` | SGO uses valid named color `green_dark`. |
| `SUP-08` | Confirmed dead event art, JE art, wrappers, helpers, modifiers, triggers, and localisation were removed. `te_sgo_united_flag.tga` remains explicitly staged. |
| `SUP-09` | Duplicate `Spies` localisation and active formatting defects were removed; localisation structure is validator-owned. |
| `TOOL-06` | Obsolete Bechuanaland migration variables and the unused Imperial Confederation scope were removed rather than allowlisted. |
| `TOOL-07` | Flag, travel-time, MZQ, Mozambique, override, and third-party compatibility documentation now describes the live implementation. |
| `PERF-08` | Fixed-tag Boer restraint uses direct optional tag scopes plus an annual recovery watchdog; no recurring `every_country` scan remains. |
| `PERF-12` | Frontier eligibility, mineral one-shots, CAP conversion, ORA refresh, and recurring pulse ownership are singular; the empty Namibia yearly handler is absent. |
| `QUAL-06` | `unused_symbol_allowlist.json` and its generated report classify the three legitimate definition-only engine entry points; accidental dead scaffolding was removed. |
| `QUAL-07` | Rebased overrides and shared lifecycle helpers now carry precise source/delta or ownership comments without renaming stable public keys. |
