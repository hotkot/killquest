# Walk scale correction (v89)

Frames 12–15 came from a wider, oversized source row. Their helmets and shoulder
mass visibly expanded compared with frames 0–11. The reproducible script
`scripts/normalize_garran_walk_v89.py` scales width only around the existing
center and sole anchors using the preserved originals. This avoids stretching
crossed legs to a common silhouette height. All sixteen runtime walk scales are
now 1; original timing, order, floor registration and leg crossings remain.

Reviewed `walk-corrected.jpg` at a constant scale. `walk-corrected.gif` contains
the entire cycle. Campaign start/replay rage and boss airborne slash regression
coverage is in character-select.cjs and bandit-king.cjs. Other boss attacks retain
jump clearance; sword sweep respects facing, lane, invincibility and per-beat hits.
Browser QA unavailable in this environment; simulation and renderer checks pass.

## v97 height repair
The source poses already stood 231–233 pixels tall. Removed the extra vertical
shrink from frames 12–15, retaining width correction and the y=408 sole pivot.
The full 16-frame cycle now varies by only three pixels, preserving gait bob.
