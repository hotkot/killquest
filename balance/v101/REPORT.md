# KillQuest combat balance audit — v101

Ran 832 matched seeded fights before and after tuning (1,664 total), plus 40
controlled 30-second probes and defensive exploit regressions. These run the
actual combat simulation without Phaser rendering. Baseline source commit:
`4b164274301c8e5bdef968cbd0f988d2a3a78c4d`.

Each version includes 32 AI seeds × four heroes × six arena policies (light
combo/dodge/rage, adaptive mixed attacks, heavy-focused, heavy without rage,
aerial-focused, ranged positioning), plus eight starting layouts × four heroes
× two boss policies. The arena contains eight enemies covering dagger, sword,
bruiser, archer and dog types, approached from both sides. Encounters have a
90-second limit, three lives, no food or containers and empty starting rage.
Boss tests disable reinforcements to isolate the duel. All policies remain
identical between before/after; every run is retained in before.json/after.json.

## Changes made

- All heroes: minimum 0.75 seconds between dodge starts. Previously repeated
  inputs gave Kael, Lyra and Selene effectively continuous invincibility.
  Invulnerability duration, movement and teleport distance remain unchanged.
  Cooldowns belong to each player independently.
- Garran: shield bash direct damage 42 → 35, recovery ends at 1.05s instead of
  0.90s. Frontal guard covers windup/travel through 0.65s, then exposes him
  during recovery. Charge movement, launch and landing damage remain unchanged.
- Selene: forward ground heavy direct damage 45 → 35, duration 0.78 → 0.94s.
  Contact remains at 0.35s; range, throw, knockdown and aerial heavy stay intact.
- No light combo damage or rage-special damage changed.

## Controlled single-target damage

Stationary armored target at 110px, 30 seconds, repeated actual action inputs;
player position maintained to isolate damage and timing, no rage activation.
This is a controlled diagnostic, not a prediction of live boss DPS.

| Hero | Light DPS | Heavy DPS before | Heavy DPS after | Repeated-dodge invulnerability after |
|---|---:|---:|---:|---:|
| Kael | 59.9 | 40.2 | 40.2 | 53.2% |
| Lyra | 49.5 | 60 | 60 | 61% |
| Garran | 59.5 | 44.8 | 32.7 | 0% |
| Selene | 59.5 | 58.5 | 37.3 | 76.6% |

Garran uses directional shield protection rather than dodge invulnerability;
his 0% value does not mean his backstep has no defense. Lyra's higher arrow DPS
is single-target and interruptible; the melee heavies offer area control.

## Arena results after tuning

All heroes cleared all 32 light-combo/dodge/rage runs without losing a life.
Adaptive uses range and character-specific heavies; its decisions are heuristic.
Times below include failures/timeouts where present.

| Hero | Light/dodge clear time | Incoming damage | Adaptive clears | Adaptive time | Adaptive incoming damage |
|---|---:|---:|---:|---:|---:|
| Kael | 16.9s | 45.8 | 32/32 | 13.4s | 21.7 |
| Lyra | 16.3s | 24.2 | 29/32 | 22.5s | 61.4 |
| Garran | 13.5s | 34.6 | 32/32 | 11.4s | 19.4 |
| Selene | 17.8s | 47.9 | 32/32 | 10.2s | 16.5 |

The three melee/area heavy-focused policies now average about nine seconds to
clear the group. Lyra's bow-only policy clears none of these arenas: backing
away toward walls and repeatedly attempting lane-sensitive shots performs
poorly against dogs and flankers. Her knife policy clears every seed, so this
is not enough evidence to buff arrows; it does establish that bow spam does not
automatically dominate this scenario. Incoming damage includes fatal overkill.

## Boss outcomes after tuning

Eight varied starting layouts per policy; no reinforcements, no food. These
small samples show matchups and bot weaknesses, not player win probabilities.

| Hero | Light/dodge policy wins | Heavy-only policy wins | Mean heavy-policy incoming damage |
|---|---:|---:|---:|
| Kael | 6/8 | 0/8 | 342.6 |
| Lyra | 6/8 | 2/8 | 336.9 |
| Garran | 1/8 | 8/8 | 177 |
| Selene | 8/8 | 0/8 | 338.1 |

Garran remains the strongest shield-bash boss matchup, but now takes meaningful
damage and averages a lost life with that bot. Selene wins the light/range
policy but loses every heavy-only duel. No hero dominates every tested policy.
That does not prove perfect balance: the movement and dodge bots favor some
kits, the enemy formation is fixed across arena seeds, and only the first boss
is available. Actual campaign runs, controller feel and four-player synergy
still need human playtesting. No browser/controller playtest was performed.

## Regression verification

Defensive-loop tests verify vulnerable gaps under continuous input, actual
frontal hits during Garran's bash recovery in both facings, and independent
co-op cooldowns. Knight, witch, barbarian combo/aerial, huntress, rage, boss,
co-op, controller, full Forest progression and all-player rendering checks pass.
The older knight test was corrected to expect the already implemented thrown
body landing damage on a nearby third enemy.

Re-run: `node checks/balance-runs.cjs balance/v101/recheck.json` and
`node checks/balance-safety.cjs`. Override `BALANCE_SOURCE` to a baseline bundle
and `BALANCE_SEEDS` for a different arena sample size. The committed source and
raw run logs make this audit reproducible. No EXE was built.
