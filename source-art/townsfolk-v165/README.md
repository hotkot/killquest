# Six townsfolk with frightened idles

Adds three new adult civilians: baker (woman in burgundy with a cream headscarf), weaver (woman in plum with a long braid), porter (man in blue with a wool cap). Together with the existing laborer, teal-clad woman and older traveler, the roster now has six designs, three women and three men.

Built-in image generation in reference mode, using `source-art/townsfolk-v164/run-preview.png` for identity/style. Raw sheets: `baker.png`, `weaver.png`, `porter.png` (each eight running and eight idle frames) and `original-idles.png` (eight idle frames each for the original three). Full prompts are in `prompts.json`.

Runtime assets: `dist/assets/characters/townsfolk-{baker,weaver,porter}-00.png` through `-07.png` and `townsfolk-{laborer,villager,traveler,baker,weaver,porter}-idle-00.png` through `-07.png`. Existing24 running frames are preserved. New72 frames use complete silhouette extraction, transparent448px canvases, floor408, and one shared scale per new character across both clips. Idle positions align both feet's bounding span to prevent population-median shifts between boots. `normalization.json` records each source component/scale/bounds. `idle-preview.png`, `new-runs-preview.png` and `arena-preview.jpg` document QA.

Test level cycles all six designs in staggered groups. Each person briefly hesitates in a frightened idle for3.2–3.6seconds inside the screen, then resumes fleeing left. Idles advance at four frames/second, runs remain distance-driven. Civilian positions and stride remain still while idling. No combat targeting or player collision. Test cage and two soldiers retained; campaign placement unchanged.

Checks pass for all48 idle frames, planted-foot and body-scale stability, no sprite-border fragments, timed idle/flee transitions, bounded crowd, offscreen cleanup, solo/4player resets, all1351 resources and scene lifecycle, army combat, rescue and spear readiness. Arena preview uses an offline composition from the real model at nine seconds; browser playback was not verified in this update.
