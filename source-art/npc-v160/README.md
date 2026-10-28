# NPC visual stability v160

All five rebel roles audited: swordsman, ironshield, spearman, crossbowman and knight captain, 150 images across idle, walk, attacks, defense, hurt, throw and death. The original standing silhouettes remain the standard NPC reference. Upright frames are normalized by helmet-to-floor landmarks, excluding weapons and plumes; action clips use conservative common scale corrections so crouched/falling bodies retain their pose. Canvas sizes, foot origin408, and renderer scale are preserved. Strong sole pixels are reanchored and transparent gutters verified.

`normalization.json` lists every frame, applied factor and final bounds. The before/after sheets show every pose. Head template inspection rejects low-confidence rotated matches; in particular, the spearman's broader head artwork is not mistaken for a need to shrink the entire body by 23%.

Reproduce from the original committed v159 assets with `scripts/audit_rebel_heads_v160.py`, then `scripts/normalize_rebels_v160.py`. No new generated artwork was needed.

Cage stability uses `scripts/stabilize_cage_v160.py`: the neutral cage is fixed across all idle frames; only small cloth patches between bars retain the subtle breathing differences from the approved generated poses. Damaged cages use a fixed damaged structure. Tests compare the rest of every frame byte-for-byte.

AI now retains a valid close combat target, commits for at least2.4seconds when farther away, and only changes to a substantially better distant target. Invalid/dead targets are replaced immediately. Turns require a sustained direction change for0.28seconds outside a24pixel overlap zone; attack, guard, reload and hit-reaction poses do not track a moving target by flipping every update. Bulwark's existing slower turn rule is preserved.

Seeded90second 5v5 run: target changes359→6; facing changes36→20. Targeting/facing tests cover both factions, surrounding distance jitter, target death, overlapping opponents and locked strikes. Existing formation, autonomous combat, rescue, scene lifecycle, co-op, shield/parry and airborne-hit checks pass. Browser playback was not verified in this update.
