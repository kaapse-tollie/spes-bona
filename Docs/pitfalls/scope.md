# Scope and reference identity

Read when: Scope changes, shared helpers, saved actors or foreign event roots.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x and 1.15.0–1.15.1 builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="scp-01"></a>

## SCP-01 — Changing the current scope does not change `root`

Entering `c:TAG`
inside another country's event leaves the event root intact. Capture the
current actor at a reusable helper's entry and use that reference for ownership,
variable storage and rollback. A diplomatic-play callback may intentionally
use `root` for the play itself; preserve that identity.

An explicitly guarded country reference is also valid when it identifies the
intended actor.

<a id="scp-02"></a>

## SCP-02 — Check the caller's scope contract

`on_law_activated` has a Law root;
enter its `owner` before country operations. International journal pulses
can have no country root. A country predicate at either root can fail even
when the intended country is eligible.

Option AI conditions also inherit the event's scope. Evaluate country-only
predicates in the intended country context; a state event can enter its `owner`
for those checks while preserving the event root and state-level option effects.
The [state-event AI correction](../compatibility/1_15_0_first_six_months_2026_11_05.md#paralegal-discrimination-ai-scope)
has source-level scope and preservation checks; engine replay remains separate.

Generated API descriptions can contradict their supported input/output scopes.
Resolve the conflict against the target build and observed parser diagnostics.
When replacing an invalid iterator with a broader regional one, filter back to
the exact saved object and verify coverage of custom map partitions; matching a
region alone can select another owner's land. The
[1.15 survey investigation](../compatibility/1_15_0_launch_debug_2026_11_05.md)
records a source correction whose native delivery still needs replay.

<a id="scp-03"></a>

## SCP-03 — Trace both ends of stored state

A variable written on one participant
cannot be read from another merely because both participate in the same event.
Record the holder, value type, readers and cleanup location for each shared
reference. Use captured objects when a tag may be replaced or its original
country may retag.

When changing a cross-country chain, trace the current scope, event/callback
`root`, and the holder of each variable/container at every handoff.

<a id="scp-04"></a>

## SCP-04 — Scripted-effect parameters are substituted where used

Passing
`PATRON = ruler` to a helper does not freeze a character before that helper
enters a loop. Capture the character first and pass its saved scope.

<a id="scp-05"></a>

## SCP-05 — Optional equality does not validate a missing right-hand value

A
comparison such as `this ?= scope:actor.var:old_patron` can still evaluate an
absent variable. Branch on the variable's existence before dereferencing or
comparing it; do not rely on the comparison operator to guard both operands.

<a id="scp-06"></a>

## SCP-06 — Keep temporary names distinct from persistent targets

Reusing an event
or journal target's name for a temporary scope can produce preview collisions
or select the wrong actor. Test helpers with deliberately foreign saved
targets, not only the expected local context.

<a id="scp-07"></a>

## SCP-07 — Creation callbacks have their own scope boundaries

When the caller needs
a newly created character, use the supported `create_character.save_scope_as`
field. Do not assume a scope saved only inside `on_created` is exported to
the caller. Re-enter the owner explicitly before calling country helpers there.

<a id="scp-08"></a>

## SCP-08 — Do not invent scope-navigation syntax

The inspected Tiger context does
not support `prev.prev` for Victoria 3, and no matching upstream example was
found. This establishes a validator/source limitation, not an engine experiment;
use an explicit captured scope instead.

<a id="scp-09"></a>

## SCP-09 — Verify helper routing with a foreign root

For country helpers callable from another country's event or a diplomatic-play
callback, regression checks must exercise a foreign event root and verify actor
identity for ownership gates, rollback, container parents and callback markers.
Presence-only assertions do not establish correct scope routing.

<a id="scp-10"></a>

## SCP-10 — Group conjunctions before negating them

Victoria 3's `NOT` rejects the block when any child is true: a multi-child
`NOT` behaves as `NOR`. To reject only a complete combination of conditions,
put one explicit `AND` inside `NOT` (or use the documented `NAND`). A flat
negation combining an active conflict, its participants and a foreign joining
country can otherwise deny ordinary diplomatic participation worldwide.

```text
# Reject only when BOTH conditions hold:
NOT = {
 AND = {
  <the exact authored conflict is active>
  <the joining country is a foreign participant>
 }
}
```

Global permission rules must allow missing/inactive authored state and
unrelated parties. Authenticate both recorded sides, in either order, before
applying a local veto. Test the native truth table and a fresh unrelated play;
a harness implementing `NOT` as `not all(children)` can certify the wrong
behaviour. See the [1.15.1 joining-rule reproduction](../compatibility/diplomatic_joining_and_outliner_2026_11_13.md).

Do not convert every multi-child `NOT`: an intentional "neither condition"
check needs NOR. Conversely, a cancellation or fallback intended to complement
an eligible `A AND B` branch must become true when **either** prerequisite is
lost. Test both single-invalid cases. Copying the block from a dependency does
not establish its correctness; retain the upstream pin and document any narrow
correction. See the [SB-wide follow-up audit](../compatibility/not_grouping_audit_2026_11_13.md).
