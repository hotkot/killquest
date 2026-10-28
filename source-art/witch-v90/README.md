# Selene, the Blue Pyre — fourth playable hero (v90)

Approved design: silver hair, no hat, black/cobalt clothing, wooden blue-crystal
staff. The exact approved image supplies her selection portrait and life head.
The original whole animation sheets are retained beside their registered
previews. 68 character frames and 12 flame/impact/storm textures ship in dist.

Motion: 4 idle, 8 walk, 4 jump. Combat: three distinct six-pose ground casts and
six aerial casting poses. Powers: four poses each for bilateral push, magical
slam, teleport and firestorm. Support: hurt/fall/rise, empty-hand pickup, victory.

`normalize_witch_v90.py` uses fixed scales per source group and anatomical
center/sole registration, with torso registration for flight. Overlapping row
crops retain staff tips; connected-character extraction removes neighboring
fragments and invisible RGB backgrounds. Utility/crouched poses retain natural
height instead of being enlarged. `normalize_player_render_v86.py` includes
these frames in the existing roster-wide normalization manifest (535 frames).

Runtime authored in src/witch.js and embedded via sync_witch_runtime.py. Rules
remain in Combat; scene rendering owns disposable projectile/effect sprites.
Flame bolts use swept collisions, lane/height checks, owner IDs and a short
lifetime. All effects are pooled by simulation object and disposed on reset.

J / X / square: three blue-flame casts, or diagonal downward casts while airborne.
K / Y / triangle: bilateral 45-damage flame push, or bilateral 50-damage aerial
slam, plus 25 landing damage on thrown enemies. Heavy overrides queued light.
L / B / circle: invulnerable 190px backward teleport, respecting bounds/props.
I / RB / R1: 200-damage, 680px forward firestorm; one hit per enemy per cast.
Firestorm landing damage does not recharge rage. Boss armor stays intact.
Space / A / cross jumps. Shared grab/throw, pickup, lives, respawn and score work.

Four independent controller selection panels now each expose four heroes;
claimed characters remain unavailable. All players must confirm to launch.
Campaign starts/replays empty; the test arena remains full rage for testing.

Verification: offline sprite-sheet review; simulation, four-controller lobby,
actual renderer-resource/lifecycle checks, campaign and existing-character
regressions. Browser control unavailable, so no in-browser visual playtest.
No Windows executable build requested or performed.
