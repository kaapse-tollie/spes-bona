# Repository Versioning

- Every commit must include an appropriate mod-version update unless the user explicitly says not to change the version.
- Keep `descriptor.mod` and `.metadata/metadata.json` on the same version.
- Increment the minor version for new content, such as a new event chain, journal entry, country story, or comparable gameplay feature.
- Increment the patch version for fixes, balance adjustments, localisation changes, and maintenance that do not add a new content feature.
- Increment the major version only when the user explicitly requests it.
- For a mixed batch, use the highest applicable increment. Reset lower components when incrementing a higher component.
- Complete the version update before committing or pushing, and verify the two version fields still match.
