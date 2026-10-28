# Brutal combat effects

Expanded the existing comic blood renderer: 34 light / 56 heavy / 82 fatal droplets, directional streaks and counter-spray, 3 heavy / 9 fatal flesh fragments with a short bounce, irregular layered pools, satellite splashes, and lingering debris. Impact pools remain for 32–42 seconds and fade over the final five seconds. Droplet stains last 20 seconds; fragments remain 30 seconds. Shared caps: 520 particles, 180 ground decals. Everything resets with the level.

Includes Selene impacts, thrown-body landings and successful enemy damage to players. Shield rejections remain bloodless. No damage, controls or score values changed; existing .028 second hitstop retained.

Native code effects, no generated images. impact-preview.png is an offline native Canvas rendering of the actual game blood/stain loops, using the arena background. Reproduce with node checks/render-blood-v148.cjs.

Validation: blood tiers/direction/bounce/landing/expiry/caps/reset, blocked versus successful hits, Garran combat, Selene combat, co-op ownership and actual Forest/City scene adapters pass. Browser playtest was not performed. The older player-scores check fails with 0 vs 350 on both the unchanged published baseline and this version; unrelated to these effects.
