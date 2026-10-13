# CMF 1.66.0 + SB compatibility revision sb-1.14.3-r1

This is a local patched distribution for Victoria 3 1.14.3, not an official CMF
release. CMF's mod ID, metadata version 1.66.0, and SB's launcher relationship
1.66.* remain unchanged. The earlier sb-1.14.2-r1 directory is historical evidence.

Base: official release-1.66.0.zip, commit
`807c32ff42b75714a3a0e090c0db3357b5e46ed7`, archive SHA-256
`79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b`.

From the SB root:

```sh
python3 -B tools/sync_cmf.py
python3 -B tools/sync_cmf.py --check
```

The synchronizer verifies the archive, pristine tree, and five original files;
applies the replacement payloads in staging; verifies the complete patched tree;
then installs with rollback. Repeated sync is idempotent. --check is read-only and
rejects pristine, old-revision, partial, or altered installations. --force rebuilds
the patched distribution; --latest cannot replace it. Workshop files are untouched.

The five payloads contain:

- Vanilla 1.14.3 Annex Country, Conquer State, and Return State definitions, with
  CMF's land-grab validity hook retained. Infamy uses the new global GDP/population
  values; Vanilla's control rules and territorial mirrors remain intact.
- The previous seven ideology-category repairs, unchanged because their Vanilla
  bodies did not change. CMF's USFP/ANZ extensions remain.
- CMF's cultural movement file with six primary-culture comparisons migrated to
  explicit target_country = owner, and the value accessor supplied with (owner).
  All other CMF content in that file remains byte-for-byte recoverable by undoing
  only those API substitutions.

manifest.json pins original and replacement file hashes, both complete tree
digests, and sixteen Vanilla source/object contracts. These cover the three goals,
seven ideology categories, three cultural movements, two building-browser types,
and the construction-interaction map-list type. The GUI remains customized by CMF;
it is reviewed and pinned, not replaced.

Three independent upstream-reviewable diffs apply to the immutable release:
territorial-goals.patch, ideology-categories.patch, and cultural-majority-api.patch.
Applying all three must reproduce the replacement payloads. PR submission remains
deferred.
