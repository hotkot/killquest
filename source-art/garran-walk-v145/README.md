# Garran walk v145
Eight readable poses replace the 16-frame cycle. Contact, weight shift, crossing and lift alternate between legs. Each cycle covers the existing 176 pixels of movement, with pose distances 26,22,18,22 repeated twice. Physics and movement speed are unchanged. Blocked or stationary players do not cycle.

Runtime assets: dist/assets/characters/knight-walk-00.png through knight-walk-07.png.
Source: sheet.png; normalized preview: preview.jpg and walk.gif.
Normalizer: scripts/normalize_garran_walk_v145.py.
Common scale 0.6, helmet center x232 and sole y408 on 448x448 canvases. The existing comic styling and armor finish remain active.

Generation mode: built-in imagegen, identity-preserving edit using the previous approved knight walk frame as reference.
Prompt:
Use case: identity-preserve. Production 2D game WALK CYCLE sprite sheet of the EXACT reference knight Garran. Closed helmet with red plume, weathered steel plate, white tabard with black sun emblem, brown inside of heater shield worn on forearm, straight sword carried low. Preserve reference drawing style, silhouette, armor textures, face direction RIGHT, camera and body proportions. EXACTLY8 distinct full-body frames in4columns by2rows with ample transparent gutters, SAME torso/helmet scale and stable body center in all frames. Clean controlled ordinary WALK, not run, march, attack or shuffle. Sequence left to right row1 then row2: 1 near leg forward heel contact/far leg rear toe; 2 weight shifts onto near foot, rear far foot lifts; 3 far leg passes forward across planted near leg: visibly CROSS both legs under hips, narrow passing silhouette; 4 far knee leads forward while near leg goes rearward; 5 far leg forward heel contact/near leg rear toe, reversed stride; 6 weight onto far foot, near rear foot lifts; 7 near leg passes across planted far leg: visibly CROSS legs under hips; 8 near knee leads forward/far leg goes back, naturally returns to frame1. Feet alternate forward/rear across the cycle; both crossing frames are essential. Keep helmet/shoulders/hips centered, <=2% body bob, sword/shield held quiet and consistent (no arm flailing); subtle plume movement only. One complete eight-pose cycle, not multiple repeated strides or 16 frames. Maintain anatomical leg continuity behind tabard, two legs two arms one sword one shield each frame. Actual transparency, no ground/shadows, no text, no grid or scenery. Full equipment tips and feet inside each cell.

Validation: targeted walk phase, crossing silhouettes, stable helmet/sole, blocked movement and five movement directions pass. Knight combat suite, baseline walking, Carion render, Forest scene resource checks, syntax and armor finishing on all eight new frames pass.
The broader player normalization audit has a pre-existing SHA mismatch for unchanged witch-air-cast-03; this was not altered. Browser verification was not run because browser preview was previously denied.

