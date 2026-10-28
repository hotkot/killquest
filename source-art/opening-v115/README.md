# KillQuest opening motion comic

Built-in image generation supplied three 1672 × 941 illustrated panels:
- `dist/assets/cinematic/morvane-v115.webp`: Deathless Bride in the ruined throne hall.
- `dist/assets/cinematic/village-v115.webp`: masked bandits taking adult villagers from a burning village.
- `dist/assets/cinematic/heroes-v115.webp`: Kael, Lyra, Garran and Selene overlooking the raid.

Reference images: original Kael idle sprite and approved `killquest-menu-v105.png` poster. The village panel received one targeted edit to make the mace bandit distinct from Kael. Full production prompts are in `prompts.json`. Existing logo and menu poster form the final title beat.

AI Voice Generator (deep voice) supplied the complete English narration. Source preview context: 21741d7e7c76467f8a7a9d0ab18bc776. Runtime copy: `dist/assets/audio/opening-narration-v115.mp3`. Three seconds of silence inserted at original 4.50 and 7.95 seconds align the narration with scene holds; no words or voice pitches altered. Final duration 26.808 seconds. The illustrated sequence lasts 31 seconds, then opens the existing Press Any Button screen. Menu music continues, with reduced volume during narration. Effect and music settings are respected. Browsers may require a gesture before audio becomes audible.

Narration: Queen Morvane would raise her dead kingdom... and pay for it with the living. Her bandits scour the forest for souls to feed the rite. But four survivors follow their trail. An axe sworn to vengeance. A huntress who will not abandon her people. A shield against the darkness. And a flame that will burn the dead queen's dream to ash.

Controls: Enter, Space, Escape, visible Skip button, or controller A / Cross, B / Circle, Start / Options. The opening pauses outside the focused game. Skip input is consumed and the following title screen requires a released, fresh input. Reduced motion disables image pans and atmospheric animation. All art and narration bytes join the boot asset gate.

Validation: timeline, all panels, narration prefetch, volume, finish/skip cleanup, held controller protection and focus pause/resume checks; boot, title gate, controller menus, audio mixer, four-player selection and all 543 player renderer frame checks pass. Live browser QA unavailable.

Runtime panels use high-quality WebP at the original resolution to reduce deployment/download size. Original generated PNGs are preserved beside these notes.

The unused retired menu track `killquest-menu-thrash-v53.mp3` was moved from runtime assets to `source-audio/retired-menu/` to keep the deployment archive below 100 MB. It has no active runtime references; the approved Iron Rising menu theme is unchanged.

## Concurrent loading revision
The opening now runs while the remaining game assets load. Its six essential art/audio assets receive priority. It covers the loading overlay; completion/skip reveals loading if needed, and the start screen requires both readiness and cinematic completion. Menu music begins on that start screen, never under the cinematic. Character texture styling yields between small batches so the opening keeps animating during preparation.
