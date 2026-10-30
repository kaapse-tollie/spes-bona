# Native laws, movements and political calculations

Read when: Laws, movement eligibility, recruitment or political calculations.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="pol-01"></a>

## POL-01 — Direct creation and natural eligibility are different paths

Country
history can create a political movement despite its `creation_trigger`;
`add_journal_entry` can bypass ordinary eligibility too. Test both direct
callers and natural creation after changing starting laws. Startup presence
does not establish that later recreation works. Do not assume a creation-gate
change invalidates an already-active object; verify its maintenance/removal path.

<a id="pol-02"></a>

## POL-02 — A parent's law stances are inherited

Explicit child-law ideology stances
are rejected in the inspected build. A child cannot express opposition to its
own parent through separate stances; use an independent definition when that
distinction is required. Review native family checks before removing a parent
from an existing law.

<a id="pol-03"></a>

## POL-03 — An approved current law can still have a preferred replacement

The
desired-law calculation compares eligible alternatives with the current law.
Inspect the actual demand rather than inferring its absence from an approval
icon. Having that demand still does not prove eligibility for revolution.

<a id="pol-04"></a>

## POL-04 — Movement demands and ordinary enactment need separate gates

A law may
need to remain an eligible movement demand while being unavailable through
ordinary legislation. Blocking shared law eligibility can disable both paths.
Keep demand evaluation valid and use an enactment-specific hook, such as
`on_law_enactment_started`, for the intended ordinary-enactment restriction.
Test demand selection and enactment cancellation separately; callback timing
still requires engine verification.

<a id="pol-05"></a>

## POL-05 — Eligibility, attraction, strength and clout are separate

Renaming an
interest group or increasing attraction does not change `pop_potential`,
occupations or native supporter eligibility. A percentage strength modifier is
not a grant of the same number of clout points. Inspect the full calculation.

<a id="pol-06"></a>

## POL-06 — Attraction, support, activism and war progress are separate controls

Recruitment modifiers act over time; they do not assign supporters directly.
The UI's Activism accessor is `political_movement_radicalism`.
`political_movement_radicalism_add` changes calculated pressure, not an
immediate assignment or a monthly increment. Growth and civil-war progress
require their own checks.

<a id="pol-07"></a>

## POL-07 — Movement membership is not an exhaustive division of an IG

National
movement support combines popular, military and wealth components. An IG's
internal movement backing, its national clout and the list of IGs a movement
pressures are different measurements. Absence from the pressure list does not
prove ineligibility to sponsor a revolution. Likewise, `character_ideologies`
lists possible ideologies for pressured IG leaders; it does not automatically
stack them as the movement's core platform. An agitator role also does not
guarantee attachment to a particular movement; verify the actual character
link before advancing a character-led conflict.

<a id="pol-08"></a>

## POL-08 — Native removal can follow a false scripted disband trigger

Minimum
support and movement age can still cause deletion. `minimum_support_to_maintain`
is parsed as a fixed-point number in the inspected build, not a dynamic script
value. Attraction duration does not reset the movement's grace period; no
exposed creation-age reset was found in the inspected effect registry.

<a id="pol-09"></a>

## POL-09 — A surviving database record can already be dead

Check the manager's
`dead.dead_objects` and `death_date` before treating record presence as
survival or empty supporters as the cause of deletion.

<a id="pol-10"></a>

## POL-10 — Disband notification precedes removal

Creating the same movement from
`on_disbanded` can fail because the old identity still exists. Where a
replacement is required, schedule creation from the surviving owner after
removal and consume its delivery marker once. Do not turn ordinary later
deaths into an unintended revival loop. Successful scripted creation does not
establish future recruitment or survival.

<a id="pol-11"></a>

## POL-11 — Native consumers may require exact identities

Subject drift recognises
specific pro-/anti-overlord lobby types; a custom type with the same category
need not receive the same effect. Native maintenance can also remove a lobby
after creation. Prefer reusing supported identities when only presentation
changes, and verify actual persistence.

<a id="pol-12"></a>

## POL-12 — Relationship rules may concern the other party

Subject-type eligibility
can depend on the overlord's type and rank. Liberty Desire describes the
relationship, not membership in a domestic faction. Native loyalty and ruler
popularity already feed other calculations. Audit existing contributions and
update intervals before replacing a custom value with a native one, so economic
dependence, popularity or other inputs are not counted twice.
