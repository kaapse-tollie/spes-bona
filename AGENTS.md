# Repository Versioning

- Keep `descriptor.mod` and `.metadata/metadata.json` on the same version.
- Major: only when DP explicitly says so.
- Minor: significant thematic content or engineering work (for example colonial Natal).
- Patch: tweaks and elaboration within an existing thematic content bloc (for example the Natal state-split follow-through), plus fixes, balance adjustments, localisation changes, and maintenance.
- A batch of related commits may share one bump; apply the bump before pushing. For a mixed batch, use the highest applicable increment and reset lower components when incrementing a higher component.
- Complete the version update before committing or pushing, and verify the two version fields still match.

# Localisation Review Authority

- Treat every existing `# ### REVIEWED ###` marker as DP-authored approval. Never remove, downgrade, or reinterpret it.
- A `# ### REVIEWED ###` or `# ### TO REVIEW ###` marker classifies only the event or journal-entry namespace of the first non-comment localisation key after it. It never carries into a later event, journal entry, diplomatic play, or general localisation namespace.
- A numbered event namespace is exactly `<namespace>.<number>`. Only that exact ID and its period-suffixed keys, such as `.t`, `.d`, `.f`, and `.a`, belong to it; an underscore-suffixed or otherwise unrelated key does not.
- A journal-entry namespace is the longest exact source-defined `je_*` ID matching the key. Only that ID and its underscore-suffixed keys, such as `_reason`, belong to it.
- If the first non-comment localisation key after a marker is unrelated to an event or journal entry, the marker grants no classification to a later namespace.
- Use `# TO REVIEW (non-event/JE keys)` for new or changed diplomatic-play and general prose, and list every such file/key in `Docs/localisation_review_queue.md`. This plain comment is tracking only: it is not a review-classification marker and never authorizes a later event or journal entry.
- In a `REVIEWED` localisation namespace, change only spelling or grammar. Preserve the substantive wording, meaning, tone, and presentation.
- If mechanics require a substantive rewrite of reviewed localisation, stop and ask DP to supply or approve the replacement text before editing it.
