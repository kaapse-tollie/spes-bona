# Dunn, the later princes and Hamu's coastal bargain

Implemented 30 October 2026 for the current 1.14.5/CMF baseline and new campaigns.
No game launch, save migration, dependency edit or ZAR rollout. Mandlakazi's
provisional handover/bargain remains outside this batch.

## Delivered behaviour

- Dunn's paired introduction opens from 1855 under Mpande, after Klip delivery
  completes and Natal is an actual British colony. Admission pledges Dunn to
  Mbuyazi's future succession; the strongest available unpledged house declares
  for Cetshwayo. Existing present allegiances remain separate. Refusal removes
  Dunn's court constituency and sends the living trader to Natal.
- Trader adds 10 permanent Prominence. The first and annual offers each provide
  **two** Firearms weeks on acceptance, capped at 260. One offer per 365 days,
  with its reservation on the actual Dunn identity. No post-completion reward or
  delivery popup. Britain/Natal or host eligibility loss cancels stale offers.
- The existing August 1856 retirement and 5pp weekly activism are retained. Native
  mobilisation timing remains approximate.
- When Cetshwayo actually defeats Mbuyazi, the recorded admitted Dunn is preserved
  through coalition cleanup, restored to the winning court, then judged in a
  paired event: execute (−10 GBR relations), retain (+5 and Mthonga declaration),
  or banish. Other losing members retain the existing outcome. The exemption
  does not persist into unrelated wars.
- Mthonga enters the cast from 1855 but is politically deferred until declaration.
  Retaining Dunn can declare him; otherwise the eligible 1857 fallback waits until
  Mpande no longer rules and there is no reserved accession/conflict. Declaration
  grants Claimant, without a free backer. No separate flight/refuge event.
  His age of 18 at creation is explicitly an authored estimate, not a researched
  exact birth date. Hamu enters from 1860 and silently receives Claimant.
- Hamu's offer requires Transvaal land in East Transvaal and the acknowledged
  **Boer–Swazi border** outcome. Its durable global outcome survives SWZ's demise.
  An existing/dead Hamu template is never recreated. A future sponsor retag retains
  its object reference; initial availability for a new ZAR tag is deferred.
- **1G** is quoted once and debited on acceptance; debt is allowed. One named, still
  eligible neutral house joins Hamu and relations with the court fall by 10.
  Optional funding costs £250 per budget week and adds 25 Popularity to Hamu.
  Stopping removes only those modifiers; resuming adds no grant or house.
- Completed peaceful succession, verified dynastic victory or a qualifying royal
  restoration records Hamu's earned cession. Being installed as a wartime faction
  head alone does not. Surviving neutral/third-party princes retain their claims.
- The complete five-province Greater NRP footprint, including the Zululand port,
  becomes the actual sponsor's **Confederal Partner**. The native relationship
  shares its ruler and transfers 5% income. NRP keeps the allocated economy; this
  branch adds no claim on residual Zululand or old union petition.
- One territorial reservation covers both Hamu and later Thirteen Chiefs aid.
  Genuine failure releases an unearned promise; actual fulfilment permanently
  consumes the reward, even if NRP later disappears. An earlier earned Thirteen
  Chiefs receipt cannot be overwritten merely because its container was closed.
- Britain can demand the coastal cutback only when the residual Zulu country, or
  all four residual provinces after annexation, is actually under British control.
  Eligibility can wait for years. NRP's actual overlord decides; acceptance retains
  a reduced subject. Refusal configures the exact native play, whose Return State
  demand risks NRP's whole Zululand state. No scripted wartime land enforcement.

## Source checks

Source-executed fixtures cover frozen prices/debt, stale targets, house selection,
subsidy withdrawal/resumption, failed claims, reciprocal reservations, completed
accession, subject-creation retry, authenticated territorial reunion, third-party
loss, British control and changed overlords. These do not simulate military or
market allocation, native event rendering, or native country creation.

All new event prose is TO REVIEW. The installed shogunate coalition scene and
existing two-character format informed the presentation; no reviewed prose was
rewritten. The pre-change full suite had one existing localisation-regression
failure and eight historical-input skips.

### Validation results — 30 October 2026

- Focused Dunn/later-court/dynastic/settlement run: **127 tests passed**, including
  **22 new later-court tests**. The fixtures execute the actual scripted helpers,
  including a foreign event root, incomplete country creation, failed subject
  setup and a changed/absent overlord after refusal.
- Complete discovery through `tools/validate.py --skip-cmf-sync`: **969 tests**,
  **960 passed, one pre-existing failure, eight skips, no errors**. The unchanged
  failure is `test_repository_manifests_are_current`: an old dangling review-queue
  row for `sb_swazi_frontier.098.prerogative_after_blood_river` and prior reviewed
  text drift in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050`.
  This batch did not edit that Natal localisation file or grant those approvals.
- Full validator: **14/16 gates passed, warned or skipped**. Both failed gates
  report the same pre-existing review issue: unit discovery and localisation.
  CMF compatibility, override comparison, map/naval checks, script contracts,
  event lifecycle and on-action routing pass. Remote CMF release sync was skipped;
  the existing five deferred release gates remain identified by the validator.
- Advisory Tiger was run with installed Vanilla and CMF. It still cannot validate
  the script-container syntax used by SB; its `container` diagnostic on the new
  Hamu predicate is recorded as that limitation, not an engine test.
- `git diff --check` passes. The parallel **Sol 6.1 Max** reviewer independently
  reran all 22 new tests and reported no remaining concrete blockers after fixes.

Local command evidence: `/private/tmp/sb-later-court-focused-final.txt`,
`/private/tmp/sb-later-court-validator-complete.txt` and
`/private/tmp/sb-later-court-tiger-complete.txt`. All engine scenarios below remain
pending; static success does not establish native delivery, market allocation or
subject creation.

## DP engine matrix

### 1. Dunn's arrival

**Pending.** Fresh/checkpoint-before-1855: unsettled Klip or non-British Natal
blocks the visit. Settled context admits one actual Dunn. Check both portraits,
full names, permanent Trader and the displayed strongest house.

### 2. Admit or decline

**Pending.** Admission pledges Dunn to Mbuyazi and the displayed house to
Cetshwayo, preserving current allegiance. Refusal sends Dunn to Natal and removes
his represented weight. Let a popup wait while a participant dies or changes
commitment; no silent replacement or duplicate invitation.

### 3. Annual guns

**Pending.** Accept/decline the initial offer, then wait a year. Acceptance gives
two weeks, not a monthly stream. Check 259→260 cap, completion, transfer, an open
popup during war, and no offers after completion.

### 4. The brothers' outcome

**Pending.** Both playable sides and winners. Cetshwayo winning preserves Dunn
only for judgement: test all three choices and GBR relations. Mbuyazi winning
does not open that judgement. A stale judgement must not protect Dunn in a
subsequent unrelated war. Confirm characters survive defeated-tag deletion.

### 5. Later declarations

**Pending.** Retain Dunn to declare Mthonga without a free house; otherwise test
1857 after a settled succession, including a delayed brothers' popup. Hamu
appears in 1860 without an event, with Claimant. No duplicate historical template
or early adult introduced during an open conflict.

### 6. Hamu's offer

**Pending.** TRN owns some East Transvaal, Boer–Swazi border resolved, Hamu eligible,
all five promised provinces still in the court. Verify price, debt, −10 relations,
Zulu warning and the strongest eligible uncommitted house. Change a displayed
actor or land ownership before payment; do not take a different house or charge
an invalid offer.

### 7. Continuing funding

**Pending.** Start/stop/resume: £250/week, +25 Popularity once; no second payment
or house from resumption. The paid land promise survives withdrawal. Death,
renunciation and loss of the sponsor stop funding; unrelated princely accession
alone does not invalidate a living Hamu.

### 8. Greater NRP

**Pending.** Hamu accedes peacefully and through each playable war side. Check all
five provinces, port, buildings, pops, market access and Confederal Partner
relationship. Wartime installation is insufficient. Repeat callbacks; no second
creation, whole-state claim, automatic union or duplicated reward.

### 9. Reciprocal promises

**Pending.** Accept Hamu before early partition, then attempt scripted Boer aid.
Reverse the order with accepted and earned Thirteen Chiefs backing. Check stale
buttons/appeals, AI funding and reward delivery. Failed Hamu can release the
reservation; fulfilled Hamu cannot, even after NRP is annexed.

### 10. British boundary

**Pending.** Independent residual Zulu: no demand. Later British subject or
annexation: actual overlord receives the demand. Accept retains reduced NRP as
subject; refuse produces the native play with the correct beneficiary. Change
NRP overlord while the demand is open or refused but not yet launched. Britain
must not create an external war against its own subject.

### 11. Delayed reunion and loss

**Pending.** Victory callback before reunion retains the earned cession while
the authenticated losing faction holds a province. An unrelated third-party
conquest is not a licence to seize it. A failed subject-creation step must not
transfer the full coast prematurely or duplicate economic setup on retry.

### 12. Unrelated routes

**Pending.** Repeat ordinary early Klip Crown/direct-administration, NAL/TRN
Chiefdoms interventions without a Hamu promise, and ordinary dynastic victories.
Retain earlier verified mechanics; no new unrelated-war peace prerequisite.
