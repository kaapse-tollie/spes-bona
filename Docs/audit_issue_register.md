# Spes Bona Open Audit and Victoria 3 1.13.10 Rebase Register

**Last refreshed:** 2026-08-12

**Repository baseline:** `7b31d36f188c6decb9b0361c8980914384f32d68`

**Previous game target:** Victoria 3 `1.13.9`, Steam build `23897342`

**Rebase target:** Victoria 3 `1.13.10` (Matcha), official Vanilla checksum `2964`, Steam build `24689003`

**Dependency under review:** Community Mod Framework `1.60.3` installed; SB inventory still labels `1.58.2`

**Official notes:** [Paradox forum](https://forum.paradoxplaza.com/forum/threads/hotfix-1-13-10-is-now-live-not-for-problem-reports.1938098/) · [official Steam announcement](https://steamcommunity.com/games/529340/announcements/detail/708906085669404697)

## Purpose and status

This is the live, forward-looking register. Completed tickets have been removed; Git history retains their rationale, fixes, and validation evidence. The document now contains only:

1. work required to rebase Spes Bona onto Victoria 3 `1.13.10`;
2. unresolved, blocked, or human-owned repository work; and
3. runtime verification that must be completed against the new target.

The `1.13.10` rebase is **not complete**. The installed game is confirmed as `release/1.13.10`, but SB metadata and compatibility locks still target `1.13.9`. No Victoria 3 process was launched for this refresh.

### Labels

- **Rebase gate:** must be completed before SB may claim `1.13.10` support.
- **Runtime check:** static evidence cannot certify the engine outcome.
- **Open:** actionable repository work with no external blocker.
- **Blocked:** intentionally waits on another content or release boundary.
- **Deferred / human:** deliberately owned by a later manual review.
- **Low:** useful cleanup that is not part of the immediate `1.13.10` release gate unless a rebase check promotes it.

Severity order remains **Very High → High → Medium-High → Medium → Low**. Severity and status are independent.

### Active inventory

| Workstream | Count | Items |
|---|---:|---|
| `1.13.10` rebase gates | 6 | `RB-01`–`RB-06` |
| Existing blocked/deferred work | 5 | `BC-20`, `BC-22`, `CP-07`, `SUP-05`, `QUAL-09` |
| Existing open Low cleanup | 11 | `GP-20`, `GP-21`, `SUP-03`, `SUP-08`, `SUP-09`, `TOOL-06`, `TOOL-07`, `PERF-08`, `PERF-12`, `QUAL-06`, `QUAL-07` |
| Planned content, not a rebase gate | 1 | `CONTENT-01` |

### Rebase execution order

1. Merge the upstream Cultural Supremacy fix without losing CMF or Cape behavior (`RB-01`).
2. Repoint and strengthen compatibility metadata and locks (`RB-02`).
3. Review the company, treaty-port, and subject/war-goal paths changed by the hotfix (`RB-03`–`RB-05`).
4. Run the complete static gate and triage only new diagnostics.
5. Run the `1.13.10` engine matrix, including the naval behavior checks in `RB-06`.
6. Only then declare `1.13.10` support in release-facing metadata.

---

## 1. Victoria 3 1.13.10 rebase gates

### Confirmed upstream and dependency baseline

The official notes state that `1.13.10` is a delta from `1.13.9`. The changes most relevant to SB are:

- the Cultural Supremacy movement fix for radicalism from unowned homelands;
- duplicate war-goal prevention and subject-transfer self-target protections;
- treaty-port inheritance, the new `on_treaty_ports_inherited` on-action, and `renege_treaty_ports_with`;
- restoration of generic-prestige-good journal entries after company disbandment;
- changed naval invasion, Supply Ship, visibility, embarkation, repair, and retrofit behavior; and
- new target-involvement prediction UI.

The new `create_container` scripting facility is opt-in and requires no migration by itself. SB has no direct Japanese-template, River of Coffee, or Coffee with Milk override, so those hotfix items need only the normal smoke test.

The current installed-source comparison found no SB-side hash drift. Of the inventoried surface:

- all **35** exact-path file sets remain present, and every current Vanilla/mod hash still matches the inventory;
- all **100** keyed override sets remain present, and every mod object hash still matches;
- all **17** changed state-region blocks remain the declared set;
- the approved and actual `replace_path` sets remain empty; and
- all five CMF-derived movement baseline file/object hashes still match, despite the installed CMF version changing to `1.60.3`.

Only one inventoried Vanilla object has a substantive `1.13.10` change: `movement_cultural_majority`.

### RB-01 — Very High / rebase gate — port the 1.13.10 Cultural Supremacy fix

**Evidence.** `common/political_movements/02_cultural_movement.txt` changed upstream. The Vanilla `movement_cultural_majority` object hash moved from `e614fb0b…` to `6ce77168…`, matching the official fix for movement radicalism from unowned homelands. SB fully replaces that object in `common/political_movements/zz_sb_cultural_majority_movement_override.txt`; its CMF-derived implementation still contains the pre-hotfix homeland-owner test and therefore masks the Vanilla fix.

**Required work.** Semantically port all three `1.13.10` clauses into the current CMF-derived object: both unowned-homeland owner/culture tests and the neighbouring-country insurrectionary-movement selector. Preserve CMF integration and only SB's documented Cape creation/disband exclusion. Do not copy the whole Vanilla object over the dependency baseline.

`movement_minority_rights` shares the changed upstream file, but its object hash is unchanged (`3c985315…`). It needs baseline review and metadata refresh, not a behavioral merge.

**Done when:**

- the unowned-homeland block matches the `1.13.10` scope semantics;
- the CMF compatibility additions and Cape exclusions remain intentional and documented;
- a normalized diff proves no unrelated movement behavior changed; and
- the Vanilla, CMF, and SB object hashes and rebase dates are refreshed in the inventory.

### RB-02 — High / rebase gate — refresh and strengthen compatibility metadata

The current checker fails with five diagnostics:

1. `law_frontier_colonization` still points at removed path `common/laws/00_colonial_affairs.txt`;
2. `law_legacy_slavery` still points at removed path `common/laws/00_slavery.txt`;
3. `movement_cultural_majority` has an upstream source-file hash change;
4. `movement_cultural_majority` has an upstream object hash change; and
5. `movement_minority_rights` has a containing-file hash change.

The two law changes are path-only:

| Object | New `1.13.10` source | Content result |
|---|---|---|
| `law_frontier_colonization` | `common/laws/01_colonial_affairs.txt` | file and object hashes unchanged |
| `law_legacy_slavery` | `common/laws/02_slavery.txt` | file and object hashes unchanged |
| `movement_minority_rights` | `common/political_movements/02_cultural_movement.txt` | object unchanged; containing-file hash changed |

**Required work.** After `RB-01` is reviewed:

- update `descriptor.mod` and `.metadata/metadata.json` to `1.13.10`;
- update `Docs/compatibility/override_inventory.json` to target build `24689003`;
- change all 35 same-path `upstream_version` values to `1.13.10` only after confirming their unchanged hashes;
- repoint the two law baselines and refresh both movement baselines;
- update the dependency label from CMF `1.58.2` to reviewed CMF `1.60.3`;
- update `README.md`, compatibility documents, tests, and stale `1.13.9`/`1.58.2` script comments; and
- refresh the inventory's reviewed commit/date metadata.

The checker currently does not enforce the Steam build, `.metadata` version, generated baseline, or declared CMF version. Extend its tests or add an equivalent validation contract so these values cannot silently remain stale. Its state-region comparison must also fail if a collided Vanilla state-region file gains a top-level block absent from SB.

**Done when:** both metadata files, the inventory, compatibility prose, tests, and dependency label agree; `check_override_inventory.py` passes against the installed game and CMF; and the strengthened metadata checks have a failing mutation test.

### RB-03 — Medium / rebase gate / runtime check — company disband lifecycle

**Hotfix intersection.** Vanilla now re-enables the relevant journal entry when a company producing a generic prestige good is disbanded. SB registers its own `on_company_disbanded` handler and replaces the Mozambique Company and De Beers objects.

**Required work.** Prove that Vanilla's additive disband handler and `sb_on_mozambique_company_disbanded` both execute once with the expected company/country scopes. Re-diff both company replacements against `1.13.10`; explicitly decide the Mozambique override's removed incorporated-state checks rather than preserving the mismatch under a comment that mentions only AI weight.

**Done when:** disbanding and re-establishing the Mozambique Company performs SB cleanup, restores the eligible generic-prestige JE, and produces no duplicate or missing finalization. De Beers receives the same semantic-diff review.

### RB-04 — Medium / rebase gate / runtime check — treaty-port inheritance

**Hotfix intersection.** `1.13.10` adds treaty-port inheritance after revolution or conquest, a host choice to honor or revoke the agreement, market reconnection, `on_treaty_ports_inherited`, and `renege_treaty_ports_with`.

SB owns historical treaty data and performs scripted ownership changes, but it does not replace the new on-action. Audit:

- `common/history/treaties/00_historical_treaties.txt` and `sb_treaties.txt`;
- `common/scripted_effects/sb_treaty_effects.txt`; and
- state-owner-changing regional story effects.

**Done when:** an inherited hosted treaty port prompts exactly once, both honor/revoke outcomes work, the port reconnects to the correct market, and SB cleanup neither suppresses nor duplicates Vanilla handling.

### RB-05 — Medium-High / rebase gate / runtime check — subject transfer and fixed war-goal packages

**Hotfix intersection.** Vanilla now prevents self-transfer treaty articles and duplicate war goals already present among demands. SB has 33 `transfer_subject` references and 125 `add_war_goal` references, concentrated in the Bechuanaland, Griqualand West, BST, Natalia, and frontier-war packages.

**Required work.** Re-audit every scripted subject goal for:

- recipient already being the target's overlord;
- recipient equalling the target;
- a goal already existing before a sway or totalisation step;
- the same country/state goal being inserted through two helpers; and
- a non-transferable subject remaining a backer without an invalid demand.

**Done when:** the direct, proxy, reciprocal, and total-war packages contain each intended demand exactly once, no self-transfer is attempted, and a rejected optional goal cannot strand the surrounding crisis lifecycle.

### RB-06 — Medium / rebase gate / runtime check — initial fleets and naval operations

SB's European military-formation history is an exact-path override. Its upstream file hash did not change, so no text merge is currently indicated; the engine rules around it did.

**Required work.** Review SB-modified starting fleets for crews, reachable naval bases, marine carrying capacity, and adequate Supply Ships. In engine, cover embark, invasion, cancellation, rerouting, fleet transfer, retrofit, repair, and an intentionally unreachable coastal target. Confirm no mission accepts uncrewed ships and no invasion remains stuck at 99%.

---

## 2. Existing blocked, deferred, and compatibility work

### BC-20 — Low / blocked — restraint duration awaits the Southern African wars rework

CAP already receives the same anti-conquest/befriend restraint as GBR, with source-specific markers so the two countries do not overwrite one another. The remaining decision is the restraint's lifetime and war-specific behavior. Keep it persistent until the Southern African wars rework defines the intended post-crisis policy.

**Depro's comments:** Move to blocked, further content (esp SAn wars) are needed. Also add CAP to this befriend strategy towards the boers, otherwise a responsible one can override.

**Done when:** the wars rework supplies an explicit start, refresh, and removal contract for both sources.

### BC-22 — Low / deferred / human — Bechuanaland prose review

Review markers belong only beside localisation blocks. Structural enforcement is already in place; substantive Bechuanaland proofreading remains part of Depro's rolling in-game review and is a feature slice of `QUAL-09`.

**Depro's comments:** `### TO REVIEW ###` only applies to localisation blocs, remove those outside this. Then move this to deferred. This must be done by a human (me), I do it on a rolling basis when I come across the events in-game while testing.

**Done when:** every Bechuanaland localisation block is human-reviewed and reclassified without reintroducing markers into event script.

### CP-07 — Low / blocked — Hail Columbia compatibility patch

Both mods hard-replace `law_legacy_slavery`. SB currently requires a documented load order after Hail Columbia so the Boer visibility guard wins.

**Done when:** a dedicated compatibility patch preserves both mods' intended law behavior without relying on user-managed order.

### SUP-05 — Low / blocked — release-map spline repair

Do not edit spline, route-strip, or graph-connection data until the final release map stack is frozen. Generated spline changes are not composable across map mods.

**Depro's comments:** This you cannot fix, I've been delaying fixing this bug bc spline changes are not compatible across mods. I will fix it near release. You can mark this as low / blocked.

**Done when:** the final release stack is frozen, the spline/graph errors are regenerated and repaired against that exact stack, and cross-mod compatibility is rechecked.

### QUAL-09 — Low / deferred / human — repository-wide localisation review

Machine validation owns encoding, BOMs, headers, whitespace, duplicate/missing keys, and review-marker placement. Human review owns prose, historical tone, readability, and in-game presentation. Current structural coverage remains `89 reviewed / 131 to review`; `BC-22` is the Bechuanaland subset.

**Done when:** all active localisation blocks have been human-reviewed and reclassified.

---

## 3. Existing open Low backlog

### Gameplay and presentation

| ID | Finding | Required action / acceptance condition |
|---|---|---|
| `GP-20` | `common/diplomatic_actions/zz_sb_stake_colonial_claim_override.txt` omits the top-level sufficient-interest gate, so Stake Colonial Claim can expose an empty picker. | Restore an equivalent availability gate, or document the intentional UX; the action must never open an empty picker. |
| `GP-21` | XHG/XHR/XHT country/character histories describe live Xhosa splits with no creation/ownership path; CAP and PHL histories can create duplicate John Philip templates. | Decide whether the split tags are future API or dead history, then remove/activate them deliberately; leave one authoritative character instance. |
| `SUP-03` | `common/coat_of_arms/coat_of_arms/sb_countries.txt` gives SGO undefined named color `"dark green"`. | Change it to the valid database token `green_dark` and validate fallback rendering. |
| `SUP-08` | Confirmed candidates include `sb_je_cape_politics.dds`, `convict_crisis_1849.png`, stale Boer/Martinus/BST/Bechuanaland localisation, and definition-only economy/commandant/Delagoa helpers. | Remove confirmed dead content after save/API review; retain intentionally staged `te_sgo_united_flag.tga`. Track code removals with `QUAL-06`. |
| `SUP-09` | `sb_natal_crisis_l_english.yml` duplicates Vanilla key `Spies`; two files lack final newlines, and leading tabs/trailing whitespace remain. | Remove the duplicate and make active localisation formatting pass cleanly. |

### Tooling, documentation, performance, and maintainability

| ID | Finding | Required action / acceptance condition |
|---|---|---|
| `TOOL-06` | `sb_bechuanaland_caprivi_escalated_var`, `sb_bechuanaland_boer_influence_positive_var`, `sb_bechuanaland_swa_influence_positive_var`, and `sb_imperial_confederation_scheme_scope` are read but never set. | Classify each as migration API or dead state, then allowlist or remove it with save-compatibility evidence. |
| `TOOL-07` | The flag-assets README, cross-tag travel-time matrix, MZQ country-history comment, and Mozambique Company override comment are stale. | Make each document/comment describe the live implementation and exact override delta. |
| `PERF-08` | `sb_british_boer_restraint_effects.txt` scans all countries for ORA/TRN/ZPB/LYD/NAL/SGO/ABY/KLR and refreshes too often. | Direct-scope the optional tags and use transition-owned refresh plus a bounded watchdog. |
| `PERF-12` | Duplicate recurring checks remain in frontier-force eligibility, the empty Namibia yearly action, mineral one-shots, CAP pop conversions, ORA strategy refresh, and shown/possible predicates. | Remove each duplicate only where call ownership and lifecycle remain explicit; validate unchanged behavior. |
| `QUAL-06` | Dead/retired scaffolding and manual unused-symbol archaeology remain. | Commit an allowlisted unused-symbol report separating public/save/migration API from accidental dead code, then remove decided scaffolding rather than commenting it out. |
| `QUAL-07` | Scope comments and override-delta comments are uneven; legacy generic names and typos reduce searchability. | Add concise ownership/invariant comments and exact Vanilla-delta comments; do not rename stable keys without a compatibility alias/plan. |

### Planned content outside this rebase

#### CONTENT-01 — Low / planned — Transvaal and Orangia gold balance

The archived resource audit treats the live state file as authoritative. Gold in Transvaal and Orangia remains explicitly deferred to the next relevant content block. It is not a `1.13.10` rebase gate.

---

## 4. Required 1.13.10 runtime verification

Static review can narrow these cases but cannot certify them. Record game version, CMF version, companion-mod load order, save type, observed result, and relevant logs for every run.

| Case | Scenario | Expected result |
|---|---|---|
| `RV-01` | Fresh start with SB and CMF `1.60.3`; then save/reload. | No new SB-authored parser/schema errors, no missing required definitions, and stable journal/on-action initialization. |
| `RV-02` | Cultural Supremacy with owned and unowned primary-culture homelands. | Radicalism counts only the intended unowned homelands under the `1.13.10` scope semantics; Cape exclusions remain intact. |
| `RV-03` | Establish, disband, and re-establish Mozambique Company and a generic-prestige-good company. | SB cleanup runs once and Vanilla re-enables the eligible generic-prestige JE. |
| `RV-04` | Revolution/conquest changes a treaty-port host; choose honor and revoke in separate runs. | One inheritance prompt, correct agreement state, correct market reconnection, and no duplicate cleanup. |
| `RV-05` | All Warren/Caprivi direct and proxy routes, Boer support/neutrality, backdown, white peace, and mixed enforcement. Include an existing overlord, a non-transferable subject, a pre-existing goal, held popups, and save/reload. | Fixed packages contain each intended goal once; no self-transfer or invalid optional demand; no stalled corridor phase; terminal outcomes remain deterministic. |
| `RV-06` | Mapping Namibia succeeds and later delegates administration to SWA. | The winner receives exactly `+1,100` immediate involvement and remains Engaged through the retained persistent claim source. |
| `RV-07` | SB-modified initial fleets perform embark, invasion, cancel, reroute, transfer, retrofit, and repair paths. | Supply Ship and crew rules are respected; no destroyed/stuck army from rerouting; no 99% invasion stall. |
| `RV-08` | Hold and reload delayed Natalia and Delagoa events while the target/qualifying actors change. | Natalia death cancels safely; Delagoa remains bound to the original qualifying actor. |
| `RV-09` | Form SAF, make Cape independent, transfer/free SWA, and change SGO alignment during open and queued corridor phases. | Lifecycle precedence and ownership/claim outcomes remain stable after `1.13.10`; no unrelated war resolves the corridor. |
| `RV-10` | Exercise Cape Albany carving, Griqualand claim enforcement, subordinate-held MZQ land, and an already-started SGO transfer play. | Confirm each currently ambiguous behavior as intended or promote it to a numbered defect. |

The official Vanilla checksum `2964` is a source fact, not an expected modded checksum.

---

## 5. Static validation baseline and exit criteria

### Current `1.13.10` baseline

Run against the installed `1.13.10` game and CMF `1.60.3` without launching Victoria 3:

- `python3 -B -m unittest discover -s tests`: **19 tests pass**.
- `python3 -B tools/validate.py`: **7/8 categories pass**.
- The sole failed category is Vanilla/CMF override comparison, with the five `RB-01`/`RB-02` diagnostics listed above.
- Inventory shape is **35 same-path files / 100 keyed overrides / 17 changed state-region blocks / 0 replace paths**.
- No inventoried SB file or keyed-object hash drift was found.

Historical `1.13.9` Tiger totals and old dependency noise are intentionally absent from this live register. Establish a fresh `1.13.10` diagnostic baseline after the source rebase, and classify only new SB-authored diagnostics as regressions.

### Required static commands

```sh
python3 -B tools/check_override_inventory.py
python3 -B tools/validate.py
python3 -B -m unittest discover -s tests -v
git diff --check
```

Run Tiger or the current supported Clausewitz schema checker after these gates pass. Do not accept new parser/schema errors merely because older baseline noise exists.

### Rebase exit criteria

The rebase may be marked complete only when:

1. `RB-01` and `RB-02` are committed and the compatibility inventory is green against `1.13.10` and reviewed CMF `1.60.3`;
2. `RB-03`–`RB-06` have completed their static review and required engine cases;
3. descriptor, `.metadata`, README, compatibility docs, script comments, tests, inventory target/build, and dependency label agree;
4. the portable validation and unit suite pass without skips caused by stale local dependencies;
5. new diagnostics are either fixed or explicitly recorded with evidence; and
6. the runtime matrix records the observed `1.13.10` result rather than carrying forward a `1.13.9` assumption.

`SUP-05`, `CP-07`, human localisation review, and the Low cleanup backlog remain separately tracked and do not become silently “complete” when the base-game rebase closes.
