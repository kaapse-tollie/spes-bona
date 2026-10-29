# Zulu court event prose review — 26 October 2026

Implemented for `sb_zulu_court.210`–`.215`; every namespace remains **TO REVIEW**. The change corrects the named parties and timing of bargains, rewrites the six scenes and makes independent consequences separate tooltip rows. Existing event frequencies, rewards, payments, debt access, frozen quotations and annual allegiance rules are preserved. Council bargains now require the bargaining representative's own native Prominence ≥50 at selection and execution; they carry no amaKhosi attraction bonus.

## Scenes and native references

| Event | Revised scene | Presentation and model |
|---|---|---|
| `.210` — A Pledge for the Next Reign | A household's proposed succession pledge can be accepted or redirected through a named concession. The alternative prince offers the Council; the chief gives the pledge. | Retain the backer's portrait. Japan's `shogunate.2` supplies the model of named candidates, competing support and clear choices. |
| `.211` — A Name on Every Tongue | Public praise raises one figure's reputation; recognition or a funded rebuke has personal consequences. | Retain the subject's portrait. `regency.2` separates the public account from political motives. The praise tradition is grounded in the existing oral-history cast brief; no new historical poet or office is invented. |
| `.212` — The Terms of Service | A representative offers support in exchange for guarantees of chiefly power. | Retain the bargaining actor's portrait. `austria_events.2` models a concrete demand backed by political leverage. |
| `.213` — A Place Beside the Ruler | Welcoming a rival's adherent alienates a named existing supporter. | Two portraits: arriving and departing supporters. Japan's coalition framing and native `commander_events.4`'s paired window. |
| `.214` — One Herd, Two Claims | Two households dispute a cattle reward; the disappointed party joins the rival, or the ruler funds a second reward and both stay uncommitted. | Two portraits: both claimants. Native `commander_events.4` supplies the window; the scene retains the existing award/pay-settlement trade-off. |
| `.215` — Who Will Pay for the Guns? | A chief arranges merchant contacts; chiefly financing and a direct royal purchase carry different costs. | Retain the intermediary's portrait. `portugal_single_fire_events.1` models a specific request with an intelligible financial choice. |

The actual installed scripts and complete localisation for `shogunate.2`, `austria_events.2`, `regency.2` and `portugal_single_fire_events.1` were read. The five-shot guide also supplies the contrasting broad-introduction model; it was not forced onto these small court scenes. Gates of the Bosphorus `balkfm_bosnia.001` confirms separate custom effect rows; Hail Coloumbia `usfp_usa.7` confirms a saved subject in a native portrait window. These mod examples inform implementation, not historical or artistic substitution.

All dialogue is authored flavour, not a claimed historical quotation. The existing [oral-history brief](zulu_oral_history_cast_research_2026_10_19.md) supplies context for political praise. Prose uses full names and scope-correct pronouns; existing approved localisation elsewhere is untouched.

## Council contract

For the reported example, **Dambuza pledges his household to Gqugqu; Gqugqu promises a Chiefly Council upon accession**. The household keeps its current allegiance in this succession scene. In `.212`, the incumbent enacts the Council immediately in exchange for current support. Repeal consequences remain intact. The separate privileges option still grants its existing ten-year attraction modifier; no Council choice grants it or consumes the privilege concession.

The original source allowed Council bargains below 50 Prominence. Regression tests reproduced that failure before the change. Tests cover 49.99/50, a high-Prominence prince with a low-Prominence backer, a large combined household, a fall below the threshold during the popup, the shared execution helper and a deck with no available concession. Static checks cannot establish native portrait layout or tooltip wrapping; those remain pending in the [DP matrix](zulu_court_runtime_matrix_2026_10_19.md).

## Follow-up: preventing a succession pledge

DP requested and confirmed **10 Prerogative** for stopping a chief's proposed pledge, required and spent by `.210.z`; personal allegiance stays intact and no future pledge is recorded. Accepting the proposal (`.210.a`) is now the timeout default. Refusal revalidates the price and participants, and a stale scene can close without charging. The new named cost tooltip remains TO REVIEW; native timeout/rendering checks are pending DP.

Follow-up verification: **126 focused court tests pass**, including exact payment, insufficient Prerogative, stale actors/rulers and repeated resolution. Runtime-contract and delayed-lifecycle gates pass. Localisation still reports only the three existing reviewed-text mismatches listed below. The full suite and Tiger were not rerun for this small follow-up.

## Validation

- Focused court checks: **123 passed**.
- Complete discovery: **686 tests; 677 passed, eight skipped, one failed**. The failure is the existing reviewed-localisation drift in `sb_klip_river_county.060`, `sb_klip_river_county.080` and `sb_natal_crisis.050`. This rewrite does not touch those namespaces or regenerate their approvals.
- Full validator: **15/17 gates passed, warned or skipped**. The two failed gates are unit discovery and localisation, both reporting that same existing drift. Compatibility, map/naval, runtime contracts and event lifecycle checks pass. Five existing deferred release gates remain; dependency synchronisation was skipped.
- Advisory Tiger: **1,067 errors and 146 warnings** across the existing tree, with **no diagnostic blocks touching this rewrite's added/replaced lines**. Its 1.13.5 knowledge base remains behind the installed 1.14.5 game.

Command: `python3 -B tools/validate.py --skip-cmf-sync --tiger`. Full output: `/private/tmp/sb-court-prose-2026-10-26-validation.txt`. No launch or engine validation was performed; all six scenes remain TO REVIEW.

## Natal and Swazi playtest follow-up

**Earlier timing, superseded below:** Dingane must still rule. After the Natal outcome is resolved, P <10 can open the Swazi question; Blood River victory or white peace can open it independently of P. No opening at the 1836 start. The honour/guns description flags alone do not prove that the Boer recipient has resolved the settlement. Existing monthly housekeeping retries when eligibility returns; delivery checks eligibility again, while an open popup retains its receipt and choice. Existing diplomatic-play prerequisites and war goals are unchanged.

Previously `.021` was the honour-route follow-up and unconditionally offered the Swazi question. The land-for-guns acceptance called the same opener. `.021` now describes the grant and neighbouring republic without implying a political penalty which its effects do not apply. The reported `.097` is **`sb_swazi_frontier.097`**, not a Natal namespace event.

| Event | Revised purpose and presentation |
|---|---|
| `sb_natal_crisis.020` | Retief's fulfilled cattle demand and the competing purposes of the land grant; retain the ruler/Retief paired portraits and all three existing choices. |
| `.021` | The consequences of honouring the grant, with the existing African diplomatic illustration. Background Swazi scheduling is hidden. |
| `.026` | A refused firearms bargain and a clear yield/resist ultimatum; the current ruler's portrait, modelled on the DLC's personal political decisions. |
| `.080` | Zulu victory as a political success; a portrait of the actual campaign sovereign, or the current ruler for presentation if that sovereign has died. Reward attribution retains the recorded campaign sovereign. |
| `.081` | A negotiated stand-down without an invented decisive battle; African diplomatic illustration. No victory reward is added. |
| `sb_swazi_frontier.094` | A proposed northern campaign, with description variants for the actual Natal outcome and Dingane's portrait. |
| `.097` | Swazi campaign victory and its effect on the court; campaign-sovereign portrait and the actual named reward recipients. |

Installed `shogunate.2` and `austria_events.2` were reread in full alongside the skill's five-shot and visual guides. Outcome scenes follow the native acknowledgement model rather than inventing a second reward choice. Existing African diplomatic artwork is reused deliberately; Bink2 preview was unavailable in the local decoder, so final artwork/rendering remains an engine check. All seven namespaces remain TO REVIEW. Reviewed Boer passages and their markers are unchanged.

Campaign tooltips no longer claim that Usurper was removed: the current reward script does not remove it. They show the named sovereign's permanent +40 Popularity and the actual recruited houses. List rows use the current `THIS` character rather than a scope saved only inside tooltip preview. Firearms reward wording uses the existing 10 percentage points, not an unexplained six points on the 60-point internal bar.

### Firearms, fictional heir and formation tooltip

- **Firearms:** the previous trigger required the treaty supplier to own an active arms factory. This excluded imported guns being passed on through a treaty. The replacement checks positive small-arms treaty imports in the receiving market and a matching inward treaty, capturing the current recipient rather than using a foreign event ROOT. A month without deliveries pauses that lane; accumulated progress remains. The native references are `13_goods_transfer.txt`'s `treaty_imports` checks and `00_gfx_route_graphics_values.txt`'s country → market → `mg:small_arms` scope. Market imports are aggregate, not an individual article's shipment count. The retained 1 February 1843 save has 4.8 treaty-lane months and 12 visible bar points; it does not prove a delivery time series.
- **Uthumbu:** remove startup creation. Present Dingane's Son creates the explicitly fictional character on demand, registers him, and uses the existing heir-assignment helper. P ≥50 and the 25-P cost remain; birth date 1828, normal age and the CMF heir blocker remain. Reuse an existing living identity rather than duplicate it. No save migration.
- **KwaNguni:** replace internal container/variable expansions with named requirements. A structural comparison stripping only the tooltip wrappers confirms identical underlying predicates and effects. Peace, Nationalism, the required territories and the other kingdoms' elimination remain required.

Nine new source-execution tests cover the timing boundary, pending-offer recovery, actual import months, foreign ROOT/direction/goods, creation once, age, registration and heir-blocker continuity. Native shipments, event delivery, portraits and long-name wrapping remain pending DP; see the added runtime rows.

### Follow-up verification results

- **124 focused tests pass**, including the nine new cases and Blood River's existing launch/default-option tests. The latter now follows the presentation-only `hidden_effect` wrapper; the exact launch call and popup-lifetime checks are retained.
- Final complete discovery: **698 tests — 689 passed, eight skipped, one pre-existing failure, zero errors**. The failure is reviewed-localisation drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. A direct comparison against the pre-edit snapshots confirms that this follow-up does not change those namespaces.
- Full validator: **15/17 gates passed, warned or skipped**. Unit discovery and localisation report that same baseline drift. Its earlier run also exposed the presentation-wrapper test error; the final complete discovery above resolves that error. Local override inventory, Vanilla/CMF comparison, maps/naval network, runtime contracts and delayed-event lifecycle pass. The five existing deferred release gates remain. CMF synchronisation passed in the first run and was skipped in the repeat; installed-tree verification passed in both.
- Advisory Tiger: **1,067 errors, 145 warnings**, zero diagnostics on this follow-up's substantively added/replaced lines. It still targets 1.13.5, behind installed 1.14.5. Existing `container_exists` diagnostics on the re-indented KwaNguni predicates are unsupported-API warnings from that baseline, not new predicates.
- Zulu's exact-path history pin was refreshed only after verifying its old hash against the pre-edit file. The sole history change is removal of the four-line startup Uthumbu creation. The dependency payload is unchanged. `git diff --check` still reports an existing trailing blank line in the unrelated `sb_zulu_court_events.txt`.

Outputs: `/private/tmp/sb-26oct-frontier-focused-final.txt`, `/private/tmp/sb-26oct-frontier-units-final.txt`, `/private/tmp/sb-26oct-frontier-static-final.txt`, `/private/tmp/sb-26oct-frontier-tiger-changed.txt`. Static checks are complete; no game was launched, and all new runtime scenarios remain pending DP.

## Blood River outcome options: collected firearms

DP clarified that `.080`, `.081` and `.082` must grant the guns through their option,
not on opening. The existing court consequences keep their timing, including the
−25 P defeat shock. A valid option applies the existing capped 10-percentage-point
adoption reward, then consumes its settlement receipt. The programme must still be
active at selection. A missing progress counter is guarded during tooltip preview.

All three unreviewed descriptions, flavour passages and options now make the guns
concrete: victory brings them into the royal homestead; an indecisive settlement
leaves a returning soldier asking where to take one; defeat brings a commander's
request to preserve the collected weapons for instruction. These are authored
scenes, not historical quotations. Collection along the frontier fits both fought
and diplomatic outcomes without asserting that backdown involved battlefield loot.

Installed `regency.2` supplied the public-result/private-scene model; `regency.3`
supplied the single acknowledgement with an effect-bearing option. The existing
`.080`/`.082` sovereign portraits and `.081` diplomatic scene still suit the primary
political outcome. No new art or GUI is introduced. The exact `.080`/`.081`/`.082`
namespaces remain TO REVIEW; reviewed neighbouring events are untouched.

Validation: **57 focused tests pass**. Runtime contracts, delayed delivery,
stale/unused symbols and changed-file whitespace checks pass; localisation reports
the same existing reviewed-text drift in `.050` and Klip River `.060`/`.080`.
Opening/hovering versus executing the button is now covered explicitly. Native
delivery, rendering and timeout behaviour remain pending DP in scenarios 71–73.

26 October follow-up: DP lowered the resolved-Natal low-Prerogative branch from P < +10 to **P ≤ −10**. Blood River victory and white peace remain independent of P. The existing Dingane, settlement and delivery checks remain. No Swazi event prose changed.
