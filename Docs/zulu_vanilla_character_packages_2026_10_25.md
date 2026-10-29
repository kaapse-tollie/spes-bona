# Zulu character packages: Vanilla's apparent rationale and role effects

25 October 2026. **Analysis and design only; no gameplay changes.** This supplements the [first-principles historical assessment](zulu_starting_character_traits_research_2026_10_25.md), rather than treating its sparse recommendations as an approved replacement batch.

**Package locked, 25 October:** DP has accepted the [complete playtest baseline](zulu_character_package_proposal_2026_10_25.md), including the opening roster, controlled initial generation, reputation values/durations and Retief exchange. The alternatives and source findings below remain supporting evidence. Implementation is still pending; the [event package](zulu_court_event_package_2026_10_25.md) is a separate proposal for agreement.

**DP decision:** retain permanent campaign rewards, player choice of claimant-war side, coalition prominence influencing strength, and trial immediate defeat shocks as the design direction. **Defer the proposed explicit Kill Retief → lose Blood River → attack Swazi → lose trigger. Playtest ordinary political consequences and −10 Prerogative shocks first.** No unconditional historical-sequence war trigger is authorised. The native claimant-war path remains an unverified test prototype.

## What can be established

The installed Vanilla templates and trait definitions establish the packages and their current mechanical effects. They do **not** explain every historical selection. The historical and gameplay rationale below is an inference, except where a source comment supplies a reason. A targeted official-forum search did not locate a designer explanation of these Zulu packages. Current global trait effects also need not be identical to those in force when a template was first authored. Do not infer that Paradox chose each character to achieve every present-day numerical consequence.

The five explicit opening ZUL characters are Dingane, Mpande, Mkabayi, Ndlela and Zulu kaNogandaya. Cetshwayo and Zibhebhu have additional Vanilla templates but are not in that opening history. SB creates its own child Cetshwayo template using the same adult trait list. The same Vanilla template file also includes Mzilikazi, covered below as a useful ruler-and-general comparison. [1]

| Character | Vanilla package | SB distinction relevant to this review |
|---|---|---|
| Dingane | Hedonist, Imperious, Ruthless | Inherited package. SB separately adds the opening Usurper modifier; it is not a Vanilla personality trait. |
| Mpande | Compliant, Honourable, Tactful, Political Operator | SB adds **Reserved**, changes AF to LO and removes the opening heir designation. |
| Mkabayi | Ambitious, Tactful, Elder | Inherited package; LO leader. |
| Ndlela | Ambitious, Tactful, Elder | Inherited package; AF leader **and general**. |
| Zulu / Komfiya | Imposing, Brave, Popular Commander | Inherited general. |
| Cetshwayo | Ambitious, Imperious, Diplomat | Vanilla ruler template; SB reuses the list in its own child template. |
| Zibhebhu | Ambitious, Arrogant, Reckless, Pillager | Vanilla's later LO politician/leader opportunity, with usage beginning in 1877; not an opening commander. SB's partition route gives him a different context. |
| Gqugqu, Mbuyazi, Uthumbu | **No package for these identities in Vanilla's ZUL template/history** | Authored by SB; not evidence of Paradox's intended contrast between princes. |
| Dambuza, Mawa, Nongalaza, Sotobe | **No authored opening package in the inspected Vanilla ZUL sources** | SB's empty lists invoke native random generation. Random results are not historical package choices by Paradox. |

“Political Operator” and “Diplomat” are the displayed names of `basic_political_operator` and `basic_diplomat`. This brief uses British spelling for Honourable while preserving the source identifier `honorable` in references. [1], [2]

## Reading effects correctly

- **Universal character effects** apply regardless of office. Popularity and direct Prominence are separate values; the native prominence calculation also incorporates popularity at a coefficient of 0.25, other modifiers and a maximum of 100.
- **Ruler effects** apply to the country only while the character rules. Being an AF member does not make the king a general.
- **Command effects** apply in the documented command context, including fully mobilised combat units. They are not national army bonuses simply because the owner of the trait is sovereign. Actual multi-role characters can supply both ruler and command effects.
- **IG-leader effects** require leadership of that IG, not merely membership. A court adviser does not automatically provide these benefits.
- Native trait-generation can add experience/skills to eligible older characters. The tables describe authored packages, not guaranteed final save totals. Age traits, role modifiers, allegiance cards, SB house modifiers and later events are excluded unless expressly stated. [2]

All percentages below preserve the source distinction between relative modifiers and additive values. “Recovery −5 percentage points” is `unit_recovery_rate_add = -0.05`, not morale recovery. “Defence +5” is flat, not +5%. Battle-condition multipliers modify selection weights, not fixed probabilities.

## Why these packages are plausible choices

### Dingane: coercive royal power, personal unpopularity

The three traits construct a recognisable portrait of a pleasure-loving, domineering and coercive monarch. That is a plausible shorthand for older accounts of Dingane; it is not a secure account of either his full personality or public opinion in 1836.

**Hedonist:** Isaacs explicitly describes courtly pleasures, dancing and singing with women in his portrait of Dingane. This supplies a possible literary route to the selection. But the same pages describe a reserved, deliberate speaker, curiosity about outside knowledge and sensitivity to disrespect. Selecting only the sensual strand makes a partial portrait. Isaacs's moral and colonial assumptions matter. [3, pp. 280–282]

**Imperious:** sensitivity to disrespect and insistence on royal deference plausibly map to this trait. Vanilla's description is about domineering conduct, not simply holding an autocratic office. Its −35 Popularity is therefore a strong design interpretation, not an inevitable historical consequence of monarchy. **Ruthless** has a firmer basis in documented coercion: Gardiner describes a royal brother's execution in 1835, while distinguishing what he witnessed from reported motives. That supports a political interpretation without requiring the later Retief killings to have happened already. [3], [4, pp. 44–47]

The package is mechanically more interesting than three disadvantages: **−65 Popularity**, but **+15 direct Prominence**, cheaper decrees, more Authority and favourable movement-generated loyalist/radical modifiers. It depicts rule through control rather than affection. This is a reading of the effects, not a claim about a documented design brief. Okoye's reappraisal explicitly challenges the conventional hostile portrait; the extract was inspected, not the full article. [5]

**Assessment:** Ruthless is the strongest candidate to retain. Hedonist is the first I would reconsider. Imperious versus Reserved needs a deliberate choice about royal style and gameplay: neither should be selected solely to hit a popularity target. Removing Imperious also removes useful ruler effects, so it is not merely making Dingane 35 points more likeable.

### Mpande: an accommodating, credible alternative to Dingane

Compliant + Tactful suggests an accommodating survivor and negotiator; Honourable gives a favourable personal reputation; Political Operator prevents the package from representing complete political ineptitude. The resulting contrast with Dingane is substantial: **+25 versus −65 intrinsic Popularity**, but **−5% versus +5% Authority as ruler**. Mpande is easier to like and less forceful in central government.

This is a plausible reading of the familiar contrast between the two reigns. It risks turning strategic accommodation into inherent submissiveness. Shamase challenges the indolent/cowardly caricature and distinguishes Mpande's subordinate early position from his later political and military agency. That supports caution over Compliant; it does not independently prove Honourable. [6]

**SB's addition matters:** Reserved adds −25 Popularity, reducing Mpande's authored intrinsic total from +25 to **0**. It also adds −10% command morale loss and +0.05 health, if those contexts matter. Vanilla did not make that trade. The present Gqugqu comparison combines SB's Reserved addition, its removal of Mpande's heir role and its newly authored Gqugqu package. It should not be explained as Vanilla favouring Gqugqu.

**Assessment:** Tactful + Political Operator is a useful, restrained foundation to consider. Honourable and Compliant remain separate historical/gameplay judgements. Reconsider SB's Reserved addition before adding compensating prominence to Mpande.

### Mkabayi: an influential elder and political broker

Ambitious + Tactful + Elder looks like a general political-broker package: a substantial personal constituency, skill in handling people and recognised senior standing. The installed comment specifically notes that she remained politically active into the period. Oral-history scholarship describes her regency, royal authority and interventions in succession; these support political experience more directly than a claim about personal ambition. [1], [7]

The gameplay result is coherent for an LO leader: **+25 Popularity, +15 direct Prominence, +10% IG political strength**, attraction and approval effects. Elder is a **skill**, not an automatic age condition. The game's own description concerns recognised local experience and prestige, so retaining it is not just awarding influence for being old. [2]

**Assessment:** Elder and Tactful are defensible approximations. Replacing Ambitious with Experienced Political Operator is a meaningful alternative: it preserves the same intrinsic Popularity/direct-Prominence totals and +10% IG strength while representing accumulated practice instead of an inferred temperament. It changes other role effects and is still a proposal.

### Ndlela: the same political package, with substantial military consequences

Vanilla gives Ndlela exactly Mkabayi's package. That suggests a shared abstraction for influential senior political figures rather than two independently exhaustive psychological portraits. Gardiner's account places Ndlela in high-level deliberation and control of access to the king. That makes Tactful and political experience intelligible choices; his office alone does not prove Ambitious. [4]

Unlike Mkabayi, Ndlela begins as a general. The package supplies **+5 flat Defence, +5% Offence, +10% home-territory Offence and Defence, and −10% supply consumption**, alongside penalties to recovery and inflicted morale damage. Elder's territorial bonuses are particularly consequential for fighting in Zululand. The same list thus produces a court broker in one case and a capable, locally effective commander in the other.

**Assessment:** replacing the entire package with Political Operator would remove a large part of his military value. The earlier sparse proposal is an evidence filter, not a complete military-balance specification. A narrower alternative is to retain Tactful/Elder and review Ambitious separately. Do not silently remove the command bonuses while tuning Dingane's reputation.

### Zulu kaNogandaya / Komfiya: an established martial reputation

This is the clearest explicitly annotated military package. The source comment says he served with honours under Shaka in the 1820s and identifies his son. Imposing represents intimidating bearing, Brave personal courage, and Popular Commander an established reputation usable in command and politics. The earlier research connects the identity to Mkehlengana's recorded family testimony, while warning that the son's account of the Shaka period is transmitted history rather than eyewitness evidence. [1], [8]

The apparent aim is a reliable martial figure: **+25 Popularity, +20% command limit and −20% morale loss**. Popular Commander itself contributes **no direct Popularity**; that comes from Brave. Its native description concerns using reputation to promote an IG, which is consistent with its political effects.

**Assessment:** this is one of the better-fitting Vanilla packages. If stronger evidentiary restraint is wanted, Popular Commander is the disputed inference about the extent of his following; removing it primarily removes command capacity and conditional political/prestige effects. Removing it does not make him 25 points less popular.

### Cetshwayo and Zibhebhu: later adult portraits

**Cetshwayo:** Ambitious + Imperious + Diplomat reads as an assertive royal leader with diplomatic capacity. Diplomat partially offsets Imperious's popularity penalty and its slow morale recovery. The resulting ruler has **−45% decree cost** and +5% Influence: this is an active, controlling royal package, not simply a poor ruler because its intrinsic Popularity is −25. The template has no accompanying explanation of the trait selections. Its absence from opening Vanilla history matters: **SB is responsible for putting this adult package on nine-year-old Cetshwayo**. Later achievements should not be explained as childhood accomplishments.

**Zibhebhu:** Ambitious + Arrogant + Reckless + Pillager reads as an assertive, risky military contender rather than a conciliatory national ruler. The source comment explicitly identifies his later Mandlakazi position and rivalry. However, Vanilla supplies him as a later LO political opportunity; Pillager's command effects are not automatically active in that role. As ruler he would lose 5 Legitimacy and generate 10% more Infamy. This package deserves a role-specific review before SB installs him as the chief of a client settlement; it cannot simply be classed as four military traits. [1], [2]

No new historical trait recommendation for these later adult careers is settled by this opening-cast review.

## Combined package effects

### Universal character effects

These are authored trait totals only. The last column is **direct Prominence + 0.25 × Popularity**, an uncapped diagnostic; it is not the final in-game prominence calculation.

| Package | Popularity | Direct Prominence | Other universal effects | Uncapped diagnostic |
|---|---:|---:|---|---:|
| Dingane | −65 | +15 | N/A | −1.25 |
| Mpande, Vanilla | +25 | 0 | N/A | +6.25 |
| Mpande, current SB list | 0 | 0 | Health +0.05; additional Careful Manoeuvre weight | 0 |
| Mkabayi / Ndlela | +25 | +15 | N/A | +21.25 |
| Zulu / Komfiya | +25 | +5 | Health −0.05; command limit +20%; Aggressive Manoeuvre weight | +11.25 |
| Cetshwayo, adult package | −25 | +20 | N/A | +13.75 |
| Zibhebhu | −15 | +15 | Health −0.20 | +11.25 |
| Mzilikazi, comparison | +35 | +5 | Health −0.25; command limit +20%; Aggressive Manoeuvre weight | +13.75 |

Pillager separately contains −10 Popularity **inside `command_modifier`**. It is not included as a universal −10 above; the effect on displayed character popularity in that context needs engine checking. A child's age trait is also excluded from the adult Cetshwayo row. [2]

### When ruler

| Package | Combined ruler effects |
|---|---|
| Dingane | Authority +5%; decree cost −20%; loyalists from political movements +10%; radicals from political movements −20%; clergymen political strength −10%; Piracy Income +5 percentage points. |
| Mpande | Authority **−5% net**; Improve Relations speed +20%; Piracy Income −2.5 percentage points. Reserved adds no ruler modifier. |
| Mkabayi / Ndlela | Decree cost −25%; Improve Relations speed +20%; prestige from army/navy power projection +10%; **Elder ambiguity below**. |
| Zulu / Komfiya | Prestige +10%; prestige from army/navy power projection +5%; Infamy decay −25%. |
| Cetshwayo | Decree cost **−45% net**; Influence +5%; prestige from army/navy power projection +10%; loyalists from political movements +10%; radicals from political movements −20%. |
| Zibhebhu | Legitimacy −5; decree cost −25%; diplomatic-play manoeuvres +20; Infamy generation +10%; prestige from army/navy power projection +10%. |
| Mzilikazi | Prestige +10%; prestige from army/navy power projection +5%; diplomatic-play manoeuvres +20; Infamy generation +10%; Infamy decay −25%. |

Elder contains **two** `country_modifier` blocks in the installed file. One gives peasants +15% and farmers +10% political strength; the other gives Prestige −5%, Infamy decay −50% and Authority +100. Both are source facts; their effective combined runtime treatment is unverified. Do not report a silently flattened combined total as engine-proven. Neither Mkabayi nor Ndlela is an opening ruler. [2]

### When commander

| Package | Land-command effects | Other command effects and cautions |
|---|---|---|
| Dingane | Morale loss −15%; morale recovery **−10% net**; supply consumption +10%; Aggressive Manoeuvre weight +100% | Coup strength +5%; ship supply efficiency −10%. **He is not an opening general.** Ruthless supplies no army kill-rate bonus. |
| Mpande, Vanilla | Defence **+5 flat**; inflicted morale damage −5%; Careful Manoeuvre weight +100% | Coup strength **−5% net**. SB Reserved additionally gives morale loss −10%, naval critical-hit chance −10% and another careful-manoeuvre weight in character scope. |
| Mkabayi / Ndlela | Offence +5%; Defence **+5 flat**; home Offence/Defence +10%; supply consumption −10%; recovery −5 percentage points; inflicted morale damage −5%; Careful Manoeuvre weight +100% | Coup strength +5%; naval critical-hit chance +25%. **Ndlela commands at launch; Mkabayi does not.** |
| Zulu / Komfiya | Morale loss **−20% net**; command limit +20%; Aggressive Manoeuvre weight +100% | Naval vulnerability +25%, critical-hit chance +15%. |
| Cetshwayo | Offence +5%; morale loss −15%; morale recovery **+10% net**; recovery −5 percentage points; Aggressive Manoeuvre weight +100% | Coup strength +10%; naval critical-hit chance +25%. |
| Zibhebhu | Offence +5%; recovery **−15 percentage points net**; command limit +25%; devastation +25%; Guerrilla Ambush weight +800% | Coup strength −5%; naval vulnerability +30%, critical-hit chance +35%; command-scoped −10 Popularity requires verification. |
| Mzilikazi | Morale loss −20%; command limit +20%; recovery −10 percentage points; Aggressive Manoeuvre weight +100% | Coup strength −10%; naval vulnerability +45%, critical-hit chance +25%. Vanilla expressly makes him both ruler and general. |

Naval effects are recorded to avoid silently dropping part of a package; they do not describe opening Zulu armies. Command-condition weights are not guaranteed battle rolls. Additive source totals do not establish every stacking order in the engine. [2]

### When IG leader

| Package | Combined IG-leader effects |
|---|---|
| Dingane | Political strength +15%; attraction +25%; approval +1 while in government. |
| Mpande | Political strength −5%; attraction +2%; additional **government-attraction modifier +50%**; approval +1 generally and +2 additionally in government. Those two attraction fields are distinct, not an unconditional +52%. |
| Mkabayi / Ndlela | Political strength +10%; attraction +2%; net approval +3 in government or −1 in opposition. These apply to their respective LO/AF groups. |
| Zulu / Komfiya | Political strength +2%; approval +1 in government / −1 in opposition. |
| Cetshwayo | Political strength +10%; attraction +25%. |
| Zibhebhu | Political strength +15%; attraction −10%; approval −2 in opposition. |
| Mzilikazi | Political strength +2%; approval +1 in government / −3 in opposition. |

For completeness, as **agitators**, the packages yield: Dingane +0.10 activism pressure; Mpande −0.10 and +5% attraction; Mkabayi/Ndlela net zero pressure and +10% attraction; Zulu +5% attraction; Cetshwayo/Zibhebhu +0.10 pressure; Mzilikazi +5% attraction. These are native `political_movement_radicalism_add`/attraction fields, not scripted court allegiance or a guarantee of actual activism. [2]

Executive effects are irrelevant to their authored opening roles: Ambitious gives +5% company throughput; Ruthless gives +5% throughput and +10% mortality in its specified industrial/agricultural groups, with Honourable reversing those signs. They must not be misread as army lethality or national production bonuses. [2]

## Implications for SB balance

1. **Do not equate an evidence-minimal package with a balanced replacement.** Mkabayi/Ndlela each carry +25 Popularity and +15 direct Prominence before roles. Removing those changes their houses as well as any military effects.
2. **Dingane's popularity reform and Zulu combat strength are partly separable.** He is ruler-only, while Ndlela and Zulu carry the actual command packages. Raising Dingane's Popularity still affects SB's target and later military Prerogative effects, so it is not wholly militarily neutral.
3. **Our Q/2 model amplifies differences Vanilla did not tune for.** At fixed house weights and without clamping, each +10 ruler Popularity shifts T by +3.75. Replacing Dingane's intrinsic −65 with −25 changes T by +15 before removing Usurper or changing any other reputation modifier. Popularity can also alter house prominence, so the full court must be recalculated.
4. **Mpande versus Gqugqu is our comparison to solve.** The current SB lists give direct trait Prominence 0 versus +25, while their respective universal Popularity is 0 versus −35. Final prominence also includes native roles, additional generated skills and SB status modifiers; do not add a generic “historical rightful heir” compensation while the design deliberately starts without an heir.
5. **Keep first-pass changes narrow enough to attribute playtest results.** Review Dingane's reputation/temperament, Mpande's added Reserved and Gqugqu's authored package together. Retain or explicitly replace the commanders' military contribution rather than discarding it accidentally.

A restrained alternative to the sparse research packages is therefore: preserve most of Vanilla's differentiated military and elder packages; revise the poorly supported temperament labels and SB-created asymmetries; grant lasting campaign achievements separately. The later locked package selects this direction in the precise form linked above. Retain the sparse alternative as design history, with its removed combat and house-weight effects explicit. Neither the comparison nor the later approval constitutes implementation.

## Verification and references

Checked the eight Vanilla template lists against installed source, including the comparative Mzilikazi template; extracted modifier blocks and summed numeric keys separately by role using decimal arithmetic. Kept Elder's duplicate ruler blocks outside the verified sums and Pillager's popularity outside universal totals. These are source/arithmetic checks, not engine tests. No game launched, source/dependency changed, or save modified.

[1] Paradox Interactive, installed *Victoria 3* 1.14.5: [Zulu templates](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_templates/country_zul.txt>), [opening history](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/history/characters/zul - zulu.txt>). Compared with [SB dynasty templates](../common/character_templates/sb_zulu_dynasty_characters.txt) and [SB opening history](../common/history/characters/zul%20-%20zulu.txt), inspected 25 October 2026.

[2] Paradox Interactive, installed [trait-scope documentation](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/character_traits.md>), [personality definitions](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/personality_traits.txt>), [skill definitions](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_traits/skill_traits.txt>), [trait descriptions](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/localization/english/character/character_traits_l_english.yml>), [defines](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/defines/00_defines.txt>) and [generation rules](</Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/character_templates/00_default_template.txt>), inspected 25 October 2026.

[3] N. Isaacs, *Travels and Adventures in Eastern Africa*, vol. II, 1836, pp. 280–282. [Public-domain original, UCT](https://emandulo.apc.uct.ac.za/collection/FHYA%20Depot/Isaacs_Nathaniel_Travels_and_adventures_in_eastern_Africa_vol_2.pdf). Previously retrieved text re-read for this comparison; the web renderer rejected the large PDF. Colonial eyewitness interpretation, not an impartial character assessment.

[4] A. F. Gardiner, *Narrative of a Journey to the Zoolu Country, in South Africa. Undertaken in 1835*, 1836, especially pp. 34–50 and 137–140. [Public-domain scan](https://archive.org/details/narrativeofjourn00gard_0). Cached original OCR inspected. Distinguish eyewitness actions from attributed motives.

[5] F. N. C. Okoye, “Dingane: A reappraisal,” *Journal of African History*, 10(2), pp. 221–235, 1969, [doi:10.1017/S002185370000949X](https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/dingane-a-reappraisal/16F30C648B56730FC0D957F534C30109). Publisher extract only; no claim of full-text access.

[6] M. Z. Shamase, “The nature and extent of the Zulu military engagements under Emperor Mpande,” *Military History Journal*, 16(4), December 2014. [Full text](https://samilitaryhistory.org/vol164ms.html).

[7] M. Z. Shamase, “The royal women of the Zulu monarchy – through the keyhole of oral history: Princess Mkabayi Kajama,” *Inkanyiso*, 6(1), pp. 15–22, 2014. [Full text](https://inkanyisojournal.org/index.php/ink/article/download/241/347), doi:10.4102/ink.v6i1.241. Interpretative oral-history scholarship, not an independently witnessed psychological profile.

[8] Mkehlengana kaZulu, testimony recorded April 1905, in *The James Stuart Archive*, vol. 3, 1982, pp. 210–221. Identity and evidentiary limitations are recorded in the [first-principles brief](zulu_starting_character_traits_research_2026_10_25.md), reference 7. This turn relies on that completed research and the explicit Vanilla source comment; the attempted web re-fetch timed out.
