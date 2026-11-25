# Unused Symbol Report

`tools/validate.py` counts every `sb_*` token across active script and localisation, then compares definition-only top-level keys with `tools/unused_symbol_allowlist.json`.

The earlier review recorded three engine entry points.

| Symbol | Classification | Why it has no textual caller |
|---|---|---|
| `sb_ai_economy_helpers` | Engine entry point | Victoria 3 discovers the top-level game-rule key. |
| `sb_frontier_ai_behavior` | Engine entry point | Victoria 3 discovers the top-level game-rule key. |
| `sb_bechuanaland_influence_bar_visible_sgui` | Engine entry point | CMF invokes the scripted GUI through its journal interface data context. |

Victoria 3 also looks up six modifiers for the temporary BST raid culture by name. The positive and negative pairs cover standard of living, cultural acceptance and fervor. [Generated modifiers](../../common/static_modifiers/sb_culture_generated_modifiers.txt) · [Exact allowlist](../../tools/unused_symbol_allowlist.json)

There are no allowlisted save, migration, or staged public APIs. A newly definition-only key fails validation until it is removed or explicitly classified with a source path and rationale.
