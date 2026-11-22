# CMF 1.67.1 — implemented SB compatibility layer

**5 November 2026. Source implementation and static verification; engine checks pending.**
This implements the CMF/political-movement/territorial portion of the approved
1.15 rebase. No game was launched and no commit or mod release was made.

**Superseded dependency pin, 7 November:** the active installation is CMF
**1.67.2 + `sb-1.15.0-r2`**. The [new patch report](cmf_1_67_2_patch_2026_11_07.md)
records current identities and checks. This report preserves the original
1.67.1 integration evidence; its two payloads carry forward byte-for-byte.

## Installed identity

- Upstream [CMF 1.67.1](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/releases/tag/1.67.1),
  commit `f2dea1dde7b87098b504d120b2b20e963e1d4fb6`.
- Archive SHA-256:
  `8c7030df04c13ff47e9ade339abb3d96796c53122f73f0a0e2f3bb67e145264b`.
- Active patch: [`sb-1.15.0-r1`](../../patches/cmf/sb-1.15.0-r1/README.md).
- Complete installed-tree SHA-256:
  `5cd2ff82fb47384da257da22db0907ca9521245d4f8724ffbb34b222b54139b7`.

The archive was installed twice through the existing verified staging/atomic
replacement path; both results have the same complete tree hash. A subsequent
`tools/sync_cmf.py --check` reports the exact release and patch current without
network access or writes. The previous full installation is retained in the
ignored implementation backup `generated/rebase_1_15_0/cmf_before`.
The [machine-readable evidence](evidence/1_15_0_cmf_implementation.json) records
the input identities, active payloads and affected SB source hashes.

## Changes and preserved contracts

| Surface | Implemented change |
| --- | --- |
| Seven ideology-category helpers | Complete current Vanilla definitions and tooltip wrappers, retaining CMF's USFP/ANZ extensions. Character socialism uses `ideology_communist_leader`; the interest-group ideology is not globally renamed. |
| Journal/outliner native-bar fallback | Adds the native dynamic renderer when CMF-owned styling is not set. Existing CMF styling, targets and drift remain intact. The patch loader allows only this exact extra GUI target and checks its payload/hash. |
| Territorial goals | The active CMF patch no longer supplies annex/conquest/return-state copies. SB's conquest and annexation are complete 1.15 native bodies plus the Swazi guard and existing British–Zulu pre-annex handoff. Obsolete territorial-hook calls are gone. Native claim-infamy context and Russian-unification infamy are restored. |
| Cultural-majority movement | CMF's current German/Italian/Yugoslav creation/disband rules, anti-communist support adjustment and radicalism helpers, plus SB's Cape exclusion and existing neutral/reordered predicate optimisations. |
| Cultural-minority movement | Current native/CMF secession weighting, isolation and radicalism helpers, preserving SB's authenticated Natal Zulu movement replacement/handoff and pure filter reordering. |
| Minority rights | Current CMF body with SB's Cape creation/disband exclusion. |
| Absolutists | Current CMF council-republic handling, anti-communist folding, Russian ideology and radicalism helpers; preserve SB's authored-movement exclusion and merged creation scan. |
| Utilitarian, Liberal and Radical | Full current CMF bodies, including newly added native political branches, with SB's Cape JE gate and Anglo-African Utilitarian eligibility. |

The old cultural-majority API patch is unnecessary because CMF 1.67.1 supplies
it. Older patch directories remain historical evidence; active installation
does not read them. The new manifest pins the seven native ideology contracts
and `gui/shared/progressbars.gui`'s native `scripted_progressbar_dynamic` type.
This does not claim exhaustive semantic certification of every CMF override.

Inspection also found that upstream CMF's retirement override lacks native
1.15's politician-conversion roll. The main SB rebase owns the effective SB
retirement replacement: use the complete native body, retain SB's Basotho AI
restriction and CMF's `com_block_retire_var` possible/tooltip guard. There is no
additional CMF retirement role-cleanup delta beyond native role removal.

## Verification

The targeted suite ran **55 tests: zero failures/errors, five historical skips**.
It covers release identity, download/hash rejection, repeat/forced installation,
rollback, unchanged non-payload files, exact GUI allowlisting and tampering,
native ideology parity, both complete territorial-body deltas, all seven SB
movement deltas and retained predicate equivalence. Historical manifest/build
tests retain their old identities and conditional skips.

The broader integration run exposed three stale test assumptions. After updating
territorial parity to its effective native owner and separating the new native
anti-communist movement scan from the older radical-poaching optimisation,
**23 frontier/Swazi/precision tests also pass**. The precision test still requires
identical numerical results and tooltip breakdowns, and now includes countries
with an anti-communist movement; only the redundant zero-radical traversal is
allowed to disappear.

The smaller pre-edit dependency suite ran 31 tests with four failures, one error
and five historical skips against the old installed dependency and new game.
The main rebase records the independent complete pre-edit suite separately.

Static body parity verifies source preservation, not native execution. DP must
still check dynamic bar rendering in journal and outliner, political movement
creation/disband and secession behaviour, and both territorial callbacks and
their pre-annex character handoff. No performance improvement is inferred from
the retained predicate optimisations or upstream helper substitutions.
