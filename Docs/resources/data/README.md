# Data Package

This folder is split into two surfaces:

- `raw/`
  - maintained inputs
  - includes both formula-driving tables and supporting source material
  - maintained evidence rows are append-only during the state-audit loop
- `derived/`
  - generated output
  - current caps, denominators, delta tables, and model surfaces

Classification rule:

- `formula-driving`
  - the builder reads this table directly into cap arithmetic
- `supporting source material`
  - research support, seed material, or context that does not directly enter formulas
- `generated output`
  - rebuilt from the raw package
- `review surface`
  - generated table meant for auditing or judgment, not direct arithmetic

Read these next:

- [raw/README.md](./raw/README.md)
- [derived/README.md](./derived/README.md)
