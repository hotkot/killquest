# Carion Crossbowman

Added one city crossbowman to the test arena, entering from the right, alongside the two guards and Ironshield. Campaign populations remain unchanged.

95 HP, 225 score, 24-damage bolt at 720px/s. Aim locks to the target position at windup; release at 0.62s, firing animation 1.15s. Afterward he reloads stationary for 1.90s, then has a 0.25s ready pause. No second shot is possible without completing reload. Stagger/grab/throw pauses reload without resetting it or granting a loaded weapon. He prefers distance and backs away when approached, with ordinary navigation/collision.

Bolts use shared swept 3D projectile/body contact, so player lane and actual airborne body height determine hits. Nonlethal hits launch the victim 235px in the travel direction, then use existing flight, knockdown, recovery and invincibility. The launch preserves airborne height at impact. Lethal hits use normal life/death handling. Garran can block frontal bolts; dodge/rage/respawn invincibility works. First valid player contact consumes the projectile, including co-op ordering. Ordinary archer arrows still deal their existing 9 damage and hurt without launch.

Crossbow release is registered to the normalized firing frame: muzzle forward62 / height112 in world space. Bolt rendering reuses the drawn arrow asset at a shorter 58x14 size. Fire uses a lower-pitched bow twang; impact uses the heavy hit cue. Reload/aim/walk/grab/throw/down/death have dedicated sprites.

## Assets and prompt

Built-in image generation, one transparent 30-frame six-column/five-row source sheet (`sheet.png`), style reference `dist/assets/characters/city-guard-00.png`. Shipped frames `dist/assets/characters/city-crossbow-00.png` through `city-crossbow-29.png`. Shared scale .90, 448px canvas, fixed foot anchor408, explicit body anchors. Normalization excludes disconnected generated bolt and blood flecks because runtime owns those effects. `preview.jpg` is the inspected contact sheet. All frames retain their pose height and common body scale.

Prompt: Production game sprite sheet for KillQuest. Use the existing city guard as style/costume-family reference: gritty hand-inked 2D 80s fantasy cartoon, bold outlines, readable simple cel shading, sturdy human proportions. New CITY CROSSBOWMAN with steel open-faced helmet, purple/charcoal padded tunic, dull steel plates, leather bolt case and brown boots. One medieval wooden crossbow with metal limbs, stirrup and string; no shield, sword or modern firearm. Always face right, consistent outfit/weapon/body scale. Upper-chest-height horizontal firing. Exact 6 columns x5 rows, full bodies, equal slots, generous transparent gutters; no text, borders, scenery or ground shadows. Row1 six walking poses with crossing legs/crossbow low. Row2 six aim-and-shoot stages: lift, aim, hold, release, recoil, lower. Row3 six reload stages: lower, foot in stirrup, bend/pull string, cock string, place one bolt, raise ready. Row4 two breathing idles, two hurt poses, grabbed, lifted. Row5 three thrown/falling poses, two lying down poses, settled dead. Two arms/two legs, one attached crossbow only, no duplicated/detached parts. Same head/torso size in standing, crouch and prone; do not enlarge smaller poses to fill slots. Entire animation sheet in one transparent image.

## Verification

`checks/city-crossbow.cjs`: offscreen entry; aim/single-release/reload cycle both ways; interrupted reload; all four heroes both-direction damage→launch→down→recovery; airborne launch-height continuity; invincibility, lane, shield and first co-op contact; aim/target lock; grab/throw; lethal life decrement; all animation assets, score and campaign isolation.

`checks/carion-render.cjs`: actual scene adapter renders all new states, short bolt size and correct muzzle height, original arrows unchanged.

Also passed city-guard, city-bulwark, projectile-airborne, knight, jump-containers, JS syntax and diff checks. Sprite preview and muzzle registration inspected offline. Browser playtesting remains unverified under the existing preview denial. No EXE build.
