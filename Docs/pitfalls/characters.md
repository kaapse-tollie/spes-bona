# Characters, templates and political roles

Read when: Templates, identity, careers, traits, succession records or character roles.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="char-01"></a>

## CHAR-01 — Names are not identity keys

Check template, lineage, dates and existing
creation paths before adding or reusing a historical character. An absent local
character may be exiled, dead, retired or deliberately ineligible. Where an
identity must be created only once, `is_template_used` is safer than checking
only for a living local instance.

<a id="char-02"></a>

## CHAR-02 — Template dates do not schedule births

Trace eligibility → creation →
exported handle → registration. A newborn introduced at a variable date needs
age relative to creation, rather than a fixed birth date that makes late
introductions older. Reusing an existing identity must not reset its age.

<a id="char-03"></a>

## CHAR-03 — Use native adulthood for political eligibility

`is_adult` and portrait
ageing have different thresholds. Copying the portrait age into candidature
or regency rules can delay political adulthood.

<a id="char-04"></a>

## CHAR-04 — Historical status does not prevent career expiry

A long-lived authored
politician may need `set_career_length` after acquiring the role. That does
not extend life or protect against other scripted removal. Compare IDs, career
dates and death evidence before diagnosing disappearance; a template correction
does not resurrect an already-deleted save record.

<a id="char-05"></a>

## CHAR-05 — Explicit traits do not disable default generation

Even `traits = { }`
can receive random personality and skill traits through `trait_generation`.
Control generation on the affected templates where required, preserving native
experience and Child bookkeeping. Do not replace the global default to
stabilise a small cast.

<a id="char-06"></a>

## CHAR-06 — Evaluate traits in the role actually held

Universal, ruler, commander and
interest-group-leader modifiers apply in different contexts. A trait's name
does not establish its effects, and repeated or differently scoped blocks must
not be flattened into assumed engine totals. Check native office bonuses before
adding another scripted contribution.

<a id="char-07"></a>

## CHAR-07 — Native helpers can carry hidden role and scope assumptions

The inspected
`commander_coup_strength` includes an unassigned bonus outside its commander
gates and reads `root.owner`. Reusing it for civilians or from a foreign root
can therefore miscalculate or fail. Check the internal predicates and capture
the actual character before adapting a role-specific calculation.

<a id="char-08"></a>

## CHAR-08 — Keep presentation separate from political mutation

A card showing
allegiance should not repeatedly overwrite ideology. Refresh dependent
eligibility when roles or interest groups change, while preserving unrelated
commitments and claims. Capture outgoing commitments before succession clears
dead references.

<a id="char-09"></a>

## CHAR-09 — Understand dependency-owned lifecycle hooks

CMF's `no_heirs` mechanism
kills newly generated heirs in `on_heir_born`; it is not a native generation
switch. Authored appointments must coordinate with that callback, preserve
independently owned blocks and release their own block when it is no longer
needed. Callback timing requires engine verification.

<a id="char-10"></a>

## CHAR-10 — Transfer does not detach a registered political constituency

A court may intentionally count some foreign royal exiles. A refused or banished
visitor therefore needs explicit registry/home removal, not just
`transfer_character`, when the design removes their political following.
Source-executed fixtures reproduced the residual house weight; preserve the
separate intended treatment of royal exiles.
