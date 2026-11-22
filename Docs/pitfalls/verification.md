# Verification and diagnosis

Read when: Regression design, save inspection, crash attribution or engine replay.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x and 1.15.0 builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="verify-01"></a>

## VERIFY-01 — State what each check proves

Parser validation checks syntax and known
API contracts. Source-executed tests check the script behaviour represented
by their fixtures. Save inspection records an observed state. Engine replay
checks delivery, timing and native interactions. Passing one layer does not
establish the others; record unresolved hypotheses and pending scenarios.

<a id="verify-02"></a>

## VERIFY-02 — Test the failure mechanism, not just token presence

Use the actual
script references and relevant adverse contexts: foreign roots, stale objects,
held popups, duplicate delivery, changed ownership, retags, both controllers
and both outcomes. Include negative controls for unrelated countries and
conflicts. Choose cases relevant to the change rather than adding speculative
machinery.

<a id="verify-03"></a>

## VERIFY-03 — Validate the model used by tests

Fixtures must not invent inherited war
lists, propagate scopes across isolated callbacks, skip incomplete creation,
ignore fixed-point truncation or replace native caps with unrestricted sums.
Independently check API spellings and scope contracts against installed sources;
a test interpreter can reproduce the same mistaken assumption as the script.

<a id="verify-04"></a>

## VERIFY-04 — A crash stack identifies the failing operation, not necessarily its cause

Nearby log messages and recently changed code are leads. A repeated stack
establishes repeatability; a guard is a proposed mitigation until replay
establishes whether it prevents the failure. Changed timing, play order or
loaded scripts can confound an apparently successful retest.

<a id="verify-05"></a>

## VERIFY-05 — Read saves within the correct databases and dates

Numeric IDs can repeat
across managers; distinguish dead records and omitted defaults. In the
inspected save format, signed fixed-point variables can be stored as unsigned
64-bit identities: decode the sign before applying the scale. Compare event
creation/expiry, actor scopes and conflict records together.

<a id="verify-06"></a>

## VERIFY-06 — Outcome snapshots rarely reconstruct the entire cause

Post-war armies,
populations and economies may reflect subsequent hiring, migration and AI
construction. Shared terminal flags cannot identify which branch ran. Preserve
checkpoints around the relevant transition before autosaves overwrite them,
and separate observations from inferred sequencing.

<a id="verify-07"></a>

## VERIFY-07 — Retest from a checkpoint that can exercise the correction

Open events
retain saved scopes; completed settlements and deleted identities are not
undone by script reload. New database definitions may be absent from a running
process despite valid files on disk. Use a full restart and an appropriate
earlier save for load-order, startup, map and creation changes.

<a id="verify-08"></a>

## VERIFY-08 — Static map validity does not prove engine acceptance

Hash parity,
adjacency and graph connectivity can pass while a deployed spline is rejected.
Inspect the generated graph and authored ports, then verify launch acceptance
and actual movement separately. Do not repin a changed hash without review or
call a static pass proof of successful AI deployment.

Check each changed port's declared province, locator and paired land/naval anchor
identities. A valid offshore route does not prove the land anchor exists or the
locator sits in the port province. Use unmodified native controls and fixtures
that deliberately break each relation. Generated map tables may also use a
different text reader from scripts: compare encoding with the corresponding
native file, not a blanket BOM rule. These checks caught gaps in the
[1.15 launch investigation](../compatibility/1_15_0_launch_debug_2026_11_05.md);
native harbour generation and movement remain separate engine gates.

Native parity can preserve a native map inconsistency. Compare the declared port
province with both native and mod raster samples before attributing a mismatch
to the mod. The [1.15.1 Panama review](../compatibility/1_15_1_launch_review_2026_11_11.md)
establishes identical mismatched source data, not successful native port operation.

For a country-specific HQ warning, inspect contemporaneous coastal control and
occupation as well as ownership before changing the map. The missing-connection
wording alone does not establish missing map data; the
[occupied-coast investigation](../compatibility/1_15_0_fresh_smoke_bolivia_2026_11_07.md)
records intact native routes alongside loss of the country's controlled coast.

A cached naval graph can retain generic landing harbours on land a mod makes
impassable. Check harbour destinations against the effective passability mask,
not just designated building ports or sea reachability. Preserve actual port
splines separately; removing obsolete leaf landings must not remove through
routes. Runtime node IDs may include nodes created before the cached records,
so establish their ordering before mapping IDs to file indices. See the
[impassable-coast evidence](../compatibility/1_15_0_launch_retest_2026_11_05.md).

<a id="verify-09"></a>

## VERIFY-09 — Declare intentionally callerless test events

Use the supported
`orphan = yes` for events invoked only through console tests. Do not add a
fake production caller merely to silence orphan warnings; keep accidental
orphan detection useful for events that require a real delivery path.

<a id="verify-10"></a>

## VERIFY-10 — Console tests can introduce their own failure mode

The inspected native
event wrapper acquires random access before dispatch, so an event-internal
guard cannot protect that boundary. Pause and wait for the date to stop before
manual event calls; this is a precaution, not a verified fix for every console
crash.

<a id="verify-11"></a>

## VERIFY-11 — Keep engine verification with the maintainer

Follow [AGENTS.md](../../AGENTS.md)
for launch responsibility. Record required replay conditions and limitations
without describing a source correction as an engine-confirmed fix.
