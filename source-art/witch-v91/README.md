# Selene walk and ground-heavy revision (v91)

Walk: 12 frames, one shared scale calibrated from the face-to-sole distance of
her approved idle. Head/body horizontal registration excludes the staff. The
original 168px stride length remains; each frame advances after 14px of travel.
The guide and diagnostic color keys prove that both feet swap their leading
order, with passing poses at indices 3 and 9. The final whole sheet recolors
those same leg shapes into the approved brown/gold armored flat-soled boots.
Final lower-body silhouette overlap with the checked keys is at least 0.81 IoU.

Ground heavy: eight forward staff-thrust poses. The contact pose (index 4)
starts exactly at the existing 0.35s impact. Front-facing range and lane checks
apply to enemies and destructibles. The flame graphic occupies the forward
half only and mirrors with facing. Throw and landing damage are preserved.
The aerial heavy remains a bilateral magical slam; other moves are unchanged.

Assets were drawn/edited with built-in ImageGen, then split and registered with
normalize_witch_v91.py. Source sheets, gait guide, checked keys, contact sheets,
and GIF loops are retained here. The v90 normalizer reapplies these overrides
when rebuilding all witch assets. Runtime source: src/witch.js, embedded with
sync_witch_runtime.py. The roster normalization table now covers 543 frames.

Generation briefs: exact approved Selene appearance; whole 12-frame walk loop
following the colored gait guide, both opposite contacts and passing poses;
recolor red/cyan diagnostic legs only, retaining pose outlines; whole eight-pose
forward-only staff-thrust cast with compact blue flare. All sprite sheets use
transparent backgrounds, right facing, fixed proportions and generous padding.

Verification: witch.cjs, witch-assets.py, witch-walk-v91.py,
player-normalization.cjs, huntress-render.cjs, character-select.cjs,
four-player-selection.cjs, knight.cjs and ultra-shield.cjs passed. Browser
control is unavailable; no browser playtest or Windows executable build ran.
