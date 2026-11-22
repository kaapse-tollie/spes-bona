# CMF 1.67.1 compatibility patch for Victoria 3 1.15.0

This patch is applied to the exact upstream release in staging by
[`tools/sync_cmf.py`](../../../tools/sync_cmf.py). The manifest checks the archive,
pristine tree, original files, replacement files and complete installed tree.
`--check` is read-only; failed replacement restores the previous installation.

The two payloads are:

- **Ideology categories:** current Vanilla's seven complete category definitions,
  including native tooltip wrappers and the distinction between character and
  interest-group ideologies, with CMF's USFP/ANZ extensions retained.
- **Progress-bar GUI:** native dynamic-bar rendering in CMF's journal and outliner
  fallback branches. The CMF-owned styling, target and drift paths are unchanged.
  Only `gui/com_gui_progressbars.gui` is additionally allowed by the patch loader;
  this is not general permission to patch arbitrary GUI or localisation files.

The former territorial overrides are retired from the active patch. SB's separate
annex/conquest overrides are based on native 1.15 and retain the British–Zulu
handoff and Swazi guard. CMF 1.67.1 already supplies the cultural-movement API
migration. Older patch directories remain historical evidence, not installation
inputs for this release.

Native source contracts in the manifest cover the seven ideology definitions
and the dynamic renderer on which these payloads depend. Other CMF and SB
overlaps remain subject to the main rebase's effective-definition review.

See the [implementation report](../../../Docs/compatibility/1_15_0_cmf_implementation.md)
for identities, checks and outstanding engine verification. The installer and
static checks do not establish successful rendering, movement calculations or
native war-goal settlement in the engine.
