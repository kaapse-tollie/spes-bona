# John Dunn and Mbuyazi — implementation record

`sb_court_dunn.001` introduces Dunn's support for Mbuyazi's succession. The new
namespace is **TO REVIEW**. This does not rewrite reviewed prose or claim that
his later chiefdom already existed in 1856.

## Evidence and adaptation

John Laband places Dunn and his gunmen with Mbuyazi during the late-1856 contest;
Mbuyazi was defeated on 2 December. The 29 October mobilisation follow-up moves
the scripted visit from November to **July 1856**, preceding the revised
**1 August** retirement eligibility by one month. This preserves time for the
offer before the slower claimant build-up towards December. It is a gameplay
scheduling adaptation, not evidence for a historical July meeting.
[Laband, *Historical Dictionary of the Zulu Wars*, “Ndondakusuka”](https://sahistory.org.za/sites/default/files/archive-files/john_laband_historical_dictionary_of_the_zulu_wabook4me.org_.pdf)

Walmsley's letter to Shepstone of 11 January 1857 distinguishes Dunn's private
trading/intermediary activities from official government service and describes
lending him guns. The letter is a defensive account of disputed conduct. It
supports avoiding an invented British military guarantee in the event.
[Primary letter, Fynn Collection 4, 9784–5, transcribed by Liz Stanley](https://www.whiteswritingwhiteness.ed.ac.uk/traces/shepstone-jan-1857/)

The description states the offer; the authored scene shows Dunn's practical
connections and its limits. It is not a historical quotation. Installed
`regency.2` supplies the public-description/private-scene model and
`commander_events.4` the two-character presentation. The small portrait icon is
present in the installed Vanilla tree.

## Contract

- Country helper: `sb_court_prepare_dunn_offer`, called monthly before succession
  reconciliation. Mpande must reign, the royal institutional court must be active,
  and both adult sons must remain eligible claimants. No unrelated-war gate.
- An open, still-valid offer reserves retirement until answered. Invalidated
  participants release that reservation on the next monthly check.
- Reuse `SB_ZUL_john_dunn` and following 7. Respect both the used-template check
  and the existing global creation receipt. A dead or absent Dunn is not
  resurrected or stolen from another country. The existing neutral 1857 creation
  remains a fallback when this visit never qualifies.
- Opening records the visit once but grants no allegiance. Acknowledging pledges
  Dunn's house to Mbuyazi in the **next succession**. Current allegiance and
  constitutional alignment are untouched. Existing successor commitments cannot
  be overwritten by a stale popup.
- No new army, combat modifier, noble status, later clientele bonus or permanent
  allegiance lock. Existing house Prominence carries the pledge through the
  normal coalition calculation.
- The existing defeated-coalition death rule still applies to Dunn. He survived
  historically, but this task does not add an exception to the agreed civil-war
  outcome. A historical escape would be a separate gameplay decision.

## Verification

Six executable focused checks in `tests/test_zulu_dunn_event.py` cover the date
boundary, button-only and once-only effects, existing/dead/foreign identities,
wrong country/ruler, minors, renounced rivals, an active crisis, stale choices and
unchanged present allegiance. They passed on 29 October 2026.

DP checks pending: paired portraits; tooltip names and wrapping; delivery in
July 1856; retirement waiting for acknowledgement; Mbuyazi's resulting
coalition; survival and ordinary allegiance changes after a different outcome.
