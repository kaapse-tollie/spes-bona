# Civil wars, diplomatic plays and military allocation

Read when: Diplomatic plays, demands, civil-war callbacks or military allocation.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="war-01"></a>

## WAR-01 — Scripted permission cannot bypass earlier native eligibility

`revolution.possible` and `interest_group_can_join` are reached after native
support and ideological checks. High activism, a named agitator or an approval
penalty alone does not force an IG to sponsor a revolution. Test the actual
IG's internal backing, approval and law agreement before tuning pressure again.

<a id="war-02"></a>

## WAR-02 — Distinguish failure to qualify from failure to allocate

`last_failed_civil_war_start_date` records native creation attempts that can
fail for missing uprising territory or forces, followed by a retry cooldown.
It does not identify which allocation failed. A post-creation rebuild cannot
satisfy an earlier requirement that prevented country creation.

<a id="war-03"></a>

## WAR-03 — Find the exact conflict through its actual owner

Native civil-war lists
belong to the origin country, not the rebels. Use `civil_war_origin_country`
and the recorded movement to identify the war; do not select the first war
merely because one exists. Preserve the origin for later checks from either
side.

<a id="war-04"></a>

## WAR-04 — Country roles and faction identities can diverge

Player-side selection
can invert who occupies the original or rebel country. Route rulers,
commitments, progress and cleanup by the actual participants and winner,
not a presumed surviving tag. A movement leader is not automatically the
country's ruler.

In Victoria 3 1.15.2 a defending overlord can take leadership before
`on_diplomatic_play_started` receives `scope:target`. For a play against a
subject, identify the subject through the opening demand and confirm its side
in that exact play. Share that identification between the duplicate check and
the play-start callback. Inside `any_diplomatic_play`, `this` is the play.
Use explicit country references when checking the initiator and defender.

If a start callback assigns optional backers, resolve their choices before
launch. Verify the committed participants on each side and who holds each
counter-demand with either defensive leader. The save's `involved` list
also includes countries that have yet to choose a side. [Klip River save and engine investigation](../compatibility/klip_river_secession_backers_2026_11_21.md)

<a id="war-05"></a>

## WAR-05 — A territorial target is not an army allocation

`target_fraction_of_states`
does not guarantee proportional battalions or manpower. The one-state
provincial path uses movement support; multi-state proposals also depend on
geography and native military rules. Classify the origin before splitting:
two resulting one-state countries do not imply a one-state origin. One owned
state is not itself a blanket bar to ideological revolution.

A recruitment-readiness experiment must gate this movement's native
`revolution.possible` as well as scripted advancement: withholding the scripted
progress effect alone does not stop native creation. Keep the adjustable
attraction component separate from activism. A recruitment/advancement test budget
must also cover an organising war which has stalled; its existence is not proof
of a qualified advance. Issuing progress is not proof of actual rebel creation. Check final-sample success before expiry and never fabricate a
peaceful result when the experiment fails. The [one-state trial](../zulu_one_state_coalition_split_proposal_2026_10_30.md)
has source-executed checks, not verified in-engine convergence.

Before attributing a replay's result to an experimental controller, verify its
saved activation state, owned modifier and diagnostic log. A console-only entry
can leave a normal player replay on the old path. Exercise the actual event
options in regression checks and log activation before the first delayed pulse;
absence of controller evidence is not failed convergence.

<a id="war-06"></a>

## WAR-06 — Record each side's demands explicitly

In split states, Return State
targets the opponent's actual state object. The supported primary-goal field
is `primary_demand`. An opening demand does not prevent later native
additions; any intended restriction must cover selection and validity for the
exact play and parties while preserving legitimate territorial recovery.

<a id="war-07"></a>

## WAR-07 — Timer enforcement and final settlement are separate callbacks

`on_wargoal_enforced_by_timer` must not automatically perform final
`on_wargoal_enforced` bookkeeping. Do not assume the older
`enforced_by_timer` marker is supplied by the current engine. Verify each
required peace term; retaining old territory is not proof that a conquest or
subject goal succeeded.

In 1.15.2, `no_mirror` suppresses the reverse goal. The opponent can still
hold an independent demand and continue fighting after the timer enforces.
For an objective that should decide the war, match the timer and the enforced
goal to their original play and participants, then explicitly resolve that
war. Verify that combat ends and the normal war-end settlement runs once.
[Blood River saves and replay checks](../compatibility/blood_river_timer_design_2026_09_12.md)

<a id="war-08"></a>

## WAR-08 — Victory callbacks do not prove territorial reunion is complete

Preserve
needed actors before country removal and check actual ownership before applying
regional restoration. Cancellation, a dead contender or a missing war object
is not a substitute for an authenticated winner. Exercise both winners and
the native cleanup order in the engine.

A territorial promise shared by dynastic and constitutional wars must recognise
both controllers' exact faction records. Capture the defeated country before
clearing those records; repeated accession callbacks must not replace that
earned reunion identity with a later opponent. A split across the recorded pair
can wait for reunification, but third-party ownership remains a genuine loss.
Source-executed tests establish this handoff, not native reunion timing.

<a id="war-09"></a>

## WAR-09 — Buildings, employment, units and manpower are different quantities

Barracks levels do not establish staffed battalions; workforce excludes
dependants, and civilian workers are not qualified officers. Conscription has
native population and rate limits. A building's scripted `potential` is not
a proven gate on native conscription capacity.

<a id="war-10"></a>

## WAR-10 — Deleting and recreating military buildings is destructive

`create_building` increases existing levels; it does not reduce an
over-allocation. `transfer_to_formation` transfers a character, not battalions.
Rebuilding can destroy unit experience, manpower and composition. Conserving
level totals in a test does not establish military equivalence. Record the net
authored relocation around each scripted operation if cleanup must reverse it.
Construction between preparation and the split is not part of that relocation.
After actual reunion, reverse only the receipt up to surviving donor capacity;
do not guess a missing receipt from an older save. Merged ordinary levels do not
retain separate provenance after demolition and replacement.

<a id="war-11"></a>

## WAR-11 — If redistribution is part of the design, account for the actual quotas

Floors and rounding change final shares; give one side the remainder to
conserve totals and use those integer quotas for staffing calculations.
Classify regulars and levies separately. Population transfers must preserve
people and dependants, respect profession rules and retain viable donor states.
Do not restore old headcounts after wartime losses. Keep temporary recruitment
buildings distinguishable from ordinary barracks so demobilisation can preserve
permanent capacity and later construction.

<a id="war-12"></a>

## WAR-12 — Military viability includes the economy

Isolated factions need food,
employment and functioning markets as well as recruitment capacity. Temporary
assistance belongs to the tracked participants and needs terminal cleanup;
repeated pulses must not remobilise already-mobilised formations. Native
recruitment, caps, training, allocation and demobilisation require engine
checks.

If relief is intended for both native one-state and scripted multi-state splits,
attach it to the common exact-war lifecycle, not only the muster helper. The
31 October replay received no old relief because its forces were allocated
natively. Keep its application independent of AI-only supply discounts, and
remove it at exact-war end as well as finalisation/missing-war recovery. A food
security addition is partial relief after native costs/shortages; it is not
commercial grain production or a guarantee against starvation.

<a id="war-13"></a>

## WAR-13 — Hidden action availability is not structural subject eligibility

A diplomatic action's `potential = { always = no }` deliberately prevents its
ordinary selection. Checking that action's availability can therefore block an
authored subject pact. Use the installed `can_have_as_subject` trigger with the
actual country and subject type, then verify the resulting relationship before
delivering dependent territorial rewards. The Confederal Partner definition and
existing Bechuanaland usage establish this source contract; native pact creation
still requires engine verification.
