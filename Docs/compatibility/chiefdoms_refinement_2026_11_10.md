# Chiefdoms refinement — compatibility and verification

10 November 2026. Source delivery for the
[current implementation](../zulu_thirteen_chiefs_implementation_2026_11_10.md).
Current target remains Victoria 3 **1.15.0**, build **26453692**, core manifest
**7727600027425614094**; CMF **1.67.2 + sb-1.15.0-r2**. No dependency or map
payload was changed. Historical reports and reviewed-prose baselines are retained.

## Override boundaries

The joining-rule extension preserves CMF's complete body and SB's existing exact
Zulu–Swazi restriction. It adds an exact-partition foreign-join veto for the
**opt-in native test only**. Automatic subject intervention is still an engine
verification requirement; no foreign backer is removed after joining as a proxy
for passing that requirement.

Sixteen additional ideological movement definitions are keyed replacements of
the installed CMF body. The only change to each is the scoped possible predicate
in its existing uprising modes. Whole-object hashes are pinned in
[chiefdoms_uprising_contracts_1_15_0.json](chiefdoms_uprising_contracts_1_15_0.json),
and source tests remove only that insertion before asserting exact CMF parity.
The copies preserve CMF hooks, native geographical weights, recruitment, timing
and ideological positions.

| Added definitions | Count |
| --- | ---: |
| Anti-/pro-slavery, constitutional royalist, labour | 4 |
| Socialist, anarchist, communist, fascist, corporatist | 5 |
| Nihilist, positivist, land reform, feminist, reactionary, moderniser, anti-communist | 7 |

Existing SB replacements of Absolutist, Minority Rights, Utilitarian, Liberal and
Radical movements receive the same scoped gate. SB Traditionalists and the
dynastic movement also receive it; royal/chiefly movements use the separate
native-test predicate. Both uprising modes are covered where supplied. Cultural
and religious secession definitions remain unchanged. Foreign-specific authored
movements whose eligibility excludes the Zulu polity are not copied into SB.
Outside the exact contest, the new predicates leave ordinary behaviour intact.

The canonical override inventory now records **151 keyed overrides**, including
these sixteen additions, with the changed joining-rule and existing movement
object hashes reviewed on this date. The installed CMF tree/patch hashes remain
unchanged. The two affected JEs retain their 1.15 outcome migration contracts;
[the amendment record](chiefdoms_journal_amendments_2026_11_10.json) records both
the historical retained-field hashes and this authorised source amendment.

## Validation

The final machine-readable record is
[evidence/chiefdoms_2026_11_10/verification.json](evidence/chiefdoms_2026_11_10/verification.json).
It records full unit discovery, the complete validator, historical skips, current
dependency/map/naval/override checks and advisory Tiger. Current-target checks
remain mandatory. No failed check has been relabelled as engine pending.

Focused source-executed tests exercise expiry/mixed constitutions, the actual
Activism boundary, invalid claimants, lost territorial/pact conditions, exact
native pair/winner receipts, reunion delay, duplicate callbacks, persistent
branches, junior claimant accounting and the payer-G quote. The institutional
exit regression verifies that court reservations are cleaned while partition
cards survive. Existing installation/rollback tests, dynastic succession,
firearms, NGN, NRP and annexation-movement tests remain in full discovery.

Independent Sol 6.1 Max review checked the movement-body parity, exact-war receipt,
shared Country contexts and the IR exit/annual maintenance paths. Initial review
missed two parser mistakes found by advisory Tiger: a script-style unnamed GUI
`types` block and a decision `ai_chance` using `base`. Both now use installed
Vanilla/CMF syntax; their diagnostics disappeared on rerun. New script files
carry UTF-8 BOMs. This is why Tiger diagnostics were triaged rather than dismissed
wholesale due to its age.

Installed **vic3-tiger 1.19.0** targets game 1.13.5. The manual final advisory run
reports **0 fatal, 2,057 errors, 196 warnings, one untidy and one tip** across the
whole current SB tree. This is **not a clean Tiger pass** or a count of new defects.
It does not model 1.15 containers, journal outcomes, revised population predicates
or some GUI functions. New movement copies also expose inherited CMF diagnostics
as SB diagnostics. The affected container and `target`/comparison-value forms are
present in the installed 1.15 reference; current override contracts confirm the
copied bodies. No remaining actionable issue was identified in this change's
advisory review. The repository validator therefore warns for this unsupported
schema rather than accepting it as target certification.

`git diff --check` over the entire already-dirty tree still reports pre-existing
whitespace in the state-history override, outside this task. That file is
byte-identical to the pre-task snapshot. No unrelated formatting was changed.

## Engine boundary

No game launch or save migration was performed. All fifteen numbered scenarios
in the [DP runtime matrix](../zulu_thirteen_chiefs_runtime_matrix_2026_11_10.md)
remain pending. In particular, verify that actual Activism reaches 100% under the
native veto, that the ten-year expiry remains reliable through re-entry, and that
the shared roster renders in both journals. Keep native-war opt-in disabled in
normal play until **all foreign regular participation** is excluded from play
creation through war start. Static success is not evidence of that exclusion.
