# Hero comic rendering pass

Kael is the style reference and remains unchanged. `dist/hero-style.js` renders Lyra, Garran and Selene with broader color bands, restrained smoothing within similar colors, and stronger ink edges. Original PNGs remain unchanged. Every alpha byte, canvas size, frame key, pose, weapon position, foot anchor, frame sequence and animation timing is retained. Selene's cyan/blue emissive pixels and standalone effects are excluded from grading.

The pass runs once after preload and before scene sprite creation. Replacement canvas textures retain their original keys and dimensions. It is cached at the texture-manager level across scene restarts. Menu poster and character portraits are unchanged.

`before.jpg` and `after.jpg` compare representative idle, walk and attack poses at identical coordinates.

Validation: 537 source character images; 361 non-Kael images changed; alpha byte-for-byte identical throughout; 95,256 magical-light pixels protected. The pixel/check pass took 3.34 seconds in Node, including assertions and file reads. Texture cache integration is checked with a mock; the existing renderer check covers all 543 calibrated player poses, and four-player selection checks pass. Live browser QA was unavailable.

To reproduce pixel validation, export RGBA bytes from each matching character PNG into a temporary directory as `<key>.raw` plus `frames.json` containing `{key,w,h}` entries; run `node checks/hero-style.cjs <temporary directory>`.
