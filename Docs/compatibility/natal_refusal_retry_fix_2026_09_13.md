# Natal refusal response regression — 13 September 2026

## Runtime evidence

DP loaded a checkpoint at Britain's ultimatum, refused as Natalia, and observed
no confrontation after more than 100 days. The latest autosave is **1850.12.1**.

- `sb_natal_crisis.114` remains queued for GBR (country 3), with the correct Natal
  recipient (16777670), and **3 days remaining**.
- The August–November autosaves also contain that response, with 5, 4, 4 and 3 days
  remaining respectively. It is being retried, not lost.
- Britain is fighting Russia (country 5) in play 100663299, war 16777234, begun
  1848.12.10. This ongoing war remains in the active diplomatic-play list.
- Natal retains its active ultimatum and unconsumed special ultimatum-truce marker.
- The inspected logs do not report a `.114` launch or parsing error.

The Port Natal repair added GBR-level `is_at_war = no` and
`is_active_in_diplomatic_play = no` conditions. Those required Britain to finish
its unrelated war before answering Natalia. That was an introduced scripting
regression, not a demonstrated engine failure.

## Correction

Remove both blanket British conditions. Instead, reject a launch if Britain is
already at war with Natalia or already initiating a diplomatic play against it.
Retain Natal's existing readiness checks, diplomatic permissions, special-truce
handling, and the 30-day retry if engine admission fails. The engine remains
responsible for whether another genuinely conflicting play prevents creation.

A regression check now distinguishes Britain-level conditions from conditions
inside Natal's scope, so unrelated British wars cannot satisfy an accidental
whole-country veto. It failed against the old event before the correction.

## Verification

- 53 focused Port Natal, ultimatum, Natal/Zululand and interwar checks pass.
- Full static validation: 16/16 checks passed or warned, zero failures; the five
  existing deferred-release warnings remain. Output:
  `/private/tmp/sb-natal-refusal-validation.txt`.
- Engine verification remains with DP. With the corrected scripts loaded, the
  December 1 save already has a response due in three days. No save modification
  or reconstructed choice is needed; successful engine creation is not yet verified.

Read-only extracts: `/private/tmp/sb-natal-refusal-2026-09-13/`.
