# Bechuanaland Map Connectivity

`STATE_BECHUANALAND` intentionally uses the Kalahari impassable mask to keep the
Cape frontier and the interior corridor geographically distinct. Three passable
provinces on the northern bank of the Orange River form one isolated component:

- `x03B0A7`
- `x2CC006`
- `x798773`

This isolation is deliberate. It preserves the intended route through
Griqualand West rather than creating a direct crossing through the desert mask.
It is not a provisional pathing defect and should not be repaired by generated
spline edits.

`tools/map_connectivity_manifest.json` records the province-raster hash, the
within-state adjacency graph, and this single allowed component. The repository
validator fails if the raster changes, a province is added without a reviewed
adjacency entry, or any additional passable component becomes isolated. A raster
change therefore requires regenerating and visually reviewing the adjacency
baseline before updating the manifest.

Cold-start gameplay remains authoritative for fronts, pathing, and map object
locators. The static check proves only the reviewed province-level connectivity
contract; it does not validate spline-network behavior.
