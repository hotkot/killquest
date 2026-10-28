# Carion City Guard
Generated with built-in ImageGen, using the shipped sword bandit as a style reference. Prompt: 24 transparent comic fantasy city guard poses, 6x4 layout; dark steel open helmet, purple tunic, crown round shield, one sword; six walks, six sword strikes/recovery, two idles, two blocks, hurt/death, six grab/throw/landing poses. Full prompt retained in the conversation.

sheet.png retains the generated source. scripts/normalize_city_guard_v128.py separates connected sprites (including sword extensions across grid gutters), uses one shared .88 scale, and exports 24 transparent 448px canvases with 408px foot anchor. preview.jpg verifies isolated poses.

Two guards enter the test arena from the right. 110HP, 15 sword damage, 200 points. Frontal light guard lasts .58s, then .20s lowering recovery, 2.7s repeat cooldown. Facing locks during guard. Grabs, rear attacks, heavy launches and rage bypass guard. Human bandit death audio is reused; shield contacts use shield-hit. Forest roster is unchanged.

Automated checks cover entry, block direction/recovery, playable-character counters, grab/throw, contact timing, score and all state frame paths. No browser playtest available in this environment.
