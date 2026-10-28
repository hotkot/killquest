# Garran horizontal second cut driven by body rotation

Built-in image generation redraws only the second ground-combo strike as a level waist/chest-height slash. The windup opens the chest toward the viewer, hip and shoulder rotation drive contact toward the right, and a rear-quarter follow-through changes the visible sun-tabard/shoulder/cape silhouette. This is a limited body twist, not a full spin. The sword stays level during the active cut, with pivoting rear heel, bent front knee and weight transfer.

The complete strip uses twelve poses in a 3×4 layout with separate full-length swords. `generation-prompt.txt` records the prompt. `python scripts/normalize_garran_v83.py` reproduces game PNGs with a shared scale calibrated against the standing chamber pose, stance-centered horizontal anchor, fixed planted baseline and transparent 640×448 canvases. Endpoints match the existing first-cut finish and stab chamber.

First-strike and stab images remain unchanged, guarded by SHA-256 checks. All move timings, damage, ranges and stepping remain unchanged; full combo duration remains 1.36 seconds. The animated preview uses the current buffered cadence without world-space stepping. Browser playtesting was unavailable; final source poses, sprite integrity, frame/contact timing and scene lifecycle are checked before publication.

The corrected strip removes the extra unarmed hand from the initial pass. The follow-through turns into a rear-quarter pose and then recovers rather than completing a full spin. The first pass is retained only as unused source history.
