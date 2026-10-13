# Klip River chain inspection — 12 September 2026, 17:07 saves

## Observed state

The latest campaign is Natal Colony on **1851.9.1**, not the earlier 1860 Natalia
campaign used for CAP deployment testing. All five current autosaves (May through
September 1851) contain only `sb_klip_river_county_pending_var` for this chain.

- NAL is country 16777670 and has `sb_natalia_british_colony_resolved_var`.
- ZUL is alive as country 481, ruled by Mpande (character 4478).
- No KLR country definition exists in the save, including a dead KLR record.
- No Klip River event is queued or open in the serialized event manager.
- No scheduled, ready, secession, punitive, delivery-generation, resolved or
  Boer-flight marker survives. There is no Klip River container or active play.

This is an unresolved, unqueued chain, not the normal initial 120/210/300/390-day
wait. The pending marker alone prevents the scheduler from restarting it. The
commission recovery branch requires the missing ready marker, so monthly
housekeeping does not advance this state either.

## Likely failure path and verified script defect

The scheduling endpoint `.001` removes `scheduled` and sets `ready` before the
commission. The commission event `.010` removes `ready` on delivery. Sending the
commissioners queues ZUL's `.020` response. Its republic option `.020.b` calls
`sb_klip_river_create_county` inside a `c:NAL` block.

That changes the current country scope but does not change the event ROOT, which
is ZUL. The creation helper's initial guard checks:

```
country_definition = cd:NAL
p:xDE0EDE.state.owner = root
p:x552449.state.owner = root
```

The two provinces must be Natal-owned for the preceding commission to be valid.
When the helper runs from ZUL's response, it instead compares their owner with
ZUL. With the expected borders the guard fails before any creation lease, county,
transfer or fallback is performed. The caller then tries the secession delivery,
which requires an existing KLR; that also does nothing. This produces precisely
the pending-only dead end observed in the saves.

This is a concrete caller-scope defect. The saved state is strongly consistent
with the republic-response branch failing, but neither the saves nor the logs
retain an explicit choice receipt proving which `.020` option the AI selected.
Mpande's `tactful` trait is not choice evidence: his starting template already
contains it. A question asking DP which commission option they selected was sent
while inspecting the scripts.

## Logs and limits

Current error/game/debug logs contain no Klip River-specific failure. Rotated
logs show the event file loading, not individual response execution. A false
ownership guard is a legal trigger result and need not produce an engine error.

Read-only extracts and summaries are under
`/private/tmp/sb-klip-investigation-2026-09-12/` and
`/private/tmp/sb-klip-summary.txt`. No game was launched, no save edited, and no
runtime change made during this inspection. Fixing this branch requires explicit
Natal actor identity throughout creation/rollback, plus deliberate handling of a
failed initial preflight; blindly replaying an unknown saved choice is not a
verified reconstruction of the original outcome.
