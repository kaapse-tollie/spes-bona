# Third-Party Compatibility Notes

Target game version: Victoria 3 `1.14.5` Open Beta Update 4, Steam build `25629520`, branch `1.14-openbeta`.

Required framework: Community Mod Framework `1.66.0` with patch `sb-1.14.3-r1`. The launcher dependency is pinned to `1.66.*`. Release validation pins exact tag `1.66.0`, commit `807c32ff42b75714a3a0e090c0db3357b5e46ed7`, asset `release-1.66.0.zip`, and SHA-256 `79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b`.

The [Workshop change log](https://steamcommunity.com/sharedfiles/filedetails/changelog/3385002128) reported “Reverted to 1.13 version” during this beta. Treat the [official GitHub 1.66.0 release](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/releases/tag/1.66.0) as authoritative until the Workshop payload is unambiguous. Normal validation follows that exact tag and digest, not GitHub's moving latest release.

Spes Bona is a Southern Africa map, population, and flavor overhaul. It is not a light overlay.

## Detection

Other mods can detect Spes Bona with:

```txt
spes_bona_is_active = yes
spes_bona_southern_africa_map_rework_active = yes
spes_bona_population_rework_active = yes
```

These are CMF-style `REPLACE_OR_CREATE` triggers.

## Map Compatibility

SB changes `STATE_CAPE_COLONY`, `STATE_EASTERN_CAPE`, `STATE_NORTHERN_CAPE`, `STATE_VRYSTAAT`, `STATE_TRANSVAAL`, `STATE_EAST_TRANSVAAL`, `STATE_NORTHERN_TRANSVAAL`, `STATE_DRAKENSBERG`, `STATE_NATAL`, `STATE_ZULULAND`, `STATE_BOTSWANA`, `STATE_BECHUANALAND`, `STATE_GRIQUALAND_WEST`, `STATE_NAMAQUALAND`, `STATE_HEREROLAND`, `STATE_ZAMBEZI`, `STATE_ZAMBEZIA`, and `STATE_LOURENCO_MARQUES`.

`STATE_NATAL` uses the new state ID `1213`; mods that assumed Natal content lived in `STATE_ZULULAND` must route settler/coastal content to Natal and retain northern Zulu content in Zululand.

Mods editing those blocks need a compatibility patch. SB also ships the province raster, terrain, locator, and spline-network baselines, so unrelated map mods may still collide at file level. The exact surface is pinned in `override_inventory.json`.

The three intentional isolated passable Bechuanaland pockets are allowlisted by exact province membership. Any new disconnected pocket fails map validation.

## Treaty And GUI Compatibility

SB does not use a treaty-history `replace_path`. Its exact-path `00_historical_treaties.txt` shadows Vanilla and changes the Southern African startup rows; uniquely named treaty files remain additive. Another mod changing the same Vanilla filename requires a merged patch.

SB does not override Vanilla 1.14.5's treaty-port inheritance on-action. It also relies on CMF 1.66.0's standard and double-sided journal widgets and ships no competing journal GUI copy.

## Global Keyed Overrides

Some definitions are global keyed replacements despite a Southern African design goal: dominion actions/types, Stake Colonial Claim, Abolish Monarchy, commander retirement, Frontier Colonization and Legacy Slavery, selected ideologies and technologies, state traits, companies, and political movements. The inventory identifies every object and pins its Vanilla or CMF source.

`add_movement_enthusiasm_modifier` is also a keyed replacement: its native grant
is unchanged, followed by hidden expiry bookkeeping for NAL's Zulu cultural
movement only. Mods replacing that helper must retain the scoped record call for
SB's annexation modifier preservation. No generic modifier copying is provided.

The Cultural Supremacy override is rebased to patched CMF 1.66.0 and Vanilla 1.14.3's explicit-country primary-culture API, while retaining only SB's CAP exclusion. Both CMF and SB carry the API migration; these bodies and all 16 pinned CMF contracts still match the 1.14.5 baseline. The existing patch is retained without new payloads.

## Hail Columbia

SB and Hail Columbia both replace `law_legacy_slavery`. Until a dedicated compatibility patch is available, SB must load after Hail Columbia so the Inboekstelsel visibility guard remains authoritative. Reversing the order may expose Legacy Slavery to Boer countries or a settler-victory Cape where SB expects the Inboekstelsel variant.

This is an explicit deferred release gate, not permission to weaken either mod's behavior.

## Validation Authority

Tiger is useful for advisory parser diagnostics. DP performs the pending 1.14.5 cold launch, fresh-start log audit, and focused engine cases in `1_14_5_runtime_matrix.md` to verify current runtime and load-order behavior. The `1_13_11_runtime_matrix.md` evidence remains historical and separate.

Current dependency: CMF `1.66.0` plus `sb-1.14.3-r1`. The patch manifest and expected installed-tree digest are pinned by the compatibility inventory. See `Docs/compatibility/1_14_5_rebase.md` and `Docs/compatibility/1_14_5_runtime_matrix.md`; earlier matrices remain historical evidence.


## Zululand movement contest

The Chiefdom/Elder Council allowances and ordinary absolutist movement exclusion
are scoped to ZUL's historical Chiefdoms context. The absolutist replacement and
uSuthu derivative retain CMF's Bavarocrat and Grey PLP hooks. SB also shadows
`common/customizable_localization/00_ep1_custom_loc.txt` to prepend two marked-ZUL
lobby names; a mod changing that same file needs a merge. Native lobby types and
all other functions/fallbacks are preserved. See the inventoried source/result
hashes and [verification report](zululand_movement_contest_2026_09_19.md).
