# Zulu court: live activation and future royal lines — 28 October 2026

## Decision and source changes

DP reports the AI replay working and approves live activation, with uncertainty about the servicemen transfer. This supersedes the earlier manual-opt-in hold. Normal Zulu/inherited-NGN and actual profiled rebel courts now enter claimant wars through the existing thresholds and reservations. `.990` is a diagnostic, not an activation switch. No war allocation, universal Approval pressure, victory, firearms inheritance or defeated-coalition rule changed in this pass.

The existing 50-P newborn action now covers Gqugqu and other undocumented royal lines. Dingane retains Uthumbu. A parent can use it once; the same newborn becomes the recognised heir. Known lines instead have dated creation: Cetshwayo → Dinuzulu (1868), Dinuzulu → Solomon (1891), preserving the existing templates' January-first dates as year-level authoring dates, not claims of exact birthdays. A living registered father is required; prior use of the child's template prevents recreation after death or exile. Birth does not automatically displace the recognised heir. The normal 25-P action can now recognise a minor; that does not supply adult Prominence. No existing descendant is replaced by a generated adult.

Fecund now has +25 Popularity and +5% Health, with its direct +5 Prominence removed. Native Popularity contributes to Prominence separately. The stronger attraction to Mpande is requested balance tuning; no source establishes a numerical historical popularity advantage over Gqugqu.

## Save evidence and its limit

Copies were made without writing to the user's saves, verifying that source size/mtime did not change during each copy. All retained files in this capture are **post-war**. They share reunited ZUL country `16777749`, ruler Gqugqu `4479`, Monarchy, both states `779`/`780`, and the resolved-conflict receipt. Mpande, Cetshwayo, Mbuyazi and Langazana remain alive in the cast. The firearm seed and fractional 10.4 qualifying weeks survive. These observations are consistent with DP's report; they do not certify every conflict path.

June has four barracks in Zululand with staffing 3.88; 4,783 servicemen and 26 officers in that state and none in Natal. October has 4,780 servicemen and 31 officers in Zululand and none in Natal. Available saved units total 3,880 manpower. The absence of a before/at-split checkpoint means this cannot prove whether the transfer failed or whether later native employment/AI rebuilding moved the distribution. **No staffing fix is inferred from this evidence.** The actual split remains scenario 118.

| Snapshot | Date | SHA-256 |
|---|---|---|
| `autosave.v3` | 1841.10.1 | `9a1a64721d5d77a8ce63e92f0b1b9a9b41cbbae5a773db1951a47d0b37b59fc7` |
| `autosave_1.v3` | 1841.9.1 | `f854a7f4e2ee33fec997f565f1af0ea8c1f126a0bc24b7f83dcf826a25bfca78` |
| `autosave_2.v3` | 1841.8.1 | `80143bc697dff3f5f7a0c31ff01d729e45e025df0680afbbaed60558795299d8` |
| `autosave_3.v3` | 1841.7.1 | `4becb9f06dcb4d24a0aac3898f971ad71311596ca29589517d2228373b1f322f` |
| `autosave_4.v3` | 1841.6.1 | `fce1604d2d9c8ba0ad923e8ab8f2efb509d72516aa493304ce62eb7f28b20265` |

Raw read-only copies, extraction script, input metadata and bounded audit JSON were kept under `/private/tmp/sb-court-release-heirs-2026-10-28/`. Hashes above allow matching the original evidence if the temporary copies are later removed.

## Historical children and confidence

Dinuzulu's birth year is 1868. He is the supported next claimant for the late nineteenth-century line. [South African History Online, King Dinuzulu](https://sahistory.org.za/people/king-dinuzulu).

Cetshwayo did have other children in the oral record. Mkebeni kaDabulamanzi's testimony names Maseyana, another unnamed boy, and Marelana/Dinuzulu; it reports the first two dying young. It also mentions Manzolwandhle around Cetshwayo's death. This is retrospective oral testimony, including a dream narrative, not a dated birth register. The record supports documenting those children, but does not justify inventing adult rivals, precise birth/death dates or numerical followings for this release. [James Stuart Archive, vol. 3, Mkebeni testimony, pp. 200–202](https://emandulo.apc.uct.ac.za/collection/KCAL/3_VOL3/KCAL_JSAVol3_1982_edited_notes_Mkebeni_ka_Dabulamanzi_091_p195_p209.pdf).

Mpande's historical survival and support reflect political alliances and the circumstances of Dingane's fall. A fruitful household is plausible characterisation; treating it as an exact popularity mechanism remains authored gameplay. Gqugqu's comparatively thin evidence does not warrant fabricating negative personality traits to force the desired result. [M. Z. Shamase, “Mpande kaSenzangakhona, 1798–1872”](https://samilitaryhistory.org/vol164ms.html).

## Validation and handoff

199 focused source-executed checks pass, including automatic entry without the test flag, contested accession, reservations, both conflict outcomes and existing allocation arithmetic; newborn price/identity, no-repeat/no-recreation, minor recognition, country/root boundaries and Fecund's exact modifiers. These fixtures supply engine objects; they are not runtime proof of recruitment or historical births rendering.

Full validator: **15/17 gates passed, warned or skipped**. Full unit discovery: **845 tests, 836 passed, eight historical skips, one existing failure and no errors**. The two failing gates are the same reviewed-prose drift reported both by unit discovery and localisation validation: `sb_klip_river_county.060`, `sb_klip_river_county.080` and `sb_natal_crisis.050` in `sb_natal_crisis_l_english.yml`. Those strings and their approval baseline were not changed. CMF installation/rollback checks, current compatibility, override inventory and map/naval checks pass. Dependency release sync was deliberately skipped; no payload was changed. Advisory Tiger remains at 1,073 errors / 149 warnings against its older schema, with no diagnostics in this task’s changed files. The final focused run includes the explicit male-newborn constraint and revised minor menu. Logs: `/private/tmp/sb-court-release-heirs-2026-10-28/full-validation.txt` and `focused-final.txt`. No game launch or save migration was performed. Next priority is runtime matrix 121 (peaceful and contested Mpande retirement), with scenario 118's population snapshots, then scenario 122 (Thirteen Chiefdoms).
