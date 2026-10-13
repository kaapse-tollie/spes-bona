# CMF 1.66.0 + SB compatibility revision sb-1.14.2-r1

This is a local patched distribution, not an official CMF release. The upstream mod ID,
metadata version 1.66.0, and launcher relationship remain unchanged. SB requires this
revision in addition to that version; metadata alone is insufficient.

Base: official `release-1.66.0.zip`, commit
`807c32ff42b75714a3a0e090c0db3357b5e46ed7`, archive SHA-256
`79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b`.

From the SB root:

```sh
python3 -B tools/sync_cmf.py
python3 -B tools/sync_cmf.py --check
```

The first command stages the verified release, checks the complete pristine tree and
each original file, applies four replacement files, verifies the complete patched
tree, and installs with rollback. `--check` is read-only and works offline for the
pinned patch. Repeated installation is idempotent. `--force` rebuilds the patched
distribution; `--latest` is rejected. No Workshop files are modified.

`manifest.json` pins both trees, all payloads, and twelve relevant Vanilla source/object
contracts: three territorial goals, seven ideology categories, and two building-browser
GUI types. Tree hashing uses sorted relative paths, a NUL separator, each file's SHA-256,
and a newline; `.git` and macOS `.DS_Store` are excluded. All other files participate.

The independent upstream-reviewable diffs are:

- `territorial-timers.patch`: restore territorial mirrors in Annex Country, Conquer State,
  and Return State; retain CMF's land-grab hook. No other goal rule changes.
- `ideology-categories.patch`: current Vanilla category bodies and tooltip/helper calls,
  retaining CMF's USFP/ANZ additions. Nihilists follow Vanilla's socialist category.

Both diffs apply to the exact release source. PR submission is deferred. A future CMF
release must be reviewed and deliberately repinned before this patch is retired.
