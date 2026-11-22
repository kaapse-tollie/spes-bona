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

In 1.14.5 the building technology check succeeds on the **first researched
entry** in `unlocking_technologies`. Adding Prospecting alongside a later
technology opens an alternative early route. Native discovery also checks
other owners of the region and eligible foreign investors. Test a Prospecting-only
owner and a technologically advanced investor separately. A saved discovery
count establishes how much has been found by the save date, not the date of the find.

For owner-only surveys, hold the budget and its timer on a persistent state
region. A province identifies the surveyed land through a state merger.
Recheck its current owner on delivery. In 1.14.5 `change_resource_potential`
reads `amount` as a literal integer. A sampled amount can be delivered with
a counted loop of literal increments. See the [survey implementation and
replay limits](../compatibility/frontier_playtest_2026_11_04.md#owner-only-surveys).

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

<a id="econ-07"></a>

## ECON-07 — Qualifications do not bypass protected subsistence employment

A farm can have cash, vacancies and qualified peasants nearby while being unable
to recruit them. In the inspected 1.14.5 engine, protected subsistence employment
compares the source building's current employees with its maximum employment;
it is not the peasant share of the country's workforce. Serfdom's 50% floor
blocks transfers from an incorporated state's subsistence building while it is
at or below that staffing ratio. More arable capacity can worsen the absolute
floor. Inspect the active law, incorporation and source employment restrictions
before adding population or qualification bonuses.

Distinguish `building_subsistence_output_mult` (in-kind household income) from
actual market-goods output/throughput. Food Security can bridge a recovery but
does not create grain. A targeted state modifier can reach the native hiring
consumer; its scope, ownership cleanup and expiry must still be tested. Removing
one hiring restriction does not establish that wages, qualifications or food
supply are then sufficient. See the [Lesotho investigation and native evidence](../compatibility/bst_lesotho_famine_2026_11_01.md).

<a id="econ-08"></a>

## ECON-08 — Moving a Pop preserves its household composition

In the inspected 1.14.5 engine, `move_partial_pop` selects total individuals and
preserves the donor's actual worker/dependant ratio, with rounding. It does not
accept a worker-share override. Runtime `create_pop` accepts
`working_adult_ratio`, but creates and initialises a new Pop rather than cloning
the moved cohort's attributes. Do not implement a demographic adjustment as an
unexamined delete/recreate operation or apply it to a merged destination Pop
while describing it as affecting arrivals only.

Runtime `create_pop` uses **`pop_type`**, not the history-only `type` field.
Creation may immediately merge with residents. If approved reconstruction needs
attribute setters, isolate arrivals under an absent staging culture, restore
attributes, then restore their real culture last. Wealth restoration must use
`update_loyalties = no`; its default otherwise rewards/punishes the apparent SoL
change. The source filter must use the original profession, while arrivals
follow native conversion (in 1.14.5: peasants → labourers; slaves → labourers where
slavery is absent). Copying a chosen donor's values is not weighted preservation
of several source Pops. Removal/creation also does not clone qualifications,
political support or migration/death bookkeeping; record these limitations.

`state_working_adult_ratio_add` changes a state-wide demographic target; it does
not guarantee an immediate ratio for selected refugees. Distinguish total
population, workers, employed workers and qualifications. Verify population
conservation and inherited attributes before replacing a native transfer, and
leave economic recovery claims pending engine replay. See the
[refugee-ratio assessment](../compatibility/bst_refuge_workforce_ratio_2026_11_01.md).
