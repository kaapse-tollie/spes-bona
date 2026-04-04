Spes Bona textured-flag asset handoff
====================================

Live active textures in this folder:

- te_cap_independent_flag.tga
  Active full-texture flag for fully independent Cape of Goodhope / Cape Republic.

- te_aby_independent_flag.tga
  Active full-texture flag for fully independent Albany.

Current live implementation:
- CAP colony uses the CAP-local `CAP_subject_colony` + `CAP_subject_colony_ensign` clone of the vanilla SAF setup.
- CAP dominion uses the CAP-local blue `CAP_subject_dominion` ensign.
- ABY colony uses the same CAP-local colony setup.
- ABY dominion uses the same CAP-local blue `CAP_subject_dominion` ensign.
- Only the fully independent CAP / ABY flags use bespoke DDS art.

Relevant script files:
- common/flag_definitions/sb_flag_definitions.txt
- common/coat_of_arms/coat_of_arms/sb_countries.txt

Source assets retained in References:
- References/flags/sp_CAP_independent.dds
- References/flags/sp_ABY_independent.dds

Conversion note:
- The supplied DDS sources are kept in `References/flags`.
- The live mod uses TGA conversions because the source DDS dimensions are not a
  clean fit for Tiger's compressed-DDS checks.

Open TODO:
- If you later want distinct colony or dominion art beyond the current shared
  SAF / blue-ensign setup, add dedicated DDS textures and wire them here.
