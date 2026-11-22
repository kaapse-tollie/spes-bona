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

In the inspected 1.14.5 engine, ordinary Pop political membership updates use an
annual cohort; each visit limits movement changes to 10% of political participants
(minimum ten individuals for small Pops). Weekly attraction changes do not create
weekly recruitment turns. `recalculate_pop_ig_support` forces a country-specific
turn, but updates other movements and IG membership too. Preserve native cache
boundaries between modifier changes, recalculation and support sampling; do not
assume a same-effect-block query is fresh. A periodic controller can refresh with
the previous interval's settled modifier, apply the next modifier afterwards,
and read support on the next interval. This deliberately delays feedback; bound
the refresh count and measure effects on other local movements and IGs. See the [failed recruitment trial](../compatibility/zulu_recruitment_stall_2026_10_31.md)
for save evidence and reproducible native excerpts. Targeted-refresh convergence
and its political side effects remain untested.

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

Equal `character_support_weight` values do not bind an agitator to the intended
cause: the installed engine favours the current movement with its stickiness
multiplier. Give an explicitly designated story leader priority only within that
story's active context, and let a later dedicated conflict take precedence.
Preserve the character's broader ideology. Check the actual movement's character
list in saves; a role or faction trait alone is insufficient evidence.

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

<a id="pol-13"></a>

## POL-13 — Present opponents and future successors are different relationships

A helper selecting constitutional opponents or eligible princes need not exclude
characters personally loyal to the ruler. For an action against a current rival
camp, use the representative's present endorsement and actual patron; validate
that patron independently, including loyal-prince protections. A future-heir
pledge is not evidence of present opposition. Capture the displayed participants
once and revalidate them together before applying effects. Dunn shipment
regressions exercise loyal princes, future-only pledges and a changed patron;
native popup persistence and rendering remain DP checks.

<a id="pol-14"></a>

## POL-14 — Gate the cause and uprising mode, not the whole movement

An ideological movement may supply both revolution and secession definitions.
A scoped restriction must inspect both possible blocks while leaving unrelated
cultural/religious causes and outside countries intact. Preserve already started
conflicts rather than deleting them through an eligibility change. When copying
CMF definitions, compare complete bodies allowing only the intended gate; do not
silently lose its geographical or timing hooks. Blocking native uprising does
not prove actual Activism can reach an event endpoint: test that endpoint and
expiry ordering in the engine. See the [Chiefdoms implementation](../zulu_thirteen_chiefs_implementation_2026_11_10.md).
