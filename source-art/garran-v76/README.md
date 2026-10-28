Garran — closed-helmet, sun-tabard knight (v76)

Approved concept: approved-concept.png. Six generated whole-sheet animation groups plus a separate eight-frame grapple. All final frames are normalized by scripts/normalize_garran_v76.py onto 448px RGBA canvases, fixed ground y408, one scale per source sheet. registration.json records source bounds and scale.

The utility source's discarded final eight poses contained touching figures, so grapple.png replaces that clip. Its duplicate-sword hurt pose is excluded from playback by copying the clean final recovery pose. Pickup poses are reordered into one kneel/reach/rise sequence. Exact pose copies connect sword and aerial combo endpoints. No runtime atlas slicing is used; every frame is an individual PNG.

Runtime: ground swords, aerial swords, shield charge, bilateral aerial slam, walking one-second front guard plus .32-second vulnerable lowering, Sunfall rage, standard pickup/grab/throw/respawn/death and victory. Dedicated shield cues are processed from existing hit/heavy/swing recordings with the same source licensing as those recordings.
