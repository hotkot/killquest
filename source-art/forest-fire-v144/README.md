# Forest fire integration — v144

Fixes the opaque rectangle at the left house/screen blend, restores drifting village smoke, replaces the earlier transition house's generic fires, and fills the four large arena brazier bowls with properly seated flames.

Runtime assets: `dist/assets/forest/ambient/fitted-{roof-left,roof-center,door,transition-roof,transition-wall}-v144.png`, 28 frames each in 4×7 RGBA atlases. Only the luminous fire regions are visible; wood, sky, smoke and rectangular patch borders are transparent. The left screen edge also uses the background's 160-pixel fade. The existing original scenery remains visible through the rest of each quad, so the layer cannot cover the blended join with an opaque square.

Two new sheets were made with the built-in image generator from exact transition-house roof and broken-window crops. Prompt set: six tightly packed 3×2 context panels, identical structural coordinates and painterly colors, animate only existing small orange flames behind the roof ridge/rafters or inside the damaged lower opening; retain surrounding smoke, roof, wall, debris and light; no pasted bonfire, oversized blaze, particles, glow or moving architecture. Raw sheets and references are adjacent. The other three locations reuse their v143 generated source sheets.

Normalize with `python scripts/normalize_fitted_fire_v144.py`. Stationary context is registered to the original art, fire color is matched, structural occlusion masks stay fixed, and seven source phases interpolate to 28 frames. The transition window uses a bounded cavity matte preserving its center mullion. `normalization.json` records registration and masks; all matte images are saved alongside previews.

Run `node scripts/bake_forest_fire_v144.cjs` to restore the earlier house plate, extract four metal bowl-front silhouettes, and render the actual overlapping panels, background edge fades, atlas frames, smoke crossfades and depth ordering. QA images: `house-left-border.png`, `transition-house.png`, `village-smoke.png`, `arena-braziers.png`.

Runtime: `dist/forest-ambience.js`. Generic fires are disabled on both house panels; drifting smoke is enabled on both (four village columns plus two earlier-house columns). Arena flame widths compensate for transparent sprite padding so their bases fill the metal rims. Original metal bowl fronts render over the lower flames; anchors stay fixed during flicker.

Validation: `checks/forest-fire-v144.cjs`, Forest ambience and actual-scene tests, and loading checks pass. They cover transparent patch edges/animated frames, custom effects on both houses, six restored smoke layers, bowl-width/metal-front placement, exact transition-background restoration, all1101 textures, co-op camera anchors and level cleanup. Canvas composites were visually reviewed. Browser playtesting remains unverified.
