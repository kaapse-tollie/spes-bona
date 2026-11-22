# Victoria 3 1.15.0 — localisation gate approval

**Approved and applied, 7 November 2026.** DP approved all four proposed
reconciliations and asked to close the core rebase. The three affected baseline
entries now match the approved current text, and the stale general-prose queue
row is removed. No player-facing text or review marker changed. The localisation
gate and full validator pass; see the [closure record](1_15_0_closure_2026_11_07.md)
and [approval evidence](evidence/1_15_0_closure_2026_11_07.json).

The original review below preserves the exact comparison and approval boundary.
The preceding [smoke/validation record](1_15_0_fresh_smoke_bolivia_2026_11_07.md)
has no new static failures. Its one existing unit failure and duplicate
localisation gate resolved to the four items below. That inspection changed no
player-facing text, review marker, queue entry or approval baseline.

## Evidence and authority

The [review baseline](../../tools/reviewed_localization_baseline.json) names
commit `51c98bf32fc9f9049c99f858f5a558bdfde0dffe`. Its three flagged namespace
hashes match that commit's text exactly. The current definitions instead match
commit `1a3d7c3` (29 October checkpoint), so these differences predate the 1.15
port and its authorised syntax escaping. A checkpoint records the text; it
does not independently establish who approved a substantive rewrite.

The [localisation policy](../policies/localisation-review.md) permits spelling,
grammar and minor necessary syntax-only corrections within REVIEWED namespaces,
while preserving substantive wording, meaning, tone and intended presentation.
Its explicit boundary is: “If mechanics require a substantive rewrite of
reviewed localisation, stop and ask DP to supply or approve the replacement text
before editing it.” Retaining the two substantive changes below as the reviewed
baseline therefore needed established DP approval; refreshing all hashes would
otherwise conceal that distinction.

## Routine reconciliation

1. **Swazi queue row:**
   `sb_swazi_frontier.098.prerogative_after_blood_river` is a period-suffixed key
   within the already **TO REVIEW** event namespace `sb_swazi_frontier.098`.
   Its row in the [general-prose queue](../localisation_review_queue.md) is stale.
   Remove that row while retaining the event's TO REVIEW marker and all text;
   this would not grant approval or lose its event review classification.
2. **Retief event:** the only definition-line change in `sb_natal_crisis.050`
   is **`Pretoriius` → `Pretorius`** in `.f`. This is a permitted spelling
   correction. Reconcile that namespace's baseline with a recorded explanation;
   leave other wording and its REVIEWED marker unchanged.

## Substantive wording for DP review

All current lines below are in
[`sb_natal_crisis_l_english.yml`](../../localization/english/sb_natal_crisis_l_english.yml).
No new replacement prose is proposed by this inspection.

### `sb_klip_river_county.060`

The description's ending changed from **“the conquest and annexation of
Zululand”** to **“the conquest of the county and subjugation of Zululand”**.
Its preceding description and flavour quotation are unchanged.

The option changed from **“Fold Zululand by force into the Colony.”** to
**“Bring the Zulu's to heel.”** The latter is quoted exactly as currently stored.

### `sb_klip_river_county.080`

Previous description:

> The Zulu court's refusal has ended not in a settled boundary, but in conquest. British and colonial forces have overthrown the Zulu Kingdom, annexed its territory, and carried Natal's administration far beyond the Tugela. To the Colony's remaining Boer families, the victory offers no cause for celebration: the government they once fled now rules a wider country, and their wagons are already turning towards the Drakensberg.

Current description:

> The Zulu court's refusal to cede the Klip river territory has ended with their subjugation under the British Empire. However, to the Colony's remaining Boer families, the victory offers no cause for celebration: the government they once fled in the distant Cape now rules the boundary territories they inhabit, and so once more wagons are already turning towards the Drakensberg.

The title, flavour quotation and option are unchanged. This changes the described
settlement, so it cannot be classified as a spelling-only baseline update.

## Completion

DP approved the two current Klip River rewrites and the routine queue/spelling
reconciliation. Only the three corresponding baseline entries were refreshed;
the other 104 entries are unchanged. Swazi event `.098` remains **TO REVIEW**.
The full validator reports **15 PASS, two WARN, zero FAIL**, including the
localisation gate and unit suite. The historical failing run above is retained
as provenance rather than overwritten.

The [core rebase is closed](1_15_0_closure_2026_11_07.md). Unitemised stress-case
limits, five deferred release gates, resource/copper auditing and the agreed
glossary/JE extensions remain separate. No commit, publication or release-version
bump is included.
