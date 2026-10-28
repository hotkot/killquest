# Carion Spearman

One new spearman walks into the test arena from the right, joining the existing guards, Ironshield and crossbowman. Forest/City campaign populations are unchanged.

110 HP, 16-damage thrust, 225 score. He prefers about 195px distance, approaches at 92px/s, and backs away at 112px/s when players crowd within 145px. Players can close faster than he retreats. Spear reach 245px is longer than the sword guard’s 145px. The attack has a 0.56s wind-up, contact window 0.56–0.74s, 1.12s animation, and 0.90s cooldown. Facing and co-op target lock throughout the attack. It hits at most once, only in front, within 30px of the lane. A 45px close shaft deadzone and the recovery give opportunities to rush/grab him; sidesteps, jumps, dodges and Garran's directional shield also counter it. No armor or special grab immunity. Existing stagger, throw, fall, death, score and enemy HUD behavior are supported.

## Assets and generation prompt

Built-in image generation, reference `dist/assets/characters/city-guard-00.png`. One transparent 4-column x6-row sheet, 24 poses (`sheet.png`). Shipped `dist/assets/characters/city-spearman-00.png` through `city-spearman-23.png`. Source frames are normalized with one 1.12 scale, a 768x448 canvas, shared body center x384 and foot y408. Wide transparent canvases preserve the entire spear without shrinking the body. All spear tips remain inside frame bounds; contact range matches the full-extension tip at runtime scale. `preview.jpg` is the inspected normalized contact sheet.

Prompt: Production sprite sheet for KillQuest, matching existing city guard's gritty hand-inked 2D 80s fantasy cartoon, bold black outlines, readable cel shading and sturdy human anatomy. New city spearman with steel open-faced helmet, muted purple tunic, leather belt/boots and dull steel shoulder armor. No shield/sword. One long straight wooden spear with one leaf-shaped steel tip, held in both hands. Same character/body scale, costume, palette, spear design and length throughout; always face right. Spear longer than character height, one continuous attached shaft, no detached/duplicated tips. Exact 4 columns x6 rows, 24 full-body sprites in wide equal horizontal cells with transparent gutters; no text, borders, scenery, ground shadow or effects. Keep body at consistent left-of-center anchor and never crop weapon. Row1 first 4 walk poses with low diagonal spear. Row2 next 4 walk poses with crossed legs. Row3 first 4 thrust poses: chest-ready, draw back/body twist, extend, full lunge. Row4 next 4 thrust poses: full horizontal extension, held follow-through, withdraw, ready. Row5 idle, breathing idle, hurt, grabbed. Row6 lifted, airborne sideways thrown, collapsed, defeated. Same head/torso/outfit size through crouched/falling/prone poses; never enlarge smaller poses to fill slots. All frames in one transparent sheet.

## Verification

`checks/city-spearman.cjs`: offscreen test entry; all four heroes/both directions; reach beyond sword range; windup, once-only contact and recovery; exact tip/depth/rear/close limits; jump/invincibility/Garran shield; approach/retreat and facing lock; stagger/grab/throw; co-op target lock; HUD/score/frames; campaign isolation.

`checks/carion-render.cjs`: actual scene adapter loads all 935 textures and renders new wide-frame idle/walk/attack/hurt/grab/throw/down/dead poses at the shared body/foot anchor.

Also passed city-guard, city-bulwark, city-crossbow, projectile-airborne, JS syntax and diff checks. Sprite contact sheet inspected offline. Browser playtesting remains unverified under the existing preview denial. No executable build.
