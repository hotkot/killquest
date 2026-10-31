# KillQuest — development handoff

Updated 2026-10-31. Read AGENTS.md before editing. GitHub is the intended development source of truth after this migration.

> New-chat prompt: Continue KillQuest from https://github.com/hotkot/killquest. Clone the repo, read AGENTS.md and docs/HANDOFF.md, inspect current Git status/recent commits and docs/MIGRATION.md, then implement my next request. Preserve the existing game and asset pipeline. Do not build a Windows EXE unless I explicitly request it.

## Migration status

**Migration in progress.** Do not assume the playable assets are present until docs/MIGRATION.md reports a verified complete source snapshot. This guide was saved first so context survives interrupted transfers.

## Run locally

The game is buildless plain JavaScript using bundled Phaser 3.90 and DOM menus. `dist/` is maintained source, not disposable compiler output. No Vite/React/TypeScript build is required.

```sh
git clone https://github.com/hotkot/killquest.git
cd killquest
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000 in a modern browser. Do not open the HTML as a local file. Click/focus the page and provide an input gesture for audio/gamepad access. No backend/CDN is required for normal play. The full tracked source snapshot is about 1 GB (3,159 original files).

Keyboard: WASD/arrows move; J light/pickup/grab, K heavy, L dodge, Space jump, I rage, Escape pause. Standard gamepad: stick/D-pad move, X/Square light, Y/Triangle heavy, B/Circle dodge, A/Cross jump, RB/R1 rage, Menu/Options pause. Additional controllers join character selection with A/Cross.

## Current game

Fantasy arcade beat em up, 80s heavy-metal/comic identity, grim bloody KillQuest logo and illustrated party poster. Four playable heroes, up to four-player local co-op, unique hero reservations, separate lives/scores/HUD, controller/keyboard/touch support. Each joining player gets their own character panel and biography. Latest-input controller owns single-controller menus; backing out returns to primary-controller control.

Final character confirmation immediately plays the power chord, then celebration and transition. Startup cinematic hides loading; if finished/skipped early, show loading until ready. Flashing Press any button follows. Menu music starts only after startup cinematic, with the retained one-second menu timing. New Game plays story intro before world map. Map confirmation leads directly to selection, including controller input. Level movies gate model reset/music/entrance and can be skipped. Victory UI leaves the level/poses visible.

Continue is present but disabled: persistent campaign progression is not implemented. Audio settings and last elite palette use localStorage; those are not a campaign save. No online multiplayer.

### Heroes

| ID | Moves | Menu color |
| --- | --- | --- |
| kael | Axe ground/aerial chains; second/third light advance; forward spin heavy hits both sides; downward aerial heavy; dodge; huge jump/ground rage slam | Brown |
| lyra | Flashy knife slash ground/aerial chains; directional bow heavy, diagonal-down aerial arrow, arrows throw/knock down; roll; arrow-rain rage | Green |
| garran | Downward slash, horizontal slash, stab; aerial combo; shield charge with frontal protection and throw; two-sided aerial slam; backward shield dodge; screen-length ultra-shield rage | Red |
| selene | Three blue-flame casting strikes; forward-only ground flame push; diagonal-down aerial casts; two-sided aerial magic slam; backward teleport; forward blue firestorm | Blue |

Canonical name/ID is Garran (user sometimes says Garren). Closed helmet, white sun tabard, shield on left forearm, textured/varnished armor. Selene has no hat, black/blue colors. Kael is the art/body-scale reference. Preserve poses, registration and outlines when editing.

Close light attacks grab human enemies for brief invulnerable follow-up throws. Light over an item picks it up with a ground-reaching pose, not a held food prop. Three starting lives; respawn drops from above, brief invulnerability, landing enemies knocked down. Separate player score, death penalty. Food heals collector. Life potion grants all players a missing life or revives an eliminated hero. Red rage potion fills only collector's rage. Items drop from containers. Containers block ground movement but can be jumped over, and thrown bodies damage objects/other enemies. Projectiles can hit airborne bodies. Rage gain from hits was reduced by 50%; campaign starts empty, Test full.

### Levels

**Test level is empty Carion City**, via CityTestCombat extends CityCombat. No enemies, allies, civilians, encounter spawns or cages. Normal scenery/destructibles remain. Immediate movement, full rage; intro/dialogue/walk-in bypassed. Restart remains empty City. Legacy TestCombat class still exists but normal UI no longer uses its arena.

**Forest** is 12,800px, woodland path → pillaged village/market → Bandit King arena. Three-second entry, frightened villagers' dialogue with one response per present hero, then villagers flee. Bandits introduced sequentially with some tougher recolors. Three life potions, one in arena, plus arena food. Forward-only progression. Party walks fully into arena before boss jumps in/reveals himself/speaks. Boss not staggered by ordinary hits; slash can hit airborne players; replacement bandits harass during fight. End returns to menu or Fight again.

**Carion City** is 25,600px at original walking speed: twelve distinct panels, eleven opaque architectural joins, three down-right descents, world height1,680. Traced pavement and smooth curb sliding, world-locked scenery. Opening right-facing bandits confront left-facing townsfolk; bandits turn toward heroes during dialogue, townsfolk flee left and despawn. Bandits first third; soldiers and bandits already fighting as party arrives in middle. One mixed formation around x17,400: 3 heavy shields, 3 light shields, 4 spears, 2 crossbows, 1 knight vs16 bandits. After that only loose3/4/3 soldier patrols near19,900/22,000/24,200, no extra knights/formations. Four cages, three life supplies, four red rage supplies. **City boss not implemented**; ending provisional.

Map future locked regions: Temple of Elements, Black Mountains, Highland Hill, Castle of Doom. Never simulate a longer level by slowing background/camera or movement. Keep actual world lengths, traced lanes, opaque joins and forward-only camera.

### NPCs

Bandits: dagger, sword, archer, mace bruiser, pouncing dog, Bandit King. Soldiers: sword/shield guard, heavy shield, crossbow, spear, elite knight palettes. Heavy shields guard a side with delayed turns: rear hits, grabs, dodge/jump-through and rage counter them. Crossbows throw/knock down and reload. Spears poke behind shields. Commanders coordinate lines, gaps close on deaths; formation reverses if no forward target. Knights have three-hit combo, delayed parry/punish, no ordinary stagger; behind hit immediately drops parry; first strike hits airborne heroes.

Cages free rebel counterparts except knight captains. Rebels independently follow into same screen and fight visible enemies rather than sticking to players; melee follow about forward two-thirds of screen. Stable target retention/facing prevents flicker. Once-visible enemies cannot leave killable screen. Stuck enemies can briefly pass a container after delay. Cage destruction stays registered, fragments removed quickly. Townsfolk use restrained idle/flee at normal NPC size.

## Code map

| Path | Responsibility |
| --- | --- |
| dist/game.js | Combat/model, hero moves, NPC AI, levels, pickups, scoring, Phaser BrawlScene, DOM/menu orchestration |
| dist/index.html, style.css | Menus/HUD/overlays/script order |
| dist/gamepad.js | Device edges, party assignment/joins, menu ownership |
| dist/audio.js | Samples/variation/pitch/gains/echo, music/effects controls/lifecycle |
| dist/loading.js, loading-assets.js | Boot loading and complete asset inventory |
| dist/boot-flow.js, start-screen.js, opening-cinematic.js | Startup/Press any button/video skip/focus gates |
| dist/hero-style.js, armor-finish.js | Cached color/ink and Garran metal finish |
| dist/forest-ambience.js, city-ambience.js, city-join-fit.js | Fitted animated materials and City joins |
| dist/object-shadows.js | Source-alpha cast silhouettes/contact shading |
| dist/assets | Delivered sprites/scenery/audio/movies/Phaser/license |
| source-art, source-audio | Approved references, raw sheets/stems, landmarks/provenance/QA |
| scripts, checks, balance, notes | Authoring/regression/balance/design evidence |
| desktop | Local Windows EXE builder UI/CLI and Electron wrapper; see desktop/BUILDING.md |
| src/witch.js | Retained authoring fragment; integrated WITCH_SYSTEM in game.js is runtime |

Combat is the model; ForestCombat extends BossCombat; CityCombat and CityTestCombat configure City. BrawlScene mirrors model into Phaser. Most modules use globals and ordered scripts, not imports. VM fixtures depend on class boundaries and globals.

## Asset editing

Inspect current texture keys and frames first. Individual padded RGBA frames are registered by reviewed body/pelvis/feet landmarks, not total alpha bounds. Weapon/hair/effects change bounds; kneels/jumps need deliberate ground placement. Some frames intentionally have640/768px wide canvases at the same body scale. Keep PLAYER_FRAME_LAYOUT/origins correct. Clear crossed-leg walking, stable body proportions, full weapon arcs/limbs/effects and gutters are essential. Keep approved raw art/prompts/landmarks and processed runtime outputs together. Update scene preload plus loading-assets.js and cache query stamps for new assets.

Runtime hero-style/armor passes preserve alpha/poses; do not double-apply them to exports. Historical normalizers may require old intermediates/absolute paths: read before running. Source-art subdirectory READMEs describe each revision.

Forest dynamic fires are tailored to source house locations, with restored static art/smoke; do not replace with generic overlaid flames. City has265 source-color animated regions across all12main panels AND11joins. Twelve-frame4×3 atlases, current stamp city-ambient-v178, ~83MiB decoded, <96MiB guard. Baker scripts/bake_city_ambient_v176.cjs invokes bake_city_joins_v178.cjs. Module uses CityCombat.ambientTime so pause freezes it. Join refs768×720, flat2048×683, descents1795×876; use correct transforms. Keep transparent gutters and fitted material edges.

Last published edit **v180 strengthened object shadows**: standing contact.90/cast.52; pickup.72/.34; broken.52/.25. Contact center.84, cast DX.42/DY.16, blur max(2,width*.009), depth9.99/10 below actors. Cached source-alpha silhouettes follow damage poses, cull offscreen, fade/clean up on removal/reset. Hooks after containers/food render and on reset. v179-named source notes/tests contain currentv180 results.

## Story/music/cinematics

Villain Queen Morvane, the Deathless Bride, raises her dead kingdom using living souls/relics. Bandits gather captives then story escalates into her forces/Temple. Kael seeks clan vengeance; Lyra rescues captives; Garran seeks the sun relic that breaks immortality; Selene follows stolen sanctuary fire to destroy the rite. Exact approved biographies live in FIGHTERS in game.js.

No spoken dialogue or cinematic narration is active. Combat grunts remain varied; Selene higher pitch. Current menu theme assets/audio/killquest-menu-iron-rising-v108.mp3. Preserve audio-credits.html, source licenses and AI provenance; not all audio is exclusively generated or under a single license.

Active movies under dist/assets/cinematic:
- killquest-hype-v126.mp4: startup action/hype.
- killquest-opening-v175.mp4: New Game44.25s.
- killquest-forest-v175.mp4: Forest20s.
- killquest-carion-v174.mp4: City34s.

Archived movies live in source-art/cinematic-archive, outside runtime. New Game/Forest use matching pixel/comic style, renderer source-art/intro-pixel-v175/render.py. City approved hopeful thrash score/art/render in source-audio/carion-intro-v174. Render serially; verify ffprobe streams/duration, watch/listen. Past parallel-heavy renders truncated outputs despite exit0.

## Tests and limits

Run from repo root. Node22+ (previous Node24/Python3.12). Canvas checks need @napi-rs/canvas0.1.100; Python art needs Pillow; media FFmpeg/ffprobe.

Focused checks:
```sh
node --check dist/game.js
node checks/four-player-selection.cjs
node checks/carion-campaign-v167.cjs
node checks/city-route-v167.cjs
node checks/city-ambient-v176.cjs
node checks/city-ambient-assets-v176.cjs
node checks/object-shadow-scene-v179.cjs
node checks/object-shadows-v179.cjs
node checks/boot-flow.cjs
node checks/start-screen.cjs
```

Related Forest/rebel/projectile/movie fixtures exist under checks; inspect relevant ones. Historical tests can expect obsolete keys/preload totals/test enemies. forest-ambient-scene.cjs specifically has stale resource-count/empty-City/test-soldier assumptions. Do not regress current behavior to satisfy it. Some pixel tests need temporary RGBA manifests described in source-art README.

VM/Canvas tests do not prove real browser rendering/audio/autoplay or physical controllers. Recent browser QA was unavailable in prior environment. Manual acceptance: loading/video/menu flow; all heroes/both facings and move combos; 2–4controllers/join/leave/disconnect; true-length City traversal/curbs/joins; shadow/material fit; Forest boss; City faction/rebel/potion progression; battlefield visible under result.

## Known debt and user preferences

No City boss, future levels locked, Continue disabled, some old City labels still say empty prototype, monolithic game.js, historical authoring paths. Keep historical implementation log but distinguish it from current docs. User wants direct action, approval previews before major new character/cinematic art, readable UI, stable scale/poses, and **no Windows EXE build unless explicitly asked**. Do not invent the next gameplay task after migration.

## Hosting/releases

GitHub push does not deploy the existing private Site. Preserve its audience and identity: appgprj_6ace65f874ec8191b570992d6bce7858, .openai/hosting.json static.directory=dist. Live https://axe-and-ash.hotkot613768.chatgpt.site, last gamev180 source6ebe5805e1950c232ba129a3fa77f8c98d70ff8d. Use current Sites skill/tools if continuing that hosting; no credential may be hardcoded or committed.

Live dist is ~243MB, close to Sites' observed256MiB expanded-directory limit. Keep old movies/source art out of runtime, measure before publication, host dist only.

Local Windows builder: desktop/Builder.bat opens desktop/compiler.py with Build, Test, Package, Run and Deploy buttons. Deploy runs those first four actions in order and stops on failure. Electron 45.2.1 is pinned and verified against official SHA256 sums. Build outputs and runtime cache are ignored by Git. See desktop/BUILDING.md for prerequisites, CLI and output paths. desktop/build_windows.py forwards to the same tool; old positional cache/destination arguments are retired. The web workflow remains buildless. Windows execution and physical-controller QA require a local Windows machine.


### Desktop builder validation (2026-10-31)

On Linux, built the official checksum-verified Electron 45.2.1 Windows x64 portable folder from current dist. Game JavaScript syntax, seven focused regression suites and the desktop protocol check passed; five builder failure-path tests passed. Damaged packaged files and stale source inventories were rejected, then the original build was restored and verified. Package validates ZIP CRCs and every bundled file hash. Windows GUI/game launch, audio/video and physical controllers remain untested here; use desktop/Builder.bat on Windows for local acceptance. Generated EXE/ZIP and runtime cache are intentionally untracked.

Desktop builder compatibility correction: replaced Python 3.8–3.11-only unlink/path/string/hash helpers with Python 3.7-compatible equivalents. Nine builder tests pass, including download completion with the legacy unlink signature, preserving network errors, multi-chunk SHA256 and archive path boundaries. Python 3.7 grammar was checked; validation ran on the cloud Python 3.12 runtime, not an actual Python 3.7/Windows installation.
