# Garran second strike: diagram-guided diagonal cut

Built-in image generation used the supplied `user-second-cut-reference.png` as the motion guide, the existing low first-strike finish as its start reference, and the preserved stab chamber as its recovery reference. The exact full-strip prompt is recorded in `generation-prompt.txt`.

The twelve poses show low transition, an upper-left/back blade chamber, upright sword, upper-right positions, level forward contact, descending rightward cuts, then a low down-left trail slightly behind the hip before recovering for the stab. Shoulder/hip rotation, forward lean, bent front knee, rear-leg loading and cape movement accompany the arm path. This is a single diagonal cut with a modest body turn, not a spin.

`python scripts/normalize_garran_v82.py` reproduces the second-strike PNGs from the complete 3×4 source sheet with one shared scale, stance-based centering and planted boot registration. Canvas remains 640×448, with full weapon tips and transparent padding. Only the new second strike's endpoints are matched to existing adjacent poses.

All eight first-strike and twelve stab PNGs are byte-for-byte unchanged, verified by stored SHA-256 records and automated checks. Combo timing, damage, controller mapping and movement are unchanged: the second strike lasts 0.48s with its sixth pose contacting at 0.24s, and the full buffered chain remains 1.36s.

Sprite padding/connectivity/registration, preservation, complete frame selection, hit timing, collision and scene lifecycle checks passed. Browser playtesting was unavailable. The animated preview shows the sprite sequence at its current buffered cadence; the game additionally applies its existing forward stepping.
