# Natal ultimatum, TRN origin, and CAP deployment follow-up

## Implemented

- Natalia's Seize Port Natal decision is disabled when the British ultimatum is
  active or has previously been dispatched. Britain's send option records a durable
  closure on Natalia before queuing delivery, so travel delay or later cleanup of
  the active ultimatum does not reopen this pre-ultimatum route. The decision displays
  a specific requirement; its new localisation key is queued for DP review.
- **TRN founding-priority change reverted at DP's request.** The original order is
  restored: `xD0A010`, `x8BDC4D`, `xA22DC2`, `xD02190`, `x6C1786`, then `x9A137B`.
  DP reported an ORA-held remnant in Transvaal and requested a revert rather than
  investigation or a new fix. Existing-TRN protection and territorial handoff remain
  intact; the later livestock-only starting-package change is retained.

The full integrated validator passes with zero failures (16 checks passed or warned;
the five previously deferred release gates remain warnings). Three new regression
tests cover decision eligibility, dispatch-time permanent closure, and founding
province precedence/fallbacks. No game was launched for this work.

## CAP deployment — unresolved pending test save

DP confirms that CAP is AI-controlled and its armies are already mobilised, sitting
at headquarters. Additional mobilisation is therefore not a supported fix.

The authored rejected-ultimatum play is GBR's protectorate demand against NAL, with
NAL's counter-demand targeting Cape-held Natal. CAP's initial army is based in the
Southern Africa HQ with two Cape Colony battalions. Its Port Natal province is a
separate Cape-held enclave. A local front there does not itself establish a traversable
land route from the army's current location. Actual ownership, military access,
transport, commander assignment, front selection and travel failure must be checked
in the failing campaign.

Initially `save games/` contained no files. A later inspection found autosaves; the
latest `autosave.v3` has metadata date 1836.11.1, no NAL country, no British Natal
ultimatum variable, and no CAP participant in its war manager. CAP is country 732;
its Cape Corps (formation 380) has current and target location state 425, home HQ
150, and AI tag `garrison`. This save does not capture the reported refused-ultimatum
war and cannot establish why a mobilised army stays idle during that war.

`ai.log` was empty, and the current game/error logs did not record CAP's deployment
decisions. A test save with the idle mobilised army during the failing war has been
requested. No speculative teleport, forced deployment loop,
army creation, or global AI define change was added. DP retains responsibility for
launching the game and reproducing the scenario.

### Later inspection: 1860 campaign

The 16:35 autosave now captures mobilised Cape Corps idling during the British
Natalia play. See [the current investigation](cap_frontline_investigation_2026_09_12.md)
for commander, unit, connected-theater and pre-war-stage evidence. The earlier
1836 save limitation above is historical; precise AI causation remains unresolved.
