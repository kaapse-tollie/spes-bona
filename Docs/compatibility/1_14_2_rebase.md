# Victoria 3 1.14.2 rebase — SB 0.20.1

Date: 2026-09-12. Scope: **new games only**. Existing saves were not opened, migrated,
or repaired. The ORA–BST two-stage design remains **ON HOLD**.

## Exact target and provenance

| Component | Pinned identity |
|---|---|
| Victoria 3 | 1.14.2, Steam build `25207758`, branch `1.14-openbeta` |
| Core depot | `529341`, manifest `2887980275526736263` |
| Starting depot | Opening beta 1.14.0, manifest `3868129321396195520` |
| SB | `0.20.1`, supported game `1.14.2` |
| CMF | Official `1.66.0` plus local patch `sb-1.14.2-r1` |

Paradox's [announcements](https://steamcommunity.com/app/529340/announcements/?l=english)
describe Update 1 and the subsequent hiring hotfix. Installed launcher metadata reports
1.14.2; the cold-launch system log reports executable revision
`6c9b008f4beb17850ee29bfb162bdbdeb3a450ce`.

`1_14_0_to_1_14_2_depot_delta.json` is reproducible with
`python3 -B tools/build_1_14_2_depot_delta.py --game-root '/path/to/Victoria 3/game'`.
The decoder verifies the exact retained manifest bytes and identities. The result is
**69 changed files, one added file, no removed files**. All 70 installed payload entries
were checked against their size and SHA-1 evidence. Earlier reports remain historical.

## Semantic decisions

| Surface | Decision and evidence |
|---|---|
| Exact-path SB overrides and map | No upstream change. Retain all existing Southern African data, port/spline repairs, and map hashes. |
| Three regional incorporation triggers | Source file changed, but each pinned object body remains identical. Keep the four owned-state priorities and owner/root guard. |
| Default AI strategy | Inherit Vanilla's updated scoring. All three `ai_can_incorporate_state` uses are within state-value scoring: owned-state value, cession reluctance, and foreign-state value. Start-incorporation routing still uses the two `will` triggers. No strategy replacement. |
| Dominion localisation sources | The containing Vanilla files changed; SB's documented custom dominion policy remains authoritative. Refresh source pins without editing reviewed narrative. |
| DP localisation bookkeeping | Preserve Boer Drakensberg naming. Recognise DP's explicit reviewed marker for Great Trek .002 and pin its unchanged definition lines. No prose rewritten. |
| Territorial war goals | Vanilla's Annex/Conquer/Return files are unchanged in this update. Move the existing mirror repair into patched CMF; remove SB's three redundant files only after byte-equivalence verification. |
| CMF ideology categories | Seven cross-file replacements were stale relative to current Vanilla. Restore current base lists, tooltip wrappers where present, and Carlist/Miguelist helper calls; retain only CMF's explicit USFP/ANZ additions. |
| CMF building browser | Two named GUI types overlap a changed Vanilla source. The inspected differences are CMF's production-method widgets; retain them and pin upstream types for future review. No CMF naval GUI replacement intersects the changed types. |
| Other changed scripts and GUI | Inherit war-support values/defines, revised non-territorial goals, free-speech laws, diplomacy values/actions/plays, treaty changes, AI strategies, and naval/building UI. The added diplomacy scripted-GUI file is Vanilla-owned. No balance overrides introduced. |

The strict inventory now covers **37 exact-path files, 109 keyed overrides, 18 changed
state-region blocks, eight localisation replace files, 20 key collisions, and two
Vanilla caller contracts**. The dependency patch separately locks twelve relevant
Vanilla objects/types and the entire installed CMF tree.

## Patched dependency

See `patches/cmf/sb-1.14.2-r1/README.md` for build instructions and the two separate
upstream-reviewable diffs. The official release archive matched its pinned SHA-256;
the previous local CMF matched that pristine tree. The installed patched tree is
`95810a77472536cabaab62dae9690e6c8828a4a7fe6d0c922d061a0683735a39`.

The synchronizer verifies staging before installation and retains rollback. Checks
reject pristine, partially patched, or otherwise altered installations even though
the metadata version remains 1.66.0. Neither routine sync nor `--force` removes the
patch. PR submission remains deferred; no commit or push was performed.

## Verification and engine limits

The dependency regression tests cover clean/repeated/forced installation, unchanged
files, tampering, original/payload hash mismatches, read-only checks, path rejection,
and rollback after an installation failure. Semantic tests compare the seven patched
categories to Vanilla after removing only documented CMF extensions. Historical depot
tests now skip installed-file comparison when their exact historical build is absent.

Cold launch reached the main menu with **1.14.2**, modified checksum **f575**, and both
mods confirmed mounted in the debug log. Evidence is retained under
`evidence/1_14_2_launch_2026_09_12/`.

This is **not a clean engine certification**. The launch error log contains 35 lines:

- one duplicate `regency.1` event from CMF's blocker;
- two duplicate on-action effect messages from CMF's heir/formation blockers;
- one invalid coastal port spline anchor, fifteen unmatched harbour-node messages,
  and fifteen coastal-graphics messages for Cape of Good Hope/Benguela Coast;
- one orphaned `portuguese_colonialism.4` event.

These were not attributed to the new patch without a Vanilla/control launch. The
changed-depot evidence shows no map/spline changes, and the scripted map/connectivity
checks pass; that does not dismiss the engine's harbour errors. No broad map or CMF
blocker rewrite was folded into this rebase.

Campaign testing is blocked by UI control: screenshots and accessibility reads reach
the main menu, but repeated New Game/window-raise actions return
`Computer Use server error -10005: noWindowsAvailable`. The game exposes an empty app
identifier. No new campaign was started through automation. War outcomes, timers,
hiring, and naval transport therefore remain **Engine pending**, as itemised in
`1_14_2_runtime_matrix.md`. Old saves were not used as substitutes.

Tiger remains advisory for the beta schema: the run reports zero fatal diagnostics,
1,108 errors, 101 warnings, one untidy diagnostic, and one tip. These are not a clean
parser result and are not represented as such. The strict semantic/hash checks remain
separate. Five previously declared deferred release gates also remain unresolved.

## Final static result

The integrated validator completed with **16/16 checks passed or warned; zero failures**.
Its unit-test gate passed (411 tests, three historical-depot skips). Map data, naval
connectivity, localisation, delayed lifecycle, runtime-script contracts, the exact
Vanilla/CMF inventory, and patched dependency verification all passed. The five
deferred release gates remain warnings. Tiger's separate advisory result is recorded
above; it is not counted as a clean parser pass.
