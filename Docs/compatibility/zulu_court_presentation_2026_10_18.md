# Zulu court presentation — 18 October 2026

SB 0.20.2; Victoria 3 1.14.5; CMF 1.66.0 + `sb-1.14.3-r1`.
DP approved replacing forced faction ideologies with visible allegiance traits.
No game was launched, dependency changed or saved campaign migrated.

## Character commitments

The existing country/character records remain authoritative:

| Record | Meaning | Presentation |
|---|---|---|
| `sb_court_alignment_var` | 0 unaligned; 1 royal; 2 chiefly | One constitutional trait: Unaligned, uSuthu or amaKhosi |
| `sb_court_endorsement_var` | 0 uncommitted; 1 incumbent; −1 named rival | One personal-allegiance trait |
| `sb_court_claimant_scope` | The actual rival character | Their name in the JE court roster |
| `sb_court_home_scope` | The court to which the character belongs | Incumbent name and roster membership, including CAP exiles |

The traits have no modifiers, random selection weight or experience value.
Each replaces only its siblings on the same axis. Registration, alignment
changes and the existing backing recalculation synchronise them. No new daily
or global character scan is introduced. The roster excludes dead, underage and
other-country records; it displays all eligible court members, while the
existing calculation still counts only one representative per following.

Registration, alignment and claimant return no longer overwrite character
ideology. The two constitutional movements retain their law platforms but no
longer assign a narrow faction ideology to pressured IG leaders. Their agitator
eligibility reads the existing alignment variable. The obsolete character
ideology definitions and localisation are removed. The three newly authored
templates previously given those packages use Moderate; their royal commitments
are recorded separately. Existing historical templates retain their own
ideologies. No reconstruction of ideologies previously overwritten in saves is
attempted; a fresh campaign is the supported baseline.

## Startup and interface

- **uSuthu** replaces the Royal Movement label. amaKhosi uses Vanilla's
  `law_icons/chiefdom.dds` symbol.
- The JE title and flavour change between Royal and Chiefly Prerogative with
  the current governance law. The flavour follows the concrete actors and
  political stakes used in the installed Japan and Two Spains DLC examples.
- The bar uses a fixed red-left/green-right scale with Vanilla's CAP-style
  marker. P −100, 0 and +100 project to the left, centre and right respectively.
  Country arithmetic and monthly progression are unchanged.
- Prerogative, Institutional Reach and movement information have separate
  explanations. The court roster names personal allegiances independently of
  constitutional preference.
- **Influential Supporters** replaces the unclear modifier label. It uses a
  valid native icon and appears only for positive attraction. Existing capped
  attraction and the agitator exclusion are unchanged.
- `AGENTS.md` now requires DLC flavour references; `common_pitfalls.md` records
  player-first tooltips, explicit history creation and allegiance presentation.

Vanilla's political-movement history explicitly creates Absolutists, bypassing
the movement's normal creation trigger. The new exact-path history shadow adds
one `NOT = { sb_institutions_eligible = yes }` condition to that call's limit.
Removing this line reproduces the installed Vanilla file exactly after BOM
decoding. Other movements and countries are untouched. Original/result hashes
were recorded after this semantic comparison. The inventory now contains
**39 same-path files, 118 keyed replacements and eight localisation replacement
files**; CMF pins and payload remain unchanged.

## Validation

The [evidence record](evidence/zulu_court_presentation_2026_10_18.json) records
commands, outcomes and remaining limitations. Focused source-executing checks
cover independent allegiance changes, repeat synchronisation, preserved
ideology, exile ownership, dead/underage exclusions, zero-strength recruitment,
startup parity and unrelated-country controls. Native asset paths and concept
references resolve. The unused-symbol checker now includes GUI references;
its regression still rejects genuinely unreferenced helpers.

- **63 focused tests pass.**
- Complete discovery: **587 tests; 578 passed, one failure, eight historical
  skips, no errors**. The remaining failure is the existing localisation
  approval-baseline check described below.
- Full validator: **14/16 gates passed, warned or skipped**. The unit and
  localisation gates expose that same approval issue. Compatibility, maps,
  naval connectivity, runtime contracts, routing and lifecycle checks pass.
  Five existing deferred release gates remain; CMF sync was skipped while
  installed-tree integrity was verified.
- Advisory Tiger: **0 fatal, 1,066 errors, 144 warnings**, using its older
  1.13.5 schema against 1.14.5. This is not a clean engine validation. The final
  bookkeeping/readout-test repairs do not change the runtime sources it checked.
- `git diff --check` passes.

The reviewed-localisation baseline differences in `sb_natal_crisis.050`,
`sb_klip_river_county.060` and `.080` predate this work and remain untouched.
Their approval records have not been regenerated. New general prose is queued
for DP review.

## DP runtime checks — all pending

| Check | Expected result |
|---|---|
| Fresh ZUL start, before unpausing | uSuthu, amaKhosi and Traditionalists; no temporary generic Absolutist duplicate |
| Opening JE | Royal title; zero at the centre of the red/green scale; one set of action buttons |
| Character cards and roster | Separate constitutional and personal traits; broader ideology preserved; actual incumbent/claimant names |
| Patronage, alignment and succession | Correct trait changes without duplicate traits or ideology replacement |
| CAP exile | Roster names the Zulu court's incumbent/claimant, not CAP's ruler |
| Chiefly constitution | Chiefly title/flavour; same signed scale and live values |
| Following recruitment | Valid icon, visible Pop Attraction at positive strength; no empty zero-strength entry |
| Layout and launch log | Readable text and functioning character links; no new GUI, trait or asset diagnostics |

Static results do not establish rendering or initialisation order in the engine.
