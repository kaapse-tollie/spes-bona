# Blood River: opposing targets and Natal control objectives

## Report and evidence

DP's 2026-09-05 23:00 screenshot shows Oranje demanding humiliation from itself. The 22:59 autosave (1839.12.1) confirms this is stored goal data, rather than a localisation-only problem:

- Play `67108865`: `dp_sb_natal_crisis`, initiator `481` (ZUL), target `474` (ORA).
- Goal `50331651`: Story Humiliation, holder `481`, target `474`, target state `783` (Vrystaat).
- Goal `67108874`: Story Humiliation, holder `474`, target `474`, target state `783`.
- State `780` is the ZUL-owned partition of `STATE_NATAL` in this save.

`sb_natal_story_attempt_exact_launch` added the ORA counter-demand inside `create_diplomatic_play` with `target_country = root`. The resulting nested payload did not retain the launcher's ZUL identity. Its recorded target is ORA.

## Change

The launcher now leaves goal installation to the existing exact-play on-start handler. That handler installs both primary demands using its admitted `scope:initiator` and `scope:target`, then removes the temporary Story Humiliation creation goal:

| Holder | Opponent | Demand | Control condition |
|---|---|---|---|
| ZUL | ORA | Defend Natal | Maintain control of ZUL's Natal state |
| ORA | ZUL | Secure Natal | Occupy that same Natal state |

The state is selected after the existing NGI absorption step, so the objective follows the resulting ZUL partition. Launch preflight requires ZUL to hold a state in Natal. The separate Cape-held partition is not an objective.

Both goals use `kind = custom`, zero infamy, and the existing peace-outcome recorder. They neither annex territory nor apply the engine's humiliation effects. They retain `assent_required`: occupation determines control, while peace/capitulation and the existing terminal resolver decide the story outcome. Natalia's creation stays with that settlement. Other story routes retain their existing goals.

Vanilla's Revoke Claim supplies the `control_own_state` pattern; Conquer State supplies `control_target_state`. Vanilla's `war_goal_types.md` documents `kind = custom` as having no predefined effect. Gates of the Bosphorus's Halt Expulsions and Hail Columbia's Mexican Cession also use custom goals with scripted enforcement.

The play icon and non-event/JE description now describe the Natal dispute rather than reciprocal humiliation. Changed/new prose is listed by exact key in `Docs/localisation_review_queue.md`.

## Validation

- Added regression checks that failed against the original nested counter-demand and absent control goals, then passed after the fix.
- All 32 story-war route tests pass, including the existing terminal outcome and delayed-delivery tests.
- Full suite: 400 of 401 tests passed. The existing Great Trek `.002` review classification failure remains (`# ### (DP) REVIEWED ###` is not recognised by the validator); DP's marker was preserved.
- Runtime script contracts, release invariants (84 war-goal definitions), router, stale/unused symbols, override inventory/comparison, map/connectivity, and delayed-event checks pass.
- Localisation rechecked after correcting the new plain review group's boundaries: only the existing Great Trek review classification failure remains.
- `git diff --check` passes.
- Engine loading, the new occupation-control display, and terminal peace outcomes still require in-game verification.

## Continuing the reported save

New launch code does not replace goals already stored in a running war. A separate repaired copy was therefore created at:

`/Users/depro/Documents/Paradox Interactive/Victoria 3/save games/SB Blood River repaired - 1839.12.01.v3`

Only the two reported war-goal records were changed: goal types, their Natal state, and ORA's opposing country/stakeholder. IDs, participants, war progress, and the rest of the save remain byte-identical; reversing those two replacements reproduces the original file exactly. The original autosave was not modified.

- Original SHA-256: `59c7aa3e7e3e856caa5a0a09ce78cbfb318c802bc6403879a066810adc361ebb`
- Repaired SHA-256: `f71224c06efa6a98bdeec140f10104947fff491772b01386d2a52f37fba2693c`

Restart Victoria 3 to load the new goal definitions, then load the repaired save. Verify opposing countries and Natal control in the peace panel. An ORA-only accepted demand must still deliver the Natalia settlement; a ZUL-only demand must deliver the Zulu outcome; white peace or both demands must retain the existing neutral outcome. For launcher verification, also test a save from before the play starts.
