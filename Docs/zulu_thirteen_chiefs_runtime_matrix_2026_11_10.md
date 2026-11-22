# Thirteen Chiefdoms refinement — DP runtime matrix

10 November 2026. All scenarios **PENDING DP**. Target: SB 0.20.3, Victoria 3
1.15.0 build 26453692, CMF 1.67.2 + sb-1.15.0-r2; all DLC. No launch by Codex.
Use a fresh campaign or checkpoints created before partition with this source.
Do not migrate an old active contest. Keep a save before each terminal result,
record exact choices/dates and retain rotated logs and both faction saves.

The [14 November follow-up](#14-november-follow-up--claimants-ai-and-activism)
updates the display and claimant checks below for 1.15.1. References to a fixed
review date mean the unchanged deadline; the current UI shows whole days left.

## 1. Early and late partition

Create Thirteen Chiefdoms from both early Klip River and later Anglo-Zulu paths.
Expect contemporary cast, retained royal identities/CAP exile, late eligible
Zibhebhu appointment, one international situation and one first-review date.
Initial Crown and direct administration must not start the contest.

## 2. Shared journal and houses

Open the situation as NAL, TRN and ZUL. All must show the same actual Zulu names,
Support, Activism, review date, active aid and Boer Commitment. Expand several
houses independently, scroll, and open leaders and members through their name
buttons. Check the Prerogative view too, including its other two court sections.
No blank title, null scope, duplicated member or oversized panel.

12 November presentation retest, **PENDING DP**, on 1.15.1 / CMF 1.67.3:
reload the reported Anglo-Zulu checkpoint and open this JE. The review date
must render without `sb_chiefs_status_review` errors and remain fixed as time
passes. Compare the outliner and expanded JE: royalist Activism fills red from
zero, Boer Commitment fills green, and neither uses the old moving balance
marker. Compact bars remain unlabelled, following the installed CMF layout.
The saved values inspected on 1 May 1880 were 2 and 0 respectively. This is a
presentation retest, not a migration or certification of older campaign state.
Keep another save after at least a week: the review wait and six-day receipt
may be frozen in the script container. Confirm the review date stays fixed and
weekly evaluation continues; see the [timing concern](compatibility/chiefdoms_presentation_2026_11_12.md#separate-timer-risk--not-resolved-by-this-presentation-change).

## 3. Persistent royal branches

Record houses and totals before accession, retirement and a head's death. The
royal office must not rename or reassign the house. Cetshwayo/Dinuzulu/Solomon
share their authored branch; Mpande/Mbuyazi have distinct branches. A junior
candidate receives external pledges without duplicating his house's own weight.
The next eligible prominent head represents the house using his own commitments.

## 4. Ten-year review and mixed laws

Reach the recorded date with complete chiefly laws, then separately with a mixed
pair. Complete chiefly settlement gives one result; mixed laws wait and retain
interventions. Complete the chiefly pair later: settle without a new ten-year
wait. There is no P or Legitimacy requirement and no unrelated-war peace gate.

## 5. Default royal endpoint

With native testing **off**, raise actual uSuthu Activism from below 100% to 100%.
The valid claimant is restored through the event/result route, without a native
civil war. Check both a domestic claimant and an exiled/returned claimant. A
missing, dead or renounced claimant must not produce a fabricated replacement or
result. Record whether the native gate still allows actual Activism to reach 100%.

## 6. Institutional exit and return

During the contest, reform until IR/constitutional eligibility closes the
Prerogative JE. Its governing effects end; the partition date, recruitment,
interventions and house display continue. Return to eligible institutions:
no new enthusiasm, no reset review date and no duplicated reward. Check a chiefly
vacancy and the January constitutional-alignment roll while IR is inactive.

## 7. Foreign bribery

Use both NAL and TRN with very different reserve capacities. Quote a neutral house
head; note his Prominence, price, current reserves and borrowing. Let reserves and
Prominence change while reading: the price stays fixed. Pay with insufficient
cash: debt is allowed. Verify only constitutional alignment changes. Repeat an
old choice, or invalidate the target before selection: no repeat payment and no
charge to a dead/already-aligned/unavailable target.

## 8. Interventions and refugee continuity

Exercise sponsorship, volunteers, policing, chief support, claimant return and
refugees. Chief support increases chiefly attraction; it does not also subtract
royal attraction. Return the actual claimant as agitator. Preserve the eligible
20% peasant transfer, loyalists among remaining NAL Zulu Pops and an open Indenture
JE. Ensure sequencing does not leak into choice tooltips.

## 9. Competing ideological uprising restriction

In the actual partition polity, organise an unrelated ideological movement and
inspect both uprising modes where applicable. New competing ideological uprisings
are blocked, while recruitment and law pressure continue. Repeat outside the
contest and in NAL/TRN: ordinary behaviour must remain. Cultural/religious
secession causes and an already started conflict must not be cancelled.

## 10. Native test opt-in and foreign exclusion — release gate

Reload a pre-conflict partition checkpoint. Set global
`sb_chiefdoms_test_tools_enabled_var` through the console, then take **Test an
Isolated Chiefdoms Conflict** as ZUL. Keep the Chiefdoms subject type. Test both
constitutional sides, British protection through Natal, alliances and other
eligible foreign supporters. Inspect participants from initial play creation,
through escalation and war start: **no foreign regular participant may join**,
including NAL, GBR and TRN. Later scripted removal is not a pass. If this fails,
keep the live default event endpoint; report the precise joining path.

## 11. Native organising and active conflict

In test mode reach the ten-year date while the exact constitutional conflict is
organising and while it is fighting. Review waits without resetting the date.
Cancel an organising object: the controller must resume rather than waiting on a
stale reference. Do not switch to the fallback during a reserved crisis.

## 12. Both native winners and reunion

Resolve separately for the original polity and actual rebel. Check the exact
winner is recognised once; wait until native reunion before subject/territorial
mutations. Surviving named actors, claimant and houses follow their recorded
side. A junior principal cannot appear on both sides. Inspect both countries'
UI contexts during the split. Repeated end callbacks must not award twice.

## 13. Permanent entitlements and NRP

Resolve both constitutional results, including royal fallback and native royal
victory with 100 earned Boer Commitment. Expect ordinary Puppet, +50% chiefly or
+10% royal NAL entitlement, non-stacking and permanent, applied upon later Natal
ownership. NRP uses the existing earned territorial contract once. No automatic
annexation, no unearned NRP and no repeat grant on institutional re-entry.

## 14. Loss, interruption and concurrent wars

Lose the Natal pact, lose Zululand territory to a third party, or remove NAL/ZUL
before resolution. No faction victory or new entitlement. Keep an unrelated war
open while valid settlement conditions hold: it must not block the result.
During an exact native split, ordinary temporary division is not treated as a
third-party loss; an unrelated/old war winner cannot reserve this contest.

## 15. Separate routes and clean logs

Check ordinary Zulu succession outside partition, NGN inheritance, initial Crown,
direct annexation and a non-Zulu court. There is no new dynastic challenge during
partition and no retired accommodation shortcut. Review fresh logs while hovering
all new text and expanding both house views. Confirm the ordinary game/dependency
baseline and unrelated reviewed prose remain unchanged.


## 14 November corrective replay — 1.15.1 / CMF 1.67.3

All new checks **PENDING DP**. The [five-save investigation](compatibility/chiefdoms_playtest_2026_11_14.md)
confirms the container timer risk above. Fully restart with the corrected scripts.
The existing 1886 saves may exercise these specific corrections; they do not
certify old-save migration or reconstruct the initial partition.

- Reload one January–May 1886 save. The review date must derive from the existing
  30 December 1879 JE activation and remain fixed across a week and save/load.
  Confirm weekly evaluation resumes despite the obsolete container markers.
  Check complete chiefly laws at age 3,650 days, mixed laws after that date,
  organising/active conflict, and one settlement when prerequisites are restored.
- View as NAL, TRN and ZUL. Check movement backing totals alongside Support and
  Activism, clean tooltips, long names and both faction orientations in the
  separate native-war experiment. In the May save, cached totals are uSuthu 209
  and Chiefly 100. These numbers may legitimately change after simulation resumes.
- Check 15% Chiefdoms tribute after budget recalculation, initially and after
  reload. Verify normal Puppet terms after settlement. Record ZUL's net balance
  and military upkeep; the static half-payment estimate is not a solvency claim.
- Make TRN a direct or indirect subject of Natal's actual overlord, including a
  non-British overlord control. It must leave the JE, lose the current promise
  and commitment, and stop intervention costs on reconciliation. Hold a bribe
  or appeal across the change; no payment, troop transfer or NRP reward follows.
  Cancel an appeal during its one-day dispatch: its country receipt must expire;
  hold a valid popup beyond two days: the open receipt must remain until answer.
  Later independence must not restore the forfeited undertaking. Existing NRP
  and Hamu's separate fulfilled contract must not be dismantled.
- From a pre-partition checkpoint with living Dinuzulu, record his identity,
  owner and roles before partition, after CAP exile/return, and after reload.
  The supplied 1886 saves contain no live Dinuzulu to recover; do not use a new
  character as evidence that preservation was repaired.

## 14 November follow-up — claimants, AI and Activism

All checks **PENDING DP**, on 1.15.1 / CMF 1.67.3. Restart the game to load scripts.
The [May–September 1889 evidence](compatibility/chiefdoms_followup_2026_11_14.md)
supports targeted replay from those saves, not general old-save certification.

- Check the countdown during all four daily ticks, after a day, after reload and
  from NAL/TRN/ZUL. It must change only by whole days and reach the existing
  3,650-day deadline without resetting the contest.
- After monthly reconciliation, the surviving adult Dinuzulu should become the
  recognised restoration claimant. From NAL, return him; inspect his actual
  owner, agitator role and attachment to the royal movement, then reload.
  An existing NAL return receipt must prevent another loyalist grant or appeal.
  With a living Cetshwayo, keep him first; with a child/dead/renounced successor,
  do not appoint or recreate an eligible adult merely to make the action work.
- From before partition, verify the captured heir leaves before the king,
  without an intervening accession. Both identities and the chiefly ruler must
  survive the intended handoff.
- Observe AI NAL in Dynamic Historical below/above 50% royal Activism, Strict
  Historical before/after three years, and Off. Eligible return actions should
  be considered only in their permitted mode. Check Shepstone's repeal lock,
  missing claimant and already returned actors. Confirm native AI button
  evaluation actually dispatches these shared-situation actions; a positive
  source weight is not that verification.
- Pause at the reported discrepancy, retain that save, and compare the same
  royal movement's current Activism with the JE as TRN and ZUL. Distinguish the
  current value from its target and record active sponsorship/volunteer/policing
  modifiers. The five retained samples match; none contains the 81% observation.
- Check strong opposition to both chiefly laws. Record movement-member radicals,
  loyalists, current/target Activism and membership after claimant return.
  The event endpoint remains **100%** pending the separate balance choice;
  do not count a source fixture assigning 100% as proof that native play reaches it.

## 15 November — political backing and Natal AI

All new checks **PENDING DP**. These supersede the preceding provisional AI gates
and settle the endpoint at 100%. Restart with the updated scripts.

- Compare full house backing before and after claimant return: the claimant
  remains counted once, although his separate scripted attraction contribution
  may fall as native agitator recruitment takes over. Check death, alignment
  changes and both faction countries in the separate native-war test.
- Inspect the royal movement's target breakdown and JE explanation at backing
  differences of 0, ±100 and ±300 or greater: expected modifier 0, ±10 and ±30
  percentage points. Repeat updates and reload; it must not accumulate or alter
  unrelated volunteers/policing. Compare target and current Activism over time.
- Resolve or interrupt the contest, including each native-war orientation.
  Confirm the prominence modifier is removed from every recorded participant.
  The ordinary court and unrelated movement modifiers remain intact.
- Dynamic AI NAL: below 20% Zulu radicals, neither action is considered. At
  20% or above, claimant return becomes eligible; offloading waits for the
  current eligible claimant to have returned and be present in ZUL. A stale
  country receipt, absent/dead successor or exiled claimant must not unlock it.
  If the first action reduces radicals below 20%, offloading waits again.
- Strict Historical: test just before and after JE age 1,095 days. Both actions
  retain their existing eligibility and delayed chance. Off must take neither.
  Human action requirements and once-only rewards must remain unchanged.
- Confirm native AI actually dispatches eligible shared-situation buttons and
  that actual Activism can reach the retained 100% endpoint under this balance.
  No source fixture or arithmetic example establishes either result.
