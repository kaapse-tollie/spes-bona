# Anglo-Zulu War Player Path — Live Design Record

Status: implemented

This file records the agreed design state while the Anglo-Zulu War player path is explored. It is not an implementation specification yet.

## Design problem

A player-controlled British Natal could not reliably bring about the Anglo-Zulu War under the former scripted ultimatum. That route was restricted to AI Natal and accelerated through AI Britain's Imperial Confederation logic. The player's practical alternative was to obtain responsible government so that Natal could start its own diplomatic plays, but that status is difficult to obtain and historically late: Natal received responsible government in 1893, whereas the Anglo-Zulu War began in 1879.

The design therefore needs to provide meaningful Natal-player agency without making an 1879 imperial war depend on ahistorically early responsible government or reducing Britain's role to flavour text.

## Evidence and current mechanics

- The former `decision_sb_anglo_zulu_ultimatum` and `sb_anglo_zulu.010` route required AI-controlled Natal.
- The implemented replacement is dispatched directly by AI Britain from monthly Imperial Confederation housekeeping and does not inspect Natal's controller.
- A normal Crown Colony cannot start its own diplomatic plays; the custom Responsible Colony subject type can.
- Cape Colony receives a special autonomy-pressure modifier worth +75 liberty desire after the Anglo-African national awakening. Natal has no equivalent pressure mechanism.
- Natal was representative but not responsibly governed in 1879. Responsible government followed in 1893.
- The supplied historical report describes the war as the convergence of local frontier disputes, Natal colonial pressure, and an imperial confederation policy culminating in Frere's deliberately coercive ultimatum. It cautions against modelling the war as a mere border accident.

Primary local evidence: `docs/Natal_and_Zululand_1847-1899_Report.md`, especially sections 4.2, 8.1, 8.4, and 8.9. The report is treated as research evidence, not as design instructions.

## Fixed constraints

- Player Natal needs a legible and sufficiently reliable route to the Anglo-Zulu War.
- Britain must retain a substantive imperial role in a war fought before Natal received responsible government.
- The war should be grounded in frontier, colonial, and imperial pressure rather than a single random raid.
- Responsible government remains a meaningful constitutional milestone and should not be an artificial prerequisite for the historical 1879 war.
- Existing AI historical scheduling still needs a viable path.

## Decision surface

1. Who has final agency over issuing the ultimatum: Natal, Britain, or a staged interaction between them?
2. What conditions allow Natal to press the issue, and how much timing flexibility should the player have?
3. What can Natal do if Britain refuses or delays?
4. Should the war path itself create constitutional pressure toward later responsible government?
5. What Natal-specific path should make responsible government achievable without simply copying Cape's national-awakening bonus?
6. How should AI Natal and AI Britain use the same system without reintroducing arbitrary stalls?

## First-choice options: constitutional agency

### A. Direct Natal ultimatum

Player Natal may issue the ultimatum once the historical gates are met, even as a Crown Colony. Britain automatically enters or sponsors the resulting war.

- Strong player reliability and simple presentation.
- Weakens Britain's political agency and makes imperial authorization implicit.

### B. Crown petition with an escalation guarantee

Player Natal first petitions Britain to issue an imperial ultimatum. Britain may approve immediately or delay/refuse according to visible conditions. A refusal does not permanently dead-end the player: Natal can build further imperial/frontier pressure and renew the demand, eventually compelling an imperial decision or taking a costly unsanctioned route.

- Preserves the three historical levels of causation and gives the player a controlled route rather than an AI lottery.
- Requires a small pressure sequence and careful limits on the override.

### C. Responsible-government prerequisite

Natal must first become a Responsible Colony, after which it may initiate the war normally.

- Uses existing subject mechanics cleanly.
- Makes the 1879 route depend on a status Natal historically received only in 1893, conflating domestic autonomy with Frere's imperial war.

### D. Britain-only initiation with stronger Natal autonomy pressure

Keep the war under British control and make responsible government substantially easier for Natal, allowing the player to declare independently if Britain does not act.

- Makes the autonomy system do double duty.
- Still leaves the historically timed route dependent on AI Britain and encourages ahistorically early responsible government.

### E. Scripted British initiation

AI Britain owns a reliable war scheduler. Natal has no request or acceleration action and may be controlled by either the AI or a player. Britain remains the formal initiator and immediately opens the standard vanilla `dp_annex_war` against ZUL when either route becomes valid. There is no custom ultimatum event or scripted delay; the ordinary diplomatic-play phase provides warning and escalation.

- Preserves the imperial character of the war and removes any responsible-government prerequisite.
- Avoids a multi-stage pressure system and makes the historical route independent of Natal's controller.
- Retires the custom locked Natal-initiated play from this route while preserving the separate postwar settlement handoff.

The automatic scheduler has two routes:

1. **Transit route:** the Imperial Confederation scheme is active, a participating Boer country has transit rights with ZUL, and NAL is a British colony. There is no date gate.
2. **1879 fallback:** the Imperial Confederation scheme is active or has previously resolved, the date is at least 1879, and NAL is a British colony. This initiates the same annexation play without requiring Boer-Zulu transit rights.

Both routes require Britain and ZUL not to have a truce. If their truce is still active when the other conditions become true, the monthly scheduler waits and may open the standard play after the truce expires.

For the fallback, “active or has previously resolved” maps to an OR between `sb_imperial_confederation_scheme_unlocked_var` and `sb_imperial_confederation_scheme_resolved_var`. The resolved flag includes both successful and failed Confederation outcomes.

After British victory, Britain owns the annexed territory. A British handoff decision then places the relevant British-held Natal/Zululand territory under NAL. AI Britain takes this decision automatically; it replaces the former automatic `sb_anglo_zulu.040` handoff event.

## Working recommendation

Option E is agreed. It decouples war access from responsible government, makes the automatic historical progression reliable, and keeps Britain as the belligerent that issues the ultimatum. Natal has no special action and its AI/player status does not alter the route.

Responsible government should be designed as a separate, later constitutional track. The Anglo-Zulu crisis may contribute political pressure to that track, but should neither require nor automatically grant it.

## Decision register

### Agreed

- Anglo-Zulu War initiation is entirely automatic; player Natal receives no request or acceleration action.
- AI Britain, not Natal, initiates the war and uses an annex-country war goal against ZUL.
- The transit route has no date gate and requires an active Imperial Confederation scheme, Boer transit rights with ZUL, and NAL as a British colony.
- The fallback route requires the Confederation scheme to be active or previously resolved, a date of at least 1879, and NAL as a British colony.
- A failed Confederation attempt counts as previously resolved for the fallback route.
- Britain immediately opens the standard vanilla `dp_annex_war`; there is no custom ultimatum event or scripted delay.
- Both routes are blocked by an active GBR-ZUL truce.
- The default Klip River outcome in which ZUL cedes `xBBCA32` creates a bidirectional GBR-ZUL truce as well as the NAL-ZUL truce.
- After victory, AI Britain hands the relevant territory to NAL through a decision.
- Responsible government is separate from Anglo-Zulu War access.
- The handoff decision replaces the former automatic `sb_anglo_zulu.040` event and retains its established coverage of British- and AI Cape-held territory in Natal and Zululand. Player Britain may take the same decision manually.
- The Klip River cession retains its existing 300-month (25-year) GBR-ZUL and NAL-ZUL truces.

### Deferred

- Campaign battle mechanics and the postwar settlement branches.
- Any Natal-specific Responsible Government boost. This will be reconsidered only after playtesting Natal with Zululand handed over, rather than balancing from the economically narrow one-state colony.
- The post-handoff audit should record liberty desire and its sources, relations and British attitude, relative power, GDP and population, fiscal capacity, political composition, and Zulu national-movement fervour/activism. Fervour is contextual evidence rather than an input in the current responsible-government acceptance formula.
