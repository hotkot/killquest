# KillQuest
Fantasy arcade beat em up prototype using bundled Phaser 3.90, DOM menus, generated raster sprite animation, and one three-wave test arena.

## Controls
WASD / arrows move on both street axes. J attacks; repeat during a swing to buffer the next combo strike. Space performs the heavy finisher directly. K dodges. Escape pauses. Touch controls appear on coarse-pointer devices.

## Validation
`node --check dist/game.js`
`node checks/combat.cjs`
Browser QA unavailable in the build environment. Generated atlas reviewed visually and normalized to fixed 256px frames with consistent feet anchors. Generation can introduce small pose/proportion differences; this is a first prototype, not a final hand-authored animation pass.

## Assets
Built-in image generation produced `dist/assets/quarter.png`, `fighters.png`, and `menu-hero.png`. Briefs: modern inked, cel shaded fantasy arcade art; a red-haired axe barbarian and green-hooded bandit in 24 animation cells; a torchlit medieval bandit street with empty walkable foreground. An extraction edit removed the sprite atlas background. Frames were then cropped, normalized at shared scale, and foot-aligned. Phaser license is included in assets.

## Animation revision
Sprites load as 66 individual padded 320px RGBA textures, not grid crops. Full-image connected components isolate complete silhouettes before normalization, preventing neighboring boots and axe heads from contaminating frames. Eight-frame walking clips use accumulated movement distance; each axe strike has six poses and its impact occurs halfway through the clip. Bandits have an eight-frame stab with damage at frame 4. Foot pivots remain at y=308.

Built-in image generation added four sheets from the shipped character references: barbarian walk (8), bandit walk (8), barbarian attacks (18), bandit stab (8). Briefs preserved costume/palette/facing and requested alternating contact/passing steps, windup/impact/recovery poses, transparent backgrounds and gutters. Source sheets live in source-art; processed runtime assets live in dist/assets/characters.

Additional validation: `python checks/sprites.py` checks alpha padding and detached fragments for every frame; combat checks verify every pose is reachable and that damage aligns with the impact frame. Browser playtesting remains unavailable.

## Body anchor and gait revision
All 66 runtime sprites now use 448px canvases and manually reviewed pelvis landmarks registered to (224,300), with a stable render origin at (224,408). Weapon extents and stepping feet no longer determine body position. source-art/registration.json records the source landmarks and translations, and scripts/center_sprites.py reproduces the centering. Validation confirms no nontransparent pixels were clipped.

Both walk cycles were regenerated with the built-in image tool using the original character design plus an explicit eight-pose leg guide. Frames 2 and 6 show lifted knees and calves crossing the supporting leg; the near/far legs exchange stride roles across the cycle. New raw sheets are source-art/hero-walk-v3.png and bandit-walk-v3.png; runtime frames remain dist/assets/characters. The guide specified alternating contact, lift, crossed passing and extension poses with constant torso position.

## Slide repair and fluid attack revision
The old dodge source had truncated boots. A new complete eight-frame sequence replaces it with entry, low slide, braking and recovery. Slide frames share a torso X anchor while preserving their ground baseline, allowing deliberate vertical crouching. Displacement follows a cosine ease over 151px instead of starting and stopping at constant speed; dodge invulnerability no longer flashes the sprite.

Three new twelve-frame barbarian strike clips and a twelve-frame bandit stab replace the earlier attack clips. Their halfway impact poses match gameplay damage timing. Hit-stop is shortened to 28ms. The built-in image tool generated each whole sequence from the shipped character reference, requesting small incremental windup, impact, follow-through and recovery poses, complete feet/weapons, transparent gutters and consistent proportions. Raw source sheets are source-art/*-v4.png; 96 padded runtime frames are in dist/assets/characters. `action-anchors.json` preserves reviewed body landmarks.

Validation passes for all twelve attack poses, eight slide poses, monotonic/eased dodge distance, impact timing, combat results, transparent gutters, detached fragments and lossless centering. Browser playtesting is unavailable in this environment.

## Lateral blade orientation revision
The first horizontal strike's twelve-frame sprite set was edited with the built-in image tool to rotate the double-bitted axe head around its haft, presenting the cutting edge in the horizontal swing plane. The edit brief preserved body poses, grips, haft placement, frame sequence and transparency. The edited source sheet is source-art/hero-slash-v5.png; runtime hero-slash frames retain the standing scale and reviewed body registration. Sprite bounds, alpha integrity, animation reachability and combat timing checks pass. Browser QA remains unavailable.

## Continuous combo revision
Buffered chains now cancel the slash recovery at 0.33s and the rising-cut recovery at 0.36s. Two new eight-frame transition clips carry the sideways follow-through into a low rising-cut wind-up, then the rising-cut momentum into the overhead wind-up. The following strikes start at pose 3 and pose 4 respectively, skipping neutral guard resets. A buffered input during a bridge queues the next strike; damage is disabled on bridge poses and triggers once per real strike. Unbuffered attacks retain their full recovery.

Built-in image edits generated whole transparent transition sheets from the exact start/end poses, requesting continuous axe arcs, consistent body proportions and no idle pose. Source sheets are source-art/hero-link-one-v6.png and hero-link-two-v6.png; runtime textures are dist/assets/characters/hero-link-*.png. Each bridge's first/last frame is locked to the exact adjacent shipped pose after normalization, with body landmarks retained in action-anchors.json.

`node checks/combo-flow.cjs` passes for all sixteen bridge poses, a continuous three-strike chain, transition input buffering, omitted guard resets, exactly three damage events and standalone recovery. Sprite checks confirm pixel-identical endpoint seams and transparent padding across 112 frames. Browser playtesting remains unavailable.

## Combat audio and music revision
Placeholder oscillator beeps are replaced by 31 original PCM samples: three variations each of axe whooshes, impacts, heavy impacts, and exertion/pain/defeat grunts for each character; plus slide scrape, UI click and result stingers. Grunts use glottal-source/formant synthesis and are stylized synthetic vocals, not recorded actors. Whooshes trigger before contact; impacts and pain/defeat responses trigger only on confirmed damage, once per strike. Variants avoid immediate repetition, with slight pitch variation, spatial panning and output compression.

`Quarter Forge` is an original locally composed 60-second, 32-bar track at 128 BPM, combining distorted power-chord/chug synthesis, electronic bass, dance drums, a breakdown and melodic climax. It is procedurally synthesized, not generated through a music AI service (none was available). The stereo MP3 plays during the level and loops; music and effects have separate persistent mute/volume controls in pause. Audio initializes after the player's start gesture; pause stops effects and preserves music position, and menu return stops music.

Reproduce with `python scripts/generate_audio.py`. Assets are dist/assets/audio; composition information is manifest.json. Validation: combat/combo checks, audio-events.cjs (correct response events), audio-mixer.cjs (lifecycle/settings), and audio-assets.py (31 varied non-silent samples, peak limits and stereo MP3 decoding). In-browser listening/playtesting remains unverified.

## Softer and less frequent character vocals
The barbarian emits exertion only when starting an attack/chain; both combo transitions are silent. Bandits no longer vocalize on attacks or ordinary hits, only on death. A new softer vocal bank uses a smoother harmonic source, gentler envelopes, less breath/roughness and high-frequency energy, lower sample peaks and quieter vocal mixing. Random selection excludes the previous sample uniformly.

The library now contains 12 barbarian exertions, 6 pain responses, 4 death responses and 6 bandit death cries (41 total effects including other sounds). These remain stylized synthesized voices. Generate base effects/music with scripts/generate_audio.py, then apply scripts/refine_voices.py. Existing music is unchanged by the refinement. Tests cover one opening grunt per complete combo, no bandit effort/pain events, death responses, random variant range/repeat avoidance, all files, audio lifecycle and PCM levels. Browser audition remains unavailable.

## Pronounced battle vocals and flesh-cut layers
The opening exertion library was rebuilt as twelve deeper, chestier battle exclamations with richer harmonics and clearer vocal formants. Bandit deaths use six longer, strained descending cries. These are original synthesized vocal designs inspired by a forceful sword-and-sorcery barbarian tone, not actor recordings or voice imitations. Vocal peaks/mix gains are increased; opening grunts and enemy deaths briefly duck the music and receive priority when effect voices are full. Combo follow-ups and ordinary enemy hits remain vocally silent.

Six new flesh-cut variations layer wet low/mid transients, fibrous tearing noise and a body thud. They play only on confirmed barbarian damage, with a lower/slower variant for heavy blows, layered with a reduced physical impact sample. Total effect library: 47 files. Reproduce after earlier generators with scripts/strengthen_combat_audio.py; music is unchanged. Checks cover vocal sample prominence, variant uniqueness, confirmed-hit slicing and no slicing on misses, audio lifecycle and combo behavior. Browser audition remains unavailable.

## AI Voice Generator integration
Procedural voice files are replaced with actual output from the user-selected AI Voice Generator plugin (`create_audio`). Each individual nonverbal transcript was generated separately: deep voice Huh/Hah/Hrrgh/Hyah for exertions; deep Argh/Urrgh for pain/death; normal Aargh/Aaagh/Urrgh/Aah for bandit deaths. The available plugin is TTS with six voice presets and no exposed acting/emotion controls; these are voice-model-generated utterances, not professionally acted recordings. Perceived realism still requires listening review.

Source MP3s and full-generation/preview URLs, transcripts and voice presets are archived in source-audio/ai-voice-provenance.json. Runtime samples are silence-trimmed, high-passed at 65Hz, lightly compressed and level-matched. Hero death variants use a slight duration extension. Runtime selection now uses four opening exertions, two pain responses, two hero deaths and four bandit death cries. The earlier first-strike-only/death-only triggers, music and flesh-cut effects remain. 31 total effect files pass decoding, levels, event and mixer checks. Reinstall with scripts/install_ai_voices.py; procedural voice generators are historical and must not overwrite the current AI bank.

## Sustained arcade-style vocal revision
New AI Voice Generator takes use elongated nonverbal spellings (Aaaaaaaaargh/Aaaaaaaaagh/Uuuuuuurrrrgh and deep variants) rather than short Argh. The tool returned approximately 0.49–0.64-second voiced takes. To achieve the requested sustained cry, the voiced middle is extended using pitch-preserving FFmpeg tempo processing while preserving the original consonantal onset and release. All six hero/enemy death samples now last approximately 1.02–1.34 seconds. This improves duration/mix presence but does not add acting controls to the underlying TTS tool; performance quality remains subject to listening review.

The four existing attack takes retain their short timing and receive restrained presence EQ, gentle saturation, tighter leading silence and a subtle 32ms room reflection. Death cries duck the music for their actual length plus 150ms and receive critical-voice priority. Direction uses the readable, punchy arcade-brawler aesthetic requested by the user, without sampling or copying Streets of Rage 4 audio. Original generated take URLs/transcripts/presets live in source-audio/long-cries-provenance.json; source MP3s are retained. Reproduce with scripts/refine_arcade_voices.py after the AI installer. File/event/mixer checks and all death-duration checks pass. Browser audition remains unavailable.

## Enemy blood effects
Confirmed barbarian hits emit directional red droplet bursts from the enemy torso. Droplets use gravity, short streaks and varied sizes; heavy and fatal hits increase spray density. Droplets leave layered dark-red ground stains on landing, fading over their final three seconds. Ground stains render below combatants and airborne blood above the playfield. Misses produce no blood, restart clears all effects, and pools are bounded to 180 transient particles and 90 stains. No sprite artwork or combat/audio rules change. `node checks/blood.cjs` passes alongside combat, combo and audio-event checks. Browser visual QA remains unavailable.

## Subtle vocal echo and volume trim
All twelve current vocal samples receive a -3dB direct-level trim and two quiet low-pass-damped echo taps at 85ms (13%) and 170ms (5.5%). The short tail adds room without a long wash. Only voices are processed; weapon, slicing, impact and music assets are untouched. Dry masters are preserved in source-audio/dry-v12; scripts/add_vocal_echo.py reproduces the pass without cumulative processing. Audio checks verify the reduced direct/overall level, delayed tail and no clipping, with event/mixer checks passing. Browser listening remains unverified.

## Tactical bandit positioning
Bandits now have pressure, flanker and harrier roles with orbit/commit/retreat decisions. They stage outside axe range, alternate upper/lower lanes, route around the player to flank, separate from nearby allies and retreat after strikes or hurt recovery. Harriers can react to a visible 180ms player wind-up with a short withdrawal. Movement and reaction speeds remain below the player; enemies do not gain invulnerability.

An attack director reserves one commitment at a time in early waves and up to two in wave 3, spacing starts by 350ms and prioritizing bandits waiting longest for a turn. Stab facing locks during the telegraphed animation, so crossing behind or leaving its range can evade contact. Corner-aware lane choices and clamped arena coordinates avoid positioning stalls. Standalone combat fixtures are stationary by design; checks/bandit-ai.cjs simulates real AI for positioning roles, turn sharing, retreats, flanking, lane variation, locked wind-ups and edge recovery. Combat/combo/blood/audio-event checks also pass. Browser playtesting and difficulty feel remain unverified.

## Forward spinning heavy attack
The overhead heavy chop is replaced by a twelve-pose full-body 360-degree axe spin showing front, left and back views. It advances 120px in the locked facing direction using smoothstep motion from 0.12–0.66s, strikes once at 0.54s, and recovers at 0.80s. Damage remains 42; the sweep reaches 140px on either side within the existing depth lane and knocks victims outward. Arena limits clamp travel. A new eight-pose transition carries the rising combo strike into spin pose 2 without a guard reset, retaining exact endpoint seams.

Built-in image generation produced the full spin sheet and transition from shipped character/pose references, with consistent costume, full feet/axe and transparent padding. Raw sources are source-art/hero-spin-v15.png and hero-link-spin-v15.png; runtime names are hero-spin and hero-link-spin. Reviewed pelvis landmarks preserve fixed body registration. checks/spin.cjs passes for both directions, all twelve poses, smooth travel, hit timing, single damage, two-sided sweep, outward knockback and edge clamp. Existing combat/combo/AI/blood/audio-event and sprite checks pass. Browser playtesting remains unavailable.

### v16 — Separate combo finisher and heavy spin
The J combo again ends in the stationary overhead chop, with its original connecting sprite frames. Space / Heavy keeps the advancing spin and two-sided sweep. Both retain their heavy impact damage.

### v17 — Heavy override and jumping
Heavy cancels any light combo phase into its dedicated forward spin; further attack presses cannot turn the spin into a combo or restart it. Controls: J light, K heavy, L dodge, Space jump. Jump has eight centered sprite poses, steerable ground movement, a separate height arc and grounded shadow. Bandit strikes miss while the hero is sufficiently airborne. Mobile actions use a compact four-button cluster.
Jump artwork generated as one transparent strip from the barbarian reference, then normalized with a shared scale and pelvis registration; generation prompt: eight right-facing guard, crouch, takeoff, ascent, tucked apex, descent, landing and guard poses, matching costume and axe, no scenery or detached parts.

### v18 — Unclipped jumps and airborne chop
Rebuilt jump sources on a 400px intermediate canvas to recover the full boots previously clipped before registration. J or K during takeoff/ascent initiates a dedicated eight-pose airborne axe chop with one forward 35-damage hit, directional knockback, blood and existing impact sounds. Jump steering, height and ground shadow remain continuous, with one chop per jump.

### v19 — Dedicated jump combo
J or K during the jump starts the existing aerial chop. Additional presses buffer a rising cut, then a descending overhead finisher (35 / 28 / 45 damage). The three-stage sequence uses registered axe poses, preserves facing, and interpolates jump height through the transitions. Stopping after the rising cut eases into a landing; the full finisher reaches the ground at impact. Each stage hits once, with reduced intermediate knockback to keep enemies in combo range. Ground combos and standalone heavy spin stay separate.

### v20 — Flashier aerial second strike
Replaced the reversed chop/rising cut with a dedicated airborne 360-degree axe spin, front/side/back poses and an elliptical gold axe trail. The rotation gets 0.56 seconds to read, then finishes axe-up to connect into the overhead landing chop. Damage and forward hit rules remain unchanged.

### v21 — Sword bandits and archers
Three waves now contain four enemies each (12 total), mixing dagger bandits, red-cloaked sword bandits and ochre-hooded archers. Sword bandits have more health, a 145px reach and a slower 15-damage slash. Archers kite at 230–540px and lock their aim during a visible 0.65s wind-up, then release finite-speed 9-damage arrows. Change lanes, dodge or jump to avoid shots; hits interrupt bow wind-up. Each new type has eight walk poses, six attack poses, idle and hurt frames. Death voices, blood and existing hit reactions apply to both. Arrow effects are bounded and reset with the level.

### v22 — Rage meter and special ground slam
Confirmed ground/air hits build 4 rage per enemy hit; damaging melee or arrow hits remove 3 rage. The meter eases visually, caps at 100 and glows when ready. I (or the touch Rage button) spends a full meter on an eight-pose ground slam: 70 damage in an elliptical area on both sides, outward knockback, arrow clearing, shockwave and brief invulnerability. The special can cancel a ground combo, requires grounded control, cannot be interrupted by regular action presses, and cannot refill itself. Reset clears rage.

### v23 — Roar, leap and explosive slam
Rage now takes 2.5 seconds: arms-open battle cry, 180px leap, then a violent impact at 1.65s with a bright flash, three broad shockwaves, radial ground streaks and 100 sparks/debris. Twelve registered poses preserve the axe and feet. Added dedicated AI-generated war cry with short damped echo and music ducking. New runs/restarts start with full rage for this test level. Archer projectiles now render as hand-painted steel-tipped, feathered arrow sprites rotated along their existing flight paths.

### v24 — Contextual grabs and directional throws
A fresh J press within 42px and the same depth lane grabs the nearest standing human bandit. The barbarian and held enemy enter dedicated grip poses, with invincibility throughout the hold. J again launches the throw; left/right movement selects its direction. An unspent hold breaks after two seconds, with a brief regrab cooldown. The throw has lift/release animation, a bounded flight arc and human-specific tumble/landing sprites, then applies 55 fall damage once on landing. Survivors lie down and recover; fatal falls count once and play the enemy death voice. Heavy attacks remain separate, and jumping/rage cannot interrupt an active hold.

### v25 — Heavy launches, pit, entrances and three lives
Heavy spin impacts now launch hit enemies, including fatal hits, with separate 25 fall damage for survivors. The stone-edged pit at the right side kills grounded players/enemies and descending throws; invincibility does not protect against it. Shared enemy pathfinding routes around the pit, including ranged positioning. Each wave walks in from alternating offscreen edges instead of appearing in the arena.
The barbarian starts with three lives. Death spends one, then a safe-position respawn drops from above after a short pause, restores health, grants brief invincibility and knocks nearby enemies down without dealing damage. Defeat occurs after the third death. Restart restores three lives and full rage for testing.

### v26 — Living idle stance
Added an eight-pose 1.28-second idle cycle with subtle breathing, grip/head shifts and wind-blown hair. All poses share a single scale and planted foot baseline; the idle clock resets during movement/actions so recovery returns cleanly to the neutral pose.

### v27 — Painted rage effects and no enemy indicators
Removed enemy melee warning circles/triangles and archer aiming lines; weapon wind-up animations remain. Rage now renders an eight-frame hand-painted impact burst with four flying gold spark variants and four stone debris sprites. Vector rage rings, streaks and debris drawing were removed. The existing particle trajectories use sprite instances, reused between frames and destroyed after expiry/reset; the impact keeps camera shake and a short camera flash.

### v28 — Bilateral aerial spin and jump heavy slash
The second J aerial-combo spin now hits enemies on either side once, with outward knockback and the existing depth/range limits. K during a jump starts a separate eight-pose downward heavy axe slash, with a continuous height transition and grounded strike. It can replace an active aerial light combo, launches hit enemies in front, and uses 42 strike plus 25 landing damage. Fatal hits still fly and count once on landing. J keeps the light aerial combo; ground K remains the advancing spin.

### v29 — Smoother player walking
Rebuilt the barbarian walk as a 16-pose natural low-foot-lift cycle with gradual passing steps, stable axe/torso and a shared ground baseline. Playback is driven by a 192px projected stride cycle (about 0.87s at full speed), with consistent cadence for vertical and diagonal movement. Standing against an arena boundary returns to idle instead of continuing to walk in place.

### v30 — Crossing walk gait

Rebuilt all 16 walking poses against a two-leg pose guide: each leg alternates between the front and back, crossing beneath the hips twice per cycle. The torso stays registered and the loop uses a 186-pixel stride, matched to the drawn planted-foot travel at the hero’s render scale. Playback advances only with actual movement.

### v31 — Mace bruiser

Each wave now includes a bulky mace bandit with 125 base health, slower movement and a 0.70-second wind-up. His 22-damage strike launches the hero 205 pixels away, followed by an animated landing and get-up; recovery is protected against follow-up hits. Dodge or jump to evade. Knockback can land in the lethal pit. Existing grabs, throws, death/life handling and pit avoidance also apply to bruisers. New assets include 24 bruiser poses and eight hero knockdown poses.

### v32 — Bruiser cleanup and combat HUD

Repaired duplicate maces in the bruiser ready and walk poses, restored his weapon in flight, and normalized the corrected frames. Injured enemies now get individual named iron-and-amber health plates at the top of the screen; same-type enemies have distinct numbers and defeated plates clear after a short delay. Removed floating world health bars. Three red-haired hero portraits display lives, with spent lives dimmed and reset on a new run. HUD layout adapts to narrow screens and exposes accessible health and life labels.

### v33 — Four bruiser anatomy and weapon repairs

Redrew walk frames 02, 03 and 04 with one mace and a visible continuous shaft, and landing frame 20 with exactly two arms and hands. The four replacements retain the existing frame keys, shared walk scale and ground baseline. Cache version updated so repaired assets load immediately.

### v34 — Rear heavy sweep and food pickups

The advancing ground heavy now covers the full swept corridor, including behind its starting position, and launches targets outward once. Two food items spawn at safe positions per wave, choosing uniformly among drumstick, bread, cheese, apple, ham and grapes. Standing within 28 horizontal and 18 depth pixels and pressing J replaces the light attack with an 0.80-second kneeling pickup; the item is consumed at 0.40 seconds and restores 25 health, capped at 100. Pickup takes priority over close grabs, locks movement/actions, and can be interrupted by damage before consumption. Eight pickup frame slots use a held kneeling pose and exact idle endpoints. Items and the contextual J prompt clean up on restart.

### v35 — Generic ground pickup

Redrew the pickup poses with empty reaching hands and no food baked into the character sprites. The kneel, grasp and rise now work with every food variant while preserving pickup timing and healing.

### v36 — Wider rage and breakable containers

Rage coverage increased from 340×110 to 410×140 ground-space radii, with a wider painted blast and matching arrow clearing. Each wave adds one barrel and one crate at safe positions. Barrels have 40 health, crates 50; light, heavy, airborne and rage strikes damage them at their normal impact timing. Containers show intact, cracked, burst and wreckage sprites. Destruction releases exactly one random food item; no food spawns directly on wave entry, and the drop API requires a destroyed container. Wreckage clears after 12 seconds. Containers do not count as enemy kills or generate rage.

### v37 — Solid container collision

Intact barrels and crates have expanded ground footprints that block actor movement. Movement resolves in small steps to prevent tunneling and slides along edges; stopped walking pauses its animation. Dodge and heavy advance also respect the obstruction. Enemy navigation shares visibility routes around both containers and the pit, with corner snapping to prevent waypoint stalls. Destroyed props immediately stop blocking. Existing overlap is pushed to a safe edge.

### v38 — PC controller support

Added polling for browser-standard Xbox and DualSense/PlayStation gamepads. Left stick provides proportional movement with a radial 18% dead zone, D-pad provides digital movement, and right stick turns the hero or chooses grab throw direction. Xbox X / PS Square = light, pickup, throw; Y / Triangle = heavy; B / Circle = dodge; A / Cross = jump; RB / R1 = rage; Menu / Options = pause. Buttons trigger once per press, preserving combo buffering. Controller menus support stick/D-pad navigation, A/Cross confirmation, B/Circle back/resume and settings sliders. HUD and pickup/throw hints use device-appropriate labels. Disconnect pauses play and clears controller motion; keyboard/touch remain available. Click the game and press a controller button to expose the device. Gamepads without a browser-standard mapping show a status message. Physical USB/Bluetooth controllers and browser layout have not been tested in this session; simulated device/input/menu checks pass.

### v39 — Rage power, attack dogs and advancing light combo

Rage now deals 160 damage, defeating all current full-health wave enemies in range, and confirmed hits grant 6 rage instead of 4. Meter interpolation scales accordingly. Each wave adds one 55-base-health attack dog (15 enemies total). Dogs gallop outside light-attack range, lock a telegraphed pounce target, leap with six dedicated poses, inflict one 14-damage hit, then retreat and cool down. Dodging, jumping or leaving the target lane can evade them. They route around containers/pits, can be launched by heavy strikes, and do not use humanoid grabs or death screams. Six run and ten other animal poses are registered. The second and third light-combo strikes smoothly advance 45 and 65 pixels in their facing direction while retaining transition poses, hit timing and solid-container collision.

### v40 — Immediate forward combo steps

Forward motion for strikes two and three now starts with their connecting animation and continues into the swing, instead of waiting until the strike-only branch. A separate eased movement clock advances 45/65 pixels incrementally; it cannot be overwritten by phase resets, and collision blocks movement without storing a later jump. Starting another action or taking a hit cancels pending motion. Regression checks verify movement during both bridge clips, exact total travel in both directions at multiple frame rates, and stationary opening strikes.

### v41 — Character selection and Kael’s celebration

The main-menu entry now opens a character-selection screen with Kael the Ashen’s backstory, full character artwork, a live eight-frame idle preview and three blank disabled future roster slots. Clicking Kael previews his axe-lifting celebration; confirming plays the 2.1-second twelve-slot animation before starting the level. Back cancels the pending launch, and background focus loss pauses selection time. Keyboard, pointer and controller navigation are supported, including right-stick profile scrolling. The win pose is also used when the test level is cleared. Existing direct restart/replay actions preserve the selected Kael. Celebration frames are normalized at shared scale and ground anchor, with exact idle endpoints; the clipped raw pose is replaced by a raised-pose hold.

Art sources: `source-art/hero-win-v41.png` generated through built-in image generation from the approved Kael idle reference; normalized output is `dist/assets/characters/hero-win-00.png` through `hero-win-11.png`. Character artwork reuses the existing approved menu illustration, trimmed into `dist/assets/ui/kael-select-art.png`. The celebration brief specifies a consistent right-facing Kael lifting his single axe above his head in a twelve-frame 4×3 transparent sheet, holding it triumphantly, then returning to guard.

### v42 — Menus without internal scrollbars

Removed scroll containers from the main menu, character profile, help and pause screens. Menus now use natural-height layouts, tighter responsive spacing and a viewport-fit fallback that scales complete surfaces when necessary instead of clipping their content. The character story is condensed without losing its premise; the artwork, idle preview and four roster boxes stay present. How to Play is a separate screen with Controls, Combat and Survival pages, keyboard/controller navigation and a Back button. Pause controls use columns when space is short. Fits refresh on menu changes, viewport changes and font loading. Character-profile right-stick scrolling is removed. Functional checks cover page changes/back, scaling bounds and resize recovery; browser layout verification remains unavailable.

### v43 — Lyra the Briar

Lyra is the second playable fighter. Her portrait, concise backstory, selected roster state, animated idle/celebration preview and HUD/life heads update together. Two future slots remain. Keyboard, mouse, touch and standard Xbox/PS5 controller bindings are shared; restart preserves the selected fighter.

- J: three quick twin-knife strikes, with forward steps on the second and third. At very close range this retains human grabs/throws; over food it kneels to pick up.
- Space + J: three aerial knife strikes, including a second strike that hits both sides and a knockdown finisher.
- K: a real forward-facing arrow projectile that deals 45 damage and knocks down, with bow draw/release/recovery. It interrupts a knife chain as a distinct heavy attack. Intact containers intercept shots.
- Space + K: one downward/forward diagonal arrow per jump, then landing recovery. One such shot can replace an aerial light chain.
- L: a 175px dodge roll with brief invincibility, respecting containers and lethal pits.
- I at full rage: an upward fan, followed by five falling arrow volleys over a 390px × 135px ellipse. Enemies in the area take at most one 160-damage rage hit per cast. Rain does not recharge rage or cause repeated hit-stop; common enemies are defeated outright. Test starts still have full rage.

136 new normalized RGBA frames cover 17 actions, anchored at the shared body center. Walking uses eight unique contact/down/passing/up poses with opposite legs crossing; source sheets, frame registration and an animation preview are retained. Kael’s existing animations and mechanics remain available. Lyra has separate AI Voice Generator vocal samples with light echoes, plus new layered bow/string/flight and cloth-roll effects.

Validation: all JavaScript combat, input and menu checks pass, including new huntress simulation/render-lifecycle checks. All 452 character frames pass transparency/padding and isolation checks (two explicitly reviewed Lyra frames include intentional drawn weapon effects). All 42 audio samples pass decode/level checks. HTML nesting/unique IDs pass. Older enemy-count/audio-count assertions were updated to the current roster. Browser visual and physical-controller verification are unavailable in this environment; the scene resource/lifecycle tests are not browser playtests.

### v44 — Simple grounded Lyra knife combo

Replaced all 24 ground light-combo frames with three restrained actions: horizontal slash, diagonal cut, forward thrust. Every pose stays upright and grounded; roll/flip poses are removed from these clips. The two strike-to-strike endpoints now match exactly. Chained attacks play through their final handoff poses; frame 05 is held at the existing damage instant. Body centers/foot baselines stay aligned, and the opener/last recovery connect to Lyra's ready sprite. Damage, reach, forward advances and aerial/bow/roll/rage mechanics are preserved.

The new source sheet, reproducible normalizer and loop preview are retained in source-art/scripts. Normalization rebuilds preserve this newer combo. The knife-specific check verifies all 24 poses actually play during a buffered chain, exact handoff seams and contact/damage alignment. Huntress combat/render, character selection, Kael combat and full sprite alpha/padding checks pass. Browser visual verification remains unavailable.

### v45 — Selection readiness and clear victory presentation

Clicking a character or confirming it with keyboard/controller marks the single active player ready, plays the celebration, then automatically starts the level. Browsing profiles does not confirm readiness; launch waits for every active selection. Back/focus-loss handling remains safe. The current build has one player, and the selected fighter is preserved on restart.

Victory uses a clear, unblurred overlay: heading/summary above the arena and compact buttons below it, on the side opposite the winner. The combat HUD is hidden, leaving the level and the continuing celebration pose visible. Defeat retains the centered modal presentation. Controller/keyboard focus moves to Fight Again.

Selection readiness, single-confirmation automatic launch, controller selection/back, cancel/focus safety, victory/defeat state switching, winner poses, scene render lifecycle and Kael combat checks pass. HTML nesting/unique IDs pass. Browser visual verification is unavailable in this environment.

### v46 — Local two-controller co-op

A / × on another standard Xbox/PlayStation controller joins P2 in character selection, up to two players. The join press is consumed before confirmation; each controller independently browses and confirms. Confirmed characters are reserved, leaving the other fighter for the partner. Both players' previews/statuses are shown, and the level starts after every joined player confirms and finishes their celebration. P2 may join during P1's celebration. B / ○ or Back/Esc cancels the screen, removes P2, clears reservations and returns menu control to the original primary controller.

Controller assignments use separate physical-device identities and press histories. A disconnected primary never falls back to P2; a disconnected active controller pauses co-op. P2 must reconnect before resuming. Other menus stay under P1's control. Pause/restart keeps the chosen party and device assignments; returning to main menu clears P2.

Both fighters play in one arena, with separate health, rage, three lives, action states and HUDs. World clocks, enemies, containers, food and projectiles advance once per frame. Enemies choose a living target and retain wind-up targets. Arrow/throw rage credit belongs to the originating player. There is no friendly fire; shared food is consumed only once. One exhausted player does not end the partner's run; team defeat requires both to be out. Victory animates both remaining fighters. Party rendering/secondary HUD/pickup prompts are cleaned up on returning to solo.

Validation: simulated Xbox/DualSense join, unique selection in either order, max-two gating, held-button edges, focus/cancel/disconnect/reconnect, primary-only menu ownership, sparse/reordered/identical-ID devices, independent combat and clock ownership, no friendly fire, shared food, separate lives/respawns, team defeat, both character orders, co-op render/effect lifecycle and victory poses. Existing single-player combat/input/menu checks pass. HTML nesting/unique IDs pass. Browser visual and physical-controller verification remain unavailable; these are simulation/resource checks, not hardware playtests.

### v47 — Party life potion

The first-wave crate now exclusively contains a life potion, visibly marked with a bottle badge and label. Breaking it drops exactly one emerald potion. Normal barrels/crates in other waves continue to drop random food. The potion persists on the ground until useful; a full party cannot waste it.

Stand over it and use J / Xbox X / PlayStation □ to kneel and collect. At the pickup contact, every player missing a life receives one, capped at three. An out-of-lives dead player instead returns with one life and full health through the existing drop-in respawn/invincibility sequence, with stale attack/pickup state cleared and controls restored. Living players receive no health heal from this item. Either player may collect it for the whole party; simultaneous pickups cannot apply it twice. A brief party-life notification and green pickup particles confirm the effect.

The generated source and normalized 128px RGBA sprite are retained with a reproducible preparation script. Life-potion checks cover exclusive drop/one-per-run placement, persistence/full-cap preservation, delayed team effects, either player resurrected, solo, interrupted/simultaneous pickup and restored controls. Food/container, co-op controls/combat, scene resource/render cleanup, collision/pit routing, potion transparency/padding and HTML checks pass. Browser visual verification remains unavailable.

### v48 — Hide the contained potion
Removed the floating potion sprite from the intact dedicated crate while retaining its LIFE POTION label. The actual pickup appears only after the crate breaks; team life and resurrection behavior is unchanged.

### v49 — DragonQuest identity and result audio
DragonQuest title, subtle menu navigation/confirmation/back cues across mouse, keyboard and controller; an original 14-second synthesized metal guitar solo for victory and a six-second descending minor defeat lament. Wide gold victory lettering keeps the level and winning poses visible. Fanfares stop when starting another round; menu cues work while gameplay audio is paused and respect effects settings. Reproducible composition: scripts/make_menu_fanfares.py.

### v50 — KillQuest storm-metal menu
Renamed to KillQuest, with a new original painted 1980s fantasy-metal storm background, lightning and ember arcs around the barbarian and huntress. Dark left-side composition protects menu readability. Chrome/crimson title, violet forged buttons, ember confirmation accents, and responsive sizing retain keyboard/controller focus and existing menu sounds.

### v51 — Menu anthem and power-metal victory lick
Menu cues lowered one octave. Victory replaced with a five-second 200 BPM harmonized guitar lick. A 24-second original 160 BPM 1980s fantasy-metal menu loop combines galloping stereo guitars, bass, analog-style pads, lead harmonies and snare. Starts after interaction, carries through help/selection, stops for gameplay/results, returns on quitting, follows music volume/mute, and suspends in inactive tabs. Reproducible script: scripts/make_metal_menu_v51.py.

### v52 — Riff-driven thrash and main-menu options
Original 144 BPM menu loop rebuilt around low-E palm-muted plucked-string guitars, stereo distortion/cabinet processing, chromatic syncopated power chords, bass and restrained drums; no high-register lead. Main-menu Options exposes persisted music/effects mute and independent volume, shared with pause controls, plus keyboard/controller navigation, range adjustment and back.

### v53 — Two-minute layered thrash menu arrangement
Expanded the established riff sound into an original 120-second, 144 BPM arrangement: intro, main riff, power-chord refrain, half-time breakdown, bass bridge and final reprise. Five independent layers: stereo rhythm guitars, moving centered bass, varied drums/tom fills/crashes, restrained mid-register answering guitar and dark low atmosphere. Five lossless source stems and section timing map retained under source-audio/menu-v53. Playback and saved options remain shared with the existing mixer.

### v54 — Grounded Lyra pickup and balanced menu stems
Ground-registered all eight existing pickup poses to Lyra’s 403px foot baseline, preserving art, scale, alpha and horizontal registration. The normalization survives full huntress rebuilds. Rebalanced the existing two-minute menu composition using active-block RMS per stem, with lower rhythm guitar and audible bass, drums, answering guitar and atmosphere; shared master headroom preserves the new balance. Scripts and original pickup frames plus mixing settings are retained for reproducibility.

### Windows desktop build
The desktop/ folder contains the offline Electron wrapper and reproducible Windows x64 portable packaging script. Build uses official Electron 44.7.2 win32-x64 ZIP, verifies SHASUMS256, copies the shipped dist assets, and checks the PE architecture and ZIP integrity. Extract the whole portable ZIP and launch KillQuest.exe; F11 toggles fullscreen. Browser navigation and external networking are disabled. No separate Electron installation is needed. Windows runtime/controller launch requires verification on Windows. The hosted edition is unchanged.

### v55 — Visible controller menu selection
Controller-selected buttons now use a brighter fill, inset gold edge and border, in addition to the outline. These accents survive angular clip-path buttons and outrank the later metal-menu styles. Applies to main menu, help, options, pause and results; options sliders retain a clear focus ring. Windows portable build updated.

### v56 — Separate player scoring
Dagger 100, sword 150, archer 150, dog 125, bruiser 300. Finishing hits, owned arrows/rain, throws/landing and player-caused pit defeats award exactly once to the responsible player. Unassisted environmental deaths only advance level progress. Each lost life deducts up to 200 points (minimum zero), without repeating on respawn/resurrection. Live P1/P2 score counters and victory/defeat earned/lost/foes/deaths/final score breakdowns; restarting resets scores. checks/player-scores.cjs exercises attribution and penalties.

### v57 — Larger readable text (hosted update only)
Increased secondary HUD, enemy names, score breakdowns, help, character select, option labels, menu hints and world pickup labels. Tightened letter spacing and compacted decorative space on short screens; retained automatic menu fitting and no internal scrollbars. Standing orders: do not rebuild Windows EXE unless the user explicitly requests a build. Last downloadable desktop build remains v56.

### v58 — Campaign menu and disconnected regional atlas
Main menu: New Game, disabled Continue (no campaign save exists), Test level, How to Play and Options. New Game opens a new original painted regional map: Forest, Carion City, Temple of Elements, Black Mountains, Highland Hill and Castle of Doom. No route lines or gameplay connections. Forest is the first region and provides the existing solo/co-op character-select preview; other regions can be inspected. All campaign launch paths are hard-gated, including automatic ready launch and direct start calls. Test level remains playable. Back from campaign character select returns to the map and clears the second controller/claims; map Back returns to the main menu. No EXE rebuild.

### v59 — Latest-input controller owns single-user menus
Main/help/options/campaign/pause/result menus follow fresh button presses or deliberate stick input from any connected standard controller. Each device keeps independent edge history; held buttons, stick drift and auto-repeat do not retake menu ownership. Menu ownership is separate from fixed P1/P2 gameplay bindings; unconfirmed one-player character selection also follows latest input, while an A/× press from another controller explicitly joins P2. Confirmed or two-player selections keep fixed ownership and unique choices. Inactive windows do not change ownership. No EXE rebuild.

### v60 — At least 30% larger bars and typography
Scaled every explicit text size (including responsive viewport clamps and canvas labels) by 1.3, rounding pixel values upward. Player health bars 16→21px, rage 9→12px, enemy health 11→15px (9→12px compact baseline overridden by 15px); player HUD widths scaled by 1.3. Main menu buttons use fewer rows; character/help/options panels widened and decorative spacing compacted to reduce auto-fit shrinking. HUD offsets updated for the larger blocks. No EXE rebuild.

### v61 — Forest walkthrough
New Game → Forest → Choose Warriors now launches a solo/co-op exploration preview. The 12,800px route is ten screens: five woodland screens, four pillaged-village screens, and one empty Bandit King arena. No enemies, boss, pit or automatic victory are present. Players walk in from the left for exactly three seconds; the village elder then displays the requested plea, with Enter/Space/J, A/× or the Continue button dismissing it. Attacks and movement are gated during the entrance/dialogue. The elder uses a grounded breathing/blink loop. Breakable stumps populate the forest; sacks, baskets and barrels populate the village and retain collision and container-only food drops. A shared co-op camera keeps partners within 850px without dragging the rear player forward. Player movement, combos, respawns, arrow lifetimes and Lyra rain use the longer world bounds. Test level remains unchanged; other campaign regions and Continue (no saved campaign) remain unavailable. No EXE rebuild.

New art was generated with the built-in image generator; source images are in `source-art/forest-v61`, runtime WebP backgrounds and PNG frames in `dist/assets/forest`. Prompts: full-width side-on ancient forest path with clear lower walk strip; pillaged medieval village with ruined cottages and clear horizontal street; empty arena with ruined hall, palisades and crimson banners; transparent elder idle/stump/sack/basket damage atlas. `scripts/prepare_forest_assets.py` preserves alpha and aligns feet/prop bases. Validation: Forest model and scene lifecycle tests, character-select solo/co-op campaign launch tests and existing controller/combat/container regressions. Browser visual playtesting was unavailable in this environment; generated art and extracted sprites were inspected directly.

### v62 — Direct map confirmation
Clicking or confirming the Forest map pin now immediately opens campaign character selection. Arrow/stick navigation continues to preview regions; unavailable region confirmation stays on the map. The map confirmation input is consumed by the screen transition, so a second fresh press is required to select a warrior. Existing Choose Warriors button and Back-to-map behavior remain available. Covered by click, Enter, Xbox A, PS5 × and held-input regression checks. Hosted update only; no EXE build.

### v63 — Forest scenery, props and frightened elder
Five unique forest screens now appear in sequence (grove, creek, woodland ruins, orchard, forest edge), followed by a painted forest/village transition, market, village, village/arena transition and arena. No image is mirrored and no adjacent screen repeats. Backgrounds overlap 160px with a cached canvas alpha gradient for softened joins; perspective/path baseline and lighting are coordinated. The elder has four newly painted worried/trembling poses in an eight-frame idle loop; visible height is approximately 150px, matching bandit idle/walk silhouettes, and feet remain anchored.

Six indestructible props (two rocks, two empty market stalls, one empty handcart and one well) have appropriate collision footprints and passable detours. Two barricades, each three destructible pieces, span every walking lane and must be broken to cross. They do not drop food. Existing destructible stumps/sacks/baskets/barrels keep container-only food rewards. Permanent props ignore damage and block arrows according to their footprint. Both solo and co-op remain enemy-free. No EXE build.

New art and prompts: `source-art/forest-v63`; runtime assets: `dist/assets/forest`; extraction: `scripts/prepare_forest_v63.py`. Generated with the built-in image tool. Art brief: coordinated wide side-on fantasy comic backgrounds, golden afternoon palette and clear horizontal dirt road; unique grove/creek/ruins/orchard/forest-edge scenes; gradual forest-to-village and village-to-arena connectors; smoky village market and an amber-lit version of the existing great-hall arena; frightened version of the green-shawled elder with planted feet; transparent permanent props and four-stage wooden barricade damage atlas.

Validation: asset gutters/alpha/baselines and elder scale; full solo/co-op walkthrough after clearing barriers; permanent prop immunity and detours; full-road blockage and clearance; no incidental food; cached background blend textures and scene cleanup; character selection, controller ownership, food/containers and combat regressions. Art inspected directly. Browser visual playtesting unavailable in this environment.

### v64 — Aerial vocals and attack dog audio
Kael and Lyra now play their existing character-specific effort variants on aerial light-combo openers and aerial heavy windups, once per action rather than every combo link. Co-op preserves the speaker identity. Dogs growl when committing to a pounce, bark on takeoff and make bite-contact audio only when landing damage. Nonfatal damage triggers a throttled canine yelp; death has a separate once-only canine cry, replacing the generic impact placeholder. Added eleven short mono WAV variants sourced from CC0 real dog recordings (credits and original recordings in source-art/dog-audio-v64). Voices, effects volume, pause, spatial panning and anti-repeat controls continue through the existing mixer. No EXE build.

Validated both heroes' aerial light chains/heavies and co-op voice ownership, one-shot dog attack/contact/death triggers, hurt throttling, audio file format/amplitude and existing audio, dog AI/combo, huntress and aerial-heavy regressions. Browser listening/playtesting unavailable.

### v65 — Falling bodies damage props; standing bow alignment
Airborne thrown enemies now pass over prop collision footprints during flight. At landing they apply their existing fall-impact damage (heavy launches 25, grabs 55) once to nearby destructible props using each prop's footprint plus body contact padding. Destruction follows the existing flash/break/sound/food rules; permanent scenery remains immune. Fatal flying bodies also damage props and keep normal once-only defeat/score credit. Long-world heavy throw destinations use level bounds.

Lyra's standing arrow visual muzzle now derives from bow-grip pixel (296,260) in huntress-bow-05, sprite origin (224,408), scale .84, and a 28px tip offset. The arrow renders 124.32px above her feet, 49.32px higher than before, in both directions. The existing collision layer remains at 75 to preserve dog/container hits; aerial/diagonal/rain trajectories are unchanged.

Validated impact once-only behavior in both directions, 25/55 damage, prop types and food, permanent immunity, fly-over/depth misses, fatal bodies and scores, long-level launches, standing muzzle model/render coordinates and unchanged Huntress/grab/pit/collision regressions. No browser visual playtest available. No EXE build.

### v66 — New chugging menu theme: Iron at the Gate
Replaced the previous synthesized thrash arrangement with an original 120-second 112 BPM low-D guitar groove built from recorded distorted/palm-muted guitar articulations. Five-section arrangement plus entry/turnaround: main groove, chord response, half-time, bass pocket and reprise. Real guitar samples are transposed and sequenced into new riffs; no Doom MIDI/melodies are reused. No bright lead or atmospheric synth layers. Separate guitar-left/right, bass and drum stems are balanced independently; final master targets -17 LUFS and -1.5dBTP. Menu looping, volume controls and stored preferences are unchanged. Source, stems, script and attribution/license are in source-audio/menu-v66; user-visible music credits/player available from Options. The sampled/adapted music is CC BY-SA 4.0 (Skimel source); unrelated game materials retain their existing terms. No EXE build.
