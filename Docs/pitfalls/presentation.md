# Tooltips, localisation and GUI

Read when: Tooltip evaluation, localisation context, journal widgets, portraits or GUI layout.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="ui-01"></a>

## UI-01 — Preview does not execute prior mutations

Tooltip traversal can inspect
hidden effects, `after` blocks, variable increments and dependent comparisons
without first creating their counters or containers. Guard every dependent
read and scope write behind an existence check. Hiding an effect removes its
presentation; it does not make invalid references safe.

<a id="ui-02"></a>

## UI-02 — Test preview separately from execution

Run preview checks without
mutations and include missing counters, exhausted lists, stale actors and
foreign roots. A test that initialises state or forwards callback scopes for
convenience can conceal the real failure.

<a id="ui-03"></a>

## UI-03 — Localisation contexts do not automatically survive nested calls

`JournalEntryType.GetName` supplies no script root; promoting a missing
`ROOT` can fail before a validity test. `SelectLocalization` can create a
fresh data container without temporary `ROOT`, `SCOPE` or `THIS` bindings.
Use scope-free lobby checks such as `IsInGame` before selecting text that
requires an in-game context. For that text, use the actual widget context,
such as `JournalEntry.GetCountry` where available, or keep scoped text in the
outer row. `GetPlayer` is not a substitute for the displayed object's owner.

<a id="ui-04"></a>

## UI-04 — Tooltip-only loops must use their available context

Do not rely on
`save_scope_as` inside a preview loop to supply later names. Prefer direct
localisation against the current `THIS`, and select a branch in script if
nested localisation would lose the required actors.

<a id="ui-05"></a>

## UI-05 — Custom tooltips must cover the requirement they describe

Use a named
`custom_tooltip` when raw variables or other implementation checks need a
player-facing explanation. If one compound requirement contains an `OR`,
wrap the full relevant predicate; covering only its numeric branch can still
expose internal conditions. Preserve readable native condition tooltips where
they already explain the rule. Hide bookkeeping, random scheduling and
remove/reapply maintenance while showing the real costs, consequences and
failure reasons.

<a id="ui-06"></a>

## UI-06 — Preview the effect actually applied

A scaled or decaying timed modifier
differs from its static definition. Use supported live UI accessors, such as
`Country.GetTimedModifier` and `TimedModifier.GetDesc`, in their proper
context. These GUI methods are not event-script APIs. Avoid empty zero-strength
modifier rows and verify their icons exist.

<a id="ui-07"></a>

## UI-07 — Journal presentation has separate mechanisms

`event_outcome_completed_desc`
can describe alternative outcomes; `show_as_tooltip` can preview a shared
effect without executing it. Neither should duplicate the reward. A progress
bar's `desc` labels the bar, while ordinary hover breakdowns use declared
periodic progress. A `set_bar_progress` projection may need a widget tooltip;
adding fake periodic progress changes the simulation.

A bespoke bar does not consume CMF target-container settings automatically.
Reuse the installed marker templates with an explicit normalised value when
adding a fixed threshold to such a bar; retain the moving value indicator.
A visual threshold is only one entry condition, so its explanation must name
the relevant backing pool and preserve eligibility/cooldown qualifications.
Native marker overlap and tooltip hit areas still need rendering verification.

<a id="ui-08"></a>

## UI-08 — Use supported journal fields and renderers

The default pin field is
`should_be_pinned_by_default_uninvolved_or_context`. A custom `complete`
trigger can make automatic `_goal` text redundant. Adding CMF's scripted-button
widget does not replace the default button grid. Inspect the existing renderer
before adding a second one.

<a id="ui-09"></a>

## UI-09 — An invented event window can crash

Resolve `gui_window` against actual
installed GUI definitions. Native character windows include
`event_window_1char_tabloid` and `event_window_2char`; supply their expected
saved portrait subjects, including `left_icon` for the single-character window.
An event icon alone does not provide that portrait.
Script parsing and effect tests do not validate the window contract. Validate every
reachable follow-up window too: a valid arrival popup can crash when its option
immediately opens a delivery event with an absent template.

<a id="ui-10"></a>

## UI-10 — Do not make an expired optional handle the GUI root

A character-scoped
scripted GUI can fail its type check before its predicates reject a stale
character. Anchor the operation on a stable owner and pass the optional actor
as a guarded saved scope.

<a id="ui-11"></a>

## UI-11 — Give each button one interaction target

Formatted character links inside
button labels can compete with the button's own click action. Use passive
labels and the live item's Character context for navigation. This is a
plausible prevention pattern, not proof of the cause of every missed click;
repeated clicks and nested lists still need engine testing.

<a id="ui-12"></a>

## UI-12 — Layout and quoted text need rendering checks

A window inside a flow can
still occupy space despite `layer = popups`. Constrain widths, use native
scroll widgets and allow multiline content to resize. Text inserted into a
quoted GUI expression can break that expression: an ASCII apostrophe in a
substituted name can terminate a single-quoted tooltip argument. Test the
actual renderer and use a compatible escape or typographic form.

<a id="ui-13"></a>

## UI-13 — Write about the player's decision

Name the actors, distinguish promises
from immediate changes, and explain values and available actions. Keep internal
variable names and implementation commentary out of ordinary prose. Follow
comparable DLC presentation and the review-marker rules in [localisation review policy](../policies/localisation-review.md);
moving a marker must never manufacture approval.
