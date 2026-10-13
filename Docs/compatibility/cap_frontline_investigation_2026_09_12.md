# CAP frontline investigation — current autosaves, 12 September 2026

## Evidence inspected

Read-only inspection of `autosave.v3` and `autosave_1.v3` through
`autosave_4.v3`, captured at 16:34–16:35 local time. These cover 1860.2.1 through
1860.6.1. Extracted records are retained under
`/private/tmp/sb-cap-deployment-2026-09-12/`. No game or save was modified.

| Item | Latest save, 1860.6.1 |
|---|---|
| CAP country | 732, AI enabled |
| Cape Corps | Formation 380, sole CAP army, `ai_tag=garrison` |
| Mobilisation | `flags={ is_mobilized }`; mobilised in April, May and June saves |
| Current/destination | Both state 424, Cape Colony; no frontline destination |
| Home HQ | 150, CAP land HQ in Southern Africa |
| Force | One lancer battalion, unit 4278, 1,000 manpower; no CAP infantry unit |
| General | Benjamin Smith, character 33556747, assigned to 380, `order_type=advance` |
| Organisation/supply | 50 organisation, 70 supply |
| Play | 150994945, GBR (3) versus NAL (16777670), Make Protectorate |
| Stage | Started 1860.3.19, escalation 74, `war=4294967295` (no war yet) |
| CAP participation | Listed on initiator side |
| Front | 352321542, CAP theater 2342 against ORA theater 83887179 |

The army's province 4585 and CAP's frontline provinces are in theater 2342's
serialized province ranges. This is a connected Cape–Oranje front, not a stranded
Port Natal enclave. No naval transport is required merely to bridge separate
Cape-owned theaters in this case. This does not prove that the engine will accept
a particular movement or supply order.

Oranje's formation 381 and Natalia's 838861570 have this front as both current and
target location. Oranje's army is also tagged `garrison`, so that tag alone cannot
explain CAP's inactivity. Oranje has four battalions (2,256 manpower); Natalia has
two (2,000 manpower). CAP has only one, with no infantry. SB's starting Cape Corps
package defines one dragoon and one line-infantry battalion; the current save does
not establish when or why the infantry disappeared.

## Logs and script review

`ai.log` is empty. CAP's AI record includes deployment, commander-order and
formation-management goals and is enabled. Current error/game/debug/warning logs
do not identify a CAP deployment or pathfinding failure. Front-related errors
include the existing Dingane's Amabutho tooltip quoting failures; these are not
proof of a CAP movement failure. Other generic UI/script errors lack a CAP
assignment context and cannot establish this cause.

No SB or CMF AI define overriding garrison/front assignment was found. The
existing SB frontier deployment helpers mobilise TRN; they do not order CAP to
remain at headquarters. This inspection supports neither another mobilisation
call nor a missing-general fix.

## Conclusion and next engine check

The saves reproduce persistent pre-war idling by a mobilised, commanded, very
small CAP army despite a connected front and deployed opposing armies. They do
not yet capture this play after war begins. AI allocation of CAP's one-battalion
army is a lead, not a demonstrated root cause; the garrison tag is not sufficient
on its own.

DP's next diagnostic check is to manually order Cape Corps onto front 352321542
in this campaign, noting any UI rejection or route/supply failure. If accepted,
that separates automatic allocation from inability to move. A subsequent wartime
save with CAP still idle will establish whether the issue persists after the
play escalates. No forced deployment, army creation, global balance change or
save recovery was applied. Game launches and engine testing remain with DP.

## DP manual-deployment test — confirmed at 16:43

DP manually ordered Cape Corps to the front. The subsequent autosaves confirm
that the order succeeds:

| Save date | Formation 380 result |
|---|---|
| 1860.7.1 (`autosave_1.v3`) | Target is front 352321542; active land travel path from province 4585 to 4580, with travel progress recorded. |
| 1860.8.1 (`autosave.v3`) | Current and target locations both front 352321542; base camp state 422, province 4580. No remaining travel-progress block. |

At arrival the formation remains mobilised and tagged `garrison`, with
organisation 50, supply 70, delivered supply 4.6594 and a complete supply path
from its hub to the frontline camp. The British–Natalia play has now reached
escalation 100 and is attached to live war 16777241. Thus the result also verifies
that CAP can remain assigned to this front during the war.

The new log entries do not record a CAP assignment/pathfinding error. Extracted
records are retained separately from the earlier evidence under
`/private/tmp/sb-cap-manual-deployment-2026-09-12/`.

This test rules out an inability to reach or supply this particular front, and
rules out the garrison tag as an absolute deployment prohibition. The earlier
idling lies in automatic assignment/AI selection; the precise reason for that
selection remains unlogged. It does not establish that every isolated Natal
front is reachable, or which AI scoring rule should be changed. No runtime or
save edit was made during the inspection.
