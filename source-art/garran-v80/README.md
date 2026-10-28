# Garran reference-guided cut and faster combo

The user supplied `user-slash-reference.png`: the hand moves from behind/above the head to high-forward and then shoulder height while the blade remains upright; the blade passes through horizontal before following through low. Built-in image generation used this diagram as the motion reference and the shipped Garran idle as the identity reference. `generation-prompt.txt` records the exact full-strip prompt. A transparent cutout pass removes the original generation's surrounding haze without intentionally changing the poses.

The first strike now has eight selected poses. The approved grounded spin is compacted to twelve poses by removing its held recovery frames; the full right/back/left/front/right turn remains. All twelve final stab PNGs are unchanged, verified against recorded SHA-256 hashes.

Reproduce assets with `python scripts/normalize_garran_v80.py`. Each generated strip uses one shared scale, planted boot registration and a centered torso. The spin source frames are retained next to this note so compacting is repeatable. Final canvases remain 640×448 with transparent weapon padding. The spin's start matches the new low cut finish, and its end matches the preserved stab start.

Ground combo timings: slash 0.44s, spin 0.48s, stab 0.56s, with buffered transitions at 0.42s and 0.46s. Full chained duration is 1.44s, versus Kael 1.415s and Lyra 1.400s in the same simulation. Contact-based frame timing aligns the first hit with the level blade pose, not a raised downward-pointing sword. Damage and the other moves remain unchanged. Browser playtesting was unavailable; sprite review, scene lifecycle, combat and timing checks were used.
