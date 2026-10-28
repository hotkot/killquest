# City curb movement regression

Replace axis-only rejection at road boundaries with a constrained edge-following candidate. Horizontal input advances along upper/lower boundaries; vertical-only input projects onto a sloped curb. Clamp to the actual road, cap displacement to the original movement budget, and accept only positions outside solid prop colliders. No speed boost or prop bypass.

Round the authored pavement samples with monotone cubic Hermite interpolation (weighted harmonic tangents). Curves preserve every traced landmark and never overshoot between samples. Full prop-footprint checks still pass against the new curves.

Validated:
- `node checks/carion-city.cjs`: 6,848 exact-edge cases across the full city, both directions, upper/lower edges, horizontal/outward diagonal inputs; progress, containment, speed cap. All four heroes complete the empty-road city while holding Right, from either edge. Existing solo/four-player traversals with props and collision stress also pass.
- `node checks/carion-render.cjs`: scene/camera registration.
- `node checks/forest-arena-entrance.cjs`: Forest unchanged.
- `node --check dist/game.js`, `git diff --check`.

Browser verification remains unavailable under the previous preview approval denial. No EXE build.
