# 1.15.0 map and world implementation — 5 November 2026

The working tree now uses the pinned 1.15.0 world and map sources, with SB's
reconstructed authored changes applied. This is static acceptance, not engine
certification. The unchanged native Benin and Bas Congo river-port cases and all
fresh-campaign map/movement checks remain pending DP.

## Evidence index

- [Raster merge and pixel counts](evidence/1_15_0_map/raster_merge.json)
- [Spline recovery, exact hashes, keyed delta and ID remapping](evidence/1_15_0_map/spline_merge.json)
- [Locator provenance and reconstructed terrain delta](evidence/1_15_0_map/text_map_merge.json)
- [World, resource and cold-bound dispositions](evidence/1_15_0_map/world_rebase.json)
- [Current-target map regression tests](../../tests/test_1_15_map_rebase.py)
- [Naval control and negative fixtures](../../tests/test_1_14_naval_network.py)
- [Current resource policy](../resource_gameplay_overrides.md#115-compatibility-update--5-november-2026)

The pre-edit inputs are retained locally in `generated/rebase_1_15_0/before/`.
The recovered old native spline is in
`generated/rebase_1_15_0/vanilla_1_14_5.splnet`. Generated inputs and test logs are
local work products; the linked JSON records preserve the reviewable evidence.

## Province raster

The retained `References/art/maps/vanilla13_provinces.png` is byte-identical to the
pinned 1.14.5 raster (`e3911fd80a40c6b297a68f66e898d9b187863b64483a9608123606143ee2ea78`).
Its name was not treated as version evidence. All three inputs are 8192 × 3616 RGB8.

For each pixel, compare pre-edit SB with old native. Copy the current 1.15 raster,
then substitute the pre-edit SB pixel only where that comparison differs. The SB
delta is 2,225 pixels; the native delta is 11,857 pixels. There are zero overlapping
changed pixels and zero conflicting pixels. Reopening the saved result proved:

- every pixel outside the SB delta equals 1.15 native;
- every pixel inside the delta equals pre-edit SB;
- the enclosing Southern Africa rectangle, including the Rhodesian footprint,
  remains identical to pre-edit SB.

The final raster hash is recorded in the evidence and current connectivity/footprint
manifests. Their existing local adjacency samples were retained after the geometry
comparison, not assumed valid because a new hash was written.

## Splines

Exact old bytes were recovered before the merge. Starting with the retained native
spline (`91c0957b4898ca4db6b66584d0ab1db1a6039825e9fd635b7a5c1e69068cf2b1`),
apply the native changes in the historical
[1.14 merge report](1_13_11_to_1_14_0_ob1_spline_merge.json). The affected record bytes
remain present in pre-edit SB. Keep point order and sort strips/links by their
encoded key. The reconstructed file exactly matches the pinned old-native hash
`ac58f5fb4cd408cf8dba8ad41c5f3a322a12c5372f055694eb85f528e650c28c`.
This also permits the original forward/reverse 1.14 reproduction test to run against
the correct historical input instead of silently reading the newly installed game.

The authored spline delta excludes 28 global editor float-roundtrip changes, whose
maximum coordinate displacement is 0.000030517578125. They are outside SB's authored
geography. Four had been deleted upstream; retaining their rounding changes would
incorrectly resurrect native-deleted records. The seven substantial modified point
records and all authored added/removed routes remain in the merge.

Six new SB strip IDs collided with different new native strips. SB strips received
unused IDs, preserving their style bits, and their link references were rewritten.
The evidence lists every old/new ID. No native strip was overwritten to resolve an
allocation collision. The record-keyed three-way merge rejects divergent same-key
content after those explicit corrections, retains target point order, and sorts
strips/links by key.

The deployed result has 33,849 points, 4,295 strips and 4,293 links. Lossless parsing,
unique IDs, closed references and encoded link endpoints pass. Regression tests also
compare every native record outside the declared SB delta byte-for-byte. This does
not prove that the engine loads the network or renders/moves along every route.

## Locators and terrain

Each locator file starts from native 1.15. The existing-ID authored changes are farm
257/259/261/262, mine 257/261, port 255/257 and wood 257/262, plus the existing custom
state records. For each changed existing ID, the earliest retained Git copy has the
same coordinates as current native, establishing that the substantial SB movement
is the authored delta. Other records remain native; global editor rounding noise is
not propagated. Native removal of port locator 575 is preserved. The evidence lists
the exact provenance commits and added IDs.

A full historical terrain byte baseline was unavailable. The authored semantic delta
was reconstructed from the retained Namibia/Botswana terrain rework and subsequent
changes: 123 deliberate desert assignments in Namaqualand, Hereroland, Botswana and
Bechuanaland. Applying those assignments to native 1.15 preserves every other native
province terrain. The full province list is retained in the evidence and checked
against native by the current regression test. This is a reconstructed semantic
port, not a claim that an unavailable historical full-file hash was verified.

## World history and resources

Global state history starts from 1.15, preserving authored Southern African ownership,
partitions, homelands and six custom states. Native Kostroma, Lithuania, Saratov, Tula
and Vologda are restored; retired Kaunas, Galich, Tartaria and Chukotka references are
absent from SB history/formations. Russian military formations are native, while the
Portuguese SB redistribution remains unchanged. Country-formation story guards and
custom requirements required no changes.

Political movement history retains the SB institutional-country exclusion and adopts
native Russian/Bukharan branches. The Nagasaki treaty adopts native copper; deliberate
SB treaty differences and the absent TRN starting treaties remain. North Angola pops
adopt native redistribution: Git blame showed the previous block had remained an
untouched import. Authored southern populations, Kazembe/Mozambique adjustments and
South Angola's Ovambo identity remain.

Untouched African state regions use complete current native blocks. Copper capacities
are Namaqualand 6, Zambia 18 and Katanga 30: 54 total, counted once per native parent.
Northern Cape's eight lead proxy levels are removed. Hereroland's genuine lead 10
and Namaqualand's provisional lead 2 remain. Copper-focused reassessment is deferred
to RES115-01; no broader resource rebalance was introduced.

Native cold bounds are copied to matching geography. Natal/Drakensberg inherit
Zululand (0–0.04), East/North Transvaal inherit Transvaal (0–0.02), and
Griqualand West/Bechuanaland inherit Northern Cape (0–0.04). Named Cape/Northern Cape
states retain their corresponding parent bounds. These are intensities; child
values are not added or divided as if they were resource capacities.

## Naval validation and its limits

The pinned 1.15 graph has 11,010 nodes and 11,091 connections. None of the 31 native
African designated building-port provinces directly matches a graph node. A checker
requiring that equality therefore rejects the unmodified control and cannot certify
this target. The repaired checker verifies port membership in the state, coastal
harbour nodes within that state, and a graph route from a harbour to a sea node.
An isolated pair of linked harbours fails; node degree alone is insufficient.

The same check passes 29 of 31 unmodified native ports and 31 of 33 SB ports. Benin
and Bas Congo lack state coastal nodes in both inputs. They generate explicit
warnings only while their port and complete province set equal the native control;
an SB alteration receives no exemption. The check does not infer river/spline access
from those omissions or certify building-port behaviour from a different coastal
province. Missing, non-harbour, out-of-state and disconnected fixtures fail as expected.

DP must still launch a fresh all-DLC campaign, inspect state/port/locator rendering,
exercise land and naval movement through the changed Southern African routes, and
compare the Benin/Bas Congo river-port cases with native. Verify copper availability
and cold behaviour on the final geography. No engine or performance claim follows
from these static checks.

## Verification record

- Full raster comparison: exact native outside authored delta; exact SB inside;
  no overlap. Southern African footprint comparison also passed.
- `validate.check_map_data()`: PASS for province/state membership, configured local
  adjacency, terrain, sampled locators/splines and reviewed hashes.
- Naval CLI: PASS for 31 SB coastal-access cases; two explicit unchanged-native
  runtime warnings, as above.
- Targeted map/resource/history suite: 59 tests, 58 passed, one historical-input
  skip (the unavailable 1.14.4 manifest). Current 1.15 checks and exact recovered
  spline reproduction passed. Log: `generated/rebase_1_15_0/map_tests_after.log`.
- Historical spline fixtures remain historical. Current-target checks separately
  enforce native record preservation and graph consistency.
- `git diff --check` reports 14 space-before-tab lines copied unchanged from new
  native Russian state-history blocks. They were retained to preserve native source
  formatting; this is not a script or semantic failure.
