# Anchored cage destruction

`anchor_cage_v161.py` reuses the approved v160 artwork, registers every damaged/destruction frame to the neutral cage's front platform pivot (239,448), and reconciles the older collapse set's scale. It does not center on the changing debris silhouette. `anchors.json` records each source landmark, shared collapse scale and translation. `anchored-preview.png` shows the world-fixed pivot on every stage.

Cage debris fades during the last0.22seconds and is removed from the model and scene at0.72seconds. Ordinary destroyed props retain their existing12second lifetime. Rescue remains once-only and immediate on break; the cage stops blocking movement immediately.

Checked: eight pivot registrations within0.5source pixels, unchanged model position, timely model/sprite cleanup, released soldier persistence, other-container lifetimes and existing cage/rescue/scene stability checks.
