# Burning-village fire correction — v143

The village panel's original static fire and smoke are restored. Its generic fire and smoke overlays are disabled. Existing cloth motion is retained, with only the cloth silhouettes removed from the restored static plate.

Three custom animations replace prominent fires at exact source coordinates: left roof hollow `(30,25,160,113)`, burning window/collapsed rafters `(320,120,168,127)`, and doorway `(414,316,56,94)`. Each uses a 28-frame opaque context atlas, `dist/assets/forest/ambient/village-{roof-left,roof-center,door}-v143.png`. Background: `bg-village-v143.png`. Runtime integration is in `dist/forest-ambience.js`.

The built-in image generator was used for three separate six-frame sheets. Prompt set: repeat the exact attached crop in a 3-column × 2-row sheet; preserve the original framing, palette, masonry, thatch, charred timbers, mullions and doorway debris at identical positions; animate only the existing flame tongues behind those structures. No isolated bonfire sprite, new smoke, scenery, particles, relighting or flame outside the existing cavity. The roof, window/rafters and doorway each received their own location-specific prompt and original crop reference. References, raw sheets, registered previews and normalization metadata are adjacent.

Normalize with `python scripts/normalize_village_fire_v143.py`. Stationary context is registered to the original crop; one transform per location is shared by its six generated phases. Only the original luminous fire areas and their soft fringes change. Original dark structural pixels and patch borders remain byte-identical in all frames. Seven key phases (original plus six generated) interpolate to 28 loop frames, packed 4 columns × 7 rows. This keeps the building fixed and avoids rectangular overlay edges or fire appearing in front of beams.

Run `node scripts/bake_village_fire_v143.cjs` to restore the original village plate with local cloth cutouts and produce composites. `before-after.jpg` compares original art with the revised placement; `scene-{0,7,14,21}.png` shows sampled phases with cloth included.

Checks: `checks/village-fire-v143.cjs` verifies original smoke/fire restoration, no generic village overlays, all three loops, unchanged dark beams/debris and patch borders, cloth retention and world anchors. Forest atmosphere/resource and actual-scene checks pass with all1095 textures. Browser playtesting remains unverified; native Canvas composites and the registered animation sheets were visually reviewed.
