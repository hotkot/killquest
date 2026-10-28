# Knight combo, parry and squad reversal — v141

Three palettes have 12 additional hand-drawn animation frames each, generated with the built-in image tool. Runtime frames: `dist/assets/characters/commander-{crimson-lion,azure-griffin,ochre-stag}-combat-{00..11}.png`. Original walk/grapple/death frames remain in use.

Prompt set: reference each palette's approved `commander-{variant}-16.png`; preserve outfit, heraldry, helmet, body proportions, right-facing silhouette and cel shaded fantasy outlines. Draw a complete transparent 4-column × 3-row, 12-frame production sprite sheet with generous gutters and one intact longsword per body. Row 1: windup, body rotation, horizontal slash, follow-through. Row 2: low ready, gradually raised blade, upright brace, firm diagonal forward parry. Row 3: deflection, quick counter windup, forward/down counter cut, low ready recovery. No shield, text, scenery, floating parts or clipped sword tips. Generated as three full sheets, not individual frames.

Normalize with `python scripts/normalize_captain_v141.py`. One global scale per palette, calibrated to the shipped idle's body height; all frames use 512×448, foot y408/body x256, complete isolated alpha components. Raw masters and normalized preview JPGs are in this directory.

Combat: random 1–3 ground strikes: downward slash, horizontal slash, thrust. Durations .72/.64/.68 seconds; damage 20/18/22. A chain stops when its target escapes to the rear or out of reach/lane. Facing stays locked during the strike. Occasional parry has a vulnerable 1-second setup and a 1.65-second active hold. A frontal ordinary hit is deflected into a .16-second-impact, 18-damage counter. Rear attacks, grabs and rage remain counters. Unused stance expires and movement resumes; five-second stance cooldown. Both attack and counter retain normal shield, airborne and invincibility checks.

Squad: when no living, non-respawning player remains in the facing half-plane, wait .7 seconds then turn shields together, mirror support-rank slots and advance toward the other side. Maintain facing if any valid player stays in front; do not oscillate when no target remains. Survivors still close ranks; captain death still releases ordinary individual AI.

Checks: `knight-captain-v141.cjs`, `city-formation.cjs`, `carion-render.cjs`, city guard/bulwark/spearman/crossbow regressions, airborne projectiles and Forest campaign. Actual scene adapter covers 1043 resources and all captain skins/attack/parry/counter states. Browser playtest remains unverified (prior preview approval rejection).
