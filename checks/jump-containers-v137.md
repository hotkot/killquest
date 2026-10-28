# Longer player jumps and container clearance

All four heroes now use a shared 1.65 multiplier on horizontal and lane travel during jumps, including aerial attack movement. Jump height, 0.84-second base timing, animation timing, damage and normal walking speed are unchanged.

Container bounds accept an optional actor. Players with feet more than 8px above ground ignore breakable container footprints. Grounded players, dodges, NPCs/enemies, and permanent scenery keep normal collision. Both Combat and the City road resolver use the same actor-aware filter; city pavement remains enforced in the air. Landing inside a container resolves to its nearest legal edge/lane. Jumping itself does not damage containers or produce loot.

Passed `jump-containers.cjs`: measured +65% travel with unchanged height/timing; all four heroes both directions over six container kinds in Test/Forest/City (144 full-frame cases), restored grounded collision, overlap landing, permanent scenery, non-player collision, and independent co-op jumping/grounded players. Also city-bulwark, projectile-airborne, knight, carion-city, carion-render, syntax and diff checks. Browser playtesting remains unverified. No executable build.
