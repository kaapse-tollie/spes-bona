# Natalia victory-event delivery repair

## Confirmed runtime failure

DP reports that winning Blood River does not deliver the Natalia creation event. The relevant run is preserved in `save games/autosave_exit.v3` (1839.8.7.6). The newer rolling autosaves belong to a separate 1836–1837 game and contain no Natal story state.

`logs/error.2.log`, 17:38:02, records:

```text
Left side and right side during comparison were of different types
(left was 'diplomatic_play', right was 'country')
Script location: events/sb_natal_crisis_events.txt:745
common/on_actions/sb_diplomatic_play_on_action_handlers.txt:784
common/scripted_effects/sb_story_war_effects.txt:880
common/scripted_effects/sb_story_war_effects.txt:498
```

This is the `.070` Oranje-victory delivery path. Subsequent orphan-pulse errors attempt `is_country_alive` on the same diplomatic-play object.

The terminal resolver correctly enters the winning country's scope. However, each terminal receipt builder then uses `ROOT = { save_scope_as = sb_natal_terminal_recipient }`. ROOT remains the closing diplomatic play. That overwrites the previously correct country identity. The receipt also uses `parent = root`, attaching it to the closing play instead of the surviving country. The event's country-root validation rejects the stored play identity.

The shared delivery-authority trigger has a related problem: it compares the saved recipient with ROOT, even when called from a play-root callback or the other participant's watchdog. Fixing only the saved recipient would therefore leave another delivery failure.

## Repair

- Capture the builder's current country directly with `save_scope_as`.
- Parent the receipt to the explicitly saved recipient country.
- Inside the receipt scope, compare its recipient with PREV, the country whose authority is being checked.
- Apply the correction to all three builders: Oranje victory, Zulu victory, and neutral outcome. They share the same defective scope pattern.
- Preserve event prose, victory selection, guns-bargain versus Blood River formation variants, delay, popup hold, consumption guards, and the state-control war goals.

## Verification

The new regression check failed against all three old builders and the root-dependent authority check, then passed after the repair. All 33 story-war route tests pass. Runtime script contracts, delayed-event lifecycle checks, release invariants, and `git diff --check` pass. These are static/regression checks, not a completed in-game replay.

Evidence and pre-edit files are backed up under `/private/tmp/sb-natalia-delivery-2026-09-06/`, including the failed exit save and archived logs.

## Continuing the failed run

Restart Victoria 3 so the updated scripts load. A save from before the peace settlement should now deliver `.070` through the normal chain after three days. Check the popup, both player options, resulting Natalia territory, and the guns-bargain leadership variant.

The verified failed exit save already has `sb_natal_story_war_resolved_global_var` but no surviving terminal receipt. It cannot reconstruct its victory automatically from the remaining save flags: the same resolved marker also covers neutral/Zulu outcomes. A generic automatic grant would therefore be unsafe for other games.

For this specific exit save, the archived `.070` stack establishes an Oranje victory, and the remaining saved guns-bargain watchdog scopes establish that branch. Load that save and run the following once in the debug console, then advance three days. It recreates the pending victory event, rather than directly creating Natalia. This manual recovery command has not been executed in the game during this repair.

```text
effect if = { limit = { has_global_variable = sb_natal_story_war_resolved_global_var NOT = { exists = c:NAL } NOT = { container_exists = sb_natal_terminal_outcome_state } c:ORA ?= { is_country_alive = yes NOT = { has_war_with = c:ZUL } } c:ZUL ?= { is_country_alive = yes } } c:ZUL = { save_scope_as = sb_natal_terminal_counterparty } c:ORA = { sb_natal_story_begin_terminal_ora_victory = yes } container:sb_natal_terminal_outcome_state ?= { set_variable = sb_natal_terminal_guns_bargain_result_var } }
```

Do not use this victory-specific recovery for an unrelated save, white peace, or Zulu victory. The saved copy of the failed run is `/private/tmp/sb-natalia-delivery-2026-09-06/autosave_exit.v3` if the game's rotating exit save is replaced.

## Separate held design

The two-stage ORA–BST conquest proposal is ON HOLD at DP's request, pending Paradox's response/balance change in the next open-beta patch. No staged-war gameplay changes were implemented.
