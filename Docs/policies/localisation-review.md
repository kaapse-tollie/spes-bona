# Localisation Review Authority

- Use British English spelling in player-facing text and documentation, including recognise, patronise, organise, and colour. Preserve script identifiers and quoted upstream names.
- Before writing event or journal flavour prose, read comparable installed DLC examples. Match their concrete actors, period voice and clear stakes; write original text for SB's circumstances. Keep implementation details in development documentation and gameplay explanations in tooltips.
- Treat every existing `# ### REVIEWED ###` marker as DP-authored approval. Never remove, downgrade, or reinterpret it.
- A `# ### REVIEWED ###` or `# ### TO REVIEW ###` marker classifies only the event or journal-entry namespace of the first non-comment localisation key after it. It never carries into a later event, journal entry, diplomatic play, or general localisation namespace.
- A numbered event namespace is exactly `<namespace>.<number>`. Only that exact ID and its period-suffixed keys, such as `.t`, `.d`, `.f`, and `.a`, belong to it; an underscore-suffixed or otherwise unrelated key does not.
- A journal-entry namespace is the longest exact source-defined `je_*` ID matching the key. Only that ID and its underscore-suffixed keys, such as `_reason`, belong to it.
- If the first non-comment localisation key after a marker is unrelated to an event or journal entry, the marker grants no classification to a later namespace.
- Use `# TO REVIEW (non-event/JE keys)` for new or changed diplomatic-play and general prose, and list every such file/key in `Docs/localisation_review_queue.md`. This plain comment is tracking only: it is not a review-classification marker and never authorizes a later event or journal entry.
- Prose in a `TO REVIEW` localisation namespace may be revised within the task's scope. Retain the review marker until DP approves the text; an agent's review does not grant that approval.
- In a `REVIEWED` localisation namespace, change only spelling, grammar or minor necessary syntax-only compatibility fixes. Preserve the substantive wording, meaning, tone, and intended presentation. For example, adding required `|q` escaping inside a quoted localisation-function argument is permitted when it preserves the approved text and intended rendering; this exception does not authorise new flavour, rewritten conclusions or substantive presentation changes.
- If mechanics require a substantive rewrite of reviewed localisation, stop and ask DP to supply or approve the replacement text before editing it.

---

The policy above is the authoritative localisation policy. Paths named in it are
relative to the repository root. Use the [localisation review queue](../localisation_review_queue.md)
for tracked non-event/JE prose. Related engineering lessons are in
[Tooltips, localisation and GUI](../pitfalls/presentation.md).

[Repository instructions](../../AGENTS.md) · [Topic index](../../common_pitfalls.md)
