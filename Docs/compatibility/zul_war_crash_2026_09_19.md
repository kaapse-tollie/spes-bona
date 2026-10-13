# Crash during the ZUL war — investigation

19 September investigation; 20 September follow-up. **Native crash reproduced;
targeted script safeguard applied; DP reports a successful altered-order replay,
but the safeguard's effect remains unverified.**
Game 1.14.3; crash metadata lists SB and CMF. DP retains game-launch and
reproduction ownership. No save was modified.

The sections through the original fingerprints record the **19 September
read-only investigation**. The follow-up below records the subsequent runtime
change; it does not retroactively certify the original hypotheses.

## Evidence

Crash bundle: `Victoria 3/crashes/victoria3_01260819_200217/`.
Its exception timestamp is **2026-09-19 20:02:17**, despite the folder name.

The failing path in `exception.txt` is:

```text
AI ManageTreaties
  → ComposeTreaty / FilterPotentialArticleTypes
  → CTreatyArticleType::IsPossible
  → CIsMarketReachableForTradeTrigger::EvaluateDerived
  → NShippingLane::CheckCanTradeBetween
  → NShippingLane::HasMarketCapitalConnectedPort +124
```

The effective Vanilla `common/treaty_articles/13_goods_transfer.txt` calls
`is_market_reachable_for_trade = scope:other_country.market` in `possible`.
It is the only installed treaty-article definition using this trigger. Neither
SB nor CMF overrides that file. The stack therefore identifies Goods Transfer
eligibility during an AI treaty proposal, not an executing Zulu settlement event.
It does **not** identify the country being evaluated or establish why its native
port/capital lookup failed. Mod-created state and a Vanilla engine defect remain
possible causes; the stack alone cannot distinguish them.

From 20:02:12 until the crash, `error.log` repeatedly reports invalid `capital`
links in Vanilla journal entries, subject AI, diplomatic values and treaty
articles. An invalid country/capital reference is a **hypothesis**, not a proven
cause. The earlier barracks assertion and naval-battle localization errors are
not the crashing stack. There is no memory dump in this bundle.

## Autosave cross-check

The current `save games/autosave.v3` was written at 20:02:12, five seconds before
the exception; its game date is **1874.7.1**. Read-only parsing of the country,
state, market and diplomatic-play databases found:

| Actor | Country ID | Capital / market-capital state | State ownership |
|---|---:|---:|---|
| NAL | 16777216 | 16777400 | NAL |
| ZUL | 481 | 779 | ZUL |
| GBR | 3 | 5 | GBR |

NAL belongs to market 0, owned by GBR. ZUL belongs to market 116, owned by ZUL.
Both markets exist. The ZUL play has GBR as initiator, ZUL as target and NAL as a
participant; its type is `dp_make_protectorate`. Neither NAL nor ZUL has a
`sb_zululand*` country variable in this snapshot. The new Chiefdoms contest has
not started in the inspected state.

Dead HOL and LIP country records also remain in the save. LIP's archived capital
no longer exists as a state. Retained dead-country records do not prove that AI
evaluated them, or that they caused this crash. Omitted serialized fields must
not automatically be treated as corrupt references.

## Separate map finding

The launch log rejects spline port anchor **8414308** as non-coastal, reports
unconnected harbor nodes, and reports missing port nodes around the Benguela
Coast and Cape of Good Hope sea regions. This remains unresolved.

The authored ZUL port is `x9E9742`; the deployed spline anchor is `(4834, 850)`.
Raster sampling places that anchor in the configured province, and four-neighbor
pixel adjacency confirms that province touches sea province `x78FCFC`, listed
in Vanilla's `sea_starts`. Thus simply moving an allegedly inland province's
port is not justified by this evidence.

`tools/check_naval_network.py` passes: **6,641 nodes, 7,191 connections and 33
connected SB state ports**. That check reads the shipped generated network; it
does not reproduce the engine's spline-node acceptance. Its pass does not clear
the launch errors or establish that this map discrepancy caused the crash.

## Next verification

- **Pending DP:** reload the inspected autosave with the same mod stack and record
  whether the crash repeats, its game date and the new exception stack. Do not
  load the modded campaign with SB removed as a Vanilla comparison.
- If it reproduces in the same native lookup, investigate an isolated diagnostic
  guard at Goods Transfer's native reachability call. Such a guard would be an
  experiment until a same-checkpoint before/after run establishes its effect;
  do not silently disable the article or attribute the defect to ZUL.
- For the separate harbor issue, compare fresh Vanilla-only and SB launch logs
  before changing the generated map network. Existing `SUP-05` keeps broad
  spline regeneration deferred to DP.

Only investigation documentation and pitfalls were changed. No runtime files,
dependency, gameplay gates, maps or save files changed for this investigation.
The full static suite was not rerun for documentation-only changes.

## Evidence fingerprints (SHA-256)

```text
exception.txt  0c2db2ca7912329ec3824f72f230b2d4a84388765c484e185b07d7ab9918ed48
error.log      854d724a3ffef2a79bdaa22befe91a61ba2750c41ead3b646ed0b200660b2ecf
meta.yml       6475daa5f4ffd465cd4736b0d8d529b0e545c56c711f6fec51e87417e57cf6df
autosave.v3    33b6118b6827d0d403ce7cfa9adf47f660f0d350bd837aa0155c80466bea7711
```

## 20 September: repeated crash and scoped safeguard

DP reports another crash, possibly when ZUL capitulates. The new bundle is
`victoria3_01260820_100855`, timestamp **2026-09-20 10:08:55**. All demangled
Victoria 3 stack frames match the 19 September 20:02:17 exception after removing
load addresses. The same invalid-capital error sequence precedes it.

The new autosave again records **1874.7.1**. A line-by-line comparison against
`autosave_1.v3` finds only six differences: save header, real date, packed real
timestamp and three generated naval-battle tooltip strings. No gameplay state
differs. War 182 / play 167772170 has:

- ZUL war support **97.11901**; GBR and NAL **100**.
- GBR's primary `make_protectorate` against ZUL, target state 779,
  enforcement progress **0**.
- ZUL's primary `return_state` against NAL, target state 16777400,
  enforcement progress **0**.
- No annexation demand; no peace date or selected peace-deal country.

This snapshot does not establish imminent capitulation. It also cannot rule out
a later capitulation or market change between the save and the exception.
The generic SB Zulu defeat helper only subtracts dynastic stability; British
scripted annexation callbacks require their separately bound annexation play.
The active play is `dp_make_protectorate`. No war-settlement code was changed.

Read-only inspection of the installed arm64 executable adds a concrete boundary:
`HasMarketCapitalConnectedPort` calls `CCountry::GetMarketCapital` and passes the
result into `HasConnectedPort`, which immediately reads its state identifier and
uses it to index the visited-state array. There is no intervening state-validity
branch in those instructions. The exception offset is at the return site from
that port search. This supports guarding invalid market capitals; it still does
not identify the actual failing country, state, or instruction inside that search.

### Applied change

`common/treaty_articles/13_goods_transfer.txt` is a pinned exact-path Vanilla
shadow. Only `possible` changes. A `trigger_if` requires live parties and existing
personal and market-owner market-capital scopes before executing **the complete
original Vanilla `possible` body**. Its invalid-scope branch returns false.
The branch is deliberate: merely adding sibling validity tests would not express
the same explicit boundary around the native lookup during trigger evaluation.

No ordinary peace, subject-status or territorial restriction was introduced.
Article maintenance, existing goods transfers, AI scoring, costs and the rest of
the file remain unchanged. CMF is unchanged and has no competing definition.
Inventory: **39 exact-path files, 112 keyed overrides**. This is a narrow
**mitigation awaiting replay**, not a confirmed root-cause fix.

### Verification and replay

- **17 focused tests passed**, covering the guard, full-file Vanilla parity after
  unwrapping only `possible`, hash pins, and existing baseline metadata checks.
- Full suite: **467 tests; 459 passed, five skipped, two failed and one errored**.
  The existing failures concern the indenture goal localisation key and the
  missing reviewed `sb_boer_conventions.141` baseline. The existing error is the
  missing historical 1.14.2 Steam manifest. These checks were not weakened.
- Static gates: **15/17 passed, warned or skipped**; unit tests and localisation
  remain failing as above. Compatibility inventory, map checks and native/CMF
  comparison pass. Tiger is advisory (1.13.5 schema against 1.14.3); its findings
  in the new shadow concern unchanged Vanilla `can_ratify`/`infamy` bodies,
  not the added guard. [Compact results](evidence/zul_war_crash_guard_2026_09_20.txt).
- **Pending DP:** restart the game so the changed definition loads, replay the
  same checkpoint through the previous crash point, and retain the new logs. If
  it still crashes, compare the new stack before broadening the patch. Game
  launches and engine validation remain DP's responsibility.

New fingerprints:

```text
exception.txt  a83c992166bfb63816a8832d3eae942f51d8e35d7b871437609918e994e9e289
error.log      a8a06ddf75735df7f5adb4fe2abfd52f969c6f2a1a9eb386249d2f3ff2637c9b
meta.yml       4622c899d3f7bb71afb298a86f4cd86144f718777f77e328a278c678e1f09434
autosave.v3    eb8003890d46dec762bfd50d6ebbd018aab667ae3b61681672381b838d4fbdaf
```

## DP follow-up: delayed advance completes without a crash

DP reports switching the army to Defend, waiting roughly a month, then resuming
the advance and obtaining ZUL's capitulation without a crash. This is a successful
player-reported route past the failure, and weakens the hypothesis that ZUL
capitulation necessarily triggers it.

It is not a controlled test of the Goods Transfer safeguard: the army orders and
timing changed, and whether this run restarted with the safeguard loaded is not
yet confirmed. Changed occupation, market or AI timing could have avoided the
failing state; none is established as the cause. The earlier exception stacks
still identify the native trade-reachability lookup as the failure site.

Status: **campaign progressed; underlying crash and safeguard efficacy remain
unresolved**. No additional runtime changes were made for this report. Do not
change ZUL capitulation mechanics or declare the guard validated from this run.
