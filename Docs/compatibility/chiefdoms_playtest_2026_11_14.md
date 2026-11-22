# Thirteen Chiefs playtest corrections and autosave investigation

14 November 2026. Target: Victoria 3 1.15.1, build 26591675, CMF 1.67.3 +
`sb-1.15.1-r1`, SB 0.20.3, all DLC. No game launch or save modification.

DP reported a moving review date, excessive G-scaled costs, an absent Dinuzulu,
hard-to-read movement backing, Boer participation after joining Natal's overlord,
and Zululand's deficit after partition. Source corrections are implemented;
engine acceptance remains open. DP subsequently approved the half-price curve
for Chiefdoms bribes only, which is now applied to new offers.

## Save evidence

The five autosaves cover 1 January–1 May 1886. The [extracted evidence](evidence/chiefdoms_playtest_2026_11_14.json)
records their SHA-256 hashes, dates, counters, budgets and character checks.
They all postdate the Chiefdoms JE's activation on 30 December 1879. They cannot
establish the immediate partition budget or reconstruct an earlier character loss.
The latest save has NAL as a British colony and ZUL under the Chiefdoms pact;
TRN is not yet a British subject. The exclusion is therefore a source correction
for DP's requested scenario, not a reproduced subject transition in these saves.

## Review clock

The same container retains `sb_chiefs_review_wait_var` at **3,650** days and
`sb_chiefs_weekly_tick_var` at **six** days in every save. A country-owned control
counter falls from 17,538 to 17,418 over the same 120 days. Adding the frozen
remaining duration to today's date explains the constantly moving review date.
The six-day receipt also prevents later weekly controller evaluation. Monthly
and law-change paths still evaluate the controller; the whole system is not idle.
This confirms the [previously recorded timer risk](chiefdoms_presentation_2026_11_12.md#separate-timer-risk--not-resolved-by-this-presentation-change).

The deadline now uses the existing shared JE's native `journal_entry_age >= 3650`.
The date display derives the remaining days from the same age, with an explicit
`FixedPointToInt` conversion for the date formatter. A permanent last-evaluated-age
receipt suppresses duplicate weekly callbacks without a timed container variable.
The original JE activation is retained on reload; the ten-year interval is not
restarted. Obsolete saved container markers are ignored and disappear with normal
container cleanup. Mixed constitutions and organising/active conflicts retain
their existing deferral and outcome priority.

The native model is Russia's [Provisional Government](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/journal_entries/08_russia_provisional_government.txt:192>),
with direct [condition wording](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/ip5_07_l_english.yml:153>).
Native [coup arithmetic](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt:1259>)
also subtracts a JE age from a duration. Gates of the Bosphorus's
[Greek JE](<../../../Example Mods/gotb - gates of the bosphorus [1.13]/common/journal_entries/1-00_grefm_greece.txt:812>)
uses the same age primitive, but its older version is not the API authority.
SB's review prose now states the laws and date directly. All changed general
localisation keys remain in the review queue; no reviewed namespace was rewritten.

## G-price comparison — approved Chiefdoms reduction

The [shared curve](../../common/script_values/sb_court_politics_values.txt) uses
**the payer's gold-reserve capacity G**, not current cash. Its input is the
selected head's own Prominence q, clamped to 10–100, not the whole house's backing.
The existing price is frozen when the offer opens and can be paid through debt.

| Head's Prominence | Former bribe / unchanged domestic price | New Chiefdoms bribe |
| ---: | ---: | ---: |
| 10 | 0.40 G | 0.20 G |
| 25 | 0.625 G | 0.3125 G |
| 50 | 1.00 G | 0.50 G |
| 75 | 1.30 G | 0.65 G |
| 100 | 1.60 G | 0.80 G |

For q ≤ 50 the unchanged domestic fraction is `0.4 + 0.015 × (q − 10)`; above
50 it is `1 + 0.012 × (q − 50)`. DP approved multiplying the Chiefdoms bribe
price by **0.5**, leaving that shared domestic curve intact. At G = £100,000,
a new 50-Prominence bribe now costs £50,000 instead of £100,000. The
[Chiefdoms price helper](../../common/script_values/sb_zululand_drift_values.txt)
applies the reduction for both NAL and TRN. Existing open offers retain their
stored quote; the reduction is not applied a second time during payment.
Other episode prices, Hamu's offer, £250/week sponsorship, £500/week chiefly
patronage and volunteer costs are unchanged.

## Tribute and the deficit

| Save | ZUL weekly income | Weekly expenses | Balance | Tribute to NAL | Balance with half tribute |
| --- | ---: | ---: | ---: | ---: | ---: |
| January 1886 | £2,986.99 | £3,436.10 | −£449.11 | £1,037.17 | +£69.47 |
| February | £2,998.36 | £3,499.25 | −£500.89 | £1,042.35 | +£20.29 |
| March | £3,023.57 | £3,537.60 | −£514.03 | £1,048.52 | +£10.23 |
| April | £3,084.83 | £3,648.83 | −£563.99 | £1,060.37 | −£33.81 |
| May | £3,080.96 | £3,669.51 | −£588.55 | £1,059.47 | −£58.81 |

The last column is an arithmetic counterfactual with every other item held fixed,
not a simulation. The dedicated `sb_zulu_chiefdoms` relationship now transfers
**15% instead of 30%** for the whole unresolved Chiefdoms phase. Ordinary Puppet
terms after settlement are unchanged. Existing treasury and debt are not edited.

May's military-goods expense is **£1,313.73/week**, including £1,024.49 for naval
fortification and £289.24 for army logistics. Military wages add £203.15. The save
also records a bankruptcy on 23 July 1884, very high taxes and £125,228.49 principal.
Tribute relief substantially reduces the observed deficit; it does not remove
these other pressures or prove the economy is balanced at the moment of partition.

## Dinuzulu and backing

There is **no live Dinuzulu character record in any of the five saves**, no live
recognised restoration claimant, and the stored recognised-heir ID 33562073 is
absent from the live character database. Dinuzulu's name occurs once per save,
in ZUL's regnal history with number 1. That records earlier use of the royal name;
it does not identify when or why the character disappeared. No evidence here
justifies claiming he never spawned, assigning a particular death cause or
recreating him. The current preservation/return source tests pass, but they do
not establish what happened earlier in this campaign. A pre-partition replay is
still required, including a minor Dinuzulu and the ruler/heir exile sequence.

May's existing house-accounting totals are **209 royal, 100 chiefly and 158
unaligned**, out of 467 represented Prominence. January's royal total was 252;
backing is not static. The two faction panels now show their cached aggregate
Prominence alongside native population Support and Activism. They use the same
faction-country routing as the native movement displays, including the test war's
rebel orientation, without recounting junior members or using the observer's court.

Boer Commitment is 100 throughout the sample while no valid royal claimant is
recognised. Commitment alone cannot deliver restoration or the NRP reward. The
fixed chiefly deadline remains an eventual route out of that unresolved contest;
no substitute claimant or new restoration rule is introduced.

## Boer withdrawal and NRP eligibility

The condition follows **Natal's actual overlord**, using native `is_subject_of`
for direct and indirect subjection. An independent Natal, a different overlord,
and unrelated countries do not trigger it. Eligibility blocks involvement,
interventions, held bribes, appeals and the Chiefdoms/ordinary NRP creation route
immediately; reconciliation stops costs and removes aid from either Zulu faction.
Open bribe quotes retain their display data until answered, while eligibility
prevents payment; withdrawal must not leave a popup reading deleted price data.
The current contest's commitment and territorial promise are forfeited, including
at 100 commitment. Later independence does not restore them. A genuinely new
contest clears its own forfeiture receipt. Already-created NRP and Hamu's separate
contract are not dismantled or redesigned.

The NRP entitlement and delayed finaliser revalidate eligibility. A cancelled
one-day appeal dispatch now has a two-day country receipt; a valid popup makes
that receipt permanent until answered. Declining is the always-available default,
so becoming ineligible cannot force the volunteer payment. Native dispatch,
held-popup and save/load behaviour remains a replay gate.

## Verification and remaining checks

- Before editing: 29 focused existing tests passed. The full suite later exposed
  two existing Shepstone assertions expecting 0.03 against DP's 0.1 source tweak.
  DP confirmed that tweak; only their outdated test expectations were updated.
- The preceding pass ran 69 focused controller, house-price, settlement, Hamu
  and claimant tests successfully.
  New cases exercise frozen legacy markers, a stable elapsed-time deadline,
  duplicate callbacks, foreign viewers, subject ancestry, full commitment,
  stale offers, pending NRP finalisation and separated movement totals.
- Full static validation for the preceding timer/presentation/eligibility pass:
  **15 PASS, two existing WARN, zero FAIL**.
  [Complete output](evidence/chiefdoms_playtest_2026_11_14_validation.txt). The warnings
  are the five deferred release gates and Tiger 1.19.0's pre-1.15 schema. Tiger was
  not used to certify this target.
- The shared domestic G-price source and unrelated work are checked against a pre-edit hash
  manifest in `generated/chiefdoms_playtest_2026_11_14/`. Task-path whitespace and
  documentation file links pass. Existing whitespace warnings in untouched
  global state history are preserved.
- Approved half-price follow-up: **39 existing price/court tests pass**, including
  new quote amounts, frozen quotes, borrowing, duplicate acceptance and unchanged
  domestic pricing. Additional source execution confirms NAL and TRN preserve a
  stored £100,000 legacy quote while new q=50 offers at G=£100,000 quote £50,000.
  Only the foreign-price helper, its existing expectations and three current
  notes changed; the domestic formula is byte-for-byte unchanged. Evidence:
  `generated/chiefdoms_half_bribes_2026_11_14/targeted_tests.log`. No full suite
  or engine replay was repeated for this single-multiplier follow-up.
- No performance, successful rendering, native callback order, character-survival
  or economic-balance claim follows from these source tests.

See the [corrective DP replay scenarios](../zulu_thirteen_chiefs_runtime_matrix_2026_11_10.md#14-november-corrective-replay--1151--cmf-1673).
Restart the game before testing the edited scripts. The 1886 saves can test the
clock, display, finance and eligibility changes; Dinuzulu preservation and the
immediate partition deficit require a checkpoint from before partition.
