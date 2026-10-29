# Repository Versioning

- Keep `descriptor.mod` and `.metadata/metadata.json` on the same version.
- Major: only when DP explicitly says so.
- Minor: significant thematic content or engineering work (for example colonial Natal).
- Patch: tweaks and elaboration within an existing thematic content bloc (for example the Natal state-split follow-through), plus fixes, balance adjustments, localisation changes, and maintenance.
- A batch of related commits may share one bump; apply the bump before pushing. For a mixed batch, use the highest applicable increment and reset lower components when incrementing a higher component.
- Complete the version update before committing or pushing, and verify the two version fields still match.

# Game Launch Checks

- Leave launching Victoria 3 to check launch errors to DP. Do not launch the game for this purpose.
- Run static validation and inspect existing logs as needed. Record launch checks awaiting DP as pending.

# DLC Policy

- SB requires all Victoria 3 DLC, including DLC whose content SB does not directly use. Design against that baseline; do not add no-DLC alternatives unless DP changes this policy.

# Localisation Review Authority

- Use British English spelling in player-facing text and documentation, including recognise, patronise, organise, and colour. Preserve script identifiers and quoted upstream names.
- Before writing event or journal flavour prose, read comparable installed DLC examples. Match their concrete actors, period voice and clear stakes; write original text for SB's circumstances. Keep implementation details in development documentation and gameplay explanations in tooltips.
- Treat every existing `# ### REVIEWED ###` marker as DP-authored approval. Never remove, downgrade, or reinterpret it.
- A `# ### REVIEWED ###` or `# ### TO REVIEW ###` marker classifies only the event or journal-entry namespace of the first non-comment localisation key after it. It never carries into a later event, journal entry, diplomatic play, or general localisation namespace.
- A numbered event namespace is exactly `<namespace>.<number>`. Only that exact ID and its period-suffixed keys, such as `.t`, `.d`, `.f`, and `.a`, belong to it; an underscore-suffixed or otherwise unrelated key does not.
- A journal-entry namespace is the longest exact source-defined `je_*` ID matching the key. Only that ID and its underscore-suffixed keys, such as `_reason`, belong to it.
- If the first non-comment localisation key after a marker is unrelated to an event or journal entry, the marker grants no classification to a later namespace.
- Use `# TO REVIEW (non-event/JE keys)` for new or changed diplomatic-play and general prose, and list every such file/key in `Docs/localisation_review_queue.md`. This plain comment is tracking only: it is not a review-classification marker and never authorizes a later event or journal entry.
- In a `REVIEWED` localisation namespace, change only spelling or grammar. Preserve the substantive wording, meaning, tone, and presentation.
- If mechanics require a substantive rewrite of reviewed localisation, stop and ask DP to supply or approve the replacement text before editing it.

# Cross-Country Script Scope Checks

- Read [common_pitfalls.md](common_pitfalls.md) before changing or reviewing Victoria 3 scripts and when debugging regressions. Update it when an investigation establishes a new pitfall or prevention, including the cause and verification limits; label unresolved hypotheses explicitly.
- Do not turn internal delivery or scope failures into invented player-facing event content. Fix the faulty handoff; do not add redundant fallback choices or narrative explanations for implementation errors.
- When changing a cross-country event chain, trace the current scope, event/callback `root`, and the holder of each variable/container at every handoff. Entering `c:TAG` does not rebind `root`.
- Country helpers callable from another country's event or a diplomatic-play callback must capture their current actor or use an explicitly guarded country reference. Preserve `root` where it intentionally identifies the actual diplomatic play.
- Regression checks for such helpers must exercise a foreign event root and verify actor identity for ownership gates, rollback, container parents, and callback markers. Presence-only assertions do not establish correct scope routing.
- Keep static verification and engine verification distinct in reports; successful static checks do not prove in-game event delivery.