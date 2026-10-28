# Carion Ironshield — test arena enemy

New heavy city enemy (`bulwark`), added alongside the two existing guards in TestCombat. Walks in from the left. Forest and Carion campaign populations are unchanged.

Behavior: 180 HP, 18-damage guarded thrust (0.56s contact, 1.10s animation), slow 64px/s shield-first approach, 350 score. Upright frontal protection remains active during movement, turning delay, attack windup/contact/recovery, and rear-hit recoil; ordinary heavy attacks do not break it. Ordinary attacks require a rear source at least 12px behind his center. As of v135, grabs are allowed from either side, and all four rage specials bypass the shield, including Lyra’s arrow rain. Incoming projectiles use travel direction, rather than the shooter's current position. Arrow rain uses the caster's side. Rear hits can stagger/launch/grab normally; a fallen/thrown/held guard is unguarded. Throws and landing damage retain their established behavior.

Facing changes only after the target stays on the other side for 0.70s; returning to the front resets the timer. Attack facing and target stay locked through the whole thrust, and the turn delay starts afterward. In co-op he targets the nearest living player outside attacks, with the same delay. Raised shield frames communicate his guarded side. Physical player collision prevents normal walking and ordinary charges through him. As of v135, dodges/backsteps/teleports pass through him while still colliding with scenery; the upper/lower lanes also remain open for flanking. Frontal shield impacts use the existing metal impact sound and sparks.

## Assets and prompt

Built-in image generation, one transparent 24-pose 6x4 sheet, reference: existing city-guard-00.png. `sheet.png` is the source; `preview.jpg` is the normalized contact sheet; shipped frames: `dist/assets/characters/city-bulwark-00.png` through `city-bulwark-23.png`. Normalizer uses one shared .88 scale, a 448px canvas and foot anchor y408, preserving pose height changes and separating components. Existing guard scale is retained in-game.

Prompt: Create a production sprite sheet for KillQuest matching the existing city guard's gritty 2D inked 80s fantasy cartoon style, bold black outlines and simple readable cel shading. Stocky armored human heavy city shield guard; dark steel closed helmet, muted purple tunic, one large rectangular iron-rimmed dark purple tower shield with tarnished gold crown, one short stabbing sword behind shield. Always face right, shield covering shoulder to shin throughout guarded movement and thrusts. Exact six-column/four-row grid, equal slots, consistent body scale and grounded foot baseline, generous transparent gutters, no scenery/text/slot outlines or detached/duplicated weapons/limbs. Row1: six shield-up walking poses, feet crossing through walk cycle. Row2: six shield-covered thrust stages, wind-up, draw back, start thrust, extended thrust, withdrawal, return to guard. Row3: two guarded idles, brace, shield recoil, rear hit recoil, crouched stagger. Row4: rear grab, lift, airborne knockback, falling, defeated, settled defeated. Keep head/torso size consistent; do not enlarge crouches or prone poses to fill slots. One solid shield attached to left forearm; one straight sword in right hand. All poses in one landscape transparent image.

## Verification

`checks/city-bulwark.cjs`: offscreen entry, all four heroes ground/air ordinary light/heavy frontal block and rear damage, all rage frontal damage, delayed facing/reset, complete attack facing lock, projectile arrival side, both-side grab/throw and directional body impact, guarded thrust windup/once-only hit, player block, physical flank, co-op retargeting, scoring, every frame state, campaign isolation.

Also passed city-guard, projectile-airborne, knight, loading, four-player-selection, carion-render, carion-city (including 6,848 edge checks), forest-arena-entrance, JS syntax and diff whitespace checks. Sprite contact sheet inspected. Browser/in-engine visual playtest remains unverified under the previous preview approval denial. No EXE build.

## v135 counter update

Front grabs and throws now work through every hero’s normal light-input grab flow. All four dodge paths pass through Ironshields in either direction; a per-update dodge marker also covers the dodge-ending frame and the outer collision sweep. Normal walking still collides, and scenery is never bypassed. Shield breaking by ordinary heavies remains disabled. Rage bypass uses its own explicit guard flag, separate from the ordinary heavy/launch break-guard flag. Kael’s slam, Garran’s charge, Selene’s firestorm and Lyra’s rain all deal frontal damage.

Passed city-bulwark, city-guard, knight, projectile-airborne, carion-render, JS syntax and diff checks. New tests cover actual full-frame dodge updates for all heroes/both directions, scenery blocking, frontal grab-to-throw input, and every frontal rage. Browser playtesting remains unverified.

## v136 jump counter

Airborne players (feet more than 8px off the ground) bypass the Ironshield's physical body collider. The exception applies only to this enemy, not scenery or attack protection. Grounded collision returns during descent/landing; an overlapping landing resolves to the nearest free side or lane. Tests use actual jump/world updates for all four heroes in both directions, restored ground collision, solid crates, and landing overlap separation. Passed city-bulwark, projectile-airborne, knight, JS syntax and diff checks. Browser playtesting remains unverified; no EXE build.
