# Second succession replay: recruitment controller inactive

30 October 2026, evening follow-up. **Next test build implemented; engine result pending.**

The replay again produced a one-province rebellion with only one staffed battalion.
However, it did not activate the new recruitment controller. The first delivery
required a console diagnostic before answering the side choice; the normal choice
alone still followed the old path. The correction enables recruitment directly
from either ordinary choice in a new one-state crisis.

## Evidence

Read-only inspection of `autosave_4.v3` through `autosave.v3`, written around
22:23–22:24, covers September 1856 through January 1857. Source hashes, selected
country/movement fields, province runs decoded to IDs, military records and log
hashes are retained in the [evidence JSON](evidence/zulu_second_succession_replay_2026_10_30.json).
These are a separate replay from the earlier 29 October report.

| Observation | Saved result |
|---|---|
| Frozen coalitions | Mbuyazi 248; Cetshwayo 185 |
| Player side | Cetshwayo in the original country 481 |
| Actual rebels | Mbuyazi in country 16777788 |
| Frozen rebel target | 0.57275; correct for 248 / 433 at saved precision |
| Recruitment variables | Absent from every inspected country in all five saves |
| Recruitment modifier | `sb_court_coalition_recruitment` absent from the exact movement in all five saves |
| Diagnostic log | Zero `SB recruitment trial` lines in the copied `debug.log` |
| Movement | 33554488, created 19 August 1856; activism 5%, 30%, 50%, 70%, 95% over the five snapshots |
| Exact civil war | 201326596, originating in 481; linked to that movement and rebel country |
| Provinces at division | Original country retains 4469–4476; rebels receive 4477 only |
| Rebel army | Formation 485; three unit records, only one staffed, with 732 manpower |
| Original army | 21 unit records; three staffed, with 3,000 total manpower |

The rebel army also has only 4 Organisation and 24.9809 Supply in the final save.
These are post-division observations, not proof of the exact movement support
when the engine allocated territory. Empty unit records must not be counted as
combat-ready battalions. A second rebel formation is marked dead.

The copied error log contains 254 repeats of `Invalid right side during comparison
's'` at Vanilla `common/ai_strategies/00_default_strategy.txt:2535`. No recruitment
controller error appears. The debug log also contains an invalid-formation
reposition message; its cause is not established by this audit.

## Implemented correction

After a valid `.004.a` or `.004.b` choice freezes the sides and target, the normal
handler enables and initialises recruitment if the origin owns exactly one state.
Initialisation precedes movement creation and the first weekly poll. An immediate
`SB recruitment trial started:` line records the actual rebel, target and factor.
The movement receives **Mustering the Coalition**.

The existing trial still adjusts only its attraction modifier, gates both native
revolution eligibility and scripted advancement on measured support, and logs
combined/popular/military/wealth support weekly. Five-point weekly activism,
the 26-sample failure budget, participant checks and terminal cleanup are retained.
No army reconstruction or province transfer is added to the one-state path.
The multi-state path and already-created movements remain unchanged.

This is a correction to trial delivery, not evidence that recruitment converges
or that native army allocation matches the coalition ratio. The old result cannot
justify changing those coefficients because the controller never ran.

## Tomorrow's replay

1. Restart with this source and load a checkpoint before the contender choice is
   answered. The inspected September–January autosaves are already too late.
2. Choose normally; no `.990` command is needed. Confirm the immediate start log
   and the movement's **Mustering the Coalition** modifier.
3. Keep `debug.log` and saves around the division. For the same frozen 248:185
   contest with Cetshwayo backed, the actual rebel target should be 57.275%.
   Record provinces and staffed units/manpower, not only building or unit counts.
4. If the controller reaches its 26-sample limit, preserve that result and reload
   the pre-choice checkpoint. It deliberately grants neither victory nor peace.

All native convergence, allocation, timing and log-interpolation checks remain
pending DP. The current side-choice tooltip still broadly describes the
multi-state army-rebuilding behaviour; that pre-existing presentation gap does
not establish that rebuilding occurs in this one-state path.

## Source verification

105 focused recruitment, claimant-war and muster checks pass. They execute both
actual event option effects without the console diagnostic, and cover target
orientation, readiness, repeated delivery, no retrofit, multi-state controls,
expiry and cleanup. Native support and callbacks are explicit test inputs, not
a simulated engine outcome. Independent Sol 6.1 Max review ran 145 related checks
and found no blocking source regression.

Full discovery: **1,002 tests; 993 passed, eight existing skips, one existing
localisation-review failure and no errors**. The validator remains **15/17**:
its unit and localisation gates both report the dangling Swazi `.098` review row
and previously recorded reviewed-prose drift in Natal `.050` and Klip `.060`/`.080`.
Those namespaces and approvals were not changed here. CMF verification,
compatibility inventory, script contracts and map/naval checks pass. Advisory
Tiger remains at 0 fatal, 1,076 errors, 149 warnings, one untidy and one tip,
matching the preceding baseline; no diagnostic names a recruitment source file.

Output: `/private/tmp/sb-recruitment-auto-acceptance-20261030.txt`.
`git diff --check` passes. No game was launched, no save was edited, and no
commit or push accompanies this follow-up.
