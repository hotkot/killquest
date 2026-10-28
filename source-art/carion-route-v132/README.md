# Carion City pavement and placement correction

The old collision lane was a generic center +/-45px and narrowed by another 25px at every connector. It did not describe the artwork. Replace it with separately traced rear and foreground pavement edges for all twelve panels and eleven opaque fitted joins. Coordinates use the actual displayed panel heights (720/1040) and connector dimensions (768x720), with an 8px foot clearance. Join endpoints sample the adjacent panel traces for continuity. Camera follows the midpoint of these same bounds.

All 50 prop bases are fitted across their complete collision width to the traced pavement, with clearance. Food containers near wide solid props move horizontally to avoid overlapping bases. Breakable barricades remain destructible. Prop textures already end at their common 240/256 ground anchor, so no art transform change is needed.

City movement now resolves road and object constraints together in <=4px swept steps. A separate object pass followed by road projection could push an actor into the other constraint. The unified resolver accepts only points valid for both and allows axis sliding; decorative connector artwork has no separate collision box. Forest mechanics are unchanged.

Verification:
- `node checks/carion-city.cjs`: solo and full four-hero traversal with all actual props; unchanged walk speed; three real descents; camera/tether; wall-safe actions; independent artwork landmarks; every prop footprint on road; 44 bidirectional edge-lane connector crossings; solid/curb diagonal collision stress.
- `node checks/carion-render.cjs`: actual scene resource/camera registration and cleanup.
- `node checks/four-player-selection.cjs`, `node checks/forest-arena-entrance.cjs`, `node checks/city-join-fit.cjs`.
- `python scripts/check_city_pavement_v132.py`: reproducible offline image review, composites runtime join-fitting output and actual prop sprites with rear/foreground edges and footprints. All twelve sections reviewed in `pavement-and-props.jpg`.

Browser automation was unavailable due to the existing preview approval denial; no browser verification is claimed. No executable build.
