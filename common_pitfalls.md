# Common Victoria 3 scripting pitfalls

Read this before changing or reviewing Victoria 3 scripts and when investigating
a regression. These notes record lessons from SB's bug investigations, not a
replacement for the installed game's script documentation and working examples.
Update them when a new cause or useful prevention is established. Label hypotheses
and unverified engine behavior; do not promote them into rules merely because a
static test passes.

## Crash attribution and generated map validation

- A native exception stack identifies the failing operation, not necessarily the
  cause of its invalid state. The 19 September 2026 ZUL-war crash enters Goods
  Transfer eligibility from AI treaty selection and fails in a market-capital
  port lookup. It does not identify the evaluated country or prove a Zulu event,
  mod defect or Vanilla defect caused it. Nearby log errors are leads, not proof.
- A second matching stack and matching gameplay snapshot establish a repeatable
  failure, not its proposed association with capitulation. The 20 September
  replay still saved ZUL at 97.1 support with zero demand timer progress. Native
  inspection found an unguarded market-capital-to-port-search boundary; the
  Goods Transfer eligibility wrapper now guards scope validity explicitly before
  evaluating the original native predicate. This mitigation awaits DP's replay.
  Do not call a guard a verified crash fix solely because static parity passes.
- DP subsequently completed ZUL capitulation after defending for roughly a month
  before advancing again. An altered-order replay can demonstrate a playable
  route without isolating a patch's effect: record both the changed timing and
  whether the new script was loaded before attributing the successful outcome.
- Check save references against their exact manager/database boundaries. IDs can
  repeat across managers; a broad numeric-record search can silently overwrite a
  state with another type. Dead countries can retain stale capitals normally,
  and omitted serialized fields may represent defaults.
- A valid configured port and a connected harbor in the shipped naval graph do
  not prove that the engine accepts the deployed spline. Anchor 8414308 was
  rejected at launch even though raster sampling and sea adjacency pass. Record
  that runtime discrepancy; do not certify it from hashes or static counts.
  See `Docs/compatibility/zul_war_crash_2026_09_19.md`; the cause remains unresolved.

## Country scope is not event ROOT

- Entering `c:NAL` from a Zulu event changes the current scope, not `ROOT`.
  Klip county creation compared Natal-owned provinces with Zulu's event root and
  rejected its valid input. Capture the current actor for reusable country helpers.
- In play callbacks, `ROOT` may intentionally identify the exact diplomatic play.
  Preserve that reference when recording or comparing the play; do not replace
  every `ROOT` mechanically with a country tag.
- Trace who writes and reads each variable. The Klip punitive queue wrote its
  pending marker on Natal, while a callback originally looked for it on Zulu.
- A fixed tag can later identify a different country. Rollback must return land
  to the original captured owner, including if that owner retags. Do not adopt
  a new country simply because it now has the expected tag.

## Preconditions must admit the intended scenario

- In a split state, Return State targets the opponent's actual state, not the
  holder's existing portion. Klip's Natal demand is NAL against the ZUL-owned
  `STATE_NATAL` state. ZUL's counter-demand targets NAL's different state object.
  Use `primary_demand = yes` for the added primary goal (installed 1.14.2 effect
  documentation), not an invented `primary` field.
- A two-demand victory needs both actual outcomes. Retaining original territory
  is not proof of gaining the disputed land. Check stable province ownership
  after split-state merging and the actual protectorate relationship. Preserve
  the route's eligibility requirement after transient war markers are cleared,
  so partial peace cannot accidentally open the government choice.
- Scope and eligibility restrictions are design requirements: agree them explicitly
  with DP before adding them. Do not invent peace, diplomatic-play, ownership,
  subject-status, or other broad gates because they seem prudent. Keep technical
  scope-validity checks tied to the actual operation; they do not authorize extra
  gameplay restrictions.
- Natal's annexed-Zululand government choice was blocked by an unrelated WTI–WAS
  war. Both settlement eligibility and punitive orphan cleanup required blanket
  peace/no active play, leaving a deleted Klip play reference in place from August
  through November 1851. Remove those broad gates from both steps; test cleanup
  followed by eligibility while unrelated wars/plays remain active. The saved
  blockers are confirmed; why the original war-end callback missed cleanup is
  unresolved, and engine delivery after this correction still awaits DP.
- British Natal is a colony. Ordinary aggressive-play permission therefore cannot
  be required for a bespoke Klip play that deliberately bypasses diplomatic
  status. The contradictory condition also caused monthly cleanup to mistake
  normal colonial status for permanent failure.
- Distinguish a busy participant from an invalid route. Britain's unrelated war
  blocked the Natal refusal response when a blanket British peace check was
  added. Check the relevant confrontation and actor, not unnecessary world peace.
- Test player and AI ownership separately. The British Zululand handoff accepted
  AI subject owners but excluded player Natal; adding a Natal-owned settlement
  also requires excluding Natal from the competing British handoff.
- Partial ownership and an existing unrelated ZUL are not equivalent to annexed
  Zululand. A restoration option must not silently take territory or another
  country's subject to manufacture its expected starting state.

## Dispatch, open popup, and answered choice are different states

- A short dispatch timeout permits retry if an event never opens. Once the popup
  opens, retain a reservation for its entire lifetime. Clear it on answer or
  terminal cleanup, not merely on delivery. Clearing it in Klip `.060.immediate`
  caused another popup at the next monthly pulse.
- In these country events, `duration = 3` means three months. Saved `.060` events
  created on 6 January expired on 6 April. Do not compare that lifetime with a
  20-day queue timeout as though both were measured in days.
- Every settlement option must revalidate before applying irreversible effects.
  A popup may remain open while ownership, subjects, or the active play change.
  Retain the once-only outcome guard as well as exact-play checks.
- Pre-war cancellation is not white peace. Calling the Klip war-result finalizer
  from pending-delivery cleanup produced `.081` before the player answered `.060`.
- Terminal cleanup must clear the launch-pending marker too, or monthly retries
  can continue after the route is finished.
- Do not add narrative filler or redundant options to explain a missing internal
  reference. Fix the routing failure. A normal story choice should not become an
  invented “this notice is irrelevant” branch.

## Use only the state machinery the lifecycle needs

- The Klip autosave contained open events and a country variable referencing a
  container that no longer existed. The exact engine cause of that disappearance
  was not established. Do not generalize this observation into “containers never
  work.” The once-only Klip follow-ups did not need containers and were simplified
  to country-bound delivery with pending/resolved markers.
- A helper named for restoring or normalizing a country may also schedule events.
  Reusing it from an option can reopen the very choice being resolved. Keep subject
  setup separate from event scheduling where both entry paths need the setup.
- Mark a restoration choice resolved only after the required country and subject
  relationship exist. Creating a country is not proof that the subsequent setup
  succeeded. Avoid extra speculative recovery frameworks; retain valid pending
  state and inspect the actual failure.

## Tooltip evaluation does not execute prior mutations

- A progress bar's `desc` labels the bar itself. The normal hover text comes
  from `GetPeriodicProgressBreakdown`, which lists declared weekly/monthly/yearly
  progress. A bar projected with `set_bar_progress` from a shared situation has
  no such breakdown. Use a local widget tooltip for its explanation; adding
  periodic progress solely to populate the tooltip would also change the bar.
- A hidden effect is still evaluated for tooltip construction. The refugee helper
  initialized a counter during execution, but its tooltip read that counter when
  no initialization had happened. Put reads behind an existence-guarded branch.
- Likewise, an unguarded named-container lookup after `create_container` can fail
  in preview. Initialize in the supported creation context and guard later reads.
- Delayed retries must supply every localization scope they use. Do not assume
  the original foreign event's saved country scopes accompany a monthly retry.
- Hide internal cleanup effects, such as `destroy_container`, from option text;
  use authored tooltips to communicate the actual gameplay consequence.
- Internal random scheduling can also leak into option tooltips. The Chiefdoms
  follow-up helper exposes four equal cooldown branches as “25% nothing happens.”
  That lottery schedules the next incident; it does not decide whether the current
  incident's main effect succeeds. Hide scheduling and display the real outcome.

## Check native identities and mechanics before duplicating them

- Renaming an IG or increasing its attraction does not change `pop_potential`.
  Vanilla 1.14.3 PB excludes aristocrats and most subsistence peasants. A chiefly
  constituency needs eligibility reviewed before attraction or strength tuning.
  IG strength, relative clout, supporter attraction and pop profession are distinct:
  a +25% strength modifier neither adds 25 clout points nor changes occupations.
- Treat a law variant's military package separately from its political purpose.
  SB Amabutho and Vanilla National Militia differ sharply in recruitment and
  building caps. Copying the latter for chiefly political influence would also
  change military capacity; record and agree those consequences explicitly.
- Vanilla already defines `ZUL_zibhebhu_kamaphitha` with a character usage path.
  SB separately creates `ZUL_zibhebhu_ka_mapitha`. The 1878.11.1 test save contains
  both as politicians, neither with the ruler role. Reconcile the creation paths;
  do not infer the installation failure's exact cause from duplication alone.
- Native Liberty Desire already includes economic dependence and endpoint scaling
  in `liberty_desire_weekly_change`. Replacing a scripted bar requires removing
  duplicate contributions and accounting for weekly versus monthly units. A raw
  modifier contribution is not necessarily the final displayed weekly change.
- The same native calculation checks the exact `lobby_pro_overlord` and
  `lobby_anti_overlord` types. New lobby IDs sharing their categories would not
  automatically receive those LD contributions. Prefer scoped names for native
  instances. Native maintenance also disbands lobbies whose members are all
  marginal; creating the requested membership is not proof the bloc will persist.
- A saved payment modifier proves it was applied, not that the intended bilateral
  cash transfer changed. Verify both countries' actual payments and modifier scope;
  Vanilla's Decrease Payments pact provides a targeted reference implementation.

## Preserve state across annexation deliberately

- Character-valued variables are references, not backups. The Klip archive kept
  Mpande/Cetshwayo IDs, but both character records were absent after annexation;
  the Crown option could only leave the generated ruler. The intermediate custom
  annexation/custody attempt was superseded by Return State plus Make Protectorate.
  Keep ZUL alive through this choice; do not reintroduce custody machinery.
- Capture both ruler and heir before transferring or exiling either: removing
  the ruler can change the heir accessor through succession. Restore the archived
  characters after country creation and subject setup. Do not consume the archive
  in the creation baseline before those steps have finished.
- A character hosted in CAP is no longer found by exile-pool-only searches.
  Follow the explicit host when returning the king; otherwise successor fallback
  can replace a surviving original. Static ordering/reference tests cover the
  transfer contract; engine survival and return still require DP's verification.
- Annexation can remove the country and its court before a restoration event.
  Archive the royal house and story-specific firearms state before the relevant
  annexation, then restore those records when recreating ZUL.
- Create the intended state footprint explicitly. A general Release Country UI
  action may include historical territory outside the settlement's agreed area.
  Compare Vanilla and Gates of the Bosphorus creation examples against the exact
  installed version before choosing scope and origin arguments.
- Do not release and re-annex a country merely to present a direct-rule choice.
  Owned territory and an existing protectorate need different entry handling,
  even when they share the final settlement branches.

## Verification must follow the whole chain

- Check each side's primary demand separately. The authored ZUL–SWZ conquest
  play never assigned SWZ's intended humiliation counter-demand; the autosave
  instead showed SWZ demanding a ZUL state. Assign the defender's primary goal
  in the exact launch callback and remove only its unwanted opening conquest.
  Keep ZUL's conquest and later territorial recapture mirrors intact. Static
  checks cover holder/target and removal scope; engine setup and settlement still
  require DP's check from before the play starts.
- Presence tests cannot prove runtime actor identity or delivery. Test foreign
  roots, normal colony status, held popups across monthly pulses, failed dispatch,
  replacement tags, and duplicate consumption using the actual script references.
- Inspect saved event creation/expiry dates, scopes, country flags, and play
  records together. Error-log timestamps alone do not identify the saved route.
  Preserve evidence before a new autosave overwrites it.
- Separate observed engine results, static verification, and pending scenarios.
  DP confirmed the simplified Klip follow-up works; that does not establish that
  every later chiefdom or settlement branch works. Game launches and engine
  testing remain with DP, as required by `AGENTS.md`.
- An already-open popup retains saved scopes. Reloading script text does not
  convert an old container receipt into a country receipt or undo a completed
  settlement. State the checkpoint required for a meaningful retest.

## Rebases and localization

- Compare upstream semantics before refreshing inventory hashes. Exact-path
  files, keyed replacements, GUI types, and dependency patches can overlap in
  different ways; a matching filename inventory alone is insufficient.
- Keep compatibility fixes reproducible and distinguish patched CMF from the
  immutable upstream release. Do not let ordinary synchronization erase the patch.
- Rebase every effective layer of a copied definition. In 1.14.3, updating CMF's
  cultural-majority movement alone leaves SB's CAP-specific replacement using the
  old API. Six comparisons now require an explicit target_country = owner; the
  value accessor takes (owner). Verify the installed Vanilla examples and preserve
  each layer's intended additions.
- A missing historical Steam manifest is not current-build corruption. Keep old
  evidence/schema checks, condition only historical reproduction on exact retained
  inputs and old installed-payload checks on their exact build. Current-target
  manifest and payload checks must remain mandatory.
- Preserve DP-reviewed prose and its exact namespace boundaries. A variant should
  use separately tracked new localization when the existing text remains valid
  for another route. `(DP) REVIEWED` and other supported markers must be classified
  explicitly rather than moved to make a bookkeeping check pass.

For detailed evidence, see the Klip, Natal refusal, Port Natal, and 1.14.2/1.14.3 reports
in `Docs/compatibility/`.


## Native movement contests and international journals

- Trace every caller before converting a shared political effect. Chiefdoms'
  `sb_zululand_shift_liberty_usuthu_5` is used by skirmishes, defections and refugee
  returns. Replacing it with one activism modifier would also change the refugee
  route, even though recruitment is the proposed consequence there. Inventory
  narrative callers as well as direct LD writes; the new mappings remain design
  proposals until implemented and verified.
- A projected modifier breakdown must reflect current modifier strength. The
  Chiefdoms attraction display currently reports a hardcoded +50% while the
  contest is active. Adding decay to its source modifier would make that display
  stale; inspect the live decayed value rather than treating an active flag as
  proof of full strength. This is a confirmed source-level dependency, not an
  observed engine defect in the still-unimplemented decaying version.
- Liberty Desire describes the subject relationship, not membership of a domestic
  faction. A high-LD chiefly government and a low-LD restored monarchy are both
  coherent. Do not label either as a faction victory from LD alone. Native
  `political_movement_support` also combines popular, military and wealth support;
  do not label it as only popular support.
- Subject-type eligibility can depend on the **overlord's** country type. In
  installed 1.14.3, Vassal requires an unrecognized overlord; Puppet accepts a
  colonial overlord such as NAL. The subject being unrecognized does not make
  Vassal the correct native relationship automatically.
- A copied movement ideology brings active-law satisfaction with it. In 1.14.3,
  positive stances on inherited laws lower calculated activism; opposition to two
  newly imposed laws does not erase approval of unrelated retained laws. Inspect
  the full native breakdown before attributing low activism to one factor.
  `character_ideologies` lists possible ideologies for pressured IG leaders;
  it is not a list of automatically stacked core movement platforms.
- International journal pulses can have **no country root** (see the installed
  `journal_entries.md`). Select the owning story actor explicitly before invoking
  a country helper; testing `country_definition` at the pulse root silently misses
  the global situation. The Chiefdoms weekly pulse now enters `c:NAL` explicitly.
- Script-value order matters: `value = 200` after a claimant-specific `add` resets
  the accumulated result. Initialize first, then add or multiply. A structural
  order check prevents the uSuthu claimant preference from being erased.
- Customizable-localization functions do not support `REPLACE:` prefixes. Use an
  inventoried exact-path shadow where a native function must change, and compare
  every untouched function plus the changed function's native fallback branches.
- Native subject drift identifies pro-/anti-overlord lobby **types**. Renaming
  those native lobbies preserves their clout contribution; inventing equivalent
  custom type names does not establish equivalent Liberty Desire behaviour.
- A movement's `political_movement_radicalism_add` changes calculated activism
  pressure; it is not a direct assignment to current activism or a monthly
  increment. The takeover must check actual `political_movement_radicalism`.
  Keep pressure, support, attraction and native LD distinct in UI and tests.
- For an automatic terminal settlement, reserve and apply it in the event's
  immediate effect; its acknowledgement must not repeat gameplay effects. Guard
  still-open earlier incident options against an already-ended contest. This
  avoids invented fallback choices and permanent pending popups blocking timers.
- Native civil-war initiation can race an event-based takeover. Suppress that
  initiation only for the designated contest movement while its contest flag is
  active; restore ordinary political behaviour after resolution. Static checks
  establish scope and threshold ordering, not same-tick engine execution.

- Check the **effective dependency definition**, not only Vanilla, before adding a
  replacement. CMF also replaces the absolutist movement and supplies Bavarocrat
  eligibility plus Grey PLP support/state-weight hooks. The ZUL exclusion must
  retain those hooks; the uSuthu derivative preserves them too. Pin the dependency
  object and compare the whole replacement after undoing only the intended gates.
- A count of 120 month-boundary pulses can expire before ten full years have
  elapsed. Use a ten-year timed marker for the actual deadline; a monthly counter
  may remain as approximate presentation. Test both dates disagreeing and victory
  taking precedence when the expiry and 99% threshold coincide.
