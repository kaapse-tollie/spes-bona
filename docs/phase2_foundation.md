# Phase 2 Foundation

This file tracks the structural groundwork for the next layer of Southern Africa content. It is intentionally narrower than a full design document and only records what is already implemented in data.

## Scope Model

- Phase 2 is treated as a content layer, not a hard-dated chapter.
- Historical dates may still be used inside specific event chains where they are intrinsic.
- The active focus is to make later mid-century systems possible without hard-coding them to the old oversized state and tag assumptions.

## Implemented Foundations

### Cape

- `je_sb_cape_politics` remains the master Cape spine.
- The political balance bar now runs on a centered `-100 -> 100` model rather than the older `0 -> 100` framing.
- The JE no longer hard-fails on a fixed calendar year.
- Responsible Government is now a real overlord-side diplomatic action backed by `subject_type_sb_responsible_colony`, rather than just a parked journal-button shell.

### Transvaal

- New scripted region helpers now exist for the former macro-`STATE_TRANSVAAL`:
  - `sb_controls_west_transvaal_core`
  - `sb_controls_central_transvaal_core`
  - `sb_controls_east_transvaal_core`
  - `sb_controls_north_transvaal_core`
- The western helper is wired, the eastern helper now follows the current Pedi shell plus the first audited Lydenburg extras and the Swazi slice for the broader Mpumalanga region, and the northern helper follows the vanilla Venda shell plus the first audited ZPB/Limpopo extras.
- Central and eastern helpers are intentionally left inert until the province audit is done.
- `TRN` Great Trek completion now keys off the western core helper instead of full macro-Transvaal control.
- `ZPB` no longer waits for `TRN` to own the entire old `STATE_TRANSVAAL` before its split event can fire.

### New Tag Shells

- `LYD` now exists as a real Lydenburg shell.
- `RHB` now exists as a decentralized Rehoboth/Baster shell.
- Neither shell should be treated as final historical implementation; both are scaffolds for later event-driven content.

### Kingdoms

- `ZUL` now actually starts with `je_sb_zulu_kingdom`.
- The Zulu JE is no longer a dead placeholder. It now bridges:
  - Natal-political resolution
  - early succession stabilization
  - firearms modernization

## Deliberately Deferred

- The audited four-way Transvaal state split itself.
- Exact province ownership for West/Central/East/North Transvaal.
- The full Lydenburg spawn chain.
- The western Baster/Rehoboth displacement chain.
- Diamonds and northern Cape consolidation implementation.
- Wider mid-century Cape crisis content beyond the current constitutional scaffold.

## Rule Of Thumb

If new Phase 2 content needs Transvaal geography before the audited split lands, target the scripted region helpers first rather than `STATE_TRANSVAAL` directly.
