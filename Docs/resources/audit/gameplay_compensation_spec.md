# Gameplay Compensation Spec

This note records the non-cap implementation direction for SB states whose remaining identity should not be solved by higher resource caps.

## West Transvaal

- Chosen layer: `state_modifier`
- Keep out of caps: `yes`
- Hook family:
  - [`/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/static_modifiers/sb_modifiers.txt`](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/common/static_modifiers/sb_modifiers.txt)
  - [`/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/on_actions/sb_on_actions.txt`](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/common/on_actions/sb_on_actions.txt)
- Implementation direction:
  - Add a future West-plateau industrial modifier in `sb_modifiers.txt`.
  - Apply it from the Transvaal ownership/on-action flow once the west-plateau industrial core is consolidated.
  - The compensation should express infrastructure access and industrial linkage, not broader natural-resource volume.

## Drakensberg

- Chosen layer: `journal_flavour`
- Keep out of caps: `yes`
- Hook family:
  - [`/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/journal_entries/1-07_sb_bst_frontier.txt`](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/common/journal_entries/1-07_sb_bst_frontier.txt)
  - [`/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/on_actions/sb_bst_on_actions.txt`](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/common/on_actions/sb_bst_on_actions.txt)
- Implementation direction:
  - Keep Drakensberg capped as a constrained mountain state.
  - Express its wool, mohair, and mountain-pastoral niche through `je_sb_settle_drakensberg` or the wider BST frontier journal flow.
  - Any gameplay reward should be tied to frontier settlement flavour, not extra raw resource caps.

## Botswana

- Chosen layer: `state_modifier`
- Keep out of caps: `yes`
- Hook family:
  - [`/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/static_modifiers/sb_modifiers.txt`](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/common/static_modifiers/sb_modifiers.txt)
  - [`/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/common/on_actions/sb_bst_on_actions.txt`](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/common/on_actions/sb_bst_on_actions.txt)
- Implementation direction:
  - Add a future ranching-quality modifier in `sb_modifiers.txt`.
  - Apply it through BST/Tswana ownership logic or equivalent Botswana-focused content, not through higher caps.
  - The compensation should express cattle-first quality and specialization rather than broad land-capacity inflation.
