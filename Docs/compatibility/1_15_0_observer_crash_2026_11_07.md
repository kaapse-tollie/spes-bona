# Victoria 3 1.15.0 — construction-tooltip crash, 7 November 2026

**CRASH115-03: failing UI path identified; cause and engine replay open.**
The 14:01 crash occurs while rendering the construction tooltip's investment-pool
modifier breakdown. It has no law activation, journal creation or country-creation
frame. It is separate from [CRASH115-01](1_15_0_crash_2026_11_07.md) and does not
test whether the [law-callback corrections](law_callback_readiness_2026_11_07.md)
prevent that earlier failure. No gameplay, GUI, localisation or save change is
justified by the evidence currently available.

## Preserved evidence and version limits

DP reports switching to observer after viewing BST, having resumed an existing
save and run several years. In follow-up, DP could not remember whether a
construction tooltip was open or the pointer was over its button during the
switch. Both remain unknown; the stack establishes tooltip rendering at the
crash, not the pointer position or tooltip state at the earlier toggle.

The exception in
`../crashes/victoria3_01261007_140131/` records **2026-11-07 14:01:31**; the folder
and YAML date have malformed year/month values. All seven crash files and five
stable monthly autosaves, **1 April–1 August 1855**, were copied unchanged to
[`generated/crash_2026_11_07_140131/`](../../generated/crash_2026_11_07_140131/).
The [evidence record](evidence/1_15_0_observer_crash_2026_11_07.json) retains
their hashes, source identities, bounded save observations and stack frames.
Native source snapshots, disassembly, the save-inspection script and the pre-task
working-tree hashes remain in that ignored directory.

The crash reports game **1.15.0**, commit
`6338547985dbc271523e149f362a6fd93dc62975`, with CMF then SB. The inspected game
remains build `26453692`, core manifest `7727600027425614094`; its ARM64 binary
SHA-256 is `a1e032aad26636414046d19ed6eb01b6f4f8e79bffabebd32b60a7b9fce46f11`.
The current installed dependency is **CMF 1.67.2 + sb-1.15.0-r2**, and its
read-only synchroniser/integrity check passes. Crash/save metadata records the
mod names, not the exact loaded CMF release. Current disk identity cannot prove
which scripts were loaded into that process or which dependency created an
earlier save. Neither the update nor the existing-save history is an established
cause.

## What failed

```text
GUI tooltip update / lock-on timer
→ Country.GetConstructionQueueDesc
→ CONSTRUCTION_QUEUE_DESC
→ ConcatIfNeitherEmpty(..., Country.GetPrivateConstructionQueueDesc)
→ CCountry::CanUseInvestmentPool(..., description)
→ AppendShortDescriptionFor
→ CDataModifierBreakdown::AppendTooltippableModifierValue
→ DATA_OBJECT_MODIFIER_BREAKDOWN_TOOLTIP
→ ModifierBreakdown.GetName
```

Native `interfaces_l_english.yml:4404–4406` and
`customized_tooltips_l_english.yml:701` supply that localisation. Native widgets
in `timemanip.gui`, `states_panel.gui` and `building_browser_panel.gui` use the
construction tooltip. SB and CMF neither shadow these files nor mention the
relevant tooltip keys, getters or `country_disable_investment_pool_bool` in their
current scripts/GUI/localisation. The two example mods, Hail Columbia and Gates
of the Bosphorus, provide no workaround for those identifiers either.

Read-only binary inspection confirms that the private-construction getter asks
for a modifier description **before** choosing the private-projects or disabled
text. The object-breakdown branch eagerly renders its nested tooltip, including
`GetName`, while building the outer tooltip. A separate hover over the nested
modifier is therefore unnecessary to reach this stack. The native construction
button already uses `Country.IsValid` for visibility; adding the same check does
not establish that the nested modifier owner is valid.

The recorded `GetName +60` frame follows its variant visitor dispatch. There is
no core/register snapshot, country ID, modifier-owner ID or widget identifier.
An invalid or stale modifier context around observer switching is a plausible
explanation, **not a proven null-pointer diagnosis or confirmed Vanilla bug**.
The native stack also cannot exclude bad mod-created state by itself. A broad
modifier-tooltip replacement or economic-law change would mask an unproven
cause and alter unrelated behaviour, so none was applied.

## Timeline and save checks

- **14:01:09:** last dated simulation message, Parma's election campaign begins
  on **15 August 1855**. This bounds the timeline; it is not an exact crash save.
- **14:01:14:** console command `observe`; response **`Ending observe mode`**.
  This differs from the reported direction, so replay must record the actual
  starting mode and exercise both directions.
- **14:01:31:** construction-tooltip crash, 17 seconds after the toggle.

In all five checkpoints, BST is live country **519**, with state **1154** and
**Traditionalism**. In August it has an investment pool of **7,612.44133** and a
government artillery-foundry project marked `valid_construction=yes`.
Its three saved timed modifiers are `sb_new_tactics`, `sb_bst_biding_time` and
native `government_slave_catchers`; the two SB modifiers affect military
research and subsistence output, respectively. None supplies the investment-pool
disable modifier. The save metadata name is **Potchefstroom**, not BST; metadata
and historical player-manager rows do not identify the country in the later
tooltip frame. BST's reported viewing context is not proof that it owns the
failing modifier.

Earlier invalid-country warnings have unknown script locations. The nearby
`agitators_law_events.txt:1037` unset `supporting_ig` errors and Ezochi HQ/port
warnings are separate leads, absent from this stack. They remain recorded in
the captured logs; no causal link or speculative correction is claimed. Low
available-memory metadata likewise does not establish this crash's cause.

## Focused DP replay

1. Fully restart the game. Use the preserved **1 August 1855** checkpoint
   ([copy](../../generated/crash_2026_11_07_140131/saves/autosave.v3)) for diagnosis;
   keep it unchanged and pause immediately. Record the actual controlled/viewed
   country and whether observer mode is already active.
2. View BST and hover its construction indicator **before any observer toggle**.
   Repeat for the controlled country's construction button. This distinguishes
   an ordinary tooltip failure from a transition-dependent one.
3. Reload the same checkpoint. Close open panels/tooltips, move the cursor onto
   empty map space, then toggle observer. Record the console's direction. After
   it settles, hover construction again. Separately test a toggle with the
   construction tooltip open. Repeat the reverse transition if safe.
4. If reproducible, retain an immediate pre-toggle manual save and the new crash
   folder. Compare the stack, not just the fact of a crash. A fresh SB/CMF
   campaign and a separate unmodified Vanilla campaign can distinguish persisted
   campaign state from a general UI defect. Do not load an SB save without its
   mods as a Vanilla control.

Closing tooltips and moving off the UI is an **untested avoidance measure**,
not a crash fix. [RT15-19](1_15_0_runtime_matrix.md) remains open until replay.
Only evidence/documentation changed in this investigation. Capture hashes,
source routing, dependency integrity and local documentation links were checked;
no game launch, native crash reproduction or runtime certification was performed.
