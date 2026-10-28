# Extended City atmosphere coverage

265 animated source-art regions, up from 116: 149 additional details. All twelve City panels and all eleven fitted architectural joins are covered. See coverage-summary.json for the per-section counts.

The missed joins are separate, opaque foreground architecture. Their atlases are baked from the exact fitted connector image and render above it at depth -9, rather than below it with the main-panel effects. Connector positions use the actual destination tile and 768×720 world transform, including the descents. Main-panel materials remain behind the architectural joins.

This pass also adds cart covers, washing lines, distant flags, merchant fabrics, small torches, larger lantern glow areas and wet reflections. Flame layers sort above light layers. Cloth and light patches now have material-shaped alpha masks, so an unchanged rectangular patch cannot cover another moving object. Metal medallions and supports stay fixed.

Reproduce with `node scripts/bake_city_ambient_v176.cjs`; it invokes `scripts/bake_city_joins_v178.cjs` first. Runtime assets retain stable numeric names, with the v178 query stamp invalidating prior atlases. Approximately 83 MiB decoded textures and 19 MiB compressed PNGs. Current scene/atlas tests cover all joins, placement, draw order, frame changes, clipping, preload registration, culling, and level cleanup. Browser playback was not retested in this session.
