# Griqualand East and Natal playtest — 14 November 2026

DP requested that GLE's province transfer include Cape-owned land. DP then
clarified the Natal observation: the other +20% throughput bonuses came from
Farmers and Extraction Economy. Natal's existing +20% sugar-only state trait
is correct and remains unchanged.

## GLE correction

The [march-state helper](../../common/scripted_effects/sb_griqualand_west_effects.txt)
previously required Xhosa ownership in all four founding-province candidates
and all five later transfers. Cape-owned parts of the intended settlement were
therefore omitted; if all founding candidates belonged to CAP, no GLE country
was created.

Those nine ownership guards now admit **CAP or XHO**. The existing footprint
remains `x708ADB`, `xC57FEF`, `xCA8474`, `x678D6E` and `x7524D4`; the four
founding candidates and their priority are unchanged. Land held by another
country, land already owned by GLE and provinces outside the footprint are
untouched. The event still requires an unsettled eastern frontier; this change
does not open a new post-frontier creation route.

The CAP monthly pulse schedules `.220`; CAP remains the event root when its
acceptance invokes this helper. The existing CAP origin, puppet relationship,
relations reward, ruler/law setup and migration effects are unchanged. Declining
the petition retains its resolved-state behaviour. No localisation changed.

Native [guarded province transfer](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_chris_scripted_effects.txt:314>)
and [princely-state creation](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/events/india_events/princely_state_creation.txt:78>)
confirm the existing ownership/scope pattern. Hail Columbia's
[Deseret creation](../../../Example%20Mods/hc%20-%20Hail%20Coloumbia%20%5B1.13%5D/events/usfp_mormon_events.txt:294)
and Gates of the Bosphorus's
[Kotor transfer](../../../Example%20Mods/gotb%20-%20gates%20of%20the%20bosphorus%20%5B1.13%5D/events/7-12_eqfm_karadag_events.txt:583)
provide comparable province-list examples, not engine proof for this target.

## Verification

The new [source regression](../../tests/test_frontier_playtest_november.py)
failed against the old helper: nine CAP ownership gates rejected the land and
the mixed-ownership case skipped its Cape founding candidate. It now checks
all nine gates for CAP, XHO, GBR, ZUL and existing GLE ownership, then simulates
founding and transfers from a mixed footprint. It verifies third-party and
outside-footprint land stays with its owner.

The 37 pre-existing focused tests passed before editing; **38 focused tests pass**
afterwards, including Natal's unchanged sugar-trait contract. Full validation on
the current Victoria 3 **1.15.1 / CMF 1.67.3 + sb-1.15.1-r1** target reports
**15 PASS, 2 existing WARN, 0 FAIL**. The warnings retain the five deferred release
gates and Tiger 1.19.0's incomplete 1.15 schema; Tiger was not run as a target
validator. All **69 local documentation links** across this note and the open
register resolve, including line and anchor targets.

The final scope check permits only this report, its register entry, the source
helper and its regression test. Reversing the nine ownership-guard edits restores
the effect file byte for byte; Natal's source/tests, localisation, review
classifications and all unrelated captured files are unchanged. Captured inputs,
the task-only patch and check output are under
`generated/playtest_gle_natal_2026_11_14/`.

## DP replay

Restart with a save before accepting `.220`. With the footprint split between
CAP and XHO, accept the petition and confirm all eligible footprint provinces
join GLE, it becomes CAP's puppet, and its ruler and migration setup still work.
Also check a Cape-owned founding candidate and a third-party-owned footprint
province: GLE can start on the former but must not take the latter.

Static predicate/transfer fixtures do not validate native country creation,
state splitting, population movement or live presentation. Already completed
settlements are not repaired retroactively. No game was launched, and no
dependency, metadata, review baseline or release-version change is included.
