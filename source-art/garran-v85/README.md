# Garran second strike: concealed blade on rear poses

Replaced second-strike frames 1, 2, 8 and 9 (zero-based 0, 1, 7, 8), which previously pointed the blade behind the attack direction, with four back-facing poses. The blade is fully hidden behind the character during those poses. The five intervening poses, including the forward contact, remain byte-for-byte unchanged. First slash and final stab remain unchanged, with SHA-256 manifests retained.

New art was produced as one four-pose sheet with the built-in image-generation tool. The exact prompt is in `generation-prompt.txt`; the raw asset is `concealed-sword.png`. `scripts/normalize_garran_v85.py` uses one shared scale, planted ground y408 and a centered stance on 640×448 transparent canvases. Runtime sprites are `../../dist/assets/characters/knight-cross-00.png` through `knight-cross-08.png`; only 00, 01, 07 and 08 were replaced.

Second strike remains nine frames, .48 seconds long, with contact at .24 seconds and combo linking at .46 seconds. Full buffered combo remains 1.36 seconds. Damage, movement and ranges are unchanged. `second-strike-preview.jpg` shows the revised sheet and `combo-preview.gif` shows the full combo without world movement. Browser visual playtesting was unavailable. Hosted web update only; no EXE rebuild.
