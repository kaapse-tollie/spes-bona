# Economy, resources and effect semantics

Read when: Construction queues, resource discovery, markets or payments.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="econ-01"></a>

## ECON-01 — Construction caps must include queued work

For a country-wide limit,
count queued as well as completed levels across all of the owner's states.
Checking only finished buildings allows several queued orders to exceed the
intended cap. Test concurrent orders and the native queue behaviour, not only
the completed-building count.

<a id="econ-02"></a>

## ECON-02 — Capacity is not a delivered quantity

A supplier owning an arms factory
does not establish treaty imports. Inspect actual inward transfers and the
recipient's market goods; aggregate market totals do not identify a particular
treaty article. Likewise, an applied payment modifier does not prove the
intended bilateral cash transfer changed: inspect both countries.

<a id="econ-03"></a>

## ECON-03 — Resource capacity and undiscovered reserves are separate fields

`add_resource_potential` and `change_resource_potential` change capped
capacity, not `undiscovered_amount`. A discoverable building group alone
does not hide those grants. Use native reserve entries and the relevant
building technology requirement when discovery must be gated; preserve shared
bonuses and company coverage. Timing, split ownership and foreign investment
still need campaign verification.

<a id="econ-04"></a>

## ECON-04 — An additive modifier is not a percentage change in the final result

Reducing one base contribution by half does not halve the final total.
Education access, literacy growth, research speed and technology spread are
separate controls. Validate the final engine breakdown before describing the
effect to the player.

<a id="econ-05"></a>

## ECON-05 — Clamped displays can hide the raw value

Food Security applies its
additive adjustment before clamping to 0–1 in the inspected build. A displayed
zero can therefore conceal a negative raw score; adding a threshold-sized
bonus need not reach that threshold. Distinguish modifying the score from
supplying goods.

<a id="econ-06"></a>

## ECON-06 — Price basis and affordability are different design choices

Reserve
capacity is a soft threshold, not a hard treasury ceiling. A cost scaled from
it need not be limited to current reserves. Implement the intended borrowing
rule explicitly and verify native debits; do not infer a cash-only gate from
the price formula.
