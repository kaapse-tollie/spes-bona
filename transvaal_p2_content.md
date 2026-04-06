# Plan: ZPB Recognition Crisis and LYD Reunion Arc

## Summary

Keep the current split structure intact:
- `ZPB` remains a **Cape-politics-driven spawn**
- `LYD` remains a **TRN internal secession** caused by the centralizing branch of `A Republic Established`

Then layer the new mid-century content on top:
- `TRN` and `ORA` each get a **recognition convention** event after Great Trek completion
- `TRN` gets a later **ZPB lawlessness / civil-war** branch if `ZPB` exists after recognition
- `TRN` gets a **peaceful-only LYD reunion JE** once `LYD` exists

This keeps the current scaffolding and adds the stronger gameplay consequences you want.

## Key Changes

### 1. Recognition conventions for TRN and ORA

Add a parallel convention chain after Great Trek completion:
- `TRN`: `Convention of Sand River`
- `ORA`: `Convention of Bloemfontein`

Trigger shape:
- Great Trek JE completed
- independent
- not at war
- has not already resolved its convention
- no hard phase date gate

Options for both republics:
- `Accept the Convention`
  - `set_country_type = recognized`
  - renew/create `10`-year `GBR` truce
  - renew/create `10`-year transit-rights treaty with `GBR`
  - enact `law_slavery_banned`
  - set a convention-resolved country flag/var used by follow-on content
- `Refuse`
  - remain unrecognized
  - keep current slavery law
  - queue a delayed British response event
  - British response starts a real vanilla `dp_ban_slavery`

For `ORA`, this is the whole recognition lane for now.
For `TRN`, this also unlocks the later ZPB crisis content.

### 2. ZPB stays Cape-spawned, then becomes a recognition problem

Do not replace the current Cape-linked `ZPB` spawn.
Keep:
- the Cape liberalization trigger
- `sb_trek.110` / `sb_trek.120`
- play-as option for `ZPB`

Add a later `TRN` branch only if all are true:
- `ZPB` exists
- `TRN` accepted Sand River recognition
- `TRN` is still recognized
- `ZPB` is independent and still practices slavery

Then fire `Lawlessness in Northern Transvaal`.

Options:
- `Bring order to Zoutpansberg`
  - give `TRN` a claim on `STATE_NORTHERN_TRANSVAAL`
  - start a timed JE to eliminate `ZPB` by direct conquest
  - success: preserve recognition, improve `GBR` relations modestly
  - failure: `GBR` fires the follow-up slavery event, `TRN` loses recognition, and `GBR` may open `dp_ban_slavery` against `ZPB`
- `Zoutpansberg keeps the true frontier spirit`
  - improve `TRN`-`ZPB` relations
  - add defensive pact
  - re-enact `law_legacy_slavery` in `TRN`
  - queue delayed British response
  - British response removes `TRN` recognition and starts `dp_ban_slavery`

This is the Transvaal civil-war layer: not a random fracture, but a recognition crisis caused by whether `TRN` disciplines or embraces `ZPB`.

### 3. Republican direction choice remains shared, but LYD stays TRN-only

Keep `A Republic Established` for both `TRN` and `ORA`.

Both tags still choose between:
- a more centralizing, presidential republic
- a more frontier-dominated agrarian republic

Use your current gameplay logic:
- centralizing route enacts `law_presidential_republic` and `law_interventionism`
- frontier route keeps the commandant-general / agrarian direction

Only `TRN` centralization continues into `LYD`.
`ORA` gets the same identity choice, but no eastern secession content.

### 4. LYD secession and peaceful reunion

Keep the current `LYD` spawn structure:
- `TRN` centralization sets the delayed eastern secession
- `LYD` spawns through the existing split event
- `LYD` remains a Boer republic with the hidden Boer setup stack

Add a new `TRN` JE: `Transvaal Unity`.

It appears when:
- `LYD` exists
- `TRN` exists
- `LYD` is independent
- `TRN` has not already reunified with `LYD`

Completion condition:
Maintain all of the following for `5` cumulative years:
- legitimacy is `legitimate` or `righteous`
- `Intelligentsia`, `Petty Bourgeoisie`, `Industrialists`, and `Trade Unions` are all out of government
- law is `law_national_supremacy` or `law_ethnostate`
- law is `law_national_militia`
- `amendment_sb_commando_corps` is active
- relations with `LYD` are `amicable` or better
- `TRN` GDP is at least `1.5x` `LYD` GDP

On success:
- `LYD` peacefully joins `TRN`
- `STATE_EAST_TRANSVAAL` transfers to `TRN`
- `LYD` is removed
- `TRN` incorporates the east
- core Boer characters/IG setup from `LYD` are merged into `TRN`

No coercive `LYD` reunion lane in this first implementation pass.

## Interfaces / New Content

Add:
- two convention events: `Sand River` and `Bloemfontein`
- one British response chain using real vanilla `dp_ban_slavery`
- one timed TRN JE for the ZPB crackdown path
- one persistent TRN JE for peaceful LYD reunion
- a small set of flags/vars for:
  - convention accepted
  - convention refused
  - ZPB crisis resolved
  - LYD union completed

Keep existing content as-is where possible:
- current Cape-linked `ZPB` spawn
- current `LYD` secession setup
- current `A Republic Established` fork, extended rather than replaced

## Test Plan

- `TRN` Great Trek completion triggers Sand River convention at peace.
- `ORA` Great Trek completion triggers Bloemfontein convention at peace.
- Accepting a convention:
  - grants recognition
  - grants/renews `10`-year `GBR` truce
  - grants/renews `10`-year transit rights
  - enacts `law_slavery_banned`
- Refusing a convention:
  - does not grant recognition
  - later produces British `dp_ban_slavery`
- `ZPB` still spawns from Cape politics while Great Trek is active.
- If `ZPB` exists after recognized `TRN`:
  - `Lawlessness in Northern Transvaal` fires
  - crackdown route creates the timed anti-`ZPB` JE
  - failure removes recognition and triggers British pressure
  - pro-`ZPB` route reintroduces slavery and triggers British pressure
- `LYD` still spawns only from the TRN centralizing route.
- `Transvaal Unity` tracks the 5-year cumulative conservative-stability conditions correctly.
- On JE success, `LYD` peacefully merges into `TRN` and east Transvaal transfers cleanly.

## Assumptions and Defaults

- `LBY` in your draft is treated as `LYD`.
- `ZPB` remains Cape-spawned; the new content is layered on top, not a rewrite.
- British anti-slavery enforcement uses the real vanilla `dp_ban_slavery`.
- `law_legacy_slavery` is the slavery law restored when `TRN` sides with `ZPB`.
- `ORA` gets the same republic-direction choice and its own recognition convention, but no `LYD`-style splinter branch.
- `LYD` reunion is peaceful-only in this first pass.
