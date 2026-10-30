# Second Zulu succession: one-province rebellion — 29 October 2026

**Finding:** Cetshwayo's frozen coalition and the scripted territorial target were
correct. The native one-state provincial split uses movement support instead of
that target. SB currently does not scale the claimant movement's recruitment with
its frozen coalition share. No gameplay scripts or saves changed in this check.

## Saved sequence

The five retained autosaves cover 1 November 1856 through 1 March 1857. Their
hashes, country variables, movement and exact war record are preserved in
[evidence](evidence/zulu_second_succession_split_2026_10_29.json).

- November/December: ZUL country 481 owns only its portion of STATE_ZULULAND.
- January: succession crisis reason 2; Mbuyazi 4481 is the nominee, Cetshwayo 4480
  the rival. Frozen backing is **190 versus 189**, giving rebel target **0.49868**.
  The claimant movement 33554505 was created on **16 December 1856** and has 50%
  activism on 1 January, with `sb_court_claimant_mobilisation` present and
  Cetshwayo attached. No native civil-war record exists yet in that checkpoint.
- February/March: tracked revolution **134217731**, originating in 481 with
  rebel country **16777853**, is linked to that exact claimant movement. Mbuyazi
  rules 481 and Cetshwayo rules the rebel. The target remains 0.49868 on both.
- Original state 779's January province run is `4469 8`: nine owned provinces.
  Afterwards 481 retains `4469 7` (eight), and Cetshwayo receives `4477 0` (one).
  Rebel `land=0.07692` is a share of the full state region; it must not be read as
  evidence that the original owned state had thirteen provinces.
- No scripted multi-state muster applies: the origin had one state. Military
  reconstruction/population transfer is deliberately bypassed for that route.

This is the authored dynastic movement, `movement_sb_dynastic_test`, rather than
the separate ordinary `movement_sb_zulu_royal` constitutional movement.

## Why 49.87% did not produce approximately half the provinces

The movement's `target_fraction_of_states` reads the frozen rebel target. In the
installed engine's **one-origin-state / one-uprising-state** branch,
`CreateNonDynamicCivilWarCountry` instead calls `GetCivilWarSupport` and calculates:

```text
combined support = 0.34 × popular support
                 + 0.33 × military support
                 + 0.33 × wealth support
rebel province count = clamp(truncate(owned passable provinces × combined support),
                            1, owned passable provinces − 1)
```

`GetCivilWarSupport` reads the movement's cached combined support. The passable
province accessor operates on the owned CState, not the full state region.
[Read-only native excerpts](evidence/zulu_one_state_provinces_1_14_5_arm64.txt)
and installed `common/defines/00_defines.txt:93–95` establish these links.
For nine passable provinces, combined support below 22.222% produces one province;
49.868% combined support would target four. The save does not serialize the exact
cached support at the moment of division, so this report does not claim its exact
value at that instant.

As a separate recruitment observation, the January checkpoint records 5,872
individual movement backers across eighteen Pop groups. That is not 49.87% court
support and must not be labelled the engine's combined support. Popular support's
denominator is political participants; military/wealth contributions are separate.

## Current recruitment and advancement

- Fixed **+100% Pop Attraction** from `sb_court_claimant_mobilisation`.
- Pop support weight also uses `clamp(1 + rival popularity / 100, 0.2, 1.8)`.
- The named prince contributes native agitator recruitment.
- None of those terms reads frozen coalition share.
- Activism is accelerated to 25 percentage points per week. Once the named
  movement has an organising civil war and the correct prince/demand, SB advances
  that exact war by 1. No coalition-relative movement-support readiness check is
  made before advancing it. High activism does not imply broad recruitment.

## Implication, not an implemented change

A stronger attraction modifier could enlarge the one-state rebellion, but a
fixed multiplier cannot guarantee a particular provincial or military split.
A next design should connect temporary recruitment to the **actual rebel side's
frozen share** and account for support accumulation before native division. It
must preserve player-side inversion, one-state/multi-state distinctions and the
existing military allocation contract. A support threshold without a verified
reachable recruitment level could stall the war, so do not add it blindly.

No new mechanics are approved or implemented by this investigation. Independent
Sol 6.1 Max review confirmed the native branch and weighted-support calculation.
No game launched; the result is save evidence plus read-only native/source analysis.
