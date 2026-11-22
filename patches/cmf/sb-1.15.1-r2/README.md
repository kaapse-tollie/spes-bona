# CMF 1.67.9 for Victoria 3 1.15.1

Apply this revision to the official `release-1.67.9.zip` from commit
`9103c9cb4130d46cb18204d588def1266e5c1555`. The [manifest](manifest.json)
pins both release trees, the two replacement files and fourteen Vanilla contracts.

- The seven ideology-category triggers match Vanilla 1.15.1 and retain CMF’s Hail Columbia and ANZ extensions.
- The progress-bar scope trigger omits the unconditional `debug_log_details` directive.

Both payloads match the preceding revision byte for byte. CMF 1.67.9 supplies
the six movement secession flags, the dynamic renderers and the demo wrapper’s
required argument. Spes Bona owns the four-point gap in its shared outliner row.

From Spes Bona’s root, run `python3 -B tools/sync_cmf.py` to install or repair
the canonical sibling directory. Run `python3 -B tools/sync_cmf.py --check` to
verify its complete tree. The expected digest is
`58a74065dcd4f0073178b375062d4a17590ced9a15ba6d2bf643c669f3ddab05`.

The [compatibility report](../../../Docs/compatibility/cmf_1_67_9_update_2026_11_19.md)
records the release comparison, verification and replay scenarios.
