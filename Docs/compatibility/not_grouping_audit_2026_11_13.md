# SB compound-NOT audit — 13 November 2026

## Result and scope

The follow-up to the worldwide diplomatic-joining regression found **six more
incorrect negated conjunctions**: one global movement gate and five local
event/court checks. All six now use `NOT = { AND = { ... } }`. One intentional
multi-child `NOT` remains unchanged.

Baseline: Victoria 3 **1.15.1**, SB **0.20.3**, CMF **1.67.3 + sb-1.15.1-r1**.
No dependency payload, gameplay values or reviewed localisation were changed.
No new eligibility requirements were introduced; existing predicates were
regrouped to match their intended conjunctions. The working tree already contained the rebase and
other content work; this audit's comparison uses a separate pre-edit snapshot.

The lexical census inspected all **396 runtime `.txt` files** in `common/` and
`events/`: **3,122 `NOT` blocks** (2,547 common; 575 events). Comments and quoted
strings were excluded; a scope or iterator with several conditions remains one
direct child. Seven blocks had multiple direct children. The original bodies
and locations are preserved in [the census](evidence/not_grouping_audit_2026_11_13/multi_child_not_before.json).
No further script `NOT` blocks were found in SB's `gui/`, `gfx/` or `map_data/`.

An independent Sol 6.1 Max review covered global scripted rules and their
helpers, movements, interest groups, laws, buildings, AI, diplomacy, subject
types, decrees, commander interactions, amendments and on-actions. Injections
and parameterised helpers revealed no additional compound-NOT case. This is an
audit of this Boolean mistake, not certification of every global rule.

## Semantics and dispositions

The installed native `CNotTrigger` rejects **any** true direct child: flat
`NOT { A B }` means `not (A or B)`. Negating the combination requires
`NOT { AND { A B } }`. See the [native evidence and original reproduction](diplomatic_joining_and_outliner_2026_11_13.md).
Optional-scope behaviour is not used as an alternative explanation.

| Surface | Failure before correction | Disposition |
| --- | --- | --- |
| `zzz_sb_chiefdoms_uprising_overrides.txt`, reactionary creation | Inherited CMF exception excluded American countries with USFP inactive, and every country with USFP active. | Exclude only when **both** USFP is active and its American-country predicate matches. Preserve every other creation requirement. |
| `sb_court_cast_effects.txt`, brother-backing preview | With no first backer, Cetshwayo could lack a second backer without showing the no-backer message. | Negate the full Cetshwayo-and-valid-second-backer condition. Allocation effects are unchanged. |
| `sb_bechuanaland_corridor.032` | Cancellation required both eligibility and the direct-route marker to be lost. | Cancel if either condition of the original event trigger fails. |
| `sb_bechuanaland_corridor.033` | Same issue for the proxy route. | Same correction, retaining the proxy-route identity. |
| `sb_martinus_confederation.010`, fallback dismissal | Losing authority alone or the pending stage alone could leave no fallback option. | Make dismissal the complement of the valid authority-and-pending-stage option. Retain receipt-scoped cleanup. |
| `sb_natal_crisis.085`, retry option | Its flat negation included GBR/alive predicates already required outside it, making the retry unreachable. | Negate full launch readiness while retaining the separate live GBR/ZUL and unresolved-raid conditions. Existing retry timing and launch restrictions are unchanged. |
| `zz_sb_absolutist_override.txt`, character support | **No bug:** neither Monarchy nor Autocracy may have a stance below approve. | Preserve the Vanilla/CMF NOR. Approving one law while rejecting the other must still fail. |

### Global reactionary gate and dependency boundary

The faulty block is unchanged in installed CMF's
`common/political_movements/ycom_00_ideological_movements.txt:7251` and is absent
from Vanilla's equivalent. CMF's default `is_usfp_active` is `always = no`;
`usfp_country_is_american` still matches Yankee/Dixie primary cultures and the
USFP extension hook. Thus the error matters even without Hail, Columbia! active.
The comment identifies an American-only USFP exception, not a universal veto.

| USFP active | American predicate | Allowed by this exception |
| --- | --- | --- |
| No | No | Yes |
| No | Yes | Yes |
| Yes | No | Yes |
| Yes | Yes | No |

Only SB's effective overriding definition is corrected. CMF installation and
baseline hashes are unchanged. The [current movement contract](chiefdoms_uprising_contracts_1_15_1.json)
allows exactly this grouping amendment alongside the existing Chiefdoms gate.
The parity test removes that one explicit amendment before comparing the
remaining object to the original dependency hash. The override inventory records
the expanded scope and refreshes only this SB object's hash.

## Verification

The [new regression file](../../tests/test_not_grouping.py) evaluates source
Boolean expressions over exhaustive relevant truth tables. Helpers, scopes and
iterators are supplied as atomic predicates; these fixtures do not simulate
event delivery or the movement engine. Cases cover each invalidation separately,
unrelated countries, unchanged native creation restrictions and the intentional
absolutist NOR. The census test requires review before adding another flat
multi-child `NOT`.

Thirteen existing bounded test evaluators/canonicalisers also treated `NOT` as
negated AND. Their Boolean handling is corrected to NOR without changing their
scope/iterator boundaries or adding a shared emulation framework.

- Before script corrections: **six test methods failed**, reproducing the bad
  global gate, missing fallback/cancellation/tooltip behaviour, unreachable retry
  and the unreviewed flat-NOT inventory. [Before output](evidence/not_grouping_audit_2026_11_13/focused_before.txt)
- After corrections: **39 focused tests passed**, including movement/dependency
  parity, the previous diplomatic-joining regressions and performance equivalence.
  [Focused output](evidence/not_grouping_audit_2026_11_13/focused_after.txt)
- Full static validation: **15 PASS, 2 WARN, 0 failures**, including complete
  unit discovery, dependency installation integrity, override contracts, maps,
  naval connectivity and localisation. Unit discovery covers **1,146 tests**
  with nine existing historical-input skips. The first full run caught an
  outdated inventory-date assertion; it now accepts the new date for exactly
  this reactionary override. [Final validation](evidence/not_grouping_audit_2026_11_13/static_validation.txt)
- Existing warnings remain: deferred gates `BC-20`, `BC-22`, `CP-07`, `QUAL-09`
  and `SUP-05`; Tiger 1.19.0 lacks the target 1.15 JE/event schema and was not
  run as a target validator.
- Independent Sol 6.1 Max review: no remaining actionable findings. Scoped
  whitespace and documentation-link checks passed.

No engine launch or save migration was performed. DP runtime checks remain
pending: reactionary eligibility under the relevant mod/culture combinations;
held Bechuanaland and Martinus popups losing one prerequisite; Port Natal retry
after a temporary blocker; and the no-backer court preview. Movement eligibility
does not guarantee that the engine immediately creates the movement.
