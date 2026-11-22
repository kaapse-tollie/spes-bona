# Victoria 3 1.15.0 — first six months, 5 November 2026

The two paralegal-discrimination errors are native **state-to-country scope
errors**. A narrow SB compatibility correction is applied; engine replay is
pending. The Riograndense HQ warning remains an investigation item: the relevant
port sources match Vanilla, and the saved campaign brackets the country's
elimination. No map correction is justified by the available evidence.

## Inputs and preservation

The [supplied log](../../generated/rebase_1_15_0/first_six_months_2026_11_05/error.log),
system/playset logs, three autosaves and starting repository hashes are preserved
under `generated/rebase_1_15_0/first_six_months_2026_11_05/`.
The [evidence record](evidence/1_15_0_first_six_months_2026_11_05/investigation.json)
contains their hashes, source comparisons, country/HQ observations and results.
The [task diff record](evidence/1_15_0_first_six_months_2026_11_05/task_diff.json)
separates these changes from the existing working tree.
Targets remain game build `26453692`, core manifest `7727600027425614094`, CMF
`1.67.1` + `sb-1.15.0-r1`, with all DLC. No engine launch was performed by the agent.

## Paralegal-discrimination AI scope

Vanilla's `paralegal_discrimination.1` is a `state_event`. Its options B and C
call `ai_avoids_radicals` and `ai_wants_radicals` directly from their AI modifier
triggers. Both helpers query the current country's journal, matching the two
logged `has_journal_entry` scope failures. Neither SB nor CMF previously replaced
this event or these helpers. The nested French AI predicates read the same
country's path variable; they do not navigate to the event root.

The [event shadow](../../events/paralegal_discrimination_events.txt) wraps only
those two AI predicates in `owner = { ... }`. Removing the wrappers restores
the pinned native file byte for byte, including its BOM. State effects, event
root, timing, cooldown, native once-only setting, text references and AI weights
are unchanged. The full-file collision is registered in the
[override inventory](override_inventory.json); no shared AI helper is changed.

This is the only non-country event definition calling either helper in the
inspected Vanilla event files. Hail Columbia and Gates of the Bosphorus have no equivalent non-country
caller to copy. The target API's
[`has_journal_entry` contract](../../../References/Modding-Digests/1.15.0/docs/triggers.log)
and the actual native helper bodies establish the required country scope.

## Riograndense naval HQ

The warning names country **296** (`PNI`, Riograndense Republic), naval HQ **634**
in Brazil. Rio Grande do Sul uses the native state definition and identical
starting ownership. Its port `x52B247`, locator 388, paired spline anchors and
complete sea route match Vanilla. Both native coastal harbour nodes, their
connections and identities survive the earlier African graph correction exactly.
Native and SB source-access checks both pass; that is not an engine-travel pass.

| Preserved save | Observed state |
| --- | --- |
| 1 February 1836 | Country 296 owns state 312; naval HQ 634 exists |
| 1 May 1836 | Country and HQ still exist; the country is at war |
| 1 June 1836 | Country records game-over on 10 May at 12:00 and death at 18:00; state 312 belongs to Brazil (`BRZ`); HQ 634 is absent |

The 23:06:16 warning falls between the May and June autosave timestamps.
Wartime loss of port control or country/HQ retirement is therefore a plausible
explanation. The snapshots do **not** establish the exact control or travel
position at that instant, nor prove a Vanilla engine bug. No raster, state
history, passability, port, spline or naval-graph change is made for this warning.
Do not remove a working connection or add a new one merely to silence it.

## Verification and next replay

The [new regression](../../tests/test_1_15_paralegal_scope.py) reproduces both
native scope failures, evaluates the corrected predicates and nested native
French-path helpers with explicit state/country contexts, and verifies complete
native-byte parity outside the two wrappers. It covers no active journal, no
selected path, all three monarchist paths and the republican path.

The focused run passes **24 tests**. The full suite has **1,086 passed, eight
skipped and one failed**. The failure is the unchanged localisation review gate:
the dangling Swazi queue row and reviewed drift in the three previously recorded
Natal/Klip River entries. Map, naval network, script contracts and Vanilla/CMF
override checks pass. Tiger 1.19.0 remains unavailable as a target validator
because its schema lacks required 1.15 fields. Full output is
[preserved locally](../../generated/rebase_1_15_0/first_six_months_2026_11_05/full_validation.txt).

Restart before replaying: the event is a newly added exact-path shadow. Use a
fresh campaign or the preserved 1 February checkpoint, which predates the scope
errors; a later save may already have consumed the native once-only state event.
Check that AI evaluation produces no scope errors and the original choices still
apply their effects to the state.

For the HQ warning, replay the May checkpoint and observe Riograndense port
control and country elimination. If it recurs while the country still controls
its port, retain that immediate save and compare a fresh native control before
changing the map. See [RT15-16 and RT15-17](1_15_0_runtime_matrix.md).
