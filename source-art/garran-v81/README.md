# Garran: quicker body-driven cut, horizontal slash, preserved stab

The first cut now animates rear-leg loading, hip/shoulder rotation, a bent front knee, forward lean, cape follow-through, and low recovery. Its blade follows the previously supplied upright-to-forward cutting reference. Runtime adds a collision-aware 18px forward step. Duration is 0.36s, impact 0.18s, and the next strike can begin at 0.34s (Kael's first chain point is 0.33s).

The spin is replaced with a horizontal cross-body slash, remaining right-facing with a modest torso twist. The twelve-frame sheet uses a 3-column × 4-row layout to keep all sword tips separate. The original touching-tip pass is retained as unused history. Source pose 10 contained an extra cut; the preceding low follow-through is held instead so this is a single slash. Horizontal duration/impact remain 0.48/0.24s; contact is the sixth drawn pose.

All twelve stab PNGs, their 0.56s duration and 0.28s contact remain unchanged. SHA-256 preservation checks are recorded and tested. Full buffered combo duration is 1.36s.

Built-in image generation produced whole strips using the approved Garran seed; exact prompts are stored here. `python scripts/normalize_garran_v81.py` reproduces final 640×448 PNGs with one shared scale per strip. First-pose body height establishes scale so crouching stays shorter rather than making the standing knight grow. Stance/boot anchors retain the torso lean instead of recentering the chest in every frame. Alpha-core extraction and a small morphological opening remove generated background/grid artifacts while retaining original pixels around each silhouette. The horizontal strip uses its full alpha silhouette so blade tips stay complete. Exact endpoints join the two cuts and preserved stab.

Sprite margin/connectivity, contact frames, first-step collision in both directions, combo speed, scene lifecycle and Forest regression checks passed. Browser playtesting was unavailable. The animated preview shows sprite poses at the buffered combo cadence; world-space stepping is applied by the game.
