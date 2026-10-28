# Lyra's grounded crescent-slash combo

Three new eight-frame grounded attacks replace the old stabbing poses:

1. High-to-low diagonal knife sweep.
2. Turning horizontal knife crescent.
3. Simultaneous crossed-blade diagonal finisher.

Each action has a readable chamber, four windup poses, contact in zero-based frame 4, and follow-through/recovery. Silver-white painted crescents are included in the sprites, inspired by the existing aerial combo. There is no jump, dodge roll or thrust in these ground strips.

Generated using the built-in image-generation tool. Exact prompts are in `prompts.json`. Raw source sheets: `slash.png`, `rise.png`, `finisher.png`. Each sheet has nine cells: eight attack poses and a separate upright neutral scale witness. `scripts/normalize_lyra_slashes_v87.py` isolates the figures and uses one shared anatomy scale per strip. The neutral witnesses match the approved idle's 219px body-core height; the comparison is retained in `scale-witnesses.jpg`. Action poses are never stretched to fill cells or resized individually to standing height.

Runtime PNGs are `../../dist/assets/characters/huntress-slash-00.png` through `huntress-slash-07.png`, plus the eight `huntress-rise-*` and eight `huntress-finisher-*` frames. All use transparent 640×448 canvases, body/stance center x320 and planted sole y403. The wider canvas preserves complete cutting arcs without shrinking the body. First/last ready poses are padded copies of the approved idle; adjacent strikes share byte-identical transition poses.

The common player normalization table was regenerated against these new assets with factors 1.0 for these already-normalized ground strips, preventing double scaling. The established airborne animations, bow, other Lyra actions and Kael/Garran art remain unchanged. The finisher contact has two tiny low-contrast silver edge streaks, explicitly reviewed as parts of the painted X trail rather than detached anatomy.

Timing/damage/movement are unchanged: .42s / .44s / .58s individual attacks, contacts at .19s / .20s / .28s, first links at .40s / .42s, and a 1.40s buffered combo. `combo-preview.gif` uses that buffered cadence without world-space stepping. `combo-preview.jpg` shows all 24 poses.

Validation covers source-art preservation outside these 24 frames, shared witness calibration, source gutters/full blades, painted contact crescents, exact transition seams, no double normalization, all 467 actual sprite render paths, both-facing Lyra combat/bow/aerial/rage behavior, character selection, other-character combat and source sprite integrity. Browser visual playtesting was unavailable. Hosted web update only; no EXE build.
