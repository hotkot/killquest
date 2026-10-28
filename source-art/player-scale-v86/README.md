# Player animation normalization

All 467 playable poses are covered: 176 Kael frames, 136 Lyra frames, 149 Garran frames, and six older Kael fallback frames. `normalization.json` records the reviewed action scales, each frame's source hash, body silhouette measurement, sole registration, airborne status and render layout.

Normalization is non-destructive and applied by the actual game renderer. Original PNGs, approved frame order, combos, damage, collisions and move durations are preserved. The idle references retain the established equal 176.4px standing height. The main oversized sets corrected are Kael's aerial attacks and rage, Lyra's knife and aerial sets, and Garran's second slash/shield charge. Already-matched actions retain their scale. Independent source rows and clear outlier poses have their own calibrations; identical artwork shares a scale across transitions.

This is anatomy-reviewed calibration, not an automatic fit-to-bounding-box operation. Weapons, cape spread, raised arms and folded legs must not determine standing size. A morphological body silhouette measurement excludes most thin weapon geometry and was used to audit bulk discrepancies, with the complete before/after contact sheets reviewed by action. The group factors are explicitly recorded in `scripts/normalize_player_render_v86.py` and in the JSON report. Crouches and rolls remain compressed; airborne poses scale around the registered pelvis so scripted jump and rage heights remain unchanged. Grounded poses use their sole plane to eliminate floating during attack/utility frames.

The runtime table and both world/selection renderers use the same normalization. Selection previews preserve source aspect ratio instead of squeezing Garran's 640×448 sword frames into squares. Lyra's arrow release derives from her normalized bow-frame grip (296,260), scale and sole registration; projectile hit layers are unchanged.

Rebuild the table/report with `python3 scripts/normalize_player_render_v86.py`. The complete normalized contact sheets are `*-normalized-0.jpg` onward. `normalization-preview.gif` compares idle, walking, light combo and heavy poses at the real model's timing, using fixed horizontal presentation positions rather than world-space travel.

Validation: source PNG hashes, coverage of every player frame, identical-pose scale continuity, grounded soles, airborne pelvis invariance, aspect-correct previews, representative body-bulk outliers, the actual scene sprite renderer across all 467 frames, all-character combat and selection/co-op flows, source sprite integrity, and adjusted bow alignment. Browser visual/controller playtesting was unavailable. Hosted web update only; no EXE build.

## v87 follow-up
Lyra's three ground strips were subsequently redrawn and normalized directly in the PNGs. Their layout factors are now 1.0; other player calibrations are preserved. The current JSON report/table is regenerated against these updated assets. See `../lyra-slashes-v87` for source art and shared witness calibration.
