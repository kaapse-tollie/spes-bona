# Klip River scope repair — 13 September 2026

Repairs the caller-scope defect identified in the
[1851 save investigation](klip_river_save_investigation_2026_09_12.md).

## Changed behavior

| Path | Repair |
|---|---|
| ZUL response → NAL county creation | Capture the current Natal actor; compare province ownership with that actor rather than ZUL's event root. |
| Failed creation / orphaned attempt → rollback | Return the two Natal provinces to the exact caller, including a retagged original actor; preserve the recorded original owner of the Zulu province. |
| Secession and punitive follow-up containers | Parent each container to its captured Natal actor, even when called from a Zulu event. |
| Setup, preflight and cancellation gates | Identify NAL/ZUL explicitly; check duplicate plays against the correct opposing countries. |
| Punitive play on-start | Read the pending-delivery marker on Natal, where the queue writes it, rather than on Zulu. |
| Initial creation preflight fails after borders change | Use the existing standard Boer-flight fallback when no KLR or creation lease exists; do not leave a pending-only dead end. |

The actual diplomatic-play `root` remains unchanged in callbacks that store or
compare the exact play identity. The Swaziland ownership check used for Klip River
Zulu AI weights now explicitly checks ZUL, including when invoked from a play.
No prose, county footprint, starting package, AI choice weights or settlement
rewards were changed.

## Why the prior validation missed this

The implementation confused the helper's current country with its caller's event
root. Existing checks covered the presence of transaction markers, ownership gates
and rollback effects, but did not establish which actor those references resolved
to when the helper was called from another country's event. Consequently, valid
script could pass static validation while returning false at runtime or attaching
its follow-up state to the wrong actor.

The new tests resolve the references read from the actual scripts under NAL, ZUL
and diplomatic-play roots, including rollback by a retagged original actor. They
also check that a callback reads a pending marker from the same actor that wrote
it. These are focused identity tests, not a replacement for engine execution.
`AGENTS.md` now requires this scope review for cross-country changes.

## Validation

- Six regression tests fail against the retained pre-fix scripts (16 failing
  subtests, zero test errors).
- All 70 focused Klip scope, story-war, Natal/Zululand and frontier AI checks pass.
- Full static validation: 16/16 checks passed or warned, zero failures. The five
  previously deferred release gates remain warnings. Output:
  `/private/tmp/sb-klip-scope-validation.txt`.
- Engine testing remains with DP: Zulu recognition of KLR, the punitive alternative,
  successful follow-up delivery, failed-creation fallback and exact rollback.

The existing 1851 pending-only save does not retain the Zulu choice. This repair
changes future execution and does not automatically infer/replay that lost choice
or modify the save. A fresh run or a save from before the Zulu response is the
engine verification baseline.
