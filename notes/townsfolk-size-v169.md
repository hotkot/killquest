# Townsfolk size

Compared actual townsperson idle and run sprites against the purple city guard and normalized green rebel guard on the same foot baseline. Townsfolk body/head mass was too large despite similar full-alpha heights. Reduced the shared civilian render scale from0.67 to0.56 (16.4% smaller), and shadows from54x12 to45x10. Applies uniformly to all six civilian types, idle/running states, Forest/City/Test. Preserved the408/448 foot anchor, sprite poses, animation timing, navigation, exit and despawn rules.

Verified a side-by-side rendered sprite comparison, JavaScript syntax, City/Forest resource/scene adapters and NPC exit/rally/screen-bound behavior tests. No new image assets, EXE build, or browser visual QA.
