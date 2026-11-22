# CMF 1.67.2 compatibility patch for Victoria 3 1.15.0

This revision supersedes `sb-1.15.0-r1` for fresh campaigns. The exact release
archive and four payloads are verified in staging by
[`tools/sync_cmf.py`](../../../tools/sync_cmf.py), then installed atomically
with rollback. `--check` is read-only; unpatched or altered installs are rejected.

The ideology-category and native dynamic-bar fallback payloads are byte-identical
to r1. Their eight Vanilla source contracts and the exact GUI allowlist remain
unchanged. The two additional payloads only:

- remove the empty demo `run_in_com_progress_bar_scope` call, which omits its
  required `effect` argument;
- remove `debug_log_details = true` from the progress-bar trigger wrapper.

All remaining bytes of those two upstream files are preserved. CMF's anonymous
container, cache, saved-scope and wrapper behaviour remains upstream-owned.
SB uses native bar rendering and static templates, with no calls into this
container-backed styling API. SB's gameplay scripts and performance changes
are untouched; no save migration is included.

The [implementation report](../../../Docs/compatibility/cmf_1_67_2_patch_2026_11_07.md)
records source identities, preservation checks, installation and validation.
Journal/outliner rendering and fresh-start engine checks remain with DP.
