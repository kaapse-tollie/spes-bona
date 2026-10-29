# Martin West's British Natal appointment — 17 October 2026

Stack: SB 0.20.2, Victoria 3 1.14.5, CMF 1.66.0 + `sb-1.14.3-r1`.
Existing saves/logs inspected read-only. No game launch or save changes.

## Observed state

DP saw West installed as both ruler and Armed Forces leader, followed shortly
by a generated Landowner becoming ruler. The latest `autosave.v3` is dated
**1848-06-01** and confirms the resulting state:

| Record | Saved state |
|---|---|
| NAL `16777900` | Colonial country, `gov_crown_colony`; ruler `16782695` |
| Marinus Vermaak `16782695` | Generated Boer Landowner leader and ruler |
| Martin West `33560750` | Alive, `NAL_martin_west`, politician and AF leader; no ruler role |
| Landowners `16780475` | 36.870% clout, led by Vermaak |
| Colonial Garrison / AF `16780479` | 23.530% clout, led by West, in government |
| Colonial Administration | Activated **1848-05-15**, replacing the Boer governance law |

The four earlier monthly autosaves run from February through May 1848 and
still have Andries Pretorius ruling republican Natalia. They do not capture
the intermediate tick when West was ruler. The inspected error log contains
no Martin West or governor-installation script error.

## Mechanism and correction

`sb_apply_british_natal_colony_setup` already changes country/subject status,
activates Colonial Administration, then installs West. Reversing those steps
is not needed. The installed Vanilla government in
`common/government_types/01_colonial_administrations.txt` has:

```text
gov_crown_colony:
    transfer_of_power = presidential_elective
    on_post_government_type_change -> post_change_to_presidential_elective
```

In `common/scripted_effects/00_government_type_change_effects.txt`, that helper
calls `get_ruler_for:presidential_elective` and installs its selection unless
the country has `keep_current_ruler_var`. SB did not set that protection.
This provides a concrete replacement path consistent with the stronger
Landowner receiving the office after West's scripted appointment. The exact
callback tick is inferred, not traced in these monthly saves.

The correction sets `keep_current_ruler_var` for **seven days** before British
conversion in the existing setup helper. It remains set through West's later
appointment and expires naturally. Vanilla uses the same seven-day protection
for scripted government/ruler transitions in `on_law_enactment_pass`.
No governor polling, delayed event, permanent ruler lock, government override,
IG-strength adjustment or character replacement was added.

The variable is written to the helper's current country, NAL, including when
the caller's event root is GBR. Both conversion and direct British Natal
creation use the existing setup helper. Existing AF affiliation and once-only
installation behavior are retained.

## Verification

The new regression fails on the original setup and checks that protection is
on the current country, precedes conversion, and survives through the law and
governor changes. Existing checks retain installation once and prohibit a
monthly governor reinstall. After the correction, all **62 focused tests** pass
across Natal interwar, Natal/Zululand gameplay contracts, Klip River scope
context and the Natal/Zululand state split. Seven static checks pass: runtime
script contracts, stale symbols, unused symbols, the on-action router,
delayed-event lifecycle, release invariants and the local override inventory.
The localisation check still reports the existing reviewed-prose/size baseline
mismatch for `sb_natal_crisis.050`; neither its wording nor its approval
baseline was changed here. `git diff --check` passes. Engine retention remains
pending in runtime row `B145-24`.

DP should restart with the corrected scripts and replay from **before British
conversion** (the retained 1848-05-01 autosave is before it). Observe West after
the government refresh and beyond one week; also cover direct British Natal
creation. The 1848-06-01 save has already replaced him and is not repaired by
this prospective correction.

## Wider appointment audit — 17 October 2026

DP asked whether the same guard is needed elsewhere. The installed native
presidential, parliamentary and ordinary dictatorial post-change helpers all
check it; the special BIC dictatorial branch and the hereditary helper do not.
CMF does not replace these helpers. The local Hail Columbia and Gates of the
Bosphorus examples contain no alternative use of this guard; Vanilla's timed
protection remains the applicable example.

These are source-level exposures, not additional observed ruler replacements.
No further gameplay changes were made during that read-only audit. The table
records its pre-fix findings; DP subsequently authorized the implementation below.

| Route | Source evidence | Assessment |
|---|---|---|
| Boer government refresh | `sb_refresh_boer_commandant_general_government` sets the guard, switches to ordinary Presidential Republic and back, then removes it immediately. The custom government calls `post_change_to_dictatorial`. | Correct the existing guard's lifetime so it survives the refresh; avoid a permanent lock. This helper is used at startup and in live Boer setup. |
| Named Boer founders | NAL, TRN, ZPB, LYD and SGO apply government setup alongside Retief/Pretorius, Schoeman, Potgieter or Van Niekerk's appointment. The shared baseline's only protection is conditional on entering the refresh helper and is immediately removed. | Protect the specific founding transaction, including branches that do not enter refresh. Schoeman and the LYD fallback are AF appointees, so the native choice need not select them. Do not blanket-protect every call to the baseline: NRP has no equivalent explicit named appointment, and Natalia's later republican restoration must not accidentally retain its colonial governor. |
| Albany / Godlonton | `sb_cape.200.a` creates or regularizes ABY as a British colony, then installs Godlonton as Rural Folk leader and ruler. | Same government family as West; protect the appointment during this transaction. Already-established ABY without a government change is a distinct case. |
| German South West Africa | `sb_nam_finalize_swa_administration` establishes the colony and installs Göring, von François or Leutwein, then applies the Colonial Administration law package. | Protect the SWA country during the transition; this route also places the appointment before the final law setup. Apply only to the historical German appointment, not every generic colonial setup. |
| Klip River / Spies | `sb_klip_river_create_county` sets Presidential Republic + Oligarchy, then installs Spies. It leaves only the Landowners in government and makes him their leader. | The unguarded dictatorial callback is present, although native selection may choose Spies anyway. Lower-priority candidate for protection of the explicit appointment; no replacement has been observed. |

Excluded from an automatic guard rollout:

- **Zulu Chiefdoms and Crown restoration:** their intended governments use
  hereditary transfer. `post_change_to_hereditary` only installs its staged ruler
  for a parliamentary transition and never reads this variable. The ordinary
  monarchy → chiefdom → monarchy route does not satisfy that replacement branch.
  Any remaining Zulu appointment problem needs its own evidence.
- **Griqualand East and Rehoboth:** their traditional setup selects a hereditary
  government; this guard is not the remedy for their appointment handling.
- **Responsible government and Great Trek republican normalization:** these
  change constitutional arrangements without explicitly appointing a named
  ruler. Do not suppress their ordinary ruler selection without an agreed
  retention requirement.
- **Ordinary succession, same-government character transfers and disabled
  Highveld content:** no blanket protection is indicated.

## Authorized follow-up implementation — 17 October 2026

DP authorized guards for the Boer founders/refresh, Albany, German SWA and Klip
River, leaving Zulu and normal succession alone. The implementation adds only
native seven-day protection to the relevant existing paths:

- Boer refresh: replace the indefinite set/immediate removal with the timed
  variable. Existing refresh eligibility and its two law changes are unchanged.
- Named Boer founders: protect NAL's peaceful and Blood River founding paths
  (the guns route reuses peaceful founding), TRN, ZPB, LYD and SGO in their own
  country scopes before government setup. This also covers creation paths that
  never enter the conditional refresh helper.
- Albany: protect ABY in the shared regularization block before the British
  colony pact and Godlonton's transferred-or-created appointment.
- German SWA: protect SWA inside the existing German-only ruler installer,
  covering all three governor date branches and the following colonial law
  package. Other countries' generic SWA administration remains unguarded.
- Klip River: protect KLR in its committed setup before laws and Spies's
  appointment, even when the original event ROOT is ZUL or a diplomatic play.

No blanket guard was added to the shared Boer baseline, NRP setup, republican
normalization, responsible-government logic or Zulu transitions. No appointment,
government callback, law package, IG membership or ordinary succession rule was
changed. There is no recurring reinstall or permanent protection.

The new regression file reads the actual guard assignments and enclosing scopes,
tests foreign event roots, checks seven-day duration and absence of immediate
removal, and verifies ordering across the named routes. Negative controls cover
foreign-root/character writes and the excluded governance paths. Before the
correction it reported ten failing route cases; all seven test methods pass
afterwards. All **142 focused tests** pass across the new retention checks,
Boer founding armies, Natal interwar, Klip scope, Natal/Zululand contracts and
state split, frontier setup, Namibia, Bechuanaland, uSuthu and the Natal ultimatum.
Seven static checks pass: runtime script contracts, stale/unused symbols,
on-action routing, delayed-event lifecycle, release invariants and the local
override inventory. The existing `sb_natal_crisis.050` reviewed-localisation
baseline mismatch remains the sole failure among the eight selected checks.
Its wording and approval baseline were not changed. `git diff --check` passes.

Engine retention is pending in `B145-25`. DP should replay from before each
founding/appointment, check the intended ruler after government refresh and
after seven days, and confirm later normal succession. Existing saves whose
rulers have already been replaced are not repaired by this prospective change.
