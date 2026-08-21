# Spes Bona Audit Closure Register

Last refreshed: 2026-08-21

Repository baseline: `de97d34cb1776bfbe804bf524d8d9815ef55b2d7`

Target: Victoria 3 `1.13.11`, Steam build `24799966`, Vanilla checksum `a47f`

Dependency baseline: Community Mod Framework `1.63.0`, commit `bd92022`

## Status

Open work is tracked in this register: the six explicit blocked, human-review, or content gates in `tools/deferred_release_gates.json`, and the FA-round findings below. Strict release certification remains contingent on the engine-only cases in `Docs/compatibility/1_13_11_runtime_matrix.md`; those cases cannot be certified by static analysis and are not marked as passed here.

Closed tickets — the rebase resolutions, the Bechuanaland container migration with BC-25, and the correctness/cleanup batch — are archived in [audit_issue_register_archive.md](audit_issue_register_archive.md) for provenance.

## Deferred Gates

The machine-readable authority is `tools/deferred_release_gates.json`. Each entry records owner, unblock condition, artifact, and acceptance test.

| ID | Status | Owner | Gate |
|---|---|---|---|
| `BC-20` | Blocked | Spes Bona content design | Broader CAP/GBR restraint duration and war behavior waits for the Southern African wars redesign. |
| `BC-22` | Deferred human | Depro | Remaining Bechuanaland prose is reviewed during in-game testing. |
| `CP-07` | Blocked | Spes Bona compatibility | A dedicated Hail Columbia Legacy Slavery compatibility patch is still required; SB must currently load after Hail Columbia. |
| `SUP-05` | Blocked | Depro | Spline regeneration waits until the release map stack is frozen. |
| `QUAL-09` | Deferred human | Depro | Remaining event prose requires a rolling historical-tone and presentation review. |
| `CONTENT-01` | Deferred content | Spes Bona content design | Transvaal and Orangia gold balancing belongs to the next resource-content pass. |

Preserved user notes:

- `BC-20`: "Move to blocked, further content (esp SAn wars) are needed. Also add CAP to this befriend strategy towards the boers, otherwise a responsible one can override."
- `BC-22`: "### TO REVIEW ### only applies to localisation blocs, remove those outside this. Then move this to deferred. This must be done by a human (me), I do it on a rolling basis when I come across the events in-game while testing."
- `SUP-05`: "This you cannot fix, I've been delaying fixing this bug bc spline changes are not compatible across mods. I will fix it near release. You can mark this as low / blocked."

`BC-20` immediate mitigation remains active through source-tracked `befriend` goals for GBR and CAP. The separate **Respect the Boer Conventions** diplomatic AI strategy was removed so this mask no longer consumes either country's diplomatic-strategy slot; the deferred gate now covers only the eventual duration and war-specific behavior redesign.

## Validation Contract

Current static evidence (2026-08-21; corrected during the FA round — the previous entry still said 126 tests, 14/14 categories, 102 keyed overrides, and 17 state-region blocks):

- `139` unit tests pass.
- The integrated validator passes `13/13` categories with `0` failures.
- The override comparison reports `36` exact-path files, `103` keyed overrides, `18` changed state-region blocks, and `0` `replace_path` directives.
- Tiger passes against the installed `1.13.11` game data.
- Localisation structure passes with `91` reviewed and `143` still assigned to human review.
- The delayed-event lifecycle inventory and all `84` scripted war-goal blocks pass their structural checks.
- `git diff --check` passes.

Run:

```sh
python3 -B tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/Community Mod Framework' \
  --tiger
git diff --check
```

The suite checks unit tests, exact-path and keyed overrides, game/build/dependency metadata, CMF and Vanilla API surfaces, map connectivity and generated assets, localisation structure, on-action routing, stale and unused symbols, delayed-event lifecycle, deferred gates, and 1.13.11 release invariants.

Release support becomes strict only after every engine case in the runtime matrix is recorded as passing and fresh launch logs contain no new SB-authored errors. Fresh starts are authoritative; active 1.13.9 corridor crises are not migrated.

## Full Repository Audit — 2026-08-21 (FA round)

Method: four parallel read-only audit tracks (script integrity, engineering/consistency, semantic drift, historical accuracy) plus direct tooling verification against the working tree at `de97d34`. Every medium-or-higher claim was re-verified against source before inclusion. This section records findings only; no repository content outside this register was changed.

### A. Documentation And Narrative Drift

| ID | Sev | Finding | Evidence / Direction | DP Notes |
|---|---|---|---| --- |
| `FA-01` | Medium | `Docs/resource_balance_summary.md` claims Griqualand West's "later iron unlocked by technology"; no such mechanism exists anywhere in the repo. | `STATE_GRIQUALAND_WEST` carries only `building_iron_mine = 1`; no tech/trait/building-group gating exists. Delete the clause or implement the unlock. | _Tech does unlock extra iron, dynamite and iirc pumpjacks do so. Flagged for rechecking._ |
| `FA-02` | Low | README lists ABY under "custom startup work", but ABY has no startup presence: no history country file, no startup on-action, no starting states. It is a mid-game emergent tag (Albany secession). | Reword the bullet to "emergent mid-game tags" for ABY. | |
| `FA-03` | Low | README's "British ultimatum and annex-war follow-through" overstates: the ultimatum-refusal path creates `dp_make_protectorate` plays; the only `dp_annex_war` is GBR→ZUL after the Port Natal raid. | Reword to "protectorate-play follow-through" or change the war goal. | |
| `FA-04` | Low | README's day-0 firearms JE scope (ZUL/SWZ/GZA) omits BST and NGN, which `sb_is_firearms_acquisition_country` also covers. | Update the README list (feature is broader than documented). | |
| `FA-05` | Low | Metadata short_description: "21 journal entries" vs 22 SB JE definitions (plus 3 vanilla JE overrides); "content for every SA nation" is overbroad — ORL/SAN/NAM/STA/QWA receive startup data only. | Update count; soften the coverage claim. | |
| `FA-06` | Low | `resource_balance_summary.md` says Namaqualand arable 4; live value is 5. | Sync the doc. | |
| `FA-07` | Low | Hereroland consolidation tooltip says "at least 80%" of passable provinces; script requires 68 of 88 (≈77%). | Raise the trigger to 71 or reword the tooltip; recheck after the impassable-mask WIP changes. | _recheck this_ | 
| `FA-08` | Low | Comment drift: Cape JE header says timeout "by 1880" while code and loc say 1885; the favour-liberals button comment names Petty Bourgeoisie while the modifier touches Intelligentsia/Rural Folk. | Fix both comments. | _code => comments._ |
| `FA-09` | Low | `override_manifest.md` says `00_relations.txt` "removes only ORA's relation to TRN", but a second `c:TRN` relation row (line 348) and an entire `c:TRN` block (line 371, with a duplicated SWZ `-25`/`-10` pair where the second silently overwrites the first) remain. | Prune the dead rows or document them; dedupe the SWZ pair. | _elaborate?_ |

### B. Script Bugs And Dead Content

| ID | Sev | Finding | Evidence / Direction | DP comments |
|---|---|---|---|---|
| `FA-10` | High | `je_sb_griqualand_west_question` is defined but never added anywhere: its gate variable is set at `sb_griqualand_west_effects.txt:242` with no `add_journal_entry` following, so the Kimberley-dispute JE can never appear in game. | Add the guarded `add_journal_entry` where the variable is set, or remove the JE. | _think this was wip that was dropped_ |
| `FA-11` | Low | `tools/delayed_event_lifecycle_manifest.json` lists `sb_boer_republics.122`, but both the event block and its only `trigger_event` are commented out. The lifecycle check is one-directional and does not catch this. | Drop the id or restore the event; consider extending the check. | _think this event was going to be an on start event? But can del. for now and flag this (having start events for the content tags) as todos_ |
| `FA-12` | Low | 13 orphaned event-option loc keys after refactors: `sb_martinus_confederation.042/.044–.048` option keys while the events deliberately reuse `.041.a/.b`; `sb_boer_conventions.150.b` ("Back down.") is unused — possibly a lost option. | Point variants at their own keys or delete stale ones; decide whether .150 should offer the back-down choice. | _sb_boer_conventions.150.b can likely be dropped_ | 
| `FA-13` | Low | `sb_bechuanaland_influence_bar_visible_sgui` (scripted GUI) is referenced nowhere — no gui file, no loc `GetScriptedGui` call. | Wire it into the bar tooltip or delete it. | _seems like legacy, delete_ |

### C. Engineering Practice And Consistency

| ID | Sev | Finding | Evidence / Direction | DP comments |
|---|---|---|---|---|
| `FA-14` | Medium | Override-contract blind spots: additive `zz_sb_portuguese_kongo_secret_goal.txt` is unregistered, and all 7 `localization/english/replace/` files sit outside the inventory, although the manifest promises it "records every exact-path collision and keyed override". Root cause: `check_override_inventory.py` only detects `REPLACE:/TRY_REPLACE:/REPLACE_OR_CREATE:` directives. | Register both surfaces (explicit ADD/no-upstream classification for the former; a localization section for the latter) and teach the checker to flag unregistered `zz_*` files. |
| `FA-15` | Medium | AGENTS.md requires "every commit must include an appropriate mod-version update", but 141 of 198 commits touch no version file; practice is batched dedicated bump commits (0.14.0, 0.19.0 — including this refresh's own 13-commit batch). Nothing enforces the rule. | Either amend AGENTS.md to describe batched pre-release bumps, or add a CI check comparing descriptor version across commits. | _this is partially due to it coming in later as engineering practice. The rule should be smt like: 'Major on DP saying so, minor for significant thematic content / eng. work (e.g. colonial natal ), patch for tweaks / elaborating on thematic content bloc (e.g. the state split) ' or smt. High quality engineering practice._ |
| `FA-16` | Medium | A stale pre-split worktree copy lives inside the mod folder (`.claude/worktrees/adoring-poincare-a12afa`, 319 files, including a `state_regions` file with no `STATE_NATAL`). It poisons greps and tooling and would ship in any zip-built release. Engine impact is unverified — Jomini is believed to scan only known top-level dirs, so nested dot-dir loading is unlikely but unconfirmed. | Delete the worktree (git-ignored, so no history impact); never keep worktrees inside the mod dir. | _remove it_ | 
| `FA-17` | Low | Test coverage gaps: 8 event namespaces have zero test references (`sb_boer_compacts`, `sb_frontier_ai_wars`, `sb_gaza`, `sb_griqualand_east`, `sb_griqualand_west`, `sb_swazi_border`, `sb_swazi_frontier`, `sb_zulu_court`), and ~20 `common/` subdirs (buildings, cultures, game_rules, script_values, subject_types, technology, diplomatic_plays, war_goal_types, …) have no direct tests. | Add smoke-contract tests for the uncovered chains and data domains. |
| `FA-18` | Low | BOM deviations from the dominant convention (241/243 in `common/`): `common/named_colors/sb_country_colors.txt`, `common/coat_of_arms/coat_of_arms/sb_namibia_countries.txt`; `map_data/province_terrains.txt` is BOM-less — verify that is intentional vanilla byte-parity. | Re-encode the two `sb_` files; document the province_terrains decision. |
| `FA-19` | Low | Trailing whitespace in 7 files (e.g. `sb_cape_buttons.txt`, `sb_modifiers.txt`, `zz_sb_armed_forces_override.txt`, three event files) — the repo's own contract runs `git diff --check`. | Strip; consider a CI guard. |
| `FA-20` | Low | Indentation outliers vs the tab convention: `zz_sb_dynamic_state_names_southern_africa.txt` and `sb_zulu_dynasty_characters.txt` are space-led; `zzz_sb_cape_political_movement_overrides.txt` and the `00_relations.txt` shadow are mixed. | Normalize to tabs; exempt generated files. |
| `FA-21` | Low | Two unreferenced backup binaries are tracked (`Docs/compatibility/backups/*.splnet`, ≈3.3 MB combined). | Reference them as provenance from the map-connectivity docs or drop them. | _drop or move to outer repo_| 
| `FA-22` | Low | Small hygiene items: empty untracked `gui/` directory; deferred gate CP-07's artifact path is stale (`zz_sb_slavery_law_override.txt` → actual `02_sb_inboekstelsel_slavery.txt`); `government_types` uses `00_sb_` naming instead of `sb_`. | Fix path; remove dir; naming is an edge to note in the policy. | _maybe put naming conventions in test suite_ |

### D. Historical Accuracy

| ID | Sev | Finding | Evidence / Direction | DP comments |
|---|---|---|---|---|
| `FA-23` | Medium | QWA "Qwabe" is an invented 1836 polity: the chiefdom was destroyed/absorbed by Shaka c.1819-20, and its heartland lay north of the Tugela; QWA nonetheless holds 11 of 13 Natal provinces. File comments acknowledge the Phase-1 buffer-design intent, so this is a conscious abstraction with a misleading historical label. | Rename/reframe as a generic southern-Nguni refugee-chiefdom abstraction (Thuli/Cele/Nyuswa milieu) or make it a ZUL tributary/claim rather than a sovereign state. | _More research is needed here before action is taken. Want a clearer picture of the players in Natal state in 1836. afaik wasn't directly controlled by the zulus but rather a 'sphere of influence'. If need be we can have multiple tags in the state, but as it's small I think one would be best._ | 
| `FA-24` | Medium | MTB (Mzilikazi's Ndebele) start territory over-extends far beyond the Marico heartland: all of STATE_TRANSVAAL plus parts of Northern/Eastern Transvaal and western Vrystaat. Zoutpansberg and the eastern escarpment were never Ndebele-ruled. The post-Vegkop exodus modeling itself is historically coherent. | Trim MTB to the western Transvaal/Marico zone plus raid-tribute fringe; consider Venda/Pedi/Swazi ownership for the fringes. | _Evidence this and write up a proposal_ | 
| `FA-25` | Medium | The Sand River (`sb_boer_conventions.140`) and Bloemfontein (`.141`) chains quote fixed dates (17 January 1852 / 23 February 1854) in their localisation but fire on consolidation variables with no `game_date` floor — a player unifying the republics in the mid-1840s gets an "1852" convention a decade early. | Add `game_date >= 1852.1.1` / `>= 1854.1.1` to the fire limits. | _no fixed dates, the quotes are historical flavour. SB's principle in general is mechanically driven over date driven. Drop issue._ |
| `FA-26` | Low | Kimberley diamonds are gated only on era-2 technology (`mechanical_tools`/`dynamite`) with no date floor — roughly a decade before the 1866-71 discoveries. Start-state handling is otherwise correct (no diamond potential at start). | Add `game_date >= 1866.1.1` to the yearly-pulse gate. | _See previous comment. Based on tech progression v. unlikely that (ai) WBL manages to research mechanical tools much before then. Drop issue._ |
| `FA-27` | Low | The 9th Xhosa War window opens at `game_date >= 1870.1.1`; the Ngcayechibi war was 1877-79. War numbering itself matches standard historiography. | Move the gate to ≥1877 (or 1875 for buildup). | _Support move to '75_ | 
| `FA-28` | Low | Character data fixes: H.E. Göring birth 1838.10.31 → 1839.10.31; Godlonton SAF override uses 1794.1.1 vs real 1794.9.24 (and `historical` flag disagrees between the two templates); the Gqugqu claimant is marked `historical = yes` but appears in no standard list of Senzangakhona's sons; SWZ comment "Sobhuza II (d. 1839)" should read Sobhuza I. | Apply the four data corrections. | _Gqugqu afaik allegedly was a half-brother irl purged in '43. Otherwise seems fine, just triple check these._ |
| `FA-29` | Low | Naming/prose: "Klip River County" is the later British county name — the 1846-48 polity is historiographically the "Klip River Republic"; "Truimph over Britain" typo in Bechuanaland loc; Natal whaling cap 4 is generous for the era (suggest 1-2); GZA capital at Lourenco Marques is a map constraint worth a comment. | Text/cap tweaks. | _For the whaling compare to vanilla (globally) whaling vs historical outputs. Update accordingly_ |
| `FA-30` | Low | Coverage gaps: Faku (Mpondo), Maharero kaTjamuaha, Tjamuaha, and Nicolaas Waterboer are absent despite events quoting Griqua declarations; Cape governor succession 1838-61 (Napier, Maitland, H. Smith, Cathcart, Grey) is unmodeled; the ORA-BST annexation-war anchor 1856.8.4 matches no standard date (1858.3.1 suggested); the Namibia chain lacks a Walvis Bay 1878 anchor and opens the German window early (1870/1875 vs 1883-84). | Add or consciously abstract; note abstractions in comments. | _Characters make a register of todo characters state why (back with evidence), and suggestions; this will be for a later pass. ORA-BST war can push to historical date. Walvis bay does exist as CAP owned. Namibia early window is to allow for colonisation mechanic, drop as issue._ |

### Verified Clean In This Round

- Cross-reference resolution: 625 scripted effects, 266 scripted triggers, 85 on-actions, 266 events, all JE-id references, 74 character templates, 465 country tags, and 266 static-modifier usages resolve against mod + installed dependencies; the only dangling items are FA-10 through FA-13.
- Natal/Zululand split data is fully consistent: state-region membership matches the 13+9 province brief, ownership covers every province exactly once, pops/buildings history contain no misfiled provinces, and all `set_owner_of_provinces` lists use provinces of the correct state.
- Historical spot-checks passed: Retief → Blood River → Natalia causal order (16 December 1838 was a Sunday, matching the quoted journal), Xhosa war numbering, Basutoland protection gate 1868.5.1, Rudd → Charter → Pioneer Column sequence, Rehoboth trek window 1867-71, the Cattle-Killing anchor (≥1856.4.1), and roughly 35 character birth dates.
- Tooling and hygiene: map-connectivity, rhodesian-venture, and unused-symbol manifests hash-match disk; all README/Docs relative links resolve; CI runs the validator; no stale 1.13.9/1.13.10/CMF-1.6x references in live content; LF line endings and final newlines throughout; no tracked junk; `anz_POP_NOT_T5` was confirmed present in the ANZ flavour pack, clearing the one cross-mod loc suspicion.
- Localisation numeric spot-checks: 16 sampled tooltips match their scripted values; the only mismatch is FA-07.

Register refresh corrections applied in this edit: baseline/date updated to `de97d34` / 2026-08-21, and the Validation Contract counts corrected (139 tests, 13/13 categories, 103 keyed overrides, 18 state-region blocks). `RB-05`'s historical "82 complete blocks" predates the current count of 84; the row is preserved in the archive.

### FA Round Outcomes (worked 2026-08-21, after DP review)

| ID | Outcome |
|---|---|
| `FA-01` | **Withdrawn — finding was wrong.** Recheck found the mechanism already exists in `sb_mineral_discoveries_on_actions.txt`: Griqualand West starts with 1 iron cap and gains staged potential on nitroglycerin (+4), dynamite (+5; dynamite requires nitroglycerin, so an owner at dynamite sits at 1+4+5 = 10) and pneumatic tools (+10). Matches DP's in-game observation. |
| `FA-02` | **Fixed.** README now lists ABY as an emergent mid-game tag with lifecycle scripting, not startup work. |
| `FA-03` | **Fixed.** README now says "protectorate-play follow-through". |
| `FA-04` | **Fixed.** README firearms scope now reads ZUL/SWZ/GZA/BST/NGN. |
| `FA-05` | **Fixed.** Metadata short_description now says 22 journal entries, 250+ events, deep content for the major powers. |
| `FA-06` | **Fixed.** resource_balance_summary Namaqualand arable corrected to 5. |
| `FA-07` | **Fixed.** Trigger raised from 68 to 71 provinces (80.7% of the current 88 passable), so the "at least 80%" tooltip is true under the present impassable mask; re-review still owed when the mask leaves WIP. |
| `FA-08` | **Fixed.** Comments updated to match code (Cape JE timeout 1885; favour-liberals comment now names Intelligentsia +10% / Rural Folk -1 approval). |
| `FA-09` | **Elaborated.** See note below the table. |
| `FA-10` | **Fixed.** Dropped-WIP chain removed end to end: JE definition, its five localisation keys, the `set_variable` block in `sb_kimberley_discover_diamonds`, both `remove_variable` cleanups, and the `resolved_var` set in `sb_griqualand_west_mark_resolved`. No references remain. |
| `FA-11` | **Fixed + flagged.** Phantom `sb_boer_republics.122` removed from the lifecycle manifest. New follow-up TODO recorded below: content tags currently lack on-start events. |
| `FA-12` | **Fixed.** All 13 orphaned option keys deleted, including `sb_boer_conventions.150.b` per DP. Variant events' deliberate reuse of `.041.a/.b` untouched. |
| `FA-13` | **Fixed.** Legacy scripted GUI deleted together with its unused-symbol allowlist entry (the validator rejects stale entries, so they go as a pair). |
| `FA-14` | **Open (backlog).** Extending `check_override_inventory.py` to classify additive `zz_` files and localization `replace/` files is engineering work for a maintenance pass. |
| `FA-15` | **Fixed.** AGENTS.md versioning policy rewritten to DP's rule: major only on DP's say-so; minor for significant thematic content or engineering work; patch for tweaks/elaboration within an existing thematic bloc plus fixes/balance/localisation/maintenance; related commit batches may share one bump applied before push. |
| `FA-16` | **Fixed.** Stale worktree `.claude/worktrees/adoring-poincare-a12afa` deleted (git-ignored; no history impact). |
| `FA-17` | **Open (backlog).** Smoke-contract tests for the 8 uncovered event namespaces and untested data domains remain future work. |
| `FA-18` | **Fixed.** BOM added to the two `sb_` files. `map_data/province_terrains.txt` verified against installed vanilla: vanilla is also BOM-less, so the SB override intentionally matches upstream convention; content differs by design and stays hash-pinned. |
| `FA-19` | **Deferred.** Several whitespace-flagged files are hash-pinned overrides (`zz_sb_armed_forces_override.txt`, `00_relations.txt`); stripping them requires coordinated inventory-hash regeneration, so it waits for a dedicated maintenance pass. |
| `FA-20` | **Deferred.** Same pinning complication as FA-19 — the space-indented outliers are overrides whose bytes are pinned upstream. |
| `FA-21` | **Fixed.** Both backup binaries moved out of the repo to `../References/spline_network_backups/`. |
| `FA-22` | **Fixed.** CP-07 artifact path corrected to `common/laws/02_sb_inboekstelsel_slavery.txt`; empty `gui/` directory removed. Naming-convention test suite idea noted as optional follow-up. |
| `FA-23` | **Research delivered — decision pending DP.** `../References/natal_1836_polities_research_brief.md`: the region was a raid-sphere of Zululand, not an administered possession; recommendation is one tag renamed away from "Qwabe" (e.g. Thuli / Southern Nguni Chiefdoms), zulu-culture decentralized, ZUL claim/homeland framing instead of subject type. |
| `FA-24` | **Research delivered — decision pending DP.** `../References/mtb_territory_proposal.md`: Ndebele rule was the Marico core plus a tribute belt; tiered trim proposal (26-province full trim or 9-province minimal trim) preserving every Vegkop event input province. |
| `FA-25` | **Dropped per DP.** Mechanically driven over date driven; quoted dates are historical flavour. |
| `FA-26` | **Dropped per DP.** Tech-gated progression makes an early discovery unlikely; no date floor wanted. |
| `FA-27` | **Fixed.** 9th Xhosa War gate moved to `game_date >= 1875.1.1` per DP. |
| `FA-28` | **Fixed.** Göring birth corrected to 1839.10.31; Godlonton SAF override to 1794.9.24; Sobhuza II comment corrected to Sobhuza I. Gqugqu kept `historical = yes` per DP's recollection of a purged half-brother (standard son-lists omit him; treat prose carefully). Fairbairn's placeholder 1794.1.1 remains a known minor. |
| `FA-29` | **Partially fixed.** Natal whaling cap reduced 4 → 2 (vanilla global mode is 2–4; Natal shore whaling was small and transient). "Truimph" typo fixed. GZA capital abstraction documented in-file. KLR display-name question deferred — the naming reaches loc, flags, file names and tests, and DP has not asked for the rename. |
| `FA-30` | **Mixed.** Character backlog written to `../References/character_todo_register.md` (Faku, Maharero, Tjamuaha, Nicolaas Waterboer, Cape governor succession — each with evidence and suggestions) for a later pass. ORA-BST annexation-war anchor moved to the historical 1858.3.1. Walvis Bay part dropped (already CAP-owned). Namibia early-window part dropped per DP (colonisation mechanic needs the window). |

**FA-09 elaboration.** `common/history/diplomacy/00_relations.txt` is an exact-path shadow of
Vanilla's relations file. Its manifest entry claims only ORA→TRN was removed (TRN does not
exist at start, so the upstream row would target an invalid country). That same logic applies
to rows the file still carries: line 348 sets a relation *to* `c:TRN`, and lines 371–373 keep
an entire `c:TRN ?= { ... }` block that can never run, for the same reason. Inside that dead
block SWZ receives two contradictory `set_relations` calls (`-25`, then `-10`), the second
silently overwriting the first — evidence the block was edited without being re-read. The code
is inert rather than harmful; the fix is either to prune the dead rows in the next rebase of
this shadow (preferred — it shrinks the reviewed diff surface) or to document them as
deliberately retained.

**New follow-up TODO (from FA-11).** Content tags currently have no on-start events; if DP
wants each content tag to open with a flavour/setup event, add one per tag in a future minor
pass (candidates: BST, NGN, SWZ, GZA, ORL, ABY-on-emergence).
