# Cape starting politics review — 28 October 2026

Recommendation: retain the unelected Oligarchy opening. Do not copy Portugal's electoral amendment into the 1836 Cape merely to help reform. The stronger imperial establishment is a concrete reason reform can be harder than in the earlier Cape setup. If a fresh-start comparison confirms insufficient liberal movement support, test one small movement-specific attraction bonus first. Treat a named agitator as an alternative requiring a deliberate character-role decision.

This is a review and proposal only. No gameplay, localisation, tests, dependencies or shared tracking documents were changed. Installed Vanilla 1.14.5, local CMF and the two gold-star example mods were consulted. The supplied January 1849 save is evidence about that campaign, not a substitute for an untouched 1836 CAP start.

## Actual opening

The country history calls `effect_starting_politics_conservative`, whose installed definition activates **Oligarchy**, then applies the Cape's replacements. There is no later Cape distribution-of-power replacement in that history. It does **not** start with Autocracy, Landed Voting, Wealth Voting or Census Voting.

| Component | Current starting source | Mechanical implication |
| --- | --- | --- |
| Governance | Colonial Administration, a Monarchy variant | +100% bureaucrat and officer political strength; +10 legitimacy from head of state; +20% ideological-incoherence penalty. |
| Distribution of power | Oligarchy | +50% officer and aristocrat strength, +25% capitalist strength, +120 legitimacy from government clout, +10 from head of state, +2 government size, −10% incoherence penalty. No voting-power modifier. CMF retains these numeric modifiers. |
| Bureaucracy | Imperial Administration, a Hereditary Bureaucrats variant | −25% population bureaucracy cost; +10% aristocrat strength; +50 aristocrat attraction weight towards the Armed Forces; −10 percentage points Liberty Desire. The parent supplies ideological classification; do not add the parent's numerical modifiers again. |
| Citizenship | Subjecthood + Racialized Subjecthood | The amendment changes acceptance by heritage (+40 shared trait, +30 shared group, −5 no shared heritage). It supplies no electoral franchise. |
| Other relevant laws | Homesteading, Professional Army, Agrarianism, Local Police, Freedom of Conscience, Public Schools level 1, Censorship, Migration Controls, No Colonial Affairs | Homesteading adds +25% farmer strength; Professional Army adds another +50% officer strength. No Colonial Affairs initially offsets some settler drift in the journal. |
| Authored government | Armed Forces, Landowners, Devout | The principal reform-friendly member is John Philip's Devout. Intelligentsia and Petty Bourgeoisie begin outside the authored cabinet. Actual engine startup membership/legitimacy still needs inspection. |

The three officer-strength bonuses above total **+200%** before other modifiers; that is a modifier total, not an assertion that the Armed Forces starts with a particular clout. Pop wealth, employment, acceptance, IG attraction and other modifiers still determine clout.

Starting personalities are D'Urban (Armed Forces, Moderate, ruler and leader), Stockenström (Landowners, Moderate), Philipps (Rural Folk, Ethno-Nationalist), Fairbairn (Intelligentsia, Reformer), John Philip (Devout, Humanitarian) and Montagu (Petty Bourgeoisie, Market Liberal). **Godlonton is an agitator**, aligned with Rural Folk, Ethno-Nationalist, and given +25 Popularity by `sb_godlonton_editor`. Fairbairn and Philip are IG leaders, not authored agitators.

Source locations: `common/history/countries/cap - cape colony.txt:7`, `common/history/characters/cap - cape colony.txt:3`, `common/character_templates/sb_southern_africa_character_template_overrides.txt:479`, `common/character_templates/sb_cape_and_colonial_characters.txt:3`, `common/laws/04_sb_imperial_administration.txt:1`; installed Vanilla `common/scripted_effects/00_political_setup.txt:20`, `common/laws/00_distribution_of_power.txt:344`, `common/laws/00_governance_principles.txt:290`, `common/laws/01_land_reform.txt:531`, `common/laws/00_army_model.txt:112`; CMF `common/laws/com_distribution_of_power.txt:121`.

### Which reforms actually have starting allies?

These are **source-level base-law comparisons**, before the current law's amendment, negotiations, approval state and cabinet determine the final enactment calculation. `++ / + / 0 / − / −−` mean strongly approve / approve / neutral / disapprove / strongly disapprove. An unlisted stance is marked separately rather than assumed to be an explicit position.

| Actor | Subjecthood → Cultural Exclusion | Oligarchy → Wealth / Census Voting | Imperial Administration → Appointed / Elected Bureaucrats |
| --- | --- | --- | --- |
| Armed Forces, Moderate D'Urban | Anglo-Imperialism: ++ → − | + → − / − | ++ → − / −− |
| Landowners, Moderate Stockenström | Hierarchic: + → 0 | Paternalistic: + → 0 / − | Paternalistic: + → 0 / − |
| Intelligentsia, Reformer Fairbairn | Leader: − → +; core Cape liberal: −− → + | Republican: − → + / ++ | Anti-Clerical: − → + / 0 |
| Devout, Humanitarian John Philip | Leader: − → 0 | No authored distribution-of-power stance in his package | No authored bureaucracy stance in his package |
| Petty Bourgeoisie, Market Liberal Montagu | Burgher Civic: unlisted → + | Meritocratic: − → 0 / + | Meritocratic: − → 0 / + |
| Rural Folk, Ethno-Nationalist Philipps | Leader: **−− → −**; settler core: 0 → − | Settler-Colonialist: **−− → 0 / ++** | No authored bureaucracy stance in the package |
| Cape Liberal Movement | 0 → + | −− → ++ / ++ | −− → 0 / ++ |
| ECSL | unlisted → − | unlisted → + / 0 | + → 0 / − |

Two consequences matter. First, Philip supplies a relative improvement on citizenship despite being neutral about Cultural Exclusion itself; he need not display a green approval stance on the target to favour replacing Subjecthood. Secondly, **Rural Folk are not uniformly anti-reform**: their starting leader prefers Cultural Exclusion to unamended Subjecthood despite disapproving of both, and their core ideology favours Census Voting strongly. The Racialized Subjecthood amendment uses Racial Segregation as its proxy, which Philipps approves, so his final citizenship comparison must be read from the actual law screen. After a Traditionalist replaces him, as in the 1849 save, the starting comparison no longer applies. A voting-first coalition may be broader than the racial-policy coalition; test it before assuming an elective amendment is needed.

The installed laws do not contain a CAP-specific prohibition on Cultural Exclusion, Wealth/Census Voting or Appointed Bureaucrats. The special distribution-of-power permission gate is for **BIC**, not all British subjects. CAP's tier-2 technology setup includes era 1 and therefore Democracy. Its Slavery Banned law also satisfies Cultural Exclusion's listed slavery-law prerequisite.

The plausible colonial obstruction is **cabinet arithmetic**, not an automatic governor veto. D'Urban is Moderate, with no ideological reform veto in his authored template. Keeping his powerful Armed Forces in government retains clout/head-of-state legitimacy while importing opposition to the reforms; excluding it can reduce legitimacy, and adding conflicting groups can incur incoherence. At legitimacy below 25, the installed level requires a movement to enact laws; at 25–49 it applies −25% enactment speed. The actual starting cabinet's resulting legitimacy is not saved in the history source and remains a runtime check. An attraction bonus can strengthen the required movement and supporting-law contribution, but cannot itself repair an incoherent cabinet.

Additional sources: installed Vanilla `common/ideologies/00_ig_ideologies.txt`, `common/ideologies/01_character_ideologies.txt:1692`, `common/ideologies/01_character_ideologies.txt:5538`, `common/ideologies/01_character_ideologies.txt:7288`, `common/legitimacy_levels/00_legitimacy_levels.txt`, `common/scripted_effects/00_starting_inventions.txt:29`, `common/technology/technologies/30_society.txt:100`. Later Landowner identity can differ; the 1849 save has Republican Paternalistic and is not used to substitute for the authored 1836 comparison.

## What Portugal's amendment actually does

Portugal starts with Oligarchy and Elected Bureaucrats, sets an election date of 17 July 1836, and adds `amendment_chamber_of_gentleman_deputies` to distribution of power. Its historical setup comment describes indirect, manipulated elections. The amendment's `parent = law_landed_voting` is its ideological proxy; its allowed base law is Oligarchy.

Its actual modifiers are:

- +40 legitimacy from government votes;
- +50 aristocrat voting power;
- +25 voting power each for officers, clergymen, bureaucrats and shopkeepers;
- −40% electoral-confidence impact.

It also has `amendment_activism_multiplier = 0.5`, a Portuguese-primary-culture availability condition, no AI revocation, and the ordinary legitimacy repeal gate. Portugal's historical sponsor is Petty Bourgeoisie with a 24-month cooldown, although ordinary sponsor eligibility names Landowners, Industrialists or a Cartist IG.

This **does create a franchise**: installed `country_has_voting_franchise` explicitly checks those occupation voting-power modifiers. It leaves the underlying Oligarchy strength bonuses in place. It has **no** `country_law_enactment_success_add`, universal liberal clout bonus or automatic passage effect. A Cape copy would therefore change elections, voting strength, legitimacy and politics beyond the reform being diagnosed, and would enfranchise officers and aristocrats as well as civilian groups.

Sources: installed Vanilla `common/history/countries/por - portugal.txt:2`, `common/amendments/00_amendments_historical_04.txt:201`, `common/scripted_triggers/00_scripted_triggers.txt:16`.

The Cape had a nominated council in the 1830s. Derby's 1851 account specifically describes the unofficial members as the governor's nominees and dates that arrangement to 1834; it is a contemporary political speech, so its evaluative language should not be adopted as neutral history. UCT's official-publications chronology separates the Legislative Council of 1834–1853 from the Cape Parliament beginning in 1854. Those sources support an unelected opening and a later representative reform, not Portugal's existing electoral system in 1836. [Hansard, 15 July 1851](https://api.parliament.uk/historic-hansard/lords/1851/jul/15/the-cape-of-good-hope-representative), [UCT government-publications guide](https://libguides.lib.uct.ac.za/GovtPubs/CapeColony).

The eventual low property qualification is documented directly in Newcastle's 1853 statement: the franchise threshold was reduced from £50 to £25 for houses or land. This supports a later property-based franchise; it does not establish that the game's literacy-weighted Census Voting is an exact historical equivalent. [Hansard, 16 June 1853](https://api.parliament.uk/historic-hansard/lords/1853/jun/16/cape-of-good-hope-constitution-for-the).

## Confirmed bottlenecks and limits

**1. The imperial package made reform more contentious.** Commit `74a938e` (16 August) replaced Racial Segregation with Subjecthood plus its amendment, replaced Appointed Bureaucrats with Imperial Administration, added Agrarianism, and introduced the imperial ideology package. Current Armed Forces identity removes Jingoist and adds Anglo-Imperialism alongside Colonialist, Patriotic and Loyalist. Anglo-Imperialism strongly approves Subjecthood and hereditary bureaucracy, disapproves Cultural Exclusion and elected bureaucracy, approves Oligarchy, and disapproves Wealth/Census Voting. This turns an economically strengthened establishment into an explicit obstacle across several reform groups. The earlier/current source difference is proved; the size of its effect on fresh-start enactment chances is not.

The current uncommitted Cape-event change only protects the Albany ruler during its subject handoff. The new global movement-history override adds an institutional exclusion to generic royalists; the enthusiasm override preserves Vanilla's +100% attraction, decaying over twenty years. Neither is evidence of a newly introduced Cape recruitment penalty. No causal claim about the latest Zulu edits is warranted from this review.

**2. The liberal movement recruits a less favoured constituency.** `movement_sb_cape_liberal` admits all non-slave pops, but applies `(literacy + 0.10)` to its attraction. It has base weight 6; bonuses include capitalists 45, academics 38, shopkeepers 22, bureaucrats/clergy 18, clerks 12 and peasants 0. Discrimination adds `(100 − acceptance) / 5`; full acceptance applies ×0.95. This is attractive to educated professionals but does not translate the large disadvantaged population into equally large political support.

For contrast, an accepted eastern farmer, at zero urbanisation, 20% literacy and no radicals, has a scripted liberal weight of `(6 + 14) × 0.95 × 0.30 = 5.7`. The settler weight is `(11 + 26) × 2 × 1.5 = 111`, before common/native modifiers and competition. This is a recruitment-weight illustration, **not** a support, vote or clout prediction. National movement support also combines popular support (34%), military support (33%) and wealth support (33%); popular appeal alone is insufficient.

**3. Pressure and support are different levers.** Cape Liberals can influence only Intelligentsia, Petty Bourgeoisie and Devout. This excludes Industrialists despite the high capitalist recruitment weight, and excludes the Armed Forces/Landowners/Rural Folk opposition. The filter limits IG influence/negotiation effects; it does not mean movement supporters in other IGs disappear or that direct movement support cannot affect enactment. Native influence requires 10% internal backing within an IG and has three slots. A movement's national support is not that internal percentage. Raising attraction also does not instantly replace an existing IG leader.

**4. The liberal constituency has no authored agitator.** ECSL receives Godlonton; the liberal side's prominent named figures occupy IG leadership roles. Montagu's Market Liberal ideology also fails the Cape Liberal character trigger, which accepts Liberal, Reformer or Humanitarian. This is an asymmetric package, not proof that every campaign needs another agitator. A character's eventual movement assignment must be checked in the engine.

**5. Activation and the reform objective need separating.** The normal liberal creation trigger still requires Racial Segregation, although the start now uses Subjecthood. Country movement history explicitly creates the movement, and the supplied save proves it existed in that campaign from 1836. The stale condition is therefore a **recreation/eligibility mismatch**, not demonstrated failure of starting creation. If the movement disappears below native maintenance support, it cannot normally regenerate under unchanged Subjecthood. `creation_weight = 180` affects selection priority, not the support or pressure of an existing movement.

**6. The journal does not itself pass citizenship reform.** Ordinary liberal completion needs balance ≥90 **and Cultural Exclusion already enacted**. The full Cape Qualified Franchise amendment grants +10 acceptance for no shared heritage; it grants no votes, strength or enactment bonus. Thus Cultural Exclusion + this amendment can coexist with Oligarchy. Citizenship acceptance, an electoral franchise and responsible government are separate systems here.

The liberal petition is triggered when the balance is **≤−60**, i.e. a complaint against settler dominance. It creates a promise/petition; only the AI branch directly starts Cultural Exclusion. Its +15 percentage-point enactment bonus is only the fallback when both petition slots are occupied, not a universal reward for choosing the petition. The favour-liberals button gives only +10% Intelligentsia strength and +0.1 monthly balance drift for five years. It is not +10 percentage points of clout, nor a movement bonus. The Albany crisis separately activates Cultural Exclusion directly; that exceptional route does not demonstrate ease of ordinary enactment.

**7. Do not solve this by indiscriminately raising activism.** Native movements below 25% activism do not affect law enactment chances, but the defines also specify a 25% floor while a relevant law is being enacted. The franchise event's −20 percentage-point activism modifier therefore cannot simply be assumed to remove the supporting movement's enactment contribution. A liberal rising is explicitly a settler outcome in the Cape journal, so a large activism boost can sabotage the intended liberal playthrough.

Sources: `common/political_movements/sb_political_movements.txt:585`, `common/history/political_movements/sb_movements.txt:17`, `common/scripted_effects/sb_interest_group_identity_effects.txt:27`, `common/ideologies/sb_ideologies.txt:96`, `common/ideologies/sb_ideologies.txt:331`, `common/on_actions/sb_cape_on_action_handlers.txt:598`, `events/sb_cape_events.txt:359`, `events/sb_cape_events.txt:664`, `common/amendments/sb_amendments.txt:4`, `common/scripted_buttons/sb_cape_buttons.txt:32`, `common/journal_entries/1-01_sb_cape_politics.txt:138`; installed Vanilla `common/defines/00_defines.txt:79` and `common/script_values/negotiation_values.txt:203`.

## What the supplied save establishes

Read-only inspection of `/private/tmp/sb-zulu-heirs-court-2026-10-28/autosave.v3` (1 January 1849), CAP country object 732:

- Oligarchy, Colonial Administration, Subjecthood and Imperial Administration remain active, with 1836 activation dates.
- Cultural Exclusion has been in enactment since **23 October 1848**. Its franchise-satisfaction modifier is present on the liberal movement. This proves the ordinary enactment path and amendment event were reached, not that passage is likely or completed.
- The Cape Liberal Movement has existed since 1 January 1836, has saved activism **0.25**, and no attached character. ECSL has Godlonton attached and activism **0.2875**.
- Clout is Rural Folk 32.125%, Armed Forces 15.911%, Landowners 15.495%, Petty Bourgeoisie 13.019%, Devout 8.824%, Intelligentsia 7.839%, Trade Unions 5.067%, Industrialists 1.716%.
- Government consists of Rural Folk and Devout. The current Devout leader is Traditionalist; the historical Humanitarian Philip is no longer its leader. Intelligentsia and Petty Bourgeoisie are outside government. The balance is −62.6, and the liberal-complaint flag has been set.

This shows a difficult later political configuration and confirms several pathways remain alive. It does not establish the starting clout, 1836 law screen, movement support breakdown, player choices, effect of the current complete load order, or a regression between clean starts. Do not infer 1836 chances from these 1849 figures.

## Ranked minimal proposals

1. **Preferred balance trial: a temporary Cape Liberal attraction bonus.** Before: the movement gets only ordinary twenty-year initial enthusiasm plus shared Cape tensions; there is no bespoke opening recruitment support. After: add **+0.25 `political_movement_pop_attraction_mult`**, movement-scoped, decaying over ten years, only for the unresolved Cape contest. Apply it to the **existing** Cape Liberal Movement; do not create another liberal movement. Keep activism, all laws, IG eligibility, Godlonton and the existing leaders unchanged. This is a calibration starting point, not a claimed final balance. With initial enthusiasm alone, +0.25 changes a ×2.00 attraction factor to ×2.25—12.5% more relative attraction, not 25% extra national support. More recruitment can increase the existing movement's direct enactment contribution and internal backing in its three eligible IGs; it cannot pressure the deliberately excluded establishment or guarantee an immediate leader change. The effect with other modifiers must be measured. Hail Columbia's movement modifiers distinguish modest +10–20% attraction from activism; Gates of the Bosphorus uses a +25% agricultural-reform movement attraction modifier. These are useful scoped patterns, not balance evidence for CAP.

2. **Small eligibility repair, independently of balance:** allow the bespoke movement's normal creation under Subjecthood as well as Racial Segregation, while the Cape contest remains unresolved. Before: a lost movement cannot normally recreate under its actual opening citizenship law. After: eligibility matches the authored opening, without creating duplicates or prolonging it after resolution. This fixes a real source mismatch but should not be advertised as the cause of the observed difficulty, because the supplied save retains the original movement.

3. **Agitator alternative if a visible character is preferred:** Fairbairn is the natural existing newspaper figure, but moving him from IG leader to agitator removes the guaranteed Reformer from the Intelligentsia. John Philip has the analogous problem in the starting cabinet. Do not silently add a dual role or duplicate either person; no valid dual-role template was identified in the checked Vanilla/gold-star examples. A Fairbairn conversion therefore needs an intentional replacement Intelligentsia leader and an assignment test, and is a larger change than proposal 1. He must attach to the **existing** bespoke movement: an unrelated Liberal/Modernizer movement would split the intended intervention. His current Reformer ideology qualifies for the bespoke trigger, but actual native selection among competing eligible movements needs verification. His documented press campaigns support the character choice; they do not justify a fully developed 1850s franchise platform in 1836. [Encyclopaedia Africana, John Fairbairn](https://encyclopaediaafricana.com/fairbairn-john/).

4. **Electoral amendment: reserve for a later constitutional design.** Before: nominated government, no electorate. After a Portugal-style amendment: occupation-based voting and electoral legitimacy while retaining oligarchic strength bonuses. That is a substantive constitutional reform, not a targeted opening balance adjustment. A later Cape property franchise should be designed against Wealth/Census Voting and the existing citizenship amendment explicitly. Do not add it at start on the present evidence.

There is also a separate historical-law question: Censorship is inherited unchanged despite the Cape's 1829 press ordinance. Right of Assembly may be a better abstraction, but that should be reviewed on its own merits; it alters authority, suppression/bolstering and war-support behaviour, and satisfying the liberal movement's speech preference can lower activism. It is not an automatic reform buff. [South African History Online, citing the HSRC history](https://sahistory.org.za/dated-event/freedom-press-established-cape).

## Checks needed before choosing a balance value

- After a full process restart, record an untouched CAP start: active laws/amendments, authored leaders and actual roles, government membership, legitimacy, clout, liberal/ECSL popular–military–wealth support and activism breakdowns. Check both day one and after recruitment settles, then after one year.
- Compare ordinary Cultural Exclusion, Wealth/Census Voting and Appointed Bureaucrats enactment screens with the same cabinet and game conditions. Record legal eligibility separately from success, advance, debate and stall chances. This establishes whether the bottleneck is recruitment, cabinet legitimacy, opposition clout or a specific law gate.
- For proposal 1, compare baseline against the one added modifier; confirm increased liberal support/IG pressure without accidental liberal revolt. Check expiry and journal completion cleanup. Do not simultaneously change an agitator, electoral law and activism, since that would conceal the effective intervention.
- For proposal 2, verify creation under Subjecthood and Racial Segregation, no duplicate at history startup, and no recreation after resolved flags/multiculturalism. For proposal 3, verify actual agitator attachment and retained reformist IG leadership.
- Exercise the petition when no law is being enacted, when another law is being enacted, and when both petition slots are occupied; then the 21-day franchise event. Inspect its displayed enactment effect before and after the −0.20 satisfaction modifier, respecting the native 0.25 floor.

Existing static checks run: `python3 -m unittest tests.test_cape_imperial_ideology tests.test_cape_franchise_weakening` — **12 tests passed**. These verify authored contracts, not the balance of a new campaign. No game launch or engine replay was performed.

## Eligibility repair implemented — 29 October 2026

DP approved proposal 2. Natural creation of the Cape Liberal Movement now accepts Subjecthood or Racial Segregation, requires the active `je_sb_cape_politics`, and excludes `sb_cape_liberal_resolved_var`. The journal requirement also prevents recreation after other endings or while an outcome notification awaits acknowledgement. History still creates the opening movement once. Existing movements, recruitment weights, attraction, activism, IG eligibility and starting laws are unchanged; the separate balance proposals remain unimplemented.

`tests.test_cape_liberal_creation`, `tests.test_cape_imperial_ideology` and `tests.test_cape_franchise_weakening`: **14 tests passed**. The new tests evaluate the source creation condition under both admitted laws, a closed or resolved contest, another country and other citizenship laws. DP verification of natural recreation and no startup duplicate remains **pending**; no game was launched.
