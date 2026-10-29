# Claimant test-entry console crash — 28 October 2026

The **11:51:16** crash is a native random-access/thread collision during manual event invocation. It has a different stack from the 27 October rebel-country creation crashes.

## Evidence

- The last console command is `event sb_court_succession.990` at 11:51:16.
- At the same timestamp, `consolecmdimpl.cpp:1391` reports that random access is blocked by another thread, followed by assertions about acquiring access concurrently and using global random without `ALLOW_RANDOM_IN_SCOPE`.
- The crash stack is `NRandom::CGlobalRandom::GetInteger` → `CTickTask_StartHarvestConditions::Prepare` → the daily simulation tick. This is the engine's harvest-condition processing, not SB's first-fruits event. No SB effect or rebel-creation call appears in this stack.
- Read-only inspection of installed `OnExecute_ExecuteEvent` shows `CGlobalRandom::AcquireAccess` at `0x100271a9c`, before its call to `OnExecute_Event` at `0x100271aac`. The assertion therefore identifies the console wrapper's random-access acquisition, not a malformed SB movement effect. The available single-thread stack does not establish which event effects, if any, subsequently completed on the other thread.
- The newest autosave remains the earlier 1 September 1839 snapshot, written at 11:13:39. There is no newly written autosave capturing this 11:51 crash. Do not use the earlier pending crisis as evidence of how far this invocation progressed.

[Hashes and native inspection receipt](evidence/zulu_claimant_console_crash_2026_10_28.json). Read-only input copies and function excerpts are retained in `/private/tmp/sb-console-crash-2026-10-28/`.

## Next test and limits

Restart, load a disposable pre-crisis checkpoint, **pause and wait until the date stops advancing**, then invoke `event sb_court_succession.990` once. Close the console, make the choice and resume. Pausing is a proposed way to avoid overlapping console execution and daily processing; successful replay remains **pending DP**.

No gameplay script, attraction magnitude, save or dependency was changed for this diagnosis. A script guard inside `.990` would run after the failing native acquisition, so it would not address this entry-point collision. Keep the prior +100% attraction trial and separate unresolved native-war-creation investigation intact. No game launch or new test-suite run was performed: changes here are evidence and testing instructions only.
