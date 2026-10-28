# Garran steel finish

The approved single-frame preview is retained as approved-preview.png.
All 149 knight animation canvases receive a deterministic RGB-only steel material pass during loading. The generated grayscale detail texture is dist/assets/effects/knight-steel-detail-v127.png. Neutral silver components receive subtle worked-metal variation and patina; warm cloth, wood, leather and red remain excluded.

Original sprite PNGs are untouched. Alpha, anti-aliased contours, dark ink, dimensions, anchors, poses, animation keys and timings are preserved. The pass is cached once per texture manager and applies only to Garran.

Validation: checks/armor-finish.cjs accepts a directory containing original RGBA frame exports and a 256px material tile. All 149 frames passed immutable alpha/contour/ink/source checks and deterministic output checks. Representative idle, walk, pickup, bash, ground combo and victory renders were compared visually at identical coordinates. Browser playtesting was unavailable.
