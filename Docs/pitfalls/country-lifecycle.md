# Country creation, inheritance and object lifetimes

Read when: Country creation, annexation, restoration, inheritance or creation callbacks.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="life-01"></a>

## LIFE-01 — Country creation has an incomplete phase

Inherited-law callbacks can run
before land and AI are assigned. Calling `add_journal_entry` at that point
can crash. A global post-lobby marker does not protect later country creation;
guard the actual owner and use the ready-country handoff. In the inspected
build, `is_country_alive` requires a non-zero state count. Static callback
fixtures must include the incomplete phase and cannot replace engine replay;
see the [creation-order investigation](../compatibility/zulu_contested_crown_2026_10_27.md#follow-up-rebel-country-creation-crash--guarded-replay-pending).

<a id="life-02"></a>

## LIFE-02 — Startup completion and country readiness are separate prerequisites

Law-activation callbacks also run during history setup and can add a journal
entry before history adds its authored opening entry. Where history owns that
initial entry, defer dynamic reconciliation until the startup bootstrap is
complete. A per-country readiness check does not replace this ordering guard;
the startup guard does not establish a later-created country's readiness.
Check both sequences for premature activation and duplicate entries.

<a id="life-03"></a>

## LIFE-03 — References are not backups

Annexation or country removal can destroy
characters, movements and other objects despite stored references to them.
Preserve required living actors before their owning country disappears and
restore them after the receiving country is ready. Capture ruler and heir
before moving either, because succession can change the next accessor.

<a id="life-04"></a>

## LIFE-04 — Preserve every required identity

A live adult list or aggregate faction
projection may omit minors, exiles and unrepresented advisers. Use the required identity records for lifecycle transfers; do not
reconstruct people who actually died. Skip `transfer_character` when the
character already belongs to the receiving country.

<a id="life-05"></a>

## LIFE-05 — Inheritance is field-specific

Sharing a country definition does not prove
that an active journal entry, counter, list or completion flag was inherited.
Inspect native inheritance before adding copies. Copy retained progress before
initialisation can overwrite it, and do not regrant a completed reward.

<a id="life-06"></a>

## LIFE-06 — Check evidence before replacing native inheritance

Missing explicit
technology grants in a helper do not prove missing research. Compare completed
technologies, active research, the creation origin and the founding date.
A fixed technology floor can erase the intended inheritance behaviour.

<a id="life-07"></a>

## LIFE-07 — Create the intended territory explicitly

General release actions may
include historical land outside the proposed settlement. Verify the actual
footprint and subject relationship before marking setup complete. Do not
release and re-annex a country merely to present a direct-rule option.

<a id="life-08"></a>

## LIFE-08 — Government refresh can replace a scripted ruler later

Installing the
ruler after law changes is insufficient if a subsequent native callback selects
another. Use the native temporary retention guard only in helpers that read it,
and let it outlive the refresh. `keep_current_ruler_var` is not honoured by
every government-change helper; it is not a universal succession lock.

<a id="life-09"></a>

## LIFE-09 — Create formations before commissioning their commanders

Commissioning
first can create an unwanted default formation. Select the intended commander,
create the authored formation, then assign the commander to it. Source ordering
checks cannot prove the engine avoids extra formations; do not sweep-delete
existing armies to hide the symptom.

<a id="life-10"></a>

## LIFE-10 — Inherited markers can activate unrelated native content

Country
replacement, revolution and restoration can preserve flags with Vanilla
consumers. Inspect those readers and already-queued events before assuming a
later cleanup hook prevents the inherited behaviour.
