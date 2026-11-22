# Klip River County stayed uncommitted in the play against British Natal

Natal Colony, Victoria 3 1.15.2. The secession play opened on 5 April 1846.
Britain took the defensive lead before the Klip River script checked the target.

## Save evidence

| Record | Finding |
| --- | --- |
| 1 April, `autosave_1.v3` | Natal has the northern boundary commission event (`.010`). KLR has yet to form. |
| 5 April, diplomatic catalysts retained in the May save | GBR and NAL are recorded as allies in the play. GBR and ZUL are recorded as opponents. NAL has been a British colony since 24 May 1845. |
| 1 May, `autosave.v3`, play `117440515` | ZUL (`33554891`) is the sole committed attacker. GBR (`3`) leads the defence, with NAL (`16777560`) committed. KLR (`16777860`) appears only in `involved` and has no side record. |
| 1 May, war goals and country variables | The sole goal is ZUL's opening primary demand to annex NAL (`134217742`). NAL still has `sb_klip_river_secession_delivery_pending_var`. None of NAL, ZUL or KLR has the secession active flag, and NAL has no saved reference to this play. |

The May save has SHA-256 `e5c94d17b8a9402d8fb82b9b8e02d85631e582f8604a2ab7dec667b94ff08f7b`.

## Why setup was skipped

The installed macOS 1.15.2 build creates the opening war goal, processes
automatic participants for both sides, then binds the current leaders as
`scope:initiator` and `scope:target` for `on_diplomatic_play_started`.
`CDiplomaticPlayManager::OnCreateDiplomaticPlay` establishes this order.
`CDiplomaticPlay::AddBacker` promotes the defending subject's overlord to
target in an ordinary play when the opposing leader is independent of it.

The original Klip callback required `scope:target` to be NAL, hold Natal's pending
flag and own Natal's port province (`x279045`). GBR failed that check. The skipped block would
have committed KLR unconditionally, added Natal's annexation demands against
KLR and ZUL, and recorded the play for settlement.

The same session's `error.log` also reports a country-to-play comparison at
line 473 of that file. Inside `any_diplomatic_play`, `this` is the play, so
`initiator = this` cannot identify ZUL. The saved play confirms that this
duplicate check still allowed the launch.

The old sequence also scheduled ORA's appeal too late to affect the opening.
County creation queued Natal's insurrection event after one day. ORA's appeal
was due after six days and required an active play. Even when setup succeeded,
the start callback had already chosen the backers by the time ORA could answer.

## Implemented correction

Both setup and duplicate detection recognise ZUL's secession play to annex NAL.
NAL can lead the defence or be a committed defender under its overlord GBR.
KLR joins ZUL in either case. Natal demands the annexation of KLR and a
protectorate over ZUL. When Britain leads and Natal cannot hold the native
protectorate demand, Britain presses it on Natal's behalf. Natal records the
play for settlement under either defensive leader.
[Play identification](../../common/scripted_triggers/sb_klip_river_county_triggers.txt) · [Participants and settlement](../../common/scripted_effects/sb_klip_river_county_effects.txt)

Once KLR forms, an independent ORA gets the six-day appeal before Natal can
open the play. An eligible ORA that accepts joins ZUL and takes KLR as a
protectorate. A refusal or loss of eligibility lets Natal proceed with KLR
and ZUL as the attackers. [ORA's appeal](../../events/sb_klip_river_county_events.txt)

## Appeal rejected at dispatch

In a replay from 1 April 1846, ZUL recognised KLR. The 1 May and 1 June
saves both contained KLR and both pending flags on Natal. Neither save
contained the ORA appeal, Natal's insurrection event or the secession play.
The appeal timer fell from 93 days to 62 while Natal waited.

In the installed macOS 1.15.2 build, `CTriggerEventEffect::ExecuteDerived`
calls `CEventType::IsValidToTrigger` before `CEventBackend::AddDelayedEvent`.
`UpdateDelayedEvents` checks eligibility again when the delay expires.
County creation set the appeal flag, tried to send the appeal and then set
the secession flag inside the delivery helper. ORA's event required both
flags at the first check. [Appeal requirements](../../common/scripted_triggers/sb_klip_river_county_triggers.txt)

County creation now sets both flags on Natal before scheduling ORA's appeal.
The regression fixture checks the destination trigger at the dispatch
statement. It reproduced the empty queue with the previous ordering and now
queues exactly one appeal. It also exercises both defensive leaders, ORA's
choices and loss of eligibility, duplicate detection, Natal's demands, British
backdown and ORA's eligibility to protect a restored Natalia.
A live replay from before recognition remains pending.
[Secession regression tests](../../tests/test_klip_river_secession.py)

## The Government of Zululand

In the November 1846 replay, both annexations were enforced on 10 November.
Natal owned Zululand outright in the December save. Its government event
requires a living Zulu protectorate that owns the whole of Zululand.

New secession plays use Make Protectorate as the primary demand against ZUL.
Once Natal has annexed KLR, holds the county and port, and the Zulu
protectorate exists, the peace callback transfers a British-held protectorate
to Natal and queues its three-way government choice after three days. Natal's
next monthly pulse handles peace effects that complete after the callback.
A protectorate-only peace with the county still independent leaves the choice
closed. Replay from before the diplomatic play opens to test the new demands.
[Peace settlement](../../common/scripted_effects/sb_klip_river_county_effects.txt) · [Government choice](../../events/sb_natal_interwar_events.txt)
