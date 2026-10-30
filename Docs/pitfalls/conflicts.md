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

<a id="war-05"></a>

## WAR-05 — A territorial target is not an army allocation

`target_fraction_of_states`
does not guarantee proportional battalions or manpower. The one-state
provincial path uses movement support; multi-state proposals also depend on
geography and native military rules. Classify the origin before splitting:
two resulting one-state countries do not imply a one-state origin. One owned
state is not itself a blanket bar to ideological revolution.

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

<a id="war-08"></a>

## WAR-08 — Victory callbacks do not prove territorial reunion is complete

Preserve
needed actors before country removal and check actual ownership before applying
regional restoration. Cancellation, a dead contender or a missing war object
is not a substitute for an authenticated winner. Exercise both winners and
the native cleanup order in the engine.

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

<a id="war-13"></a>

## WAR-13 — Hidden action availability is not structural subject eligibility

A diplomatic action's `potential = { always = no }` deliberately prevents its
ordinary selection. Checking that action's availability can therefore block an
authored subject pact. Use the installed `can_have_as_subject` trigger with the
actual country and subject type, then verify the resulting relationship before
delivering dependent territorial rewards. The Confederal Partner definition and
existing Bechuanaland usage establish this source contract; native pact creation
still requires engine verification.
