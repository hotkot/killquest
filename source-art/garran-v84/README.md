# Garran: prescribed second-strike sequence

The second ground strike uses exactly nine frames in the requested order:

1. Source row 3, column 2
2. Source row 3, column 3
3. New full back-facing pose
4. New rear-right turning pose
5. Source row 2, column 3
6. Source row 2, column 2
7. Source row 2, column 1
8. Source row 1, column 3
9. Source row 1, column 2

The seven selected original poses are copied byte-for-byte from the preserved reference PNGs. The two new frames were drawn together using the built-in image-generation tool, then normalized with a single shared scale, stance center x320 and planted baseline y408 on transparent 640×448 canvases. Raw generated asset: `back-transitions.png`. Final runtime assets: `../../dist/assets/characters/knight-cross-00.png` through `knight-cross-08.png`. The exact generation prompt is recorded in `generation-prompt.txt`.

Reproduce with `python3 scripts/normalize_garran_v84.py`. First-slash and final-stab PNGs remain byte-identical, verified against the preserved SHA-256 manifests. Second strike duration .48 seconds, contact .24 seconds, combo link .46 seconds; damage, range and movement unchanged. Contact now uses frame 5 (zero-based 4), the original R2C3 pose. Full buffered combo remains 1.36 seconds. The former endpoint overrides are deliberately not applied because they would replace the explicitly requested first and last poses.

`second-strike-preview.jpg` labels the exact order. `combo-preview.gif` shows all three strikes at the buffered animation cadence, without world-space stepping. Asset integrity, exact source-frame matches, frame reachability, contact timing in both directions, scene resources and cleanup checks pass. Browser visual playtesting was unavailable. Hosted web update only; no Windows EXE build.
