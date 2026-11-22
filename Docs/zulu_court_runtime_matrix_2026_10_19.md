# DP verification: Zulu court rework

**Current, 30 October:** succession disputes require **30% of succession-pledged Prominence**; living-ruler challenges retain **25% of current pledged Prominence and P ≤−50**. New JE dropdowns and the fixed −50 marker need the rendering checks in **149–150**. Earlier source/DP evidence remains historical; it does not mark these changes as engine-verified.

**Current, 28 October:** DP has approved live claimant-war activation after a successful AI replay. The older manual-only release hold below is superseded. Next priority: **121 — Mpande’s retirement / Cetshwayo–Mbuyazi**, capturing staffing evidence under **118**, then **122 — Thirteen Chiefdoms**. Newborn and dated-descendant checks are **119–120**.

19 October 2026; updated 27 October for harvest execution and campaign outcomes, following the 25 October update for the locked character packages, annual model B, independent incidents and pledge pricing, and the independent revocation/purge actions. **DP reported scenarios 1, 2, 4, 5, 6, 7 and 12 passed on 26 October 2026. Other scenarios remain pending.** Scenario numbers appear beside their titles; retain these numbers when adding later checks. Use a fresh campaign or checkpoints made before the relevant setup with this source. No save migration. Codex has not launched Victoria 3.

| Scenario | Check | Status |
|---|---|---|
| 1. Current Allegiances / Next Succession | The king and loyal supporters appear in current pledged backing. A chief backing the king today and a prince's future accession appears once in each appropriate view. Current shares sum to 100% of present pledges; future shares sum to 100% of succession pledges. Neither view changes commitments on opening. | **Passed — DP, 26 October** |
| 2. Uncommitted backing trial | H uses current pledged + 0.25 × personally uncommitted prominence. A future pledge alone does not remove the discount. Popularity still contributes Q/2; movement balance and drift caps are unchanged. Check all-neutral and opposition-dominant cases as well as loyalist dominance. | **Passed — DP, 26 October** |
| 3. Split courts and CAP exile | Exiles retain their home backing. During a constitutional split, a rival patron in the other court is shown as external opposition without contaminating that court's totals. Repeated pulses must not duplicate supporters or weights. | Pending DP |
| 4. Opening balance | Compare princes' own prominence, trait contributions and actual supporters. The retained pre-change 1 February checkpoint has Mpande 25, Gqugqu 50, and no extra future pledgers. That older checkpoint predates the newly implemented trait packages. Verify the thirteen new packages without random extra opening traits; authored initial allegiances are preserved. Dingane starts at −50 Popularity including Usurper, then reaches 0 after one campaign victory and +40 after both if no other effects intervene. | **Passed — DP, 26 October** |
| 5. Fresh ZUL; inspect domestic and foreign courts | Recognisable expand/collapse arrow opens a bounded, scrollable court section without widening or displacing the JE horizontally; correct incumbent/heir, each following once, all available princes, named current/future commitments, commanders separate, actual effects/drift. No null scopes, blank names or duplicate cast. | **Passed — DP, 26 October** |
| 6. Fresh ZUL; princes and totals | No starting heir is designated, including Mpande; he remains a living politician. The adult self-claimant's **Claimant card** shows and grants **+25 Prominence**, counted once in native Prominence and their coalition. No separate Royal Claim modifier remains. Total = pledged + unpledged; displayed prince shares divide pledged prominence and sum to 100% when non-zero. The major-challenger threshold now uses 30% of succession-pledged Prominence (30 October); unpledged prominence does not dilute that share. No claimant bonus or adult house weight for a child, and no bonus merely for supporting a claimant. | **Original passed — DP, 26 October; +25 card and pledged-threshold retests pending** |
| 7. House leaders, members and generated cast | Great Houses shows each named non-princely house once, its leader and members, and the sum of their native prominence. All adult non-leaders, including unaffiliated councillors, have exactly one −10 modifier. Procedural court adults register neutral/unpledged and appear in Other Councillors. No surname-based invented houses or repeated princes. Dead/retired members cease contributing. | **Passed — DP, 26 October** |
| 8. Change a house leader | Raise a junior's prominence above the head before SB's −10 penalty, or remove the head. The new leader loses the penalty; the former head receives it if still eligible. Repeated pulses do not oscillate. The new head retains their own commitments. An already open cash quote for a displaced head cannot charge. Native agitator contributions are excluded from additional scripted attraction, even for a junior in a combined house. | Pending DP |
| 9. Court names and roles | Repeatedly select princes, heads, members and unaffiliated councillors: native character panel opens without first destroying the court's GUI context. Rows show current IG leadership/command/other office, not provenance boilerplate. The JE no longer highlights Traditionalists; the movement remains functional. Record whether the native interest-group FindChild error recurs, without assuming that it caused the earlier click failures. | Pending DP |
| 10. Hover Recognise a Successor | Repeated hovers before and after opening the court produce no missing-counter errors. Click at sufficient P: each eligible named candidate appears once. | Pending DP |
| 11. Vacant heir slot | After the current heir dies, submits or flees, no generated replacement persists while named dynasts remain. Recognise a living prince and appoint a minor under regency: neither is killed by the blocker. Institutional exit and exhausted authored lines release the court-owned block; any independently owned block remains intact. | Pending DP |
| 12. Secure a Pledge | q 10/25/50/75/100 costs 40/62.5/100/130/160% of reserve capacity. A valid pledge can draw on debt when reserves are insufficient. Its tooltip shows reserves versus cost. Change prominence or reserve capacity after opening: the displayed payment stays fixed and no replacement popup opens; a displaced or otherwise invalidated participant still cannot be purchased. Payment changes current endorsement only, once; the purchased allegiance then follows ordinary annual persistence. Native Patronise/Ostracise/Grant Peerage remain available. | **Passed — DP, 26 October** |
| 13. Ordinary politics | January, first in 1837: model B may recruit, retain, withdraw or switch each eligible house representative’s present/future commitment separately. Umkhosi reports the actual named changes once; an unchanged year produces no popup and still consumes its annual roll. Movement alignment remains separate. The sovereign cannot abandon himself; princes keep their own future claims; minors stay under regency handling. No second roll on reopening or reload. | Pending DP |
| 14. Dingane, low P | Existing native-style coup can replace Dingane with the supported prince. Confirm remaining relatives and following identities survive; no Thirteen Chiefs reward. | Pending DP |
| 15. Dingane dies, Mpande/Gqugqu each backed | Capture both factions and pledges before native references change. This is a **prototype-only war test**, not a verified production succession. Test both player sides and a third surviving claimant. | Pending DP |
| 16. Dingane, P ≥50, Uthumbu | Absent at new-game start. Create as a newborn and recognise once for 50 P; reuse an already-existing identity without resetting its age. No free adult following. Secure a pledged adult; minority succession selects the most prominent willing adult as regent. Kill the regent: replace without deleting the child. Age 18: actual sovereign succeeds. | Pending DP |
| 17. Mpande retirement, secured | First eligible monthly pulse on/after 1 August 1856 opens one choice explicitly presenting Mpande's retirement. Check the accession/retirement tooltip and let it remain open across several pulses. Acknowledgement retires the living Mpande, installs the actual candidate, converts only relevant pledges and honours a council promise. Earlier natural death uses the same route. | Pending DP |
| 18. Mpande retirement, contested | With an eligible rival holding ≥30% of succession-pledged Prominence, the retirement episode offers the competing faction. Unpledged backing does not dilute this share. No manual opt-in is required. | Pending DP |
| 19. Renunciation costs and odds | P 24 blocks; P 25 permits and spends exactly 25. Commit 100 Authority for ten years on either result. With K=196 and each prince at 55 Prominence after the +25 card, the source fixture gives 78.1% renunciation / 21.9% refusal; compare live K/R if native prominence differs. Refusal leaves the claimant at court with +10 Prominence for ten years, without a ruler Popularity penalty. | Pending DP |
| 20. Renunciation succeeds | The prince loses the Claimant card and its +25 Prominence, not the house or other family members. Current backers become uncommitted; future promises to him end. A current king-loyalist with only a future promise retains personal allegiance. Other promises and constitutional preferences survive. | Pending DP |
| 21. Purge costs and weak-rival outcome | P 49 blocks; P 50 permits and spends exactly 50. Commit 200 Authority for ten years on either result. Opening prediction: 66.2% killed / 33.8% flight. Flight preserves the same prince, claim and surviving backing. Killing affects only the selected prince. Check notifications, correct family survival and heir blocker. | Pending DP |
| 22. Separate allowances and fresh quotes | Refused renunciation does not consume purge; a failed purge does not start renunciation’s cooldown. A returned rival can face renunciation after ten years. The same ruler cannot purge that rival twice; a different ruler can, and returning the first ruler does not reset their use. Dead/foreign targets, ruler change and repeat clicks charge nothing. Changed K/R or failure threshold requires a new confirmation. | Pending DP |
| 23. Overlapping Authority commitments | Attempt renunciation and purge at different dates: total cost reaches 300 Authority and releases 100 then 200 on their respective ten-year anniversaries. Negative available Authority does not block. The aggregate modifier is indefinite while receipts remain. Target death, ruler replacement and institutional exit neither refund early nor prevent expiry. | Pending DP |
| 24. Strong-rival purge: prototype only | At exactly 25% of all **current pledged** prominence a failed purge takes the war branch. Renunciation remains available outside test mode; purge does not. In the explicit prototype, verify actual split and both sides. A king’s loyalist with only a future pledge to the rival must not join the revolt. War delivery, force allocation and playable side selection remain pending; no foreign-war substitute or scripted winner. | Pending DP |
| 25. Chiefly bargains | Privileges: +20% amaKhosi attraction for ten years, once/reign and non-stacking. Council: the bargaining representative requires at least 50 personal Prominence. The law is enacted for present support, or promised for the named prince’s accession, with no amaKhosi attraction bonus. Voluntary departure ends only that matching unfulfilled promise. Repeal releases current backers once, with one −10 ruler Popularity penalty; unrelated pledges survive. No constitutional victory from Monarchy + Council. | Pending DP |
| 26. Independent cast episodes | Six portrait scenes (.210–.215), drawn without replacement with an inclusive 6–24-month delay after resolution. First scene also waits. Reload and reopen retain the card/time; no incident is bundled with Umkhosi. Expiry selects the default and releases the reservation once. Refill when no eligible unused card remains; avoid an immediate repeat when alternatives exist. | Pending DP |
| 27. Reserved card loses eligibility | Remove/kill the relevant people or finish firearms during the wait. At the original due date, use another eligible unused scene or wait; do not manufacture a person or restart the delay. Institutional exit/re-entry retains the pending deck state. | Pending DP |
| 28. Incident choices and prices | Award trade-off: one neutral house supports the king and another the named rival; 30% reserve-capacity payment leaves both neutral. Reputation: +10 Popularity/+10 Prominence for five years, or 20% capacity to discredit (−10 Prominence, ruler −5 Popularity; incumbent supporter withdraws). Guns: up to 6 progress for +20% amaKhosi attraction/five years, or 40% capacity without that concession, once only. Change-of-patron welcomes one house at the cost of an existing ally. Inspect named house weights and portraits. | Pending DP |
| 29. Frozen incident quote | Change reserve capacity with a paid scene open: the original quoted cost remains available and is debited directly, including from insufficient or negative reserves. No replacement confirmation or substituted people. A dead target, changed ruler or already-resolved choice cannot charge. | Pending DP |
| 30. Concession disappearance | A chiefly movement that disappears and returns naturally receives only the original remaining concession duration. No recreated movement, refreshed enthusiasm or stacking. | Pending DP |
| 31. Blood River / Swazi outcomes | Each outright victory gives the actual result sovereign permanent +40 Popularity and removes Usurper if present; up to two neutral houses support the incumbent. Each defeat gives permanent −20 Popularity and up to two neutral houses to the strongest eligible rival. Blood River defeat costs 25 P; Swazi defeat remains 10 P. Existing supporters are not overwritten. Hold popups through a ruler change: no later credit or second award. Swazi stalemate remains separate. | Pending DP |
| 32. Retief and Klip River | Honour exchanges Ruthless for Honourable; murder grants Wrathful once and an available neutral house; guns move a displayed neutral house to a rival plus the chiefly concession. Klip cession releases the displayed ally and adds only an absent future pledge; a broker gains +10 Prominence/five years; defiance recruits one neutral house. No old direct P rewards underneath. | Pending DP |
| 33. Generic wars | One neutral house supports the incumbent on victory, or strongest eligible rival on defeat. Bespoke Blood River/Swazi/Klip cases stay excluded from generic awards. No reward from partial, expired or reversed demands. Preserve the existing one-play coordinator coverage; concurrent/auxiliary wars are not newly covered. | Pending DP |
| 34. NGN inheritance | Existing identity transfer and institutional profile continue, with scoped backing and no ZUL-root leakage. | Pending DP |
| 35. Early and late partition | Contemporary chief and preserved/exiled royal identities; no premature adult Zibhebhu. Existing NAL/TRN interventions, NRP threshold and permanent 50%/10% entitlements remain intact. A royal-versus-royal outcome grants neither entitlement. | Pending DP |
| 36. Institutional exit/re-entry | Open actions cannot execute after exit. Effects disappear; political commitments survive. Re-entry does not refresh rewards, movement enthusiasm or an already resolved contest. | Pending DP |

## Explicit claimant-war probe

Use a disposable ZUL campaign before death/retirement or confrontation. Invoke `event sb_court_succession.990` for ZUL to enable the test route. Establish two actual candidate coalitions, with an opposing share of at least 25%, then trigger the relevant succession/confrontation. The test creates a native political movement under unchanged royal laws; it does **not** create a foreign diplomatic play or script a winner.

First establish whether the engine creates a revolution at all, allocates provinces/armies and exposes its actual rebel country. Then verify named supporter placement, side selection, exact opponent/conflict callbacks and both winners. The losing prince alone dies unless already in a real exile route; other relatives survive. A dynasty victory must not dispatch the Thirteen Chiefs constitutional result.

If no native split occurs, report that result and retain the checkpoint/logs. The current scripts cannot claim the war is delivered merely because the movement has high activism. No automatic production rollout of this route is authorised by static tests.

## Evidence already supplied by DP

26 October 2026: DP reports scenarios **1, 2, 4, 5, 6, 7 and 12** are all fine. Recorded as passed in engine playtesting on DP’s report; no additional results are inferred. Further testing is ongoing.

The original 19 October build displayed a plain heading and an overflowing embedded popup; hovering recognition produced repeated missing-counter errors. Saves from February–April 1836 show Mpande and Gqugqu alive after flight, no current heir and unchanged represented court backing. These observations establish the reported failures and explain the small Prerogative movement; they do not verify the corrected source. See [the evidence and follow-up](compatibility/zulu_court_runtime_followup_2026_10_19.md).

## 25 October, 18:30 playtest follow-up — all pending DP

Historical checklist: the later follow-up below supersedes cash requoting and unchanged-year popups.

| Check | Expected result | Status |
|---|---|---|
| 37. Pledge confirmation | Bold cash price in the body; payment tooltip shows cost versus reserves and prominence of backing. Test q=10/50/100, insufficient reserves drawing on debt, existing debt and a changed quote. | Pending DP |
| 38. Paid incidents | Discredit, dispute settlement and royal firearms cost 20%, 30% and 40% of reserve capacity. Renewed quotes use the same doubled formula. | Pending DP |
| 39. Claimants and native nobility | Adult active self-claimants receive +25 from the Claimant card once, removed on accession/renunciation/exit and restored on eligible re-entry. In a fresh campaign, Mpande additionally has the gold rabbit **Fecund** card: +5% Health, +10 Popularity and +5 Prominence; Gqugqu does not. Fecund is permanent and separate from allegiance/claimant cards. Authored royals and hereditary chiefs start noble; advisers and generated councillors are not automatically noble. Native Grant Peerage remains for eligible non-nobles. | Pending DP |
| 40. Empty and changed Umkhosi reports | An unchanged year says so in the body and the option tooltip. Changed entries name the house representative, former/new allegiance or future pledge, and prominence. | Pending DP |
| 41. Roster after death, exile and succession | Open each court section and hover repeatedly. No invalid-character script errors, including expired list entries. | Pending DP |
| 42. Kill Retief | No exposed watchdog schedules or missing-container/RHS errors on repeated hover. After selecting the option, the ordinary ORA response still arrives after 21 days; expiry/recovery routing remains intact. | Pending DP |

## 25 October, 21:35 playtest follow-up — all pending DP

| Check | Expected result | Status |
|---|---|---|
| 43. Character action portraits | `sb_court_politics.001` shows the sovereign; `.002`–`.006` show the chief or prince concerned, including accommodation results after action cleanup. Coup `.100`/`.101` show the named organiser. All eight use the native one-character layout. Check long names and an open popup across a character's death or a ruler change; existing choice revalidation still applies. | Pending DP |
| 44. A Name on Every Tongue and deck cleanup | Hover each `.211` choice repeatedly, then resolve or let it expire. No missing `sb_court_deck_available_var`, unset `var` or invalid-comparison errors. Repeat with the other five scenes and an exhausted deck. The next incident still waits 6–24 months; repeated cleanup does not redraw or restart that timer. An empty eligible pool must not invent an event. | Pending DP |

Static follow-up: the preview regression reproduced the missing counter before the guard and passes afterwards for all six cards with both fresh and exhausted decks. Normal source-execution tests retain the shuffle, delay and once-only cleanup contracts. This does not verify engine rendering or delivery.

Validation: 67 focused tests pass. Full discovery runs 674 tests: 665 pass, eight skip and one fails on existing localisation review bookkeeping. The full validator reports 15/17 gates passed, warned or skipped; its unit and localisation gates both report the obsolete `sb_court_patronage_tt` queue entry, missing cost/backing rows, and reviewed-text mismatches in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`. Those files were not edited in this follow-up. Compatibility, runtime contracts and delayed-event checks pass. Advisory Tiger reports no diagnostics for the two changed script files; wider existing diagnostics remain.


## 25 October, later playtest follow-up — all pending DP

| Check | Expected result | Status |
|---|---|---|
| 45. Pledge left open while time advances | Prominence and reserve-capacity changes do not alter the quoted payment or generate further confirmations. The original named representative must still be valid, eligible and not already supporting the payer. Pay once, including with debt. | Pending DP |
| 46. Paid `.211`, `.214`, `.215` choices | Show the stored cost alongside current reserves; execute directly and allow debt. Changing capacity does not change the price. Dead/ineligible participants, a changed ruler and a repeated choice cannot charge. | Pending DP |
| 47. Umkhosi | No popup if neither allegiance list changed. On a changed year, show the actual named changes only; no empty category rows. Repeated pulses do not repeat the annual roll. | Pending DP |
| 48. Recruitment | Agitators and people with Prominence ≤0 cannot enter from the uncommitted pool through annual joining, purchases, incidents or frontier rewards. Eligible generated adults remain possible. Existing committed houses are not erased. | Pending DP |
| 49. Retief's two-character petition | The native paired window shows the actual Zulu ruler and Piet Retief. All three options remain available under the existing branch rules. The guns tooltip names the neutral house, its Prominence and the rival it will join in one line, only when both are eligible. Murder targets the portrayed Retief and retains the 21-day ORA response; internal recovery schedules remain hidden. | Pending DP |
| 50. Readability | Court choices use full names. Paid choices show the price directly. Current-allegiance-only choices do not mention unchanged future pledges. Check all six incident cards and the revised Retief prose. | Pending DP |

Static follow-up: **108 focused tests pass**. Complete discovery runs **681 tests: 672 pass, eight skip, one fails** on pre-existing reviewed-localisation mismatches in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`; those exact namespaces are unchanged in this follow-up. The full validator reports **15/17 gates passed, warned or skipped**, with unit discovery and localisation reporting that same issue. The obsolete pledge queue entry and missing cost/backing rows are corrected. Compatibility, map/naval, lifecycle and runtime-contract checks pass. Five existing deferred gates remain, and dependency synchronisation was deliberately skipped. Advisory Tiger reports 1,067 errors and 146 warnings across the existing tree, with no diagnostics on this follow-up’s changed lines; its 1.13.5 knowledge base remains behind the installed 1.14.5. No engine scenario above is marked verified.


## 26 October: court prose and Council eligibility — pending DP

| Check | Expected result | Status |
|---|---|---|
| 51. `.210` succession bargain | Description names the initial preferred prince. The Council option names the alternative prince as the person making the promise, and the tooltip names the chief pledging support in return. No law is enacted until that prince accedes with the pledge intact. | Pending DP |
| 52. `.210` blocking a pledge | Refusal requires and spends 10 Prerogative once. The chief remains personally loyal and makes no future pledge. Below 10, refusal is unavailable. An unanswered valid event accepts the proposed pledge for free; invalidated participants close without a charge. Verify the tooltip, timeout and exact-boundary case at 10. | Pending DP |
| 53. `.210.c` and `.212.b` threshold | Bargaining actor at 49.99: option hidden. At 50: available if other existing requirements hold. A prince with 100 Prominence or a house with 500 does not qualify an actor below 50. A fall below 50 while the popup is open prevents execution. | Pending DP |
| 54. Council versus privileges | Council: no amaKhosi attraction modifier/receipt. Privileges: existing ten-year attraction bargain remains separate. If privileges have already been used and no eligible chief reaches 50, the deck cannot draw the chiefly-bargain scene solely for an unavailable Council option. | Pending DP |
| 55. `.211` reputation | Separate tooltip rows show the named subject's loss, the ruler's loss, any current support withdrawn and the frozen payment. Recognition retains the existing +10/+10 reward. | Pending DP |
| 56. `.213` / `.214` portraits | Paired windows show the two actual competing representatives. Descriptions identify the incumbent and rival; tooltips separately identify each household's destination and Prominence. Test long full names and a participant dying while the event remains open. | Pending DP |
| 57. `.215` firearms | The chief's contacts and a purchase through the ruler's agents are distinct choices. The attraction consequence is separate from firearms progress; the paid option retains its frozen quote and debt access. | Pending DP |

All six rewritten scenes and new general tooltip keys await DP's prose/UI review. No game launch performed.

Static follow-up: **123 focused tests pass**. Complete discovery: **686 tests, 677 pass, eight skip, one existing reviewed-localisation failure** (`sb_klip_river_county.060`, `.080`, `sb_natal_crisis.050`). Full validator: **15/17 gates pass, warn or skip**; unit discovery and localisation report that same existing drift. Advisory Tiger reports no diagnostics on this rewrite's changed lines. See `Docs/zulu_court_event_prose_review_2026_10_26.md` for the complete validation limits.

## 26 October: Natal and Swazi follow-up — pending DP

| Check | Expected result | Status |
|---|---|---|
| 58. New Zulu campaign at P =0 | No Swazi question before the Natal outcome. Uthumbu is absent from the cast. | Pending DP |
| 59. Honour / land for guns | Before the Boer settlement is resolved, no Swazi question. Afterwards P >−10 does not open it; P ≤−10 can. Honour records the outcome immediately; no `.021` aftermath popup. The Boer `.030` response still arrives after 21 days, and the existing monthly check handles later Swazi eligibility. | Pending DP |
| 60. Blood River outcomes | Victory and white peace offer the Swazi question under Dingane at any P. Defeat requires P ≤−10. Changing ruler prevents a new offer. Leave an offer pending while P recovers: cancel the undelivered offer, then allow a fresh one if P falls again. Answered questions do not reopen. | Pending DP |
| 61. Market firearms (supersedes the earlier treaty-lane check) | Positive Small Arms supply and no market shortage: advance weekly. Test imports, domestic output and a shared market. A shortage or no supply pauses without erasing progress. An idle factory or an undelivered treaty alone does not qualify. | Pending DP |
| 62. Present Dingane's Son | At P ≥50 create/register/recognise the newborn Uthumbu once, spend 50 P and preserve the heir blocker. An existing identity retains its age. Repeated activation cannot create another child or charge again. | Pending DP |
| 63. Event presentation | Check `.020`, `.026`, `.080`, `.081`, `.094` and `.097`: appropriate paired/single portraits or diplomatic scene; actual names; separate reward rows; no visible internal scheduling. Victory acknowledgement must not apply its already-recorded court reward twice. | Pending DP |
| 64. Proclaim KwaNguni | Readable requirements for no active diplomatic play, no pending frontier settlement, territory and rival kingdoms. Confirm Nationalism and existing peace requirement still appear. Test one pending settlement and one missing territory as negative controls. | Pending DP |

The Natal and Swazi follow-up scenarios in this section await a fresh launch/checkpoint test by DP. No engine scenario has been marked verified by the static checks.

Static handoff: 124 focused tests pass. Complete discovery: 698 tests, 689 passed, eight skipped, one existing reviewed-localisation failure and zero errors. Compatibility, map/naval and lifecycle checks pass. Tiger has no diagnostics on substantively changed lines; see the prose-review record for the existing whole-tree findings and evidence paths.

## 26 October adulthood / weekly firearms follow-up — all pending DP

| Scenario | Expected result | Status |
|---|---|---|
| 65. Cetshwayo turns 18 with Mpande alive outside the throne | `.003` shows son and father; Cetshwayo's current prominence joins Mpande. His own future claim remains. Repeated pulses and an unanswered notification do not apply it twice. Repeat independently for Mbuyazi; his January declaration follows the annual roll. | Pending DP |
| 66. Mpande is ruler or dead when a son turns 18 | No special declaration. A later change of ruler does not replay adulthood. Dead sons and a son already ruling cannot declare against their own throne. | Pending DP |
| 67. NGN inherits Zulu content | Existing registered identities and adulthood receipts carry over; no recreated son or duplicated declaration. | Pending DP |
| 68. Early and late introduction of Uthumbu | In either year he is a newborn, recognised immediately, and the cost is exactly 50 P. Existing rivals survive; no adult constituency is created. | Pending DP |
| 69. Weekly supply / interruptions | Count 260 supplied, non-shortage weeks from zero. Pause with zero supply or a shortage, then resume. Existing event rewards and BST's 40% seed retain their percentages; the counter caps at completion. | Pending DP |
| 70. Restoration archive | Natal or Britain preserves weekly progress through the existing restoration route and consumes the archive once. A completed firearms programme remains complete. | Pending DP |

Source-execution tests cover these state transitions and foreign event roots. They do not establish engine market accounting, portrait rendering, birthday timing or generated-heir behaviour.

Validation of the 26 October adulthood/supply follow-up:

- Focused source checks: **65 passed**. Complete discovery: **707 tests, 698 passed, eight historical/environment skips, one existing failure, no errors**.
- Full validator: **15/17 gates passed, warned or skipped**. Both failing gates reflect the pre-existing reviewed-localisation drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`; those namespaces were not edited in this follow-up. CMF, compatibility inventory, maps, naval connectivity, runtime contracts and delayed-event lifecycle pass. Existing deferred gates BC-20, BC-22, CP-07, QUAL-09 and SUP-05 remain.
- Advisory Tiger retains **1,067 errors and 145 warnings** across the existing tree; **no diagnostics on this follow-up's changed source/localisation lines**. Its 1.13.5 definitions remain behind the installed 1.14.5 game. `git diff --check` still reports the pre-existing final blank line in `events/sb_zulu_court_events.txt:298`; this follow-up leaves that file untouched.
- Evidence: `/private/tmp/sb-26oct-adulthood-firearms-focused.txt`, `/private/tmp/sb-26oct-adulthood-firearms-units-final.txt`, `/private/tmp/sb-26oct-adulthood-firearms-static-final.txt`, `/private/tmp/sb-26oct-adulthood-firearms-tiger-changed.txt`. Prior evidence and the starting files in `/private/tmp/sb-26oct-adulthood-firearms-before/` are retained.
- The adulthood/supply scenarios in this section remain **pending DP**, using fresh campaigns. No launch, save migration or dependency change was performed.

26 October, retirement of `.021`: Honour in Retief's `.020` now records the honour-deal context and invokes the existing eligibility check directly. The Boer `.030` remains scheduled for 21 days; Swazi delivery still waits for the resolved Natal outcome and existing eligibility. Scenario 59 covers the revised path and remains pending DP. **66 focused tests pass**, including source execution of the exact Honour choice, preservation of its trait reward, correct ZUL/ORA scopes, the unresolved/high-P gates and once-only monthly follow-up. Runtime contracts, delayed-event inventory and stale/unused-symbol checks pass. The same three pre-existing reviewed-localisation mismatches remain. Evidence: `/private/tmp/sb-26oct-remove-021-focused.txt` and `/private/tmp/sb-26oct-remove-021-static.txt`. No game launch performed.

## 26 October: Blood River outcome delivery — pending DP

The 1 September 1838 autosave confirms the old defect: Zulu backdown produced Natalia,
the defeat modifier and exactly 10% firearms progress without a Zulu outcome popup.
DP confirmed that both rewards and penalties must come from the post-resolution
event, including after backdown. Political consequences apply when the Zulu popup
opens; DP subsequently clarified that its option grants firearms. Neither repeats.
This supersedes the earlier callback-owned
timing in scenario 31. Use a checkpoint before the diplomatic outcome; no migration
or retroactive reward is applied to the already-resolved autosave.

| Scenario | Expected result | Status |
|---|---|---|
| 71. Kill Retief, then ZUL backs down | ORA settles Natalia through `.070`, then ZUL receives `.082`. Court consequences and −25 P arrive on opening; its option grants up to 10 percentage points of firearms progress, once. Its tooltip names the responsible ruler and affected houses. Swazi stays closed until acknowledgement and still requires Dingane/P ≤−10. | Pending DP |
| 72. Both Blood River winners through capitulation and negotiated demands | The same once-only event consequences apply: `.080` for Zulu victory, `.082` after the Boer settlement for Zulu defeat. No reward is lost merely because there was a backdown. White peace/mutual settlement remains `.081`, granting up to 10 percentage points of firearms progress but no political victory/defeat rewards. All three grant firearms to ZUL on selecting their option, never from ORA's `.070` or merely opening the popup. Descriptions and options mention the collected guns. | Pending DP |
| 73. Delayed/held outcome and ruler change | No court consequence before the Zulu event opens, and no firearms reward until its option executes. Hover without an initial firearms counter; hold a popup past monthly checks; acknowledge once. Recheck programme eligibility at selection. No duplicate settlement or award from repeated/expired options. A replacement ruler does not inherit the captured sovereign's personal reward/penalty. No malformed portraits or missing-scope errors. | Pending DP |

Validation: **93 focused tests pass**. Full discovery: **714 tests, 705 passed,
eight skipped, one existing localisation-baseline failure**. The full validator
reports **15/17 checks passed, warned or skipped**; both failed gates report the
unchanged reviewed-prose drift in `.050`, Klip River `.060` and `.080`. Compatibility,
map/naval, runtime contracts and delayed-event checks pass. The dispatch inventory
changes only by the new `.082` delivery (438 →439). Advisory Tiger targets 1.13.5
against installed 1.14.5: 1,067 errors/144 warnings across the existing tree, none
on this change's script lines. Evidence: `/private/tmp/sb-26oct-outcome-events-tests.txt`
and `/private/tmp/sb-26oct-outcome-events-validation.txt`. No engine scenario above
has been marked passed by these checks; DP performs the launches.

26 October, Blood River balance follow-up: `.081` now grants the same once-only
firearms learning as `.080`/`.082`, without political victory/defeat consequences.
Blood River defeat is −25 P, bounded by the existing −100 floor; Swazi remains
−10 P. The obsolete ORA-labelled reward tooltip is retired. Scenarios 31 and
71–73 above reflect these changes and remain pending DP.

Validation: **42 focused tests pass**; their new expectations reproduced the old
neutral-reward and defeat-penalty differences before the code changed. Full
discovery: **716 tests, 707 passed, eight skipped, one existing localisation-baseline
failure**. The static validator passes/warns/skips **14/16 gates**; the same
reviewed-localisation drift in `sb_natal_crisis.050`, `sb_klip_river_county.060` and
`.080` accounts for both failed gates. Runtime contracts, delayed-event lifecycle,
compatibility and map/naval checks pass; touched-file whitespace checks pass.
Evidence: `/private/tmp/sb-26oct-blood-river-balance-focused.txt`,
`/private/tmp/sb-26oct-blood-river-balance-validation.txt` and
`/private/tmp/sb-26oct-blood-river-balance.diff`. No launch, save migration,
dependency change or new Tiger run was performed for this narrow balance change.

26 October, corrected option timing: DP specified that the buttons award firearms.
Opening `.080`/`.082` still applies their political consequences, but firearms wait
for the selected option in all three outcomes. The descriptions and options now
mention guns collected along the frontier. **57 focused tests pass**, including
opening versus selection, duplicate/expired options, programme changes while open,
progress caps and a hover preview without an initial counter. Runtime contracts,
delayed-event lifecycle and stale/unused-symbol checks pass. Localisation retains
only the same pre-existing reviewed-prose mismatches listed above; changed-file
whitespace checks pass. The full suite was not repeated after the preceding run.
Evidence: `/private/tmp/sb-26oct-outcome-buttons-focused.txt`,
`/private/tmp/sb-26oct-outcome-buttons-static.txt` and
`/private/tmp/sb-26oct-outcome-buttons.diff`. Scenarios 71–73 remain pending DP.

## 26 October: court refusals and the Swazi threshold — pending DP

The [save extract](compatibility/evidence/zulu_court_refusals_swazi_2026_10_26.json)
records +4.19663 P on 1 January 1841, Uthumbu as recognised heir, the Honour
settlement and `.094` opened on 27 December. The old rule was P < +10, which
explains eligibility; the snapshot does not establish the exact P when Uthumbu
was presented. DP has now approved **P ≤ −10** for the resolved-Natal branch.
Blood River victory and white peace remain independent of P. Scenarios 59, 60
and 71 above use the revised threshold. Retest from before the offer is queued;
this change does not retract a popup already open in the save.

| Scenario | Expected result | Status |
|---|---|---|
| 74. Refuse a routine court request | `.212`, `.213` and `.215` show and apply −5 P once, including when P is already low. The refusal remains available and does not grant a concession. A dead participant, changed ruler or already-resolved scene can be dismissed without a charge. `.210` retains its existing 10-P cost. | Pending DP |
| 75. Present Uthumbu after Honour | At 50 P, introducing the newborn and recognising him spends 50 P, leaving zero. His introduction does not open `.094`. The button description no longer labels him fictional. Only a later fall to P ≤−10 can qualify through this branch. | Pending DP |

Validation: **60 focused tests pass**, covering the refusal charges and
invalidations, exact −10 boundary, Uthumbu's payment, delayed-offer revalidation,
independent victory/white-peace triggers and existing Blood River outcome rewards.
New expectations reproduced both old behaviours before the corresponding changes.
Runtime contracts, delayed-event lifecycle and stale/unused-symbol checks pass.
Localisation still reports only the previously recorded reviewed-prose mismatches
in Klip River `.060`/`.080` and Natal `.050`. The full suite was not repeated after
the preceding run; no game launch was performed.

Evidence: `/private/tmp/sb-26oct-court-refusals-focused.txt`,
`/private/tmp/sb-26oct-court-refusals-static.txt`,
`/private/tmp/sb-26oct-court-refusals.diff`. Scenarios 74–75 remain pending DP.

## 26 October: missing victory after the rejected guns bargain — pending DP

The five [autosave extracts](compatibility/evidence/blood_river_guns_victory_2026_10_26.json)
span 1 October 1839 to 1 February 1840. Play 16777219 is live in October and
November; by December it is gone and Zulu's demand is recorded as accepted.
Both participants still retain the play reference and active-war flag, but no
terminal outcome receipt exists. Recovery previously treated the variable's
presence as a live play. The snapshots do not establish why the original closing
callback failed to resolve the outcome.

Recovery now uses the generation's original participants, checks that both play
handles are dead and requires an accepted demand before invoking the normal
result dispatcher. Native callbacks retain their existing paths; the monthly
check catches a missed handoff. Active plays and timer-only/disappeared demands
do not earn victory. Demand enforcement captures the sovereign before delayed
recovery, and result receipts still prevent duplicate awards.

| Scenario | Expected result | Status |
|---|---|---|
| 76. Guns offer → ORA rejects → Zulu wins | `.026` previews that Zulu will **annex** the highlighted Nguni Chiefdoms. After a confirmed victory, ZUL receives `.080`, with court consequences on opening and guns on selecting the option. If the closing callback misses the handoff, the first monthly check after the exact play disappears queues the same event for three days later. | Pending DP |
| 77. Recovery boundaries and repeat delivery | Confirm the same recovery for the Kill Retief route and for an ORA victory; no award from timer enforcement alone, an active play or a missing generation. A retagged original participant retains its outcome during an unrelated war. Repeated callbacks/checks and open popups never duplicate rewards; a replacement sovereign does not inherit the recorded ruler's personal reward. | Pending DP |

The tooltip key remains **TO REVIEW**. No reviewed prose, war goals, demand
enforcement rules, saves or dependency files were changed.

Validation: **113 focused tests pass**, including execution of the monthly
recovery against the recorded stale-play state, both original routes and result
directions, repeat delivery, timer-only rejection and responsible-ruler retention.
The full validator ran 727 tests with eight skips and four failures. Three were
obsolete expectations: the launch harness counted the new recovery helper as a
delivery, and the court contract still expected only one Prerogative charge after
the approved refusal costs. These expectations were corrected and their tests
are included in the passing 113-test rerun. The remaining failure is the existing
reviewed-localisation drift in Klip River `.060`/`.080` and Natal `.050`; those
approvals were not changed. The complete suite was not repeated after the
test-only corrections.

Compatibility, override inventory, map/naval checks, runtime contracts,
delayed-event lifecycle and stale/unused-symbol checks passed. CMF network sync
was skipped; the local pin and compatibility checks passed. The five previously
deferred release gates remain open. Advisory Tiger reported no fatal errors,
1,073 errors and 146 warnings; its 1.13.5 baseline cannot validate the installed
1.14.5 container API, including the added recovery accesses and receipt scopes.
This is not a clean engine validation. No game launch was performed; scenarios
76–77 remain pending DP.

Evidence: `/private/tmp/sb-26oct-guns-victory-focused.txt`,
`/private/tmp/sb-26oct-guns-victory-validation.txt`,
`/private/tmp/sb-26oct-guns-victory-tiger.txt` and
`/private/tmp/sb-26oct-guns-victory.diff`.

## 27 October: front tooltip, Swazi cleanup and first-click heir — pending DP

The [log/source evidence](compatibility/evidence/zulu_frontier_errors_2026_10_27.json)
records the malformed front tooltip and missing `c:SWZ` comparison. The army name
now uses a typographic apostrophe; the save stores its localisation key, so the
same formation should pick up the correction on reload. Swazi muster cleanup
uses the exact play's participants after conquest removes the tag. Uthumbu uses
the native character-creation export field, allowing registration, payment and
recognition to use the newborn's handle in the same action. The former test
interpreter incorrectly exported all callback-local scopes.

| Scenario | Expected result | Status |
|---|---|---|
| 78. Hover the Zulu army at a front | “Dingane’s Amabutho” appears normally in the battalion breakdown, with no `GetRawTextTooltipTag` or `FRONT_COUNTRY_COMBATUNITS` parser errors. Check the existing saved formation after reloading as well. | Pending DP |
| 79. Conquer and annex SWZ | The exact campaign ends and removes both muster/disarray flags and modifiers without an invalid `c:SWZ` comparison. A repeated callback is harmless; unrelated plays do not clean these effects. | Pending DP |
| 80. Present Dingane’s Son once | At 50 P, one activation creates the newborn, registers him, recognises him as heir and spends exactly 50 P. The action then disappears. An existing unrecognised Uthumbu is reused without resetting age or making a duplicate; CMF's heir blocker remains active. | Pending DP |

Validation: **108 focused tests pass**, covering first-click creation with isolated
callback scopes, foreign ROOT, single payment, reuse and duplicate prevention;
Swazi cleanup with and without a surviving tag, invalid participants and repeat
calls; and the existing court, adulthood, frontier and war-route contracts. The
new cases failed against the previous source before these corrections. Runtime
contracts, delayed-event lifecycle, on-action routing and stale/unused-symbol
checks pass. Localisation retains only the existing reviewed-prose mismatches in
Klip River `.060`/`.080` and Natal `.050`. The full suite and advisory Tiger were
not repeated for these narrow changes; no game launch was performed.

The log also contains an invalid-country error in Vanilla's
`common/decrees/00_decree.txt:101` (Violent Suppression). This is separate from the
reported SB faults and was not changed.

Evidence: `/private/tmp/sb-27oct-frontier-errors-red.txt`,
`/private/tmp/sb-27oct-frontier-errors-focused.txt`,
`/private/tmp/sb-27oct-frontier-errors-static.txt` and
`/private/tmp/sb-27oct-frontier-errors.diff`.

## 27 October: intermittent court-name navigation — pending DP

All six character banners now use one local button type. It binds directly to
the list entry's `Scope.AccessCharacter`, retains native character-panel and
right-click actions, and uses a plain full-name label that passes mouse input
through to the button. The character tooltip belongs to the whole banner. The
court remains expanded when navigating; no gameplay or roster-selection rules
were changed.

Native references: Japan's `gui/journal_entry_widgets/ep2_japan_widgets.gui`
binds its character portrait with `Scope.AccessCharacter`;
`gui/shared/character.gui` supplies the panel and right-click actions;
`gui/frontend/shared/buttons.gui` and `labels.gui` define the standard label;
`gui/shared/buttons.gui` uses mouse-transparent labels within clickable headers.
The existing formatted name created a second interactive target in the banner.
This is a plausible explanation for the inconsistent clicks; the current log
does not establish the engine cause, and static checks cannot confirm hit testing.

| Scenario | Expected result | Status |
|---|---|---|
| 81. Repeated court-banner navigation | Click both the name and blank edge for the incumbent, princes, house heads, nested house members and councillors. Each opens the matching character; right-click opens that character's menu. Repeat after another character panel was open and after scrolling/roster refresh, both paused and running. The court stays expanded and a member never opens their house leader instead. | Pending DP |

Validation: **67 focused court tests pass**. The navigation contract now checks
all six uses of the shared button, its explicit item binding, single native click
action, mouse-transparent label and preserved tooltip/right-click action.
Advisory Tiger reports no diagnostics for either changed GUI file. Its full
output retains 1,073 errors and 148 warnings elsewhere, including its known
1.14 container limitations; this is not a clean engine validation. No game
launch or complete unit-suite rerun was performed.

Evidence: `/private/tmp/sb-27oct-court-links-focused.txt`,
`/private/tmp/sb-27oct-court-links-tiger.txt` and
`/private/tmp/sb-27oct-court-links.diff`.


## 27 October: construction limits, court baseline and heir support — pending DP

The [save evidence](compatibility/evidence/zulu_court_balance_2026_10_27.json)
separates historical Cetshwayo's expired politician career from an already-existing
generated namesake. The historical identity is not reconstructed in an existing
save. Test career preservation from a fresh campaign; the latest save has already
lost him. DP confirmed the −20 base deduction, recognition by supporting
Prominence (excluding the king's own house and preserving rival pledges), and
native adulthood at 16 on 27 October. These match the implementation; engine
verification remains pending.

| Scenario | Expected result | Status |
|---|---|---|
| 82. AI construction across GDP boundaries | For SB tags, GDP £99,999 blocks a first sector; £100,000 permits it. One completed or queued sector anywhere in the country blocks another below £1,000,000. At £1,000,000 native construction resumes. Check AI bulk queuing, multiple states and a later GDP fall; existing buildings are retained. Players and unrelated countries remain unaffected. | Pending DP |
| 83. Base Legitimacy and institutional exit | Updated 27 October: Courtly Politics gives −25 Legitimacy at IR 50; P −100/0/+100 gives net Legitimacy −75/−25/+25. IR 25 halves those values. Authority and military effects retain their existing formulas. The tooltip shows the actual base and Prerogative modifiers even at P 0; exit removes all, and re-entry applies one copy. | Pending DP |
| 84. Recognise an adult successor | Spend the normal 25 P. Roughly half the incumbent's supporting prominence pledges to the heir, keeping current allegiance to the king. The king's own house is excluded, whole houses stay together and rival succession promises survive. Existing pledges to this heir count towards the share; repeated recognition does not recruit the same share again. | Pending DP |
| 85. Introduce newborn Uthumbu with a coalition | One activation creates and recognises one newborn, spends 50 P and applies the same backing rule. He gains future supporters but no adult personal following. Existing princes survive and the heir blocker remains in force. | Pending DP |
| 86. The historical brothers reach native adulthood | Cetshwayo turns 16 on 27 April 1842, Mbuyazi on 1 January 1844. On the next eligible monthly pulse, each declares for a living, non-ruling Mpande once. No declaration if Mpande is dead or king. Confirm their original historical identities remain after the former career-expiry dates (30 November 1843 / 15 December 1845); no newborn/replacement is generated by this fix. | Pending DP |
| 87. Native adulthood and regency | At 15, an unrecognised prince contributes no adult following; at native adulthood (16), he becomes eligible. A recognised minor's regency ends at the same native threshold. Normal deaths, authored retirement and deliberate removal still work. | Pending DP |

Final focused source execution: **114 checks pass**, including the exiled-backer
boundary and immediate newborn-coalition projection. Full discovery ran **737
tests: 728 passed, eight skipped and one existing reviewed-localisation failure**.
The initial full run also caught an obsolete age-18 assertion; it was corrected
and the complete affected test modules pass. The final exiled-backer case and
projection refresh were verified in the focused rerun after discovery.

The full validator reports 14/16 gates passed, warned or skipped. Its unit and
localisation gates share the existing reviewed-prose drift for Klip River `.060` /
`.080` and Natal `.050`; those namespaces were not edited here. Five deferred
release gates remain unchanged. Map/naval checks, installed CMF compatibility,
override inventory, Vanilla comparison and runtime contracts pass. Dependency
release synchronisation was skipped deliberately; no payload was changed.

Advisory Tiger reports 1,073 errors and 149 warnings against its older 1.13.5
baseline. Compared with the preceding run, there are no new script diagnostics;
the sole added warning is its already-known inability to recognise the 1.14
`GetTimedModifier` GUI function, now also used for the base deduction. Native
rendering and construction queuing remain unverified. Full unit discovery also
emitted system Git/Xcode cache warnings; these were not additional test failures.
No game launch was performed.

Reports: `/private/tmp/sb-27oct-balance-focused.txt`,
`/private/tmp/sb-27oct-balance-full.txt`,
`/private/tmp/sb-27oct-balance-unit-final.txt`,
`/private/tmp/sb-27oct-balance-tiger.txt` and
`/private/tmp/sb-27oct-balance.diff`.


## 27 October: annual allegiance and war outcomes — pending DP

The mathematical annual model is unchanged; its native random-list weights are now scaled before integer conversion. Use new campaigns/checkpoints before the relevant roll or settlement; past losses are not replayed and no missing historical report is fabricated.

| Scenario | Check | Status |
|---|---|---|
| 88. Annual changes with uncommitted houses | Advance through eligible annual rolls with several uncommitted adult house heads. Current allegiance and future succession can change independently. Inspect the named changes and prominence in the harvest report; years without changes remain silent. No missing old/new patron comparisons in the log. | Pending DP |
| 89. Persistence, withdrawal and switching | Compare unpopular/popular patrons over repeated starts; committed houses usually remain, but withdrawal and switches are possible. The annual reservation prevents a repeat roll. Dynastic candidates are excluded from rolling and committing ordinary allegiance changes: Mpande and Gqugqu retain their self-claims, Claimant cards and +25 Prominence; a prince supporting his father retains that allegiance. Other houses can still join either prince. Replay before the annual transition; an already-lost card is not repaired. Minority pledges and reserved succession/conflicts retain their existing protections. | Pending DP |
| 90. Campaign and generic defeats | Generic defeat still recruits up to two eligible uncommitted houses and costs 25 P. Blood River and Swazi each send the **largest uncommitted house** and **two smallest eligible incumbent-supporting houses**, ranked by aggregate Prominence, to the **same rival**. Ndlela kaSompisi is explicitly excluded from both defection slots, including when he is the smallest or only remaining supporter. Check all named previews, unchanged allegiances before the click, and once-only changes on acknowledgement. Missing pools or stale targets are skipped without replacements. Future-successor pledges stay intact. Each campaign defeat applies a **−30 P** shock, bounded at −100, and gives its responsible ruler permanent **−25 Popularity**. Replay both losses and inspect the resulting rival strength and Prerogative. | Pending DP |
| 91. Swazi Zulu-facing outcomes | Win by conquest/Swazi backdown, or lose through Zulu backdown/enforced defeat. Exactly one Zulu outcome opens: `.097` victory or `.098` defeat. Opening reserves the preview; the option applies effects once. Repeated callbacks/acknowledgements cannot add them again. Inspect portrait, actual named houses, +40/−25 Popularity and the defeat shock of −30 P. White peace retains its separate existing treatment. | Pending DP |
| 92. Concessions and timer callbacks | A chiefly concession retains its original expiry if the movement disappears and is recreated; no bare-variable duration error. In the exact Klip/Bechuanaland plays, timer flips remain reversible evidence and final callbacks remain final. Check reversals and repeated callbacks; no rewards from missing demands. | Pending DP |

## 27 October: constitutional alignment — pending DP

| Scenario | Check | Status |
|---|---|---|
| 93. IG exclusions and personal commitments | Industrialists, Intelligentsia and Trade Unions remain constitutionally neutral, including during annual recruitment and NAL/TRN bribe or defection offers. After an IG change, native constitutional movement membership rejects the character immediately and the next backing refresh clears the alignment trait. Personal allegiance, future pledges, prominence and royal claims survive. Other IGs retain the existing opportunities. | Pending DP |
| 94. Chiefly Federalist and Moderate transitions | A Royalist joining amaKhosi becomes Chiefly Federalist; a Chiefly Federalist joining uSuthu becomes Royalist. Moderates convert only when changing alignment with their home country's Thirteen Chiefdoms JE open. Test NAL/TRN actions and CAP exiles; unrelated ideologies, repeated assignments and ordinary monthly refreshes retain their ideology. Inspect Chiefly Federalist's law stances and icon. | Pending DP |

## 27 October: outcome clicks and harvest rendering — pending DP

| Scenario | Check | Status |
|---|---|---|
| 95. Political effects wait for the option | Open Blood River `.080`/`.082` and Swazi `.097`/`.098`, inspect P, the responsible ruler's Popularity and named houses before clicking, then click. Only the click applies rewards/penalties. Defeat costs 25 P, bounded at −100. Keep a popup open while a previewed house dies or pledges elsewhere: skip it without recruiting an unpreviewed replacement. Repeat callbacks must not repeat rewards. `.081` retains its neutral firearms-only result. | Pending DP |
| 96. Harvest names in both constitutions | Trigger a changed annual report under Monarchy and Federated Chiefdoms. Check the royal name in the royal description and every join, withdrawal and switch in current/future allegiance rows. Names and house Prominence render without nested `THIS` errors. An unchanged year remains silent. | Pending DP |
| 97. Mpande and Gqugqu careers | Fresh campaign: inspect both actual characters' politician career dates; neither retires in the 1840s merely because a default role expires. Preserve disease, ordinary mortality, authored retirement and removal. No deleted character is reconstructed in old saves. | Pending DP |
| 98. Low-P legacy coup and claimant-war gap | Historical investigation retained: the October 1842 snapshots showed no legacy coup attempt despite low P. Do not infer that zero Popularity explained it. The old coup mechanism is now retired; use scenarios 99–108 for its replacement. | Superseded by Contested Crown; historical evidence preserved |

## 27 October: Contested Crown — explicit test opt-in, named faction handoff awaiting replay

Use a disposable **new campaign**, or checkpoints made from that campaign before its crisis. Opt in as ZUL with `event sb_court_succession.990`. This enables eligible challenges, contested succession and organised purge exposure for that test court; it does not force an ineligible conflict. Unopted campaigns must remain unaffected. No engine scenario below has been performed by Codex.

**Earlier scenario 99 follow-up (superseded by the native IG blocker below):** the first 1 February 1840 save showed 23% activism after roughly 23 weeks. The subsequent 100-point/week trial reached full activism in another 1 January 1840 replay, but no native organising war existed. The movement had no attached characters; the cause was unresolved at that stage. DP requested **25 percentage points/week** (`growth_mult = 24`), replayed from before movement creation. Reducing the rate does not lower already-saved activism. The pre-sponsorship 17:43 replay established the IG eligibility blocker; it had not reached the split or military allocation. Adding an agitator alone does not bypass it.

| Scenario | Check | Status |
|---|---|---|
| 99. Native demand and organising war | Fully restart before the crisis/side choice. Pause until the date stops advancing before invoking `.990`, then resume after choosing a side. Confirm Strongly Disapprove for Monarchy (Social Monarchy in its variant), the demanded Contested Crown law, attached claimant, all-IG pressure/sponsor eligibility, a −20 Approval modifier on every IG and +100% movement Pop Attraction. Verify pre-creation recruitment with 99d. Record actual sponsor, its backing/influence slots and the organising war before expecting scripted progress. | **Creation observed — DP and June–August save audit, 28 October:** war 3 organises, then splits with both rulers installed. Revised regional preference and military-household redistribution require a new pre-choice replay. [Evidence](compatibility/zulu_contested_crown_2026_10_27.md). |
| 99a. Sponsor and attraction lifecycle | Before selecting a side, no new Approval penalty. After either `.004.a/b` choice, every IG receives one −20 modifier and the temporary crisis ideology. Check both actual countries even if native modifier inheritance omits the penalty. Cancel, win as either contender, or exercise missing-war recovery: all IG packages and the movement attraction modifier clear. Preserve ordinary leader ideologies and unrelated countries. Repeated polls do not stack penalties or attraction. | **Package partly observed, 28 October:** all eight IGs carry exactly one crisis modifier and ideology in three pre-split saves. Both choices, pre-choice state, rebel inheritance, cleanup and unrelated-country controls remain pending DP. Source-executed lifecycle checks pass. |
| 99d. Recruitment before native creation | From before either side choice, use Zululand 4 barracks/17 conscription levels and Natal 0/0. Selection should produce 3/17 and 1/0 before the claimant movement organises. Check the new unit record and its recruitment, not only building levels. No total service increase, repeated relocation or change to economic/naval buildings. Confirm a one-state country needs no relocation, sparse forces are not duplicated and cancellation does not destroy/rebuild again. After an actual split, scenario 101 must still give the final coalition quotas under either geography. | **Preparation and creation observed, 28 October:** June save has 3/17 and 1/0 with a native organising war; July/August have both countries. Sparse/cancellation cases remain pending. Staffing failed in this replay; revised military-household movement is pending in 101b. |
| 99b. Rebel creation and institutional JE | Reload the mod and use a checkpoint before the side choice, with the full court snapshot. Inherited laws must not initialise the court before the rebel has land/AI. Both actual countries retain the same exact war receipt across monthly pulses and show one Prerogative JE. Generated ruler/heir placeholders die; the recorded contender governs. Preserve existing princes/children, including an authored native heir. Repeat after a native government reshuffle; keep heir generation blocked during the war. | **Partly observed, 28 October:** earlier replay retained Gqugqu/original and Dingane/rebels; latest July/August retain Dingane/original and Gqugqu/rebels with war 3, no generated heirs, and Mpande/Cetshwayo/Mbuyazi present. Full placeholder-death, JE and reshuffle checks remain pending. |
| 99c. Named claimant agitator | Start before reserving the challenge. Use `.990`, then either `.004` choice. The opposing prince gains the agitator role and joins the exact Claimant's Cause movement; ordinary character ideology is preserved. Scripted progress waits for attachment. Country ruler installation is a separate split-time step, not a consequence of the agitator role. Cancel: remove the role only if this crisis added it. A pre-existing agitator remains an agitator. | **Attachment and creation observed, 28 October:** Gqugqu is attached before war 3 organises in June. Cancellation and pre-existing-role controls remain pending. |
| 100. One-state coalition strength | In one-state Zulu with multiple provinces, test 25/50/75% claimant backing under both choices. After the actual split, verify one reset of completed recruitment levels: claimant round(total × R/(I+R)), incumbent remainder, calculated separately for regulars and conscripts. Record states/provinces, levels, unit types, available battalions, manpower, experience and commanders before/after, then after one week and one month. Verify native caps/staffing and repeat callbacks. | Pending DP; destructive rebuilding approved for testing, 28 October. Lost manpower, experience and composition are intentional; practical military influence remains unverified. |
| 101. Several states and uneven barracks | Repeat 25/50/75% backing and ties with 0/1/4/17 total regular levels. Reserve one existing level for the weaker coalition, round its share of the remainder and give the stronger side the exact rest; conserve totals. At 177:334 and four regular levels expect 2:2. Seventeen conscription levels still target 6:11, subject to native caps. Preserve training methods and economic/naval buildings. | **New floor pending DP, 28 October.** Previous replay retained 3:1 regulars, 11:0 conscription; no claim that the new quotas guarantee staffed armies. |
| 101a. Stronger coalition receives Zululand | Restart before choosing a side with both Zululand and Zulu-owned Natal. Test 300:100, 100:300 and 200:200 backing under both choices. Stronger side owns Zululand; tie favours the incumbent. Original ZUL still belongs to the selected contender. Check the native proposal before division and actual ownership afterwards; other countries and the one-state fallback stay unaffected. | **Observed for stronger Gqugqu, 28 October:** September–November saves put his 334-Prominence coalition in Zululand and Dingane's 177 in Natal. Stronger incumbent, both selections, ties and one-state controls remain pending DP. |
| 101b. Military households and recruitment | Divide existing soldiers and officers separately by actual rounded barracks quotas, including the weaker floor; four levels at 177:334 target 50:50. Move dependants and preserve people, cultures/religions and civilian professions. With zero barracks retain the existing ratio. Check immediately after split, then after one week/month; repeated callbacks must not move again. | **Pending DP, new rule 28 October.** October replay before this change has 10,241/103 servicemen/officers in Zululand and 258/16 in Natal, with 9,349 versus 274 battalion manpower. Hiring and conscription remain unverified. |
| 102. Human and AI side choice | Play both `.004` choices from equivalent pre-choice checkpoints. The human retains original ZUL with the selected contender; the opposing contender leads rebels. Native territorial target inverts with the opposing side, bounded to 10–75%. Experimental force quotas follow contender identity and the unclamped two-coalition share, regardless of original/rebel geography. Named commanders follow their frozen house; third-prince commitments remain intact. AI keeps sovereign/original versus prince/rebels. | **Both named handoffs partly observed across replays:** latest keeps Dingane/original and Gqugqu/rebels; earlier keeps Gqugqu/original and Dingane/rebels. Revised geography, army staffing, AI and full commitment/outcome checks remain pending. |
| 103. Both winners and original institutions | Win as each contender under Monarchy and Social Monarchy after both side choices. Check the actual ruler, restored royal law, losing cohort, surviving third-party princes, heir protection and once-only cleanup. No dynastic incorporation/NRP/Thirteen Chiefs reward. | **One outcome observed — DP and post-war save audit, 28 October:** Gqugqu wins in original ZUL, ordinary Monarchy returns, Mpande/Cetshwayo/Mbuyazi survive, Dingane/Ndlela are retired, crisis packages clear and one institutional JE remains. Other winners/orientations/variants remain pending. |
| 103a. Complete cast and commitments after reunification | Before the challenge record character IDs, houses, current patrons and future pledges, including minors, advisers and third princes. Win as Mpande: Dingane, Ndlela and the other incumbent coalition members die; Gqugqu, young Cetshwayo and neutral houses remain unless explicitly in the losing coalition. Repeat with Dingane winning, killing Mpande's coalition. Check again after the defeated country disappears: survivors are the same IDs in the winner's country, with distinct current/future commitments and correct house membership. Pre-existing void/exile remains; natural deaths are not undone. Test succession using future pledges instead of today's patrons. | Pending DP; requires a checkpoint before the challenge snapshot, no save migration |
| 104. Low-P and consequence entry | With opt-in, test P −49.99 versus −50 and rival share just below versus at 25% of current pledged Prominence. Check monthly entry and immediately after a committed political consequence. Use the strongest eligible rival, not a merger of every prince. An unrelated foreign war does not block entry; an existing native civil war or coup does. Without opt-in, no automatic challenge. | Pending DP |
| 105. Death, retirement and minority | Trigger contested sovereign death and Mpande's first eligible pulse on/after 1 August 1856. Use future pledges and 30% of succession-pledged Prominence, not today's patrons. Preserve a third claimant. Test an acknowledged minor, regent death/replacement, adulthood and a sole viable peaceful successor. The child receives no invented following and retirement does not script Mpande's death. | Pending DP |
| 106. Organised purge exposure | Expose a failed purge against the actual organised rival in the enabled court. It enters the shared controller with current allegiances and the correct opponent. Lesser-rival flight remains separate. No return to coup strength/resistance, foreign-war substitute or rolled military winner. | Pending DP |
| 107. Pending choices, death and cleanup | Leave `.004` open across pulses; kill/invalidate either displayed participant and check safe dismissal with no replacement or payment. Cancel/reopen before a queued `.991` delivery: at most one weekly chain. During an actual war, kill either contender without ending the war artificially; a dead winning contender invokes succession. Test a different movement splitting first, institutional exit, disappearance of the exact war object, and restoration without a fabricated winner. | Pending DP |
| 108. Integration and unrelated controls | Exercise early/later partition, chiefly and mixed constitutions, NAL/TRN interventions, NGN inheritance and separate constitutional revolutions. Their existing settlement/NRP/incorporation rules remain distinct. Under the temporary laws check Prerogative/IR, titles, heir blocking and resistance to arbitrary ruler replacement. Normal enactment/imposition cannot introduce contested laws; unrelated countries and native coups retain their behaviour. | Pending DP |

**Release gate:** a larger frozen coalition must yield a meaningful, repeatable military advantage. A changed territorial share alone is insufficient. If the native demand, war creation, callback timing or military influence fails, report the specific failure and retain explicit testing only. Do not enable stage 2 or substitute a foreign war, a rolled winner or combat modifiers.

**Latest agitator/cast follow-up:** 103 focused checks pass; final full discovery has 790 passes, eight historical skips, one unchanged reviewed-localisation failure and zero errors (799 tests). Full validator remains 15/17, with the two failures sharing the existing reviewed-prose drift. These source results leave 99c/103a and the other unperformed engine scenarios pending.

**Latest country-assignment follow-up:** 145 focused checks pass. Full discovery: 805 tests, 796 passes, eight historical skips, one unchanged reviewed-localisation failure and zero errors. Full validator remains 15/17, with the same reviewed-prose failures and advisory Tiger totals. Native war lists are origin-only; tests now reflect this. Both side choices keep the player in original ZUL and target the opposing coalition's share. New head-removal, monthly persistence and both-orientation outcomes remain pending DP.

**28 October rebuilding follow-up:** 49 focused checks pass. Full discovery: 813 tests, 804 passes, eight historical skips, one unchanged reviewed-localisation failure and zero errors. Full validator 15/17; advisory Tiger unchanged at 1,073 errors / 149 warnings. Source fixtures supply the native split and cannot establish war creation, available troops or recruitment after rebuilding. All new runtime cases remain pending DP.

Source verification and current compatibility evidence are recorded in [the implementation report](compatibility/zulu_contested_crown_2026_10_27.md). Source tests supply native callback inputs; they do not prove native allocation, popup rendering or faction handoff.

Final static results: **25 focused claimant checks pass**. Full discovery: **779 tests, 770 passes, eight historical skips, one existing reviewed-localisation failure, no errors**. Full validator: **15/17 gates passed/warned/skipped**. Tiger remains advisory (1,073 errors, 148 warnings against its older schema), with no new claimant-file diagnostics. These results do not change any pending engine status above.

## 28 October follow-up: successful victory and inherited content

Use a fully restarted game and checkpoint **before side selection/movement creation**. The previous successful post-war save predates these changes; no migration is provided.

| Scenario | Check | Status |
|---|---|---|
| 109. Mirrored Adoption of Firearms | Before the split give the original JE fractional progress, such as 10.4 supply weeks. Rebel receives one JE with exactly that progress/display and weapons penalty. Each country's market then ticks independently. A completed source transfers completion without a new JE/reward. Unrelated countries stay unchanged. | Pending DP; source checks pass. |
| 110. Victory acknowledgement | Win as either side. Opening `.005` awards no Prerogative; `.005.a` adds 10 once, capped at 100. Check an open popup, repeated callbacks and acknowledgement, and no automatic partition reward. | Pending DP; source checks pass. |
| 111. IG balance after personal war | Record pre-war ideologies/modifiers. After either victory, the twenty-year Defeated modifier added by this conflict is absent; earlier Defeated penalties and unrelated patronage remain. Temporary −20/crisis ideology clears everywhere. Do not require identical Clout percentages after character deaths or changed population. Cancelled/unrelated conflicts retain their penalties. | Pending DP; source checks pass. |
| 112. Narrow Approval experiment | Current successful source retains all-IG −20. Native sponsors were Devout/PB/RF/TU, not AF. Before narrowing, run a controlled pre-choice trial proving which targeted package reliably creates the same conflict without other tuning. Do not treat current success as proof that AF-only works. | Deferred; current package retained. |
| 113. Performance regression | Carry out `PERF-20261028-01`: matched timing/profiling in peaceful court, preparations, war and post-war; distinguish transition stalls from sustained tick costs. | Open major TODO; not profiled. |

**Current source verification:** 83 focused claimant/firearms tests pass; full discovery has 822 passes, eight historical skips and one existing reviewed-localisation failure (831 total, no errors). Validator 15/17, compatibility/maps pass, advisory Tiger unchanged with no changed-file diagnostics. See the compatibility report. These tests do not certify native recruitment, rendering or timing.

## 28 October: opening IG leadership and later Rural Folk candidate

Use a fresh campaign for opening appointments. Source details and chronology limits are in the [leadership brief](zulu_ig_leadership_research_2026_10_28.md).

| Scenario | Check | Status |
|---|---|---|
| 114. Opening appointments | Mkabayi leads LO, Ndlela leads AF and Langazana leads Devout. Langazana is historical/noble, appears once under esiKlebheni, has a single name and is royal-aligned but personally uncommitted. Her native Prominence counts once. Mpande remains a claimant/politician without an automatic LO appointment. | Pending DP; source checks pass. |
| 115. Appointments and commitments over time | Change Langazana's allegiance or future pledge, then advance several months. Records persist. Native retirement/death and IG replacement work without creating a second Langazana or restoring old commitments; ordinary court actions can target her. | Pending DP; source checks pass. |
| 116. Later amaCube candidate | No Sigananda kaZokufa before 1865. Eligible ZUL or inherited NGN with Zululand territory creates him once as an adult RF politician, with amaCube following and no predetermined allegiance. He does not force out the RF leader. A claimant crisis defers entry; an unrelated war does not. Death/re-entry cannot recreate him. The fictional Sigananda Zulu remains a separate identity. | Pending DP; source checks pass. |

**Leadership validation:** 96 focused checks pass. Full discovery plus the corrected review-date contract's targeted rerun accounts for 827 passes, eight historical skips and one pre-existing reviewed-localisation failure; no errors. Compatibility and map/naval checks pass. Tiger remains advisory with no changed-file diagnostics. The [leadership brief](zulu_ig_leadership_research_2026_10_28.md#source-validation) records the full-run/targeted-rerun distinction and unchanged prose failures.

## 28 October: live entry and the next generations

DP's successful AI replay authorises automatic entry and supersedes the older explicit-test-only release hold above. It does **not** certify troop employment or the unperformed scenarios below. Restart with the new source; use fresh campaigns or checkpoints before the relevant episode, with no save migration.

| Scenario | Check | Status |
|---|---|---|
| 117. Automatic claimant challenge | With no `.990` invocation, reach P ≤−50 with an eligible rival holding ≥25% current pledged Prominence. One side-selection event opens. Test both sides and native outcomes; no duplicate while the popup/war is open. Unrelated countries do not enter. | Pending DP on the live entry; prior manual/AI conflict success reported by DP. |
| 118. Staff at the actual split | Save immediately before choice, after preparation and immediately after rebel creation. Record state ownership, barracks, servicemen/officer workforce and dependants, vacancies, available battalions and manpower on both sides. Compare with whole-barracks ratios, not raw coalition percentages. Distinguish later AI rebuilding/migration from the initial allocation. | Pending DP. Copied June–October 1841 saves are all after reunification and cannot answer this. |
| 119. Undocumented line / Uthumbu | Gqugqu presents a newborn, pays 50 P once, recognises that identity, and transfers roughly half eligible supporting Prominence. Child has no adult following. Dingane still gets Uthumbu; a later unrelated sovereign has their own one-use opportunity. Known-line rulers cannot buy replacement sons. | Pending DP; source checks pass. |
| 120. Dated descendants / minority | Cetshwayo alive in his court: Dinuzulu appears once in 1868; Dinuzulu alive: Solomon in 1891. No birth before the date, no resurrection or duplicate when already created elsewhere. Recognition is separate and permits a minor; death with a recognised child uses the existing regency. Check early partition/exile and inherited NGN. | Pending DP; source checks pass. |
| 121. Second Zulu civil war | Mpande remains until the first eligible pulse on/after 1 August 1856. With a secured line, peaceful retirement; with an opposing coalition holding ≥30% of succession-pledged Prominence, choose Cetshwayo or Mbuyazi and resolve both outcomes. Preserve other surviving lines, original institutions and firearms progress; honour existing coalition-loss rules and +10 P only on victory acknowledgement. | **Next DP priority.** |
| 122. Thirteen Chiefdoms / third conflict | After the second-war routes work, test early and later partition, the actual living royal line (including Dinuzulu when born), NAL/TRN interventions, constitutional victory and once-only incorporation/NRP consequences. A personal claimant war must not grant these constitutional rewards. | Pending DP; main content pass follows scenario 121. |

**Live-entry validation:** 199 focused checks pass. Full discovery: 836 passes, eight historical skips and one unchanged reviewed-localisation failure (845 total; no errors). Validator 15/17; current compatibility and map/naval checks pass. Advisory Tiger unchanged, without changed-file diagnostics. [Evidence and precise limits](zulu_court_release_heirs_2026_10_28.md).

## 28 October: event popularity and Swazi demand follow-up

| Scenario | Check | Status |
|---|---|---|
| 123. Popularity-weighted episode princes | Open `.210` and `.214` with princes of different Popularity. Over repeated fresh draws, the more popular prince is selected more often; `.210` has distinct alternatives. An open popup keeps its displayed prince if Popularity changes. `.213` keeps the house's actual patron. | Pending DP; 104 focused source checks pass across this follow-up. |
| 124. Swazi's additional goals | Restart before `.094`: ZUL retains Conquer State and SWZ humiliation. During escalation SWZ cannot add Conquer State for Zulu land. Enforce ZUL's territorial demand by timer, then verify SWZ's native recovery demand remains valid. Other SWZ plays and unrelated countries remain unrestricted. | Pending DP; source eligibility and full CMF-body parity pass. |
| 125. Repeated ORA mobilisation | Let AI ORA fight Blood River across several monthly pulses. An available unmobilised army is mobilised, already mobilised armies are skipped, and the reported formation error does not recur. Check no duplicate assistance formations. | Pending DP; repeated source execution passes. |

[Change record and validation](zulu_court_swazi_followup_2026_10_28.md).

## 28 October: court icons, civil-war supply and save findings

| Scenario | Check | Status |
|---|---|---|
| 126. Modifier and movement presentation | Inspect Courtly Politics, Co-operation with the Settlement and Co-operation of the Amabutho: each has a loaded icon. The live claimant movement reads Dynastic Rivalry without a test label. | Pending DP; native asset paths verified. |
| 127. AI civil-war provisioning | From before the actual split, test backing either prince and an AI-only war. Only AI participants receive −50% Supply Consumption. Record supply, organisation and attacks; check cleanup on either victory, aborted conflict and player takeover after monthly reconciliation. Other wars receive nothing. | Pending DP; source lifecycle tests pass. AI attack behaviour remains unverified. |
| 128. Renounced claimant and Klip routing | Cetshwayo's absence in the September 1851–January 1852 saves follows his saved renunciation; Mbuyazi has none. For Klip, replay from before British Natal settlement and record `.010` choice or `.075` fallback, since every retained save already has the terminal departure flags. | Save diagnosis recorded; earlier Klip route cannot be recovered from retained snapshots. Replay pending DP. |

[Findings and validation](zulu_court_save_followup_2026_10_28.md).

## 28 October: historical AI heirs and successor preview

DP reports Klip River fired after reloading the post-civil-war checkpoint. This updates scenario **128** for that replay; the original completed route remains indistinguishable from its terminal flags.

| Scenario | Check | Status |
|---|---|---|
| 129. Historical AI Mpande's targets | Load before either son's renunciation. In Strict/Dynamic Historical, AI Mpande cannot demand renunciation or purge Cetshwayo/Mbuyazi, while Gqugqu remains eligible. Human control, Off and later rulers retain normal choices. An already-open quote must revalidate before charging after AI takeover. | Pending DP; source target and stale-quote checks pass. Existing saved renunciations are retained. |
| 130. Successor preview scope | Repeatedly open the court JE and hover Recognise a Successor. No temporary/permanent `sb_court_country` collision; eligible heirs, including acknowledged children, remain selectable. No candidates gives the normal disabled requirement. | Pending DP; foreign permanent-scope and eligibility source checks pass. |

[Evidence and changes](zulu_heirs_preview_followup_2026_10_28.md).

## 29 October: cumulative campaign defeats

This supersedes the defeat amounts in scenarios 90, 91 and 95; their other checks remain applicable.

| Scenario | Check | Status |
|---|---|---|
| 131. Blood River followed by Swazi defeat | From before acknowledging Blood River's outcome, lose Blood River: `.082.a` costs 25 P and records the defeat. After answering the Swazi offer, lose that campaign: `.098.a` displays and applies 50 P. Without a prior Blood River defeat (including victory/white peace), Swazi defeat costs 30 P. Opening either popup changes no P; repeated acknowledgement gives no extra penalty. Retain the −100 floor and existing allegiance/Popularity changes. | Pending DP; test from before the Blood River acknowledgement, since already-consumed outcomes are not migrated. |

Validation: **93 focused tests passed** across Blood River/Swazi outcomes, campaign defections, court events and institutional calculations. The new sequence cases exercise both loss branches, victory/neutral controls, AI-context cleanup, foreign ROOT, option timing and repeated acknowledgement. Runtime script contracts and unused-symbol checks pass; changed-path whitespace checks pass. The repository-wide whitespace check separately reports an existing blank line at EOF in `events/sb_zulu_court_events.txt:321`, outside this change. No game launch performed.

## 29 October: stronger AI faction and post-war consolidation

| Scenario | Check | Status |
|---|---|---|
| 132. AI chooses the stronger coalition | Before `.004`, test incumbent and claimant majorities, then a tie. AI always backs the greater frozen coalition Prominence; a tie favours the incumbent. The selected contender rules the main country, the other rules the rebels. A live Popularity/Prominence change after reservation does not change the quoted choice. Human choice remains free. | Pending DP; source choice weights and both faction assignments pass. |
| 133. Contender Prerogative and victory protection | From before the split, give Dingane negative P. His side retains that value; Mpande's side starts at 0. Backing Mpande therefore gives the main country 0 and Dingane's rebel country the old value. Check both side choices, AI/human control and both winners. Victory starts an 18-month cooldown on new automatic low-P claimant challenges before `.005` is answered; `.005.a` still grants +10 P once, capped at 100. A victor at −75 therefore reaches −65 but cannot immediately face another low-P challenge. Expiry restores ordinary eligibility. Death/retirement succession, coercion and unrelated native revolutions are not blocked by this cooldown. | Pending DP; source initialisation, repeated callbacks, actual-winner scope, duration, simulated expiry and reward checks pass. |

Validation: **124 focused tests passed** across claimant wars, court succession and institutions. Cancellation grants no victory protection. No game launch performed; use checkpoints before the relevant split/victory, since existing outcomes are not migrated.

## 29 October: AI successor recognition

| Scenario | Check | Status |
|---|---|---|
| 134. Dingane and Mpande's AI recognition | With sufficient Prerogative, AI Dingane never uses Recognise a Successor. AI Mpande uses it only without a living recognised heir, choosing eligible Cetshwayo/Mbuyazi with 66:33 weights, regardless of prominence order. If only one son qualifies, choose him; if neither qualifies, do not open recognition. After recognition, retain that heir without repeated charges or redesignation. Revalidate an already-open choice after a ruler/control change or another recognition. Human choices, other rulers and the existing 25-P charge remain unchanged. | Pending DP; source eligibility, all twelve option slots, selection, payment and negative controls pass. |

Validation: **176 focused tests passed** across recognition, court politics, succession, claimant wars, frontier integration and institutions. Runtime script contracts, unused-symbol checks and changed-path whitespace checks pass. No game launch performed.

## 29 October: Mpande's sons come of age

These events use the existing first-adult monthly check: test from before Mbuyazi turns sixteen (1 January 1844 in the authored birth record). A checkpoint whose adulthood receipt is already set will not replay it. The earlier `.003` father-support declarations remain in force when Mpande is alive but not ruling.

| Scenario | Check | Status |
|---|---|---|
| 135. The Two Brothers — `.006` | Mpande rules, both sons are living eligible dynasts, and no living recognised heir exists when Mbuyazi reaches adulthood. Both sons appear in paired portraits. Test each choice: recognise that son, spend 25 P (this birthday choice permits a negative result), retain the usual transfer of roughly half the king's supporting house prominence, and give the other son Ambitious. If the other son has no pledged outside backer, the most prominent eligible unpledged house representative promises his house to him first. Existing promises are preserved. AI weights are 66:33 Cetshwayo:Mbuyazi. | Pending DP; source option execution, ordering, costs and both outcomes pass. |
| 136. The Other Brother — `.007` | Repeat with either son already recognised. Keep the heir and charge no P; the other brother gains Ambitious and, only if he lacks a backer, the highest-prominence eligible unpledged representative's future pledge. Test an existing rival backer, no unpledged houses, dead/renounced sons, a third recognised heir, and a changed ruler/heir while the popup is open. No duplicated award, rewritten current allegiance or silent substitute backer. Cancellation releases the recognition reservation on the next monthly check. | Pending DP; source lifecycle and negative controls pass. |

DP confirmed on 29 October: the birthday choice spends 25 P and may take Prerogative below zero; a rival backer is supplied only when none exists. Here “unpledged” refers to the next succession, not current allegiance or constitutional alignment. Selection excludes agitators, zero-prominence characters, princes and ineligible house representatives. Neither event guarantees the later retirement war: that still depends on the resulting coalitions.

Validation: **237 focused tests passed** across adulthood, recognition, court politics/events, claimant wars, frontier handling and institutions. Runtime script contracts, unused-symbol and delayed-event lifecycle checks pass. The full localisation gate retains unrelated failures: reviewed drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`, plus the existing `sb_swazi_frontier.098.prerogative_after_blood_river` review-queue row. New `.006`/`.007` prose is **TO REVIEW**. Native writing model: installed `shogunate.2`; paired portrait model: `commander_events.4`. No game launch performed.

## 29 October: native one-state split and multi-state wartime muster

The staffing expectations in scenarios 112 and 118 are superseded by the full regular-plus-levy job ratios for a multi-state origin. A one-state origin now bypasses scripted military/population allocation entirely.

| Scenario | Check | Status |
|---|---|---|
| 137. One-state / multi-state force allocation | Execute the six numbered scenarios in the [muster matrix](zulu_civil_war_muster_runtime_matrix_2026_10_29.md), beginning before the claimant choice. Check both selected sides, both winners, ordinary conscription suppression only in the multi-state path, actual manpower/qualifications, population conservation and cleanup after state merging. | Pending DP. Source checks do not establish native recruitment or battle balance. |

Checkpoint: `1a3d7c3`. [Implementation record](zulu_civil_war_muster_proposal_2026_10_29.md). No save migration or game launch.

## 29 October: Mpande, Mbuyazi and Cetshwayo — revised defaults

This supersedes the AI weights in 134–135 and Cetshwayo's one-backer limit in 135–136. Replay from before the relevant one-time event; no consumed birthday or saved succession is migrated.

| Scenario | Check | Status |
|---|---|---|
| 138. Mpande consolidates against Gqugqu | In Strict/Dynamic Historical under AI Mpande, Gqugqu is targeted for a purge when existing gates allow it. At insufficient P there is no substitute renunciation. A completed purge cannot repeat in the reign; protected sons, human play and Off retain their rules. | Pending DP. |
| 139. Brothers and preferred heir | Before Mbuyazi's sixteenth birthday, test both choices in `.006`, then either already-recognised son in `.007`. AI prefers Mbuyazi 66:33. The passed-over Cetshwayo gains enough available unpledged houses to reach two outside backers; Mbuyazi's floor remains one. House totals determine ranking. Existing pledges are not taken, empty pools give no invented support, and frozen participants are revalidated. The heir still receives ordinary recognition support after rival houses are reserved. Check early/later prose variants and each named tooltip. | Pending DP; focused source execution passes. |
| 140. Dunn before retirement | From before July 1856 under Mpande with both adult claimants, inspect `sb_court_dunn.001`: Dunn/Mbuyazi portraits and named pledge. Opening grants no backing; acknowledgement adds Dunn's existing house to Mbuyazi's future coalition once. Leave it open over August: scheduled retirement waits; death or invalid participants cancels the offer. Existing, dead and foreign Dunn identities must not duplicate. | Pending DP; focused source execution passes. |
| 141. Mpande relinquishes his claim | Test peaceful retirement and both choices at contested retirement. When the new ruler takes over, Mpande survives but loses claimant status and the claimant card's bonus. He does not reappear as a candidate after recalculation. His sons and their pledges survive; later normal mortality remains possible. | Pending DP. |

Dunn's historical escape is **not** newly modelled: the existing defeated-coalition rule still applies if he backs the losing prince. This is a future design question, not an exception silently introduced by the event.

## 29 October: family backing and population return

The clarified `.007` rule supersedes case 139's top-up wording for that branch only: a rival Cetshwayo receives **two additional** unpledged houses. `.006` and Mbuyazi's one-house floor are unchanged. Use checkpoints before the relevant events or adulthood pulse; already consumed events are not replayed.

| Scenario | Required observation | Status |
|---|---|---|
| 142. Restore population after reunion | Record Zulu-owned Natal/Zululand shares before a two-region civil war. Test both winners and inspect victory day plus two days. Restore the recorded ratio among survivors, preserve losses and independent NAL territory, and inspect employment/food/manpower. Repeat a Zululand-only split: no scripted return. Detailed cases are in the population-return brief. | Pending DP. |
| 143. Cetshwayo's two new houses | Enter `.007` with Mbuyazi recognised and Cetshwayo holding zero, one or several backers. The two highest combined-Prominence unpledged houses join his future coalition on acknowledgement. No extra grant when Cetshwayo is the recognised heir. Check empty pools, stale targets, distinct named tooltips and the new option text. | Pending DP. |
| 144. Sons support the reigning father | At adulthood under King Mpande, both sons show Supports the Incumbent plus Claimant (+25 Prominence). Cetshwayo gains Charismatic. Their own houses support Mpande now; their future coalitions remain distinct. Let annual recruitment and a court dispute run: neither becomes an opposition patron against Mpande. Repeat with Mpande outside the throne and through accession/retirement. | Pending DP. |
| 145. Recognised child's adult backing | Recognise a minor, alter the king's supporters during childhood, then advance through 16. One reconciliation brings eligible future backing towards half the current royal-supporting Prominence without taking rival promises. Later pulses do not refill it. Repeat with a dead/replaced heir, exile and a birthday during civil war; the surviving court handles any valid deferred receipt once. | Pending DP. |
| 146. Names and Hamu | New campaign: royal patronymics match their fathers; generated names use the revised clan pool. Confirm no specific royal patronymics in newly generated surnames. Advance beyond 1865 to check the existing Hamu kaNzibe introduction and distinguish him from generated namesakes. | Pending DP. |

## 29 October: slower claimant mobilisation

The five-point weekly rate supersedes earlier 25-point observations and expectations. Retirement eligibility moves to 1 August 1856 and Dunn's visit to 1 July; cases 17, 105, 121 and 140 use the revised dates. Existing activism, consumed choices and active wars are not reset.

| Scenario | Required observation | Status |
|---|---|---|
| 147. Recruitment window and second-war timing | Restart from before July 1856. Acknowledge Dunn's eligible visit, then the first eligible retirement choice on/after 1 August. Record weekly activism, actual popular/military/wealth support, organising-war creation and outbreak. From zero, expect about 15 weekly ticks to 75% and 20 to 100%; the existing exact-war progress effect can split before 100%. Compare both playable sides and several replays, recording original-owned versus rebel provinces, barracks and available battalions. Slower mobilisation must be assessed against actual recruitment, not assumed to yield a 50% split. Repeat with an unanswered Dunn/retirement popup, a secured succession, a dead/replaced ruler and an already active movement; no duplicate episode, fabricated war or activism reset. | Pending DP. Source rate/threshold, date-boundary, reservation and conflict lifecycle checks pass; native timing and allocation are unverified. |

Aim: roughly late November/December after early-August acknowledgement. Native sponsorship, monthly pulses and player delay prevent a guaranteed 1 December outbreak. This adjustment changes neither the +100% attraction modifier nor the frozen coalition calculation. **110 focused tests pass.** No game launch performed.

Full static run: 935 tests passed, eight historical skips and the existing localisation-baseline failure; no errors. Validator 14/16, with unit/localisation gates both reporting the pre-existing reviewed prose drift and dangling review-queue entry. Compatibility, map/naval and script lifecycle checks pass. Native timing and military balance remain pending.

## 29 October: Firearms duration and completion presentation

| Scenario | Required observation | Status |
|---|---|---|
| 148. Firearms completion and payoff | From an unseeded counter, confirm no completion at 259 supplied weeks and completion at 260; shortages pause progress. Percentage seeds/event grants remain proportional. Hover completion: readable 260-week condition, no variable diagnostics. Hover Effects: weapons penalties removed, +10% military research for five years and conditional Innovative; no dynasty stability or Prerogative grant. Neither hover nor opening `.001` applies its rewards; acknowledging applies them once. Repeat rebel/archive inheritance. | Source checks pass; UI rendering and native delivery pending DP. |

73 focused tests passed; independent review found no blocker. Full validator: 947 tests, 938 passed, eight historical skips and one existing localisation-review failure. Both failing validator gates report that same pre-existing issue (14/16 pass/warn/skip). No game launch. Stored raw weeks in older saves are unchanged; no percentage migration.

## Later-court scenarios — 30 October 2026

The new [numbered Dunn/Hamu matrix](zulu_later_court_implementation_2026_10_30.md#dp-engine-matrix)
adds the later narrative and territorial contract. Every new engine scenario is
pending; existing DP results elsewhere in this matrix are unchanged.

## 30 October: court thresholds and separate JE sections

| Scenario | Check | Status |
|---|---|---|
| 149. Threshold boundaries and retirement replay | At death/retirement, a valid rival just below 30% of succession pledges does not contest; at 30% they do. Repeat while a peaceful handover popup is open. The retained 1 August 1856 setup still qualifies Cetshwayo at 185/596 = 31.04%. Living challenges remain current 25% plus P ≤−50: compare 24.999%/25% and −49.99/−50, preserving existing cooldowns, court reservations and Mpande-son protections. Zero pledges qualify nobody; adding unpledged prominence changes neither share. | Source checks pass; engine replay pending DP. |
| 150. Marker, independent sections and viewed court | Three sections start closed and toggle independently. Their bounded content never widens the JE; current and succession summaries remain visible while closed and use their separate supporters/totals. Inspect both ZUL and a foreign court view. The fixed gold divider is at −50 (one quarter across); the moving current-P marker still tracks the value, including crossing/overlapping the divider. Effects and threshold hover remain accessible. Loyal princes display their actual allegiance. Under Federated Chiefdoms, no dynastic divider appears and both royal-rule summaries become inapplicability explanations without deleting political records. Check long names, scrolling and character navigation with all three panels open. | Source contracts pass; native rendering pending DP. |

Static handoff for 149–150: 174 focused checks pass; full discovery has 979 passes, one unchanged localisation failure and eight skips. CMF, overrides and map/naval checks pass. Independent source review has no blocking findings. Advisory Tiger totals match the prior baseline. None of these results marks native rendering or retirement replay as performed.

## 30 October: one-state recruitment trial — automatic entry follow-up

See [setup and tuning](zulu_one_state_coalition_split_proposal_2026_10_30.md#implemented-trial-and-how-to-run-it).
Restart from before movement creation, then choose a side in `.004` normally.
No console command is required in this follow-up. Confirm the immediate
`SB recruitment trial started:` log and **Mustering the Coalition** modifier.
The September onward autosaves already contain the old movement and cannot
exercise initialisation. No migration or retroactive movement replacement.

The 22:23–22:24 replay again produced one province and one staffed rebel battalion,
but none of its saves/logs shows trial activation. Record it as **old path observed,
recruitment not exercised**, not failed convergence. [Evidence](compatibility/zulu_second_succession_replay_2026_10_30.md).

| Scenario | Check | Status |
|---|---|---|
| 151. Native support convergence | Test frozen rebel shares of 25%, 50% and 75%, both player choices, and living-ruler/retirement cases. Keep weekly total, popular, military and wealth support from `SB recruitment trial` debug lines. Confirm five-point activism, a bounded changing attraction modifier and a split within the test window. The saved 248:185 case should recruit towards Mbuyazi's 57.275% when Cetshwayo is backed. | **Failed, 31 October, 57.275% case:** active controller reaches factor 32 but support stays about 10–11%; saved failure at 26 samples, no organising war. Native annual membership cadence explains the bottleneck. Other cases remain pending; [next-trial recommendation](compatibility/zulu_recruitment_stall_2026_10_31.md). |
| 152. Native territory and usable forces | Record provinces, staffed battalions, manpower, conscripts, commanders and food supply immediately after division. Repeat matched checkpoints: stronger coalition backing must give a meaningful military advantage, not just more provinces. No army rebuilding occurs in this path. | Pending DP. |
| 153. Trial boundaries and cleanup | Call `.990` without an eligible pending choice, after movement creation and in multi-state ZUL; it must not arm a later war or retrofit the old one. Test participant death, cancellation, actual winners, support loss before division and state-count changes. A failed 26-sample trial logs failure and stops scripted polling without awarding an outcome; reload its checkpoint. Existing movements and multi-state muster remain unchanged. | Pending DP. |
| 154. Normal side-choice activation | Without `.990`, answer either `.004` side choice from before movement creation. Confirm one immediate start log with the correct actual rebel and frozen target, the attraction-only modifier, then weekly support samples. Repeat/opening previews must not create another movement, restart the sample count or change the quoted side. | **Activation observed, 31 October:** claimant-backed replay has correct saved rebel4481/target, modifier and weekly samples. Start log's character name is blank, although saved reference is valid. Other choice/repeated-preview engine checks remain pending. |

Initial source handoff for 151–153: 104 focused checks pass; independent review reports
144 passing checks and no remaining blocking finding. Full discovery has 992
passes, eight existing skips and the unchanged localisation-review failure
(1,001 total). Validator 15/17: unit/localisation gates share that existing issue;
CMF, compatibility, map/naval and script-contract checks pass. Advisory Tiger
matches the previous baseline. Qualified scripted advancement is not proof of
native rebel creation; convergence and usable-force allocation remain unverified.

Evening follow-up for 151–154: **105** focused checks pass; independent review ran
**145** related checks with no blocking finding. Full discovery: **993 passed,
eight existing skips, one unchanged localisation failure** out of 1,002 tests.
Validator remains 15/17, with the same unit/localisation issue and unchanged
advisory Tiger totals. [Evidence and full validation record](compatibility/zulu_second_succession_replay_2026_10_30.md).

## 31 October: bounded country membership refresh

The first active replay in case 151 remains recorded as failed. This follow-up
requires a restart from **before the side choice**, not the failed April episode.

| Scenario | Check | Status |
|---|---|---|
| 155. Native refresh timing, scope and side effects | Replay both choices and the 25%/50%/75% shares, including the saved 57.275% target. Keep the weekly support samples and new `SB recruitment refresh:` lines. Each eligible sample 1–25 refreshes membership using the previous week's attraction; sample 26 permits success before expiry but no further refresh. Compare Pop membership, combined/military/wealth/popular support, other movement membership and IG clout before/after. Confirm a meaningful staffed military split, not only territory. Measure tick cost while recruitment is pending. Readiness, cancellation, participant death, state-count change, advancement and active war stop refreshes; multi-state and unrelated-country controls receive none. Repeat the failed April checkpoint to confirm it is not silently rearmed. | Pending DP. Source tests verify ordering, country scope and the 25-refresh bound; they record the native effect request without simulating recruitment or allocation. |

Source handoff: 109 focused and 149 independent review checks pass. Full discovery:
997 passes, eight existing historical skips, one unchanged localisation failure;
validator 15/17. Compatibility/CMF/map/naval checks pass. Advisory Tiger retains
1,076 existing errors; no diagnostic names the recruitment files.
[Detailed validation record](compatibility/zulu_recruitment_stall_2026_10_31.md#authorised-follow-up-bounded-refresh-implemented).

## 31 October evening: observed split and Dunn/succession follow-up

**Case 155 partial result:** the subsequent replay reached 57.781% combined
support against the saved 57.275% target on sample 20. April–August saves show
five provinces for the actual rebels and four for the original country. This
supersedes the earlier stalled replay as the latest observation, while retaining
its evidence. The other shares/choices, force staffing, repeatability and tick
cost remain pending. DP reports that this war works much better; food losses
remain a problem. [Hashes, log and current changes](zulu_dunn_succession_followup_2026_10_31.md).

| Scenario | Check | Status |
|---|---|---|
| 156. Dunn after One Royal Homestead | Replay Cetshwayo's victory over Mbuyazi with admitted Dunn. Leave `.005` open: no `.003` yet. Acknowledge it: paired judgement appears three days later once. Check Industrialists, long names, conditional Mthonga prose, and each tooltip. | Pending DP. |
| 157. Dunn's three judgements | Execute: +10 ruler Popularity for five years, −10 GBR, no more deliveries. Retain: support/+5 GBR, eligible two-week annual deliveries, Mthonga introduced with Claimant and no free backer; no automatic 1857 declaration elsewhere. Banish: living trader leaves and deliveries cease without relations change. Repeat/stale answers cannot duplicate rewards or recreate unavailable characters. | Pending DP. |
| 158. New reign and July lead-in | Peaceful/death/minority succession starts P at 0. Both contested retirement candidates start at 0; same-sovereign majority/reinstallation preserves earned P. Living incumbent keeps his value; `.005` adds 10 once. Replay from before July 1856 and record choice, movement and war dates; aim for December without bypassing readiness or forcing a dated war. | Pending DP. |
| 159. Shared partial provisions | In native one-state and scripted multi-state wars, both actual countries receive one +75% Food Security modifier regardless of player/AI. No 150% modifier remains. Compare food security, shortages and population losses over the war; residual famine is possible. Exact end, either winner and missing-war recovery remove relief from both sides, leaving unrelated wars/countries unchanged. | Pending DP. |

All four are new engine checks. Static interpretation does not reproduce native
recruitment, starvation, rendering or calendar scheduling. No game was launched.

Source acceptance: 160 focused tests pass, independently reproduced. Full
discovery has 1,005 passes, eight historical skips and the same existing
localisation-review failure (1,014 tests). Validator 15/17; CMF, compatibility,
map/naval and delayed-event contracts pass. Tiger remains advisory with 1,076
errors and 148 warnings; the warning change concerns untouched scope-deduction
paths. [Full acceptance details](zulu_dunn_succession_followup_2026_10_31.md#acceptance).

## 31 October: Dunn's annual faction allocation

The [authorised combined shipment](zulu_dunn_shipments_design_2026_10_30.md)
supersedes the single-option delivery in earlier cases. No game was launched.

| Scenario | Check | Status |
|---|---|---|
| 160. National or faction guns | Open `.002` with a faithful house and genuine rival camp. Opening gives nothing. A grants two Firearms weeks; B gives the named ally +10 and named opponent −10 Prominence for five years, zero Firearms progress, and one 1% death roll against that opponent's prince. Check full names, portraits, probability, wrapping and native modifier icons. | Pending DP; source-executed choices and probability boundaries pass. |
| 161. Stale and protected targets | Keep the popup open while an actor dies, defects, moves country, loses representation, the ruler changes, or a court conflict is reserved. B becomes unavailable without choosing replacements; A remains where delivery itself is valid. Future-only pledges, loyal princes and Mpande's protected sons cannot become enemy targets. Completion/Dunn's departure cancels delivery. | Pending DP; scripted invalidation and negative controls pass. |
| 162. Repetition, caps and death | Repeat delivery annually: fresh eligible houses are preferred, otherwise five years refresh without stacking; cap-100 allies only qualify for renewal. One house member's modifier contributes once to house weight. Repeat-click cannot award another pair/roll or two weeks. Inspect an actual lethal result: only the named prince dies, his supporters survive and lose their obsolete commitments; no automatic loyalty, annexation or constitutional reward. Verify modifiers expire after five years and receipt/scopes survive save/load. | Pending DP; receipt, refresh, capped values and explicit source death-callback checks pass. |

Acceptance: **96 focused passes** independently repeated; full discovery
**1,017 passes / eight historical skips / one existing localisation-review
failure** (1,026 tests). Validator 15/17; its two failing gates report the same
unrelated review drift. Tiger remains advisory. [Details and output](zulu_dunn_shipments_design_2026_10_30.md#implementation-verification).

## 1 November: Hamu's promise and the Thirteen Chiefdoms split

| Scenario | Check | Status |
|---|---|---|
| 163. Signed Hamu promise across constitutional war | From a checkpoint before the split with an existing signed Hamu contract, divide the promised coast between the authentic uSuthu/amaKhosi factions. The monthly check retains the promise without earning it. Test Hamu winning as the original country and as the rebels: the real victory retains the defeated owner through cleanup, waits for all five provinces to reunify, then creates the sponsor's NRP Confederal Partner once. Repeat callbacks/monthly checks; no second reward. Any promised province genuinely lost to a third country must still cancel the contract. A temporary faction installation or another king's victory earns nothing. Repeat the existing dynastic route as a control. | Pending DP. Source-executed split, receipt, foreign-owner and delayed-reunion regressions pass; native callback order has not been replayed. |
| 164. First Chiefly Council after the British handoff | Start before Britain's annexation play with a living Zibhebhu. Record his character ID. Check that a surviving ZUL recovers him and that a recreated ZUL appoints that same chief on late partition. At a late partition where Vanilla never introduced him, expect one canonical Mandlakazi chief. Test an early Klip partition and a known dead chief as controls. Hover the government choices, chiefdoms interventions and incidents as NAL and TRN. Each consequence should have its own bullet and each unmet condition should explain how to satisfy it. | DP observed Mehlokazulu Nyawo in the original May–September 1881 saves. Replay with the correction pending. |
| 165. Return the actual royal claimant | Before British annexation enforcement, record the living ruler and heir IDs. Verify their preservation through recreation, partition and CAP exile. Permit the claimant's return: the same person appears in ZUL as uSuthu's agitator, without coronation or duplicate rewards. Repeat early Klip partition, reversal before NAL exists, wartime succession and a genuinely deceased claimant. A later reserved dynastic crisis must retain its own movement priority. | Pending DP. The old May–September 1881 saves instead show generated Msushwana Mpungose as a Pro-Slavery agitator. Source-executed handoff and priority checks pass; [investigation](compatibility/zulu_claimant_return_2026_11_05.md). |
