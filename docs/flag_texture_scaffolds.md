# Spes Bona Flag Texture Scaffolds

These are reference CoA blocks for DDS-based full-flag art in the same style
used by the local flag-reference example mod in `examples/3507724904`.

The live mod now already uses full-texture independent flag art for `CAP` and
`ABY`, converted from the supplied reference DDS files into engine-safe TGA
textures. This file remains as a handoff/reference note for any future colony
or dominion texture variants.

## Asset drop location

Put the finished files here:

- [gfx/coat_of_arms/textured_emblems](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/gfx/coat_of_arms/textured_emblems)

## Live and planned texture filenames

- `te_cap_independent_flag.tga` live
- `te_aby_independent_flag.tga` live
- `sp_CAP_independent.dds` source reference
- `sp_ABY_independent.dds` source reference
- `sb_cap_subject_flag.dds` optional future colony override
- `sb_cap_dominion_flag.dds` optional future dominion override
- `sb_aby_subject_gbr_flag.dds` optional future colony override
- `sb_aby_dominion_flag.dds` optional future dominion override

## CoA scaffold blocks

```txt
sb_CAP_textured_subject = {
	pattern = "pattern_solid.tga"
	color1 = "blue"
	color2 = "white"
	color3 = "red"

	textured_emblem = {
		texture = "sb_cap_subject_flag.dds"
	}
}

sb_CAP_textured_dominion = {
	pattern = "pattern_solid.tga"
	color1 = "blue"
	color2 = "white"
	color3 = "red"

	textured_emblem = {
		texture = "sb_cap_dominion_flag.dds"
	}
}

sb_CAP_textured_independent = {
	pattern = "pattern_solid.tga"
	color1 = "red"
	color2 = "white"
	color3 = "dark_blue"

	textured_emblem = {
		texture = "sb_cap_independent_flag.dds"
	}
}

sb_ABY_textured_subject_GBR = {
	pattern = "pattern_solid.tga"
	color1 = "red"
	color2 = "white"
	color3 = "blue"

	textured_emblem = {
		texture = "sb_aby_subject_gbr_flag.dds"
	}
}

sb_ABY_textured_independent = {
	pattern = "pattern_solid.tga"
	color1 = "white"
	color2 = "white"
	color3 = "white"

	textured_emblem = {
		texture = "sb_aby_independent_flag.dds"
	}
}
```

## Live swap points

If later DDS colony/dominion variants are added, swap the `coa = ...` values in:

- [common/flag_definitions/sb_flag_definitions.txt](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/common/flag_definitions/sb_flag_definitions.txt)

Current live wiring:

- `CAP` colony path -> `CAP_subject_colony` + `CAP_subject_colony_ensign`
- `CAP` dominion path -> `CAP_subject_dominion`
- `CAP` independent path -> `CAP_independent`
- `ABY` colony path -> `CAP_subject_colony` + `CAP_subject_colony_ensign`
- `ABY` dominion path -> `CAP_subject_dominion`
- `ABY` independent path -> `ABY_independent`

## Source conversions you mentioned

- [References/flags/sp_CAP_independent.dds](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/References/flags/sp_CAP_independent.dds) -> live `te_cap_independent_flag.tga`
- [References/flags/sp_ABY_independent.dds](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/References/flags/sp_ABY_independent.dds) -> live `te_aby_independent_flag.tga`

Open TODO:

- If you want distinct colony and dominion art later, provide dedicated DDS
  files and wire them over the current SAF / blue-ensign setup.
