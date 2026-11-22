# Technology-gated diamond discovery — 18 October 2026

**Subsequent implementation.** SB now uses [owner-only annual surveys](frontier_playtest_2026_11_04.md#owner-only-surveys).
The comparison below records the earlier native implementation and its investigation.

**4 November playtest correction.** The installed engine treats multiple entries
in a mine's technology list as alternatives. The original three definitions
therefore admitted Prospecting on its own. The current stage lists require only
their respective later technology. Native split-region and foreign-investor
eligibility still apply. The May–September 1881 save evidence and the regional
thresholds are recorded in the [frontier playtest](frontier_playtest_2026_11_04.md).
The original assessment below records the design and evidence available in October.

Target: the existing SB 0.20.2 maintenance batch, Victoria 3 1.14.5 build 25629520.
All resource budgets, production methods, construction costs and technology thresholds
are retained. No game launch or save migration is included.

## Native evidence and implementation choice

Inspection of the installed executable established that `change_resource_potential`
does not add undiscovered reserves, even for a discoverable building group:

- `CStateRegionPersistentResources::ChangeResourcePotential` at `0x1012d7b78`
  increments the capped amount at resource offset `0x48`. Its new-resource constructor
  also initializes that capped field, leaving the undiscovered field zero.
- `CStateRegionResources::CalcCurrentMaxNumBuildings` at `0x101a01e88` uses capped
  plus discovered capacity minus depletion; undiscovered reserves do not enter it.
- `CStateRegionPersistentResources::AttemptDiscoverResource` at `0x1012d6a18`
  requires positive undiscovered reserves at `0x4c`, then checks the resource
  building's technologies and native owner/foreign-investor eligibility.
- `ForceDiscoverResources` at `0x1012d7714` transfers the undiscovered count into
  the discovered count. It does not convert capped capacity into reserves.

These are static native-code observations, not an engine replay. Merely connecting
the old diamond building to its discoverable group would leave the capacity grants
immediately usable. The implementation therefore follows Vanilla's oil/rubber pattern:
native `resource` entries with `undiscovered_amount`, and technology requirements on
their buildings. The three mine definitions use the same Diamond Mines labels,
production methods and economics; their group inherits `bg_mining` so
existing mining bonuses continue to apply. De Beers includes all three variants.

## Unchanged reserves and thresholds

| State | Undiscovered diamond levels | Required technology |
|---|---:|---|
| Transorangia / Vrystaat | 5 | Dynamite |
| Northern Cape | 4 | Pumpjacks |
| West Transvaal | 20 | Pumpjacks |
| Namaqualand | 14 | Pumpjacks |
| Northern Transvaal | 6 | Pneumatic Tools |
| Drakensberg | 6 | Pneumatic Tools |
| Botswana | 30 | Pneumatic Tools |
| Zambezi | 10 | Pneumatic Tools |

These are 95 native undiscovered levels, geographically stored from campaign start.
The technology makes them eligible for discovery; it does not reveal them. The eight
old grant flags and immediate-capacity notifications have no remaining consumers and
are removed. Native reserves are not re-added by repeated technology or ownership hooks.

Kimberley retains its original `building_diamond_mine` in ordinary `bg_mining`, its
Prospecting requirement, unchanged discovery triggers, and unchanged event helpers
creating one mine and granting nineteen more usable levels. Its event-driven 20 plus
the 95 undiscovered levels still give the same regional diamond horizon of 115.

## Separate pre-existing finding

The seven gold and one oil technology stages use the same capped-capacity effect.
Their earlier description as undiscovered additions was incorrect. Their scripts are
unchanged in this diamond-only revision; `RES-DISC-01` in the open audit register tracks
the separate correction. The immutable August research snapshot is not rewritten.

## Verification

Focused regressions cover unchanged per-state and regional totals, native reserve
fields, technology requirements, matching mine economics, removal of immediate
diamond grants/toasts, Kimberley's separate route and De Beers compatibility.
They do not execute the engine's discovery rolls.

- The original six resource tests passed before editing. The new diamond tests
  failed against the old immediate-grant setup, then passed with the native reserves.
- All 32 focused resource, diamond, De Beers/Rhodesian and content-smoke tests pass.
- The full validator ran 532 tests: one existing reviewed-localisation test failed
  and eight historical tests skipped. The localisation gate reports the same
  reviewed-text drift in Natal `.050` and Klip `.060`/`.080`; those files were not
  edited by this revision. Map data, native script contracts, resource totals,
  Vanilla/CMF override comparison and naval connectivity pass; existing deferred
  release and Tiger warnings remain.
- Tiger is advisory because its schema targets 1.13.5. Its final output reports no
  diagnostics in the changed diamond/resource files; unrelated 1.14 diagnostics
  remain. `git diff --check` passes.

DP's fresh-campaign case is `B145-27`: check each of the three technology thresholds,
zero buildable levels before discovery, later native discovery toasts/capacity,
split-state and ownership changes, save/reload without duplicated reserves, De Beers
eligibility/construction, and Kimberley's original event route. All engine results
remain pending.
