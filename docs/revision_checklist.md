# Revision Checklist

Use this as the current technical cleanup list before deeper gameplay testing.

## 1. Isolate The Test Environment

- [ ] Boot once with only `Spes Bona - A Southern Africa Flavour Pack` enabled.
- [ ] Boot once with `Community Mod Framework` enabled again and compare the logs.
- [ ] Treat these as external until proven otherwise:
  - [ ] `yes_election_chaos` persistent-reader error
  - [ ] `cmf_heir_blocker.txt` duplicate `effect`
  - [ ] `com_formation_event_blocker.txt` duplicate `effect`
  - [ ] `com_regency_blocker.txt` duplicate `effect`
- [ ] Confirm whether any remaining startup errors still reproduce with `CMF` disabled.

## 2. Clean Up Accidental Map-Editor Output

- [ ] Audit the untracked generated `.bin` files under [gfx/map/map_object_data](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/gfx/map/map_object_data).
- [ ] Decide which generated assets are intentionally shipped and which were accidental editor exports.
- [ ] Remove accidental generated assets before doing more route debugging.
- [ ] Recheck `git status` after cleanup so only intentional map files remain dirty.

## 3. Rebuild The Transvaal Route Layer

- [ ] Confirm whether a custom [gfx/map/spline_network/spline_network.splnet](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/gfx/map/spline_network/spline_network.splnet) now exists or needs to be added.
- [ ] If a custom `.splnet` exists, inspect it in the map editor and remove the stale strip between `25901` and `26403`.
- [ ] If no custom `.splnet` exists, regenerate one intentionally instead of continuing to shuffle only state ids.
- [ ] Remove stray low-numbered anchors `1-5` if they were created accidentally in the spline editor.
- [ ] Remove or reconnect strips using the broken anchors:
  - [ ] `2 <-> 5`
  - [ ] `3 <-> 25401`
  - [ ] `2 <-> 25802`
  - [ ] `1 <-> 25901`
  - [ ] `3 <-> 25901`
  - [ ] `1 <-> 26204`
  - [ ] `3 <-> 26302`
  - [ ] `3 <-> 26403`
  - [ ] `4 <-> 26404`
- [ ] Remove land/naval mixed strips:
  - [ ] `25701 <-> 8415008`
  - [ ] `26403 <-> 8415008`
- [ ] Recheck that every split Transvaal state has at least one valid land path to each adjacent land state.

## 4. Revalidate Hub Mapping

- [ ] Confirm the city hub provinces are now correct in [04_subsaharan_africa.txt](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/map_data/state_regions/04_subsaharan_africa.txt):
  - [ ] North Transvaal city -> `x4760DD`
  - [ ] East Transvaal city -> `x91CA59`
  - [ ] Drakensberg city -> `x8C39B6`
  - [ ] Northern Cape city -> `xC95189`
- [ ] Confirm the stray unnamed city node north of Transvaal is gone.
- [ ] Confirm Springbok now appears in Northern Cape.
- [ ] Confirm East / North / Drakensberg city hubs are no longer unnamed or randomly placed.
- [ ] Confirm hub loc matches the intended owner-culture naming:
  - [ ] East Transvaal -> `Nelspruit / Mbombela`
  - [ ] North Transvaal -> `Pietersburg / Polokwane`
  - [ ] Drakensberg -> `St. Monica / Ladybrand / Maseru`

## 5. Recheck Generated Locator Files

- [ ] Refresh the shipped generated locator files only from the latest files in `/Users/depro/Documents/Paradox Interactive/Victoria 3/generated/`.
- [ ] Verify [generated_map_object_locators_city.txt](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/gfx/map/map_object_data/generated_map_object_locators_city.txt) matches the intended live node positions.
- [ ] Verify [generated_map_object_locators_port.txt](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/gfx/map/map_object_data/generated_map_object_locators_port.txt) matches the latest generated file exactly.
- [ ] Boot again and confirm the `map object locator` incomplete errors stay gone.

## 6. Audit Duplicate Journal Entry Seeding

- [ ] Recheck why startup still logs duplicate JE warnings for:
  - [ ] `je_sb_zulu_kingdom`
  - [ ] `je_sb_adopt_firearms` for `ZUL`
  - [ ] `je_sb_adopt_firearms` for `GZA`
  - [ ] `je_sb_adopt_firearms` for `SWZ`
- [ ] Confirm these JEs are only added once between:
  - [ ] country history files
  - [ ] any startup on-actions
  - [ ] any event-side emergency setup

## 7. Final Log Pass

- [ ] Fresh boot with `Spes Bona` only.
- [ ] Fresh boot with `Spes Bona + CMF`.
- [ ] Fresh `1836` observe test.
- [ ] Confirm no remaining:
  - [ ] travel anchor errors
  - [ ] unknown-anchor strip errors
  - [ ] land/naval mixed-strip errors
  - [ ] `25901 <-> 26403` route-strip warning
  - [ ] South Pacific routing / teleport bugs

## References

- [Modding State Regions, Splines, Provinces, Cities, and Roads](https://steamcommunity.com/sharedfiles/filedetails/?id=3165669021)
  - Useful for hub ids, land/naval hub types, and spline editing in the map editor.
- [How to make a new state (without the in-game editor)](https://steamcommunity.com/sharedfiles/filedetails/?id=2892376601)
  - Useful for the text-side state split workflow and the generated locator files.

## Current Notes

- Current `content_load.json` shows `Community Mod Framework` is enabled alongside Spes Bona.
- The routing issues now look like a mix of:
  - accidental map-editor output in the mod folder
  - stale / broken spline anchors and strips
  - one surviving legacy Transvaal route connection
