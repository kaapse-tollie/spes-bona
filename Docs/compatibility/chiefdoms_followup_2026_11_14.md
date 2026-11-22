# Chiefdoms follow-up: claimant continuity, AI and movement readings

14 November 2026. Source corrections applied for Victoria 3 1.15.1 and
CMF 1.67.3 + sb-1.15.1-r1. Engine replay remains pending. No save was edited,
game launched, dependency changed, commit made or release version bumped.

## Save evidence

The five retained autosaves now cover **May–September 1889**. They are distinct
from the overwritten January–May 1886 observations in the
[earlier report](chiefdoms_playtest_2026_11_14.md). Exact hashes, identities,
movement modifiers and selected fields are in the
[compact evidence](evidence/chiefdoms_followup_2026_11_14.json).

| Date | Actual royal Activism | JE bar | Royal / chiefly backing | Royal / chiefly members |
| --- | ---: | ---: | ---: | ---: |
| May 1889 | 38.556% | 38.556 | 254 / 100 | 10,593 / 8,974 |
| June | 40.17% | 40.17 | 256 / 100 | 10,345 / 8,999 |
| July | 44.17% | 44.17 | 358 / 100 | 10,373 / 9,112 |
| August | 49.17% | 49.17 | 358 / 100 | 10,882 / 10,820 |
| September | 53.17% | 53.17 | 358 / 100 | 10,913 / 10,845 |

Members are the sums of saved Pop `political_movement_support` participants,
not native weighted Support percentages. The single royal movement is
100663308 in ZUL country 33554432. JE 83 was added on 31 December 1879.
There is no recorded rebel country redirecting the displayed side. All five
samples lack active TRN sponsorship/volunteer flags and their movement modifiers;
NAL policing is also absent. These samples cannot reconstruct the earlier 81%
reading or establish why aid ended. They do establish matching saved JE and
movement readings, rather than a sponsor-country reading, at these five dates.

**Dinuzulu exists:** character 33562073, template `ZUL_dinuzulu_heir`, born
1 January 1868, adult, historical, exiled and carrying the agitator role. He has
no current owner. ZUL's recognised-heir reference still points to him, but its
restoration-claimant reference is absent. Cetshwayo has no live record in these
samples; they cannot establish when he lost a role or died. The earlier absence
observation must not be treated as proof that this later campaign needs a newly
created Dinuzulu.

## Corrections

- **Claimant selection:** the monthly partition route already called
  `sb_court_refresh_royal_claimant`, but that helper still required the obsolete
  `sb_zululand_usuthu_context_var`. It now also accepts the actual active contest.
  The existing recognised-heir priority and living/adult/renunciation checks
  remain in force. No historical identity is recreated.
- **Return:** the return receipt now also belongs to the returned character.
  A later eligible adult successor can be returned through the same action.
  Natal's country receipt still prevents a second loyalist reward or Boer appeal.
  Old saves with only that country receipt can return their surviving claimant
  without repeating those rewards. Return explicitly sets the agitator career
  after role acquisition; native lifetime, movement attachment and rendering
  remain engine checks. No claim is made that career expiry explains Cetshwayo's
  reported state.
- **Partition order:** move the captured heir before the captured ruler, matching
  the existing pre-annexation shelter order. This avoids an intervening native
  accession when removing the king. The later save's Dinuzulu retains a ruler
  career entry at partition, but does not prove all intervening callbacks.
- **Review display:** replace `TimeKeeper.GetCurrentDateWithDiff`, whose CString
  includes the flashing hour suffix seen in DP's screenshot, with a whole-day
  countdown. Both the countdown and resolution still use the same native JE age
  and 3,650-day deadline. No new clock or reset is introduced.
- **Natal AI:** both actions now use the same conditional `ai_chance` value of
  25. Dynamic Historical considers them at royal Activism of at least 50%
  (native Protesting); Strict Historical after 1,095 days of the actual JE.
  Off gives zero. Existing `visible`, `possible`, Shepstone repeal lock and
  claimant checks remain authoritative. This is an eligibility/weight change,
  not a guarantee of a particular action date. The approach follows conditional
  [native button weights](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/06_canada_australia_buttons.txt:81>)
  and [HC's Underground Railroad buttons](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Example Mods/hc - Hail Coloumbia [1.13]/common/scripted_buttons/usfp_underground_railroad_scripted_buttons.txt:47>);
  [GotB](</Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Example Mods/gotb - gates of the bosphorus [1.13]/common/scripted_buttons/7-00_eqfm_balkans_buttons.txt:85>)
  also demonstrates zero weights where a separate route handles an action. Native
  dispatch in this shared situation still requires replay.
- **Chiefly Council:** uSuthu now strongly disapproves, consistently with its
  opposition to Federated Chiefdoms. This strengthens native law pressure; it
  does not assign Activism directly.

## Recruitment and the endpoint

The saved recruitment multiplier is 0.22965 in May and 0.31569 in September.
The current formula is aligned recruitment backing / total backing × 0.5,
capped at +50% attraction. September's chiefly multiplier is 0.08818. Backing
therefore changes a relative recruitment weight, not a promised share of the
population. Local agitator contributions are excluded from that scripted
attraction pool to avoid adding their native recruitment twice.

Native membership adjusts on its own cadence. The prior
[annual-cohort investigation](zulu_recruitment_stall_2026_10_31.md) explains why
extra attraction need not produce an immediate matching increase. That native
inspection was on 1.14.5; no new 1.15.1 cadence measurement was performed here.
The retained saves independently show slow membership growth. Do not force a
global membership refresh or promise proportional Support from these figures.

Installed 1.15.1 defines distinguish movement-member radicals and loyalists,
active/enacted law stances, additive movement modifiers, and a one-percentage-
point weekly move towards target Activism. Countrywide 60% radicals is not the
movement's radical fraction. Volunteers add 0.20 to pressure; they do not add
20 percentage points every month. The stronger council stance alone does not
establish that 100% is reachable in a particular campaign.

**Balance decision pending DP:** retain the implemented 100% endpoint for now.
The proposed alternative is native Militant status, 75%, while retaining the
living-claimant and settlement guards. No endpoint, recruitment coefficient,
native war gate, price or tribute was changed in this follow-up. Replay the
claimant fix before choosing a larger recruitment change.

## Verification

- The existing focused baseline passed 62 tests before editing.
- The new claimant regression fails against the captured old selector and
  passes against the correction. Source-executed cases cover adult succession,
  rejected children/dead/renounced claimants, closed intervention, foreign root,
  duplicate answers, one-off rewards and career-after-role ordering.
- Additional cases cover Dynamic/Strict/Off AI weights and the same 81% movement
  reading from NAL, TRN, GBR and ZUL roots. These fixtures do not simulate native
  AI selection, agitator attachment, mortality, rendered text or population
  recruitment.
- Full validator: **15 PASS, 2 existing WARN, 0 FAIL**. The warnings remain five
  deferred release gates and Tiger 1.19.0's missing 1.15 schema coverage.
- DP replay is listed in the [runtime matrix](../zulu_thirteen_chiefs_runtime_matrix_2026_11_10.md#14-november-follow-up--claimants-ai-and-activism).

Task input hashes, before copies, save extracts, validation output and final
task diff are retained under `generated/chiefdoms_followup_2026_11_14/`.
