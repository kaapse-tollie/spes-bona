# CMF 1.67.3 / Victoria 3 1.15.1 compatibility patch

Base: commit `efa401a8944eabfa6e5577db18d6353c644d82e6`, exact
`release-1.67.3.zip`. The manifest pins the archive, pristine tree, each source
and replacement, fourteen native contracts, and the complete resulting tree.

Four payloads are byte-identical to `sb-1.15.0-r2`: seven ideology-category
helpers, the native dynamic-bar fallback, removal of the invalid empty demo
wrapper call, and removal of diagnostic logging. Four movement payloads add
only `can_secede_during_revolution = yes` to the six native 1.15.1 opt-ins:
religious majority/minority, cultural minority, Hindu/Muslim nationalist and
slave revolt. The remaining native default is `no`.

CMF's new labour ideology, anti-slavery helper and international-outliner changes
are inherited from the release. No additional GUI override is introduced.

Install using `python3 -B tools/sync_cmf.py` from the SB repository root.
`--check` is read-only and verifies the complete patched tree. `--force` retains
the patch; moving `--latest` is rejected. Preserve historical patch revisions.

The canonical patched tree SHA-256 is
`930ae6e5fe3100c17e59a1a0ca7a3ecc58fe707c7b4e445c5ef804cb2cad8266`.
Use `cmf_patch.tree_digest` to reproduce it: that function sorts `Path` objects,
not flattened POSIX path strings.

See the [implementation report](../../../Docs/compatibility/cmf_1_67_3_and_1_15_1_patch_2026_11_11.md)
and [pending DP checks](../../../Docs/compatibility/1_15_1_runtime_matrix.md).
