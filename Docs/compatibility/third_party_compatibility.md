# Third-Party Compatibility Notes

Target game version: Victoria 3 `1.15.2`, Steam build `26763837`, branch `public`.

Required framework: Community Mod Framework `1.67.9` with patch `sb-1.15.2-r1`. The launcher dependency is pinned to `1.67.*`. Release validation pins exact tag `1.67.9`, commit `9103c9cb4130d46cb18204d588def1266e5c1555`, asset `release-1.67.9.zip`, and SHA-256 `2c702bbf99fd96804366896521832d18519a6a33e94519d49160de0ece7e04ae`.

Use the verified [official GitHub 1.67.9 release](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/releases/tag/1.67.9) with the pinned patch. Validation follows that exact tag and digest, not a moving latest release or an assumed Workshop payload.

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

SB does not override native treaty-port inheritance. Its 27 JEs use 1.15 outcomes; CMF supplies the active and concluded journal interfaces and renders native dynamic bars. SB sets a six-point gap between stacked scripted bars in CMF’s shared outliner row. SB's bespoke Chiefdom/Prerogative widgets remain separate; see the [JE report](1_15_0_je_implementation.md).

## Global Keyed Overrides

Some definitions are global keyed replacements despite a Southern African design goal: dominion actions/types, Stake Colonial Claim, Abolish Monarchy, commander retirement, Frontier Colonization and Legacy Slavery, selected ideologies and technologies, state traits, companies, and political movements. The inventory identifies every object and pins its Vanilla or CMF source.

`add_movement_enthusiasm_modifier` is also a keyed replacement: its native grant
is unchanged, followed by hidden expiry bookkeeping for NAL's Zulu cultural
movement only. Mods replacing that helper must retain the scoped record call for
SB's annexation modifier preservation. No generic modifier copying is provided.

The 24 copied CMF definitions retain their framework hooks and SB rules. CMF supplies the six native secession opt-ins. The patch carries the ideology and progress-bar fixes and merges native party dominance into all eleven CMF party files. [CMF comparison](1_15_2_implementation.md#community-mod-framework)

## Hail Columbia

SB and Hail Columbia both replace `law_legacy_slavery`. Until a dedicated compatibility patch is available, SB must load after Hail Columbia so the Inboekstelsel visibility guard remains authoritative. Reversing the order may expose Legacy Slavery to Boer countries or a settler-victory Cape where SB expects the Inboekstelsel variant.

This is an explicit deferred release gate, not permission to weaken either mod's behavior.

## Validation Authority

Installed Tiger 1.19.0 lacks 1.15 outcomes and once-only fields and is not used
as a target validator. DP performs the fresh all-DLC launch and focused engine
cases in the [1.15.2 runtime checklist](1_15_2_runtime_matrix.md). Source checks do not
certify native event timing, GUI rendering or engine load order.

Current dependency: CMF `1.67.9` plus `sb-1.15.2-r1`. The patch manifest and complete
installed-tree digest are pinned by the compatibility inventory. See the
[implementation report](1_15_2_implementation.md); older reports remain historical.

## Historical movement-contest note

The following records the earlier implementation, not the current interface
inventory. Consult the current source inventory and implementation report before
adding a compatibility patch.

## Zululand movement contest

The Chiefdom/Elder Council allowances and ordinary absolutist movement exclusion
are scoped to ZUL's historical Chiefdoms context. The absolutist replacement and
uSuthu derivative retain CMF's Bavarocrat and Grey PLP hooks. SB also shadows
`common/customizable_localization/00_ep1_custom_loc.txt` to prepend two marked-ZUL
lobby names; a mod changing that same file needs a merge. Native lobby types and
all other functions/fallbacks are preserved. See the inventoried source/result
hashes and [verification report](zululand_movement_contest_2026_09_19.md).
