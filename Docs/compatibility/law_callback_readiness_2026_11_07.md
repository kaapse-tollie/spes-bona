# Law callback readiness audit — 7 November 2026

**CRASH115-02: additional source corrections implemented; engine replay pending.**
This follows the [Zulu inherited-law crash](1_15_0_crash_2026_11_07.md). The
1.15.0 native creation order permits law callbacks before land and AI creation;
inherited story flags and a date after 1836 do not establish country readiness.

## Coverage and findings

The audit resolved exact-path shadows and keyed replacements across the pinned
Vanilla 1.15.0, CMF 1.67.1 + `sb-1.15.0-r1`, and current SB tree. It inspected
**158 effective laws, 118 direct callbacks (51 activation, nine deactivation
and 58 enactment callbacks), plus nine law on-actions**, following their scripted helpers, nested law changes and event
dispatches. There were no unresolved duplicate plain law/effect definitions.
The [bounded inventory](evidence/law_callback_readiness_2026_11_07.json) records
the callbacks and classifications; full source hashes and reachability output
are retained in
[`generated/law_callback_readiness_2026_11_07/`](../../generated/law_callback_readiness_2026_11_07/).

The retained Hail Columbia and Gates of the Bosphorus 1.13 law files were also
checked as style references. Their inspected callbacks contain no direct JE
additions and provide no readiness fix to reuse; the pinned 1.15 sources and
observed native creation order govern this correction.

| Journal path | Additional unsafe call sites | Correction |
| --- | --- | --- |
| Technocracy | One unconditional law activation call | Guard and defer JE creation; retain native law cleanup |
| King in Parliament | Five voting-law callbacks relying on an inherited possibility flag | Guard all five calls; recheck monarchy, voting law and flag on delivery |
| Divided Monarchists | Monarchy and Social Monarchy | Preserve the effective CMF Monarchy body and native Social Monarchy body; recheck France, dynasty, DLC and current law |
| Spanish Provisional Government | The same two monarchical laws | Recheck Spain, current law, date, DLC and revolution/secession exclusions |
| Abolish Monarchy | Two shared helpers, reached by four republican laws and the enactment-start hook | Guard only JE addition; preserve separate enactment and completed-reform eligibility at delivery |
| Inboekstelsel reopening | SB's law on-action through its reopening helper | Guard the complete reservation/addition pair; defer without prematurely taking the seven-day receipt |

These are **13 additional journal-addition sites**, not thirteen observed
crashes. The two Zulu constitutional callbacks and their law on-action already
reach the shared guard from CRASH115-01 and required no further gameplay change.

The 58 enactment callbacks contain no reachable JE-addition paths in the
inspected helper graph. The remaining effective direct callbacks do not reach an unguarded synchronous
JE addition in the inspected helper graph. Slavery/army/party cleanup and Natal's
indenture cancellation do not add JEs. Nested `activate_law` paths reach the same
audited law definitions. Law-event follow-up inspection distinguishes actual
effects from previews: the three French pretender JE references are inside
`show_as_tooltip`; the Communist entries are in `communism.2.after`, after the
event answer, rather than in the inherited-law effect or event `immediate`.
Those event bodies were not changed. Enactment/checkpoint event pools are later
event-delivery routes, not direct inheritance callbacks.

## Implementation

- [Eight complete law replacements](../../common/laws/zz_sb_law_journal_readiness.txt)
  change only JE-addition statements. Full definitions avoid relying on partial
  callback merging. All other effective Vanilla/CMF bytes are preserved.
- [Five readiness helpers and two native helper replacements](../../common/scripted_effects/zz_sb_law_journal_readiness_effects.txt)
  preserve immediate JE creation for ready countries. Otherwise they schedule
  one hidden event one day later. Literal event IDs keep every delivery route
  visible to the existing lifecycle inventory.
- The [shared country predicate](../../common/scripted_triggers/sb_law_journal_readiness_triggers.txt)
  uses the existing post-lobby marker plus `is_country_alive` on the current
  country. No additional startup flag or global polling was introduced.
- The [six hidden delivery events](../../events/sb_law_journal_events.txt) put
  readiness and current eligibility checks inside `immediate`, allowing the
  request to be scheduled while the country is unfinished. Existing JEs suppress
  duplicate deliveries. Destroyed or ineligible countries do not retry forever.
- [Inboekstelsel](../../common/scripted_effects/sb_inboekstelsel_effects.txt) sets
  its original seven-day reopening receipt only when it can actually add the
  journal. A cancelled deferred attempt leaves no reservation blocking a later
  legitimate law change.

Native non-JE effects, law balance, country scopes and ordinary ready-country
timing remain unchanged. In particular, the existing French/Spanish setup and
monarchy-transition effects retain their original phase. This is not an audit
of every native non-JE operation during country creation.

The [override inventory](override_inventory.json) pins ten new replacements,
including CMF's exact `REPLACE_OR_CREATE:law_monarchy` source. Its checker now
accepts an explicitly declared dependency directive, retaining `REPLACE` as the
default and checking both file and object hashes. The
[delayed-event manifest](../../tools/delayed_event_lifecycle_manifest.json)
classifies all six new destinations. The installed CMF tree, archive pin and
compatibility patch are unchanged. No localisation, metadata/version or save
was edited.

## Verification and limits

The [source regression](../../tests/test_law_journal_readiness.py) reproduced
**39 premature-activation failures** across the 13 call sites and three
unfinished/startup combinations before correction. It now checks normal
immediate activation, deferred delivery, duplicate scheduling, missing readiness,
changed laws, existing JEs, a foreign root, native political exclusions,
enactment cancellation and Inboekstelsel cancellation/retry. Removing only the
new calls from the eight law/two helper replacements reconstructs their complete
effective upstream bodies byte-for-byte.

The fixture exercises eligibility both at dispatch and delivery, so safety does
not assume the native scheduler checks triggers at only one of those boundaries.
It executes the actual readiness helpers and delivery effects; it does not
simulate the native creation process, scheduler, save/load or all surrounding
law effects. The audit's reachability search identifies potential paths, while
manual review establishes their scopes, guards and effect phases.

Final unit run: **1,109 tests — 1,100 passed, eight skipped and one unchanged
localisation-review failure**. Target-aware validation also passes dependency
integrity, override hashes/parity, maps/naval connectivity, script contracts and
the complete delayed-event inventory. Its 15/17 passed/warned/skipped rows leave
the unit/localisation rows reporting the same existing review debt. The stale
override-count expectation found during the first run was updated from 125 to
the reviewed 135; the full unit rerun has no new failures.

The existing failure concerns the dangling Swazi `.098` review-queue row and
reviewed wording/size drift in Klip River `.060`/`.080` and Natal `.050`.
Localisation and approval baselines remain untouched. All 86 local documentation
links checked resolve. Tiger 1.19.0 lacks the target schema and was not used to
certify 1.15 syntax; synchroniser execution was skipped, with installed CMF
integrity checked independently.

## DP engine checks

1. Fully restart. Replay the preserved November 1856 Zulu checkpoint through
   the actual split; CRASH115-01's two-court/settlement checks still apply.
2. Exercise an inherited Technocracy or qualifying voting law during a country
   split. The JE must appear at most once after creation, including when normal
   automatic activation runs before the deferred event.
3. Reform a ready country normally, including republic enactment, French or
   Spanish monarchy restoration, and Inboekstelsel abolition/reinstatement.
   Check original law effects and journal previews as well as JE creation.
4. Where a deferred request is pending, check cancellation/changed eligibility,
   country removal and save/load across delivery. Verify that a cancelled
   Inboekstelsel request does not suppress a later valid reopening.

Static results do not close those engine gates or certify all foreign-country
creation paths. DP remains responsible for launching the game.
