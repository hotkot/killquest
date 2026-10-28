# KillQuest agent instructions
Read docs/HANDOFF.md first and docs/MIGRATION.md before assuming the migration is complete.
- This repository is the intended development source of truth. Work here and keep useful source, authoring assets, tests and notes committed.
- dist/ is maintained buildless Phaser/JavaScript source. Serve it over HTTP; do not erase it with a new scaffold/build.
- Do not build a Windows EXE unless explicitly requested. Retained desktop scripts/labels are historical v56.
- Preserve 4-player local co-op, unique heroes, keyboard/touch/gamepads and latest-input menu controller ownership.
- Test level currently means empty Carion City, immediate control and full rage. Campaign starts empty rage.
- Forest12800px; City25600px. Never lengthen a level by slowing scenery or movement. Preserve traced lanes, smooth curbs, opaque joins and forward progression.
- Kael is style/body-scale reference. Preserve poses, body/foot anchors, outlines and weapon positions; clear crossed-leg walks; no clipped effects or detached fragments. Do not normalize by total weapon/effect bounds.
- No voiced dialogue or cinematic narration. Preserve combat vocalizations and approved music unless requested.
- Preserve existing Site identity/audience. GitHub push does not deploy it. Do not create a replacement Site.
- Retain audio credits/provenance/licenses. Never commit credentials, browser state, dependency caches or release ZIPs.
- Choose focused checks from handoff; historical fixtures may encode superseded designs. VM tests do not replace browser/controller QA.
- Keep handoff accurate after meaningful changes; be explicit about untested behavior.
- Do not delegate to subagents unless explicitly instructed.
