# Unused Symbol Report

`tools/validate.py` counts every `sb_*` token across active script and localisation, then compares definition-only top-level keys with `tools/unused_symbol_allowlist.json`.

The reviewed definition-only surface contains three engine entry points:

| Symbol | Classification | Why it has no textual caller |
|---|---|---|
| `sb_ai_economy_helpers` | Engine entry point | Victoria 3 discovers the top-level game-rule key. |
| `sb_frontier_ai_behavior` | Engine entry point | Victoria 3 discovers the top-level game-rule key. |
| `sb_bechuanaland_influence_bar_visible_sgui` | Engine entry point | CMF invokes the scripted GUI through its journal interface data context. |

There are no allowlisted save, migration, or staged public APIs. A newly definition-only key fails validation until it is removed or explicitly classified with a source path and rationale.
