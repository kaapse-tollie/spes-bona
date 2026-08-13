# Victoria 3 1.13.10 Runtime Matrix

Static implementation targets Victoria 3 `1.13.10` (build `24689003`) and CMF `1.62.0` (`e06645b`). The cases below require a real game process and are not certified by repository tests.

Canonical GitHub release path: `/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework`. `tools/validate.py` updates this directory from GitHub's latest stable release before checking SB's pinned compatibility baseline. A newer minor release is installed but leaves validation red until the corresponding rebase is complete.

Record save type, active mods/load order, observed result, and relevant log lines for every run.

| ID | Scenario | Acceptance condition | Status |
|---|---|---|---|
| `RV-01` | Cold launch a fresh 1836 game with CMF 1.62.0 and SB, then save and reload. | No new parser, missing-scope, stale-JE, or duplicate Situation-widget errors. | Engine pending |
| `RV-02` | Open Bechuanaland, inspect `com_container`, save/reload, replace an actor, then resolve or invalidate the story. | Exactly one `sb_bechuanaland_corridor_state` exists while active; scopes, lists, score, drift, JE handles, and title boxes survive reload; no container remains after terminal cleanup. | Engine pending |
| `RV-03` | Exercise every Warren/Caprivi direct and proxy route, support/neutrality choice, backdown, white peace, and mixed enforcement. | Intended participants and each scripted goal appear once; no self-transfer, invalid transfer, stranded pending phase, or duplicate settlement occurs. | Engine pending |
| `RV-04` | Establish, disband, and re-establish the Mozambique Company and a generic-prestige-good company. | Vanilla HQ/assets remain valid, SB MZQ cleanup runs once, and Vanilla restores the eligible prestige-good JE once. | Engine pending |
| `RV-05` | Inherit a hosted treaty port through revolution and conquest; test honor and revoke. | One inheritance prompt appears, the agreement follows the chosen outcome, and the treaty port reconnects to the correct market without SB duplication. | Engine pending |
| `RV-06` | Test Cultural Supremacy with owned and unowned primary-culture homelands and neighbouring insurrectionary movements. | Radicalism follows all three Vanilla 1.13.10 scope fixes while CAP exclusions remain intact. | Engine pending |
| `RV-07` | Open Stake Colonial Claim with and without sufficient interest. | The action is unavailable without the required interest and never opens an empty target picker. | Engine pending |
| `RV-08` | Inspect country selection/history for XHO, CAP, and the retired XHG/XHR/XHT tags. | Retired tags are absent, XHO remains valid, and John Philip is created only through CAP's authoritative template. | Engine pending |
| `RV-09` | Use SB-modified starting fleets for recruitment, embarkation, invasion, cancellation, rerouting, transfer, retrofit, and repair. | 1.13.10 transport and Supply Ship rules work; no uncrewed mission, destroyed reroute, stuck repair, or 99% invasion occurs. | Engine pending |
| `RV-10` | Run Tiger and review fresh `error.log`, `debug.log`, and `game.log`. | No new SB-authored errors remain; any external or known false positive is recorded with exact evidence. | Engine pending |
| `RV-11` | Take the Pink Map decision before BC, while BC is active, and after invalid, British, Boer, exact-zero, and SWA outcomes. | The decision is disabled only while BC is active; pre-BC and invalid routes grant all three claims, Boer/zero grants Kazembe and Zambia, and British/SWA routes reach the recorded arbiter. Later BC rewards never duplicate a pre-BC basin package. | Engine pending |
| `RV-12` | Resolve British and SWA Pink Map arbitration through outright acceptance, favour, rejection/backdown, and defiance, including a held event whose arbiter disappears. | Dynamic names and tooltips render; acceptance transfers the intended claim package, the favour transaction targets the saved arbiter, defiance preserves competing claims with `-50` relations and temporary `+25` aggression, and a missing arbiter falls back cleanly. | Engine pending |
| `RV-13` | Let MZQ colonize a basin target, then form IBE from POR before and during the Pink Map lifecycle; save and reload both states. | Subject colonization enables the decision, claims remain on POR/IBE rather than MZQ, tag formation preserves pending state and claims, and no stale arbiter or hostility marker survives JE closure. | Engine pending |

Static validation already confirms the pinned source hashes, the Vanilla treaty-port and company-disband hooks, direct use of CMF's journal/title/container APIs, complete structure for all scripted war-goal blocks, one SB company-disband handler, and no SB treaty-port inheritance override.
