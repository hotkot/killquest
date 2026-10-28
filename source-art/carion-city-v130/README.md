# City world-space scenery correction

Removed the v129 half-camera-speed compensation. It moved the painted floor at a different speed from actors and collision props. City ground and architecture now have fixed world positions and share the main camera exactly with all props and actors.

The world remains 25,600px (Forest: 12,800px). Six newly generated connecting panoramas expand the environment from six to twelve unique sections. Each district's original scene is followed by its own new connecting street. Twelve panels cover x0 through x25600, with 320px overlaps, no gaps, mirroring or adjacent reuse. Each panel is ~2426.7px wide, rather than stretching the original six across twice their prior span. Walking speeds, animation cadence, input and collision bounds are unchanged.

New built-in ImageGen source PNGs are retained here. Prompt set: match existing market panorama style, viewpoint, building scale and empty y470–650 cobblestone lane; create six distinct new links (outskirts-to-gates, gate-barracks-to-market, market-to-houses, residential-to-prison, prison-to-royal-barracks, final citadel courtyard), 3:1 horizontal comic fantasy, consistent cool smoky light, neutral join edges, no characters/UI/text, no mirroring. WebP delivery copies are dist/assets/city/*-link.webp.

Regression checks now enforce full world-space panel coverage, unchanged panel/collider relative positions during camera motion, exactly100px scenery movement for100px camera travel, and identical one-second walking displacement in Forest and City for all four heroes. Full route traversal, destruction/collision, no enemy spawning, co-op tether and map/selection checks retained. Browser preview remains unverified after its approval gate denied access in the preceding work; no alternate browser route used. No EXE build.

Current layout: v131 replaces city overlap blending with eleven tailored opaque architectural joins, adds three down-right passages and vertical camera follow, and binds movement to painted street corridors. See ../carion-route-v131/README.md.
