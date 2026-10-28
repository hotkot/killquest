# Garran animation tuning

Generated from the approved Garran design: eight calm idle poses, sixteen walking poses, slash/stab contacts, eight dedicated finishing slash poses, eight backward shield-step poses. Reproduce runtime assets with `python scripts/normalize_garran_v77.py`.

All frames use a fixed planted baseline of 408. Ground sword clips use 640×448 transparent canvases so the extended thrust remains uncropped; other clips use 448×448. Runtime origins stay centered with character-specific visual scales. All three playable standing silhouettes measure 176.4 game pixels.

Review corrections: the last four walking source figures were generated smaller; a shared row calibration corrects that before common strip normalization. The combined sword source produced an invalid last row and a touching thrust figure. The invalid row is unused, the touching figure is replaced by a held clean contact pose, and the final slash comes from the dedicated finisher strip. Combo endpoints share exact poses. Previews show actual final assets.
