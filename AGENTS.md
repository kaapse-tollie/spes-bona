# Repository Versioning

- Keep `descriptor.mod` and `.metadata/metadata.json` on the same version.
- Major: only when DP explicitly says so.
- Minor: significant thematic content or engineering work (for example colonial Natal).
- Patch: tweaks and elaboration within an existing thematic content bloc (for example the Natal state-split follow-through), plus fixes, balance adjustments, localisation changes, and maintenance.
- A batch of related commits may share one bump; apply the bump before pushing. For a mixed batch, use the highest applicable increment and reset lower components when incrementing a higher component.
- Complete the version update before committing or pushing, and verify the two version fields still match.

# Localisation Review Authority

- Treat every existing `# ### REVIEWED ###` marker as DP-authored approval. Never remove, downgrade, or reinterpret it.
- In a `REVIEWED` localisation block, change only spelling or grammar. Preserve the substantive wording, meaning, tone, and presentation.
- If mechanics require a substantive rewrite of reviewed localisation, stop and ask DP to supply or approve the replacement text before editing it.
