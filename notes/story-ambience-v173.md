# Audible New Game intro ambience

Raised the narration-free New Game story intro bed from-35.98LUFS to-21.03LUFS integrated, matching the updated Forest intro. Encoded true peak is-10.21dBTP. Applied measured two-pass normalization to the clean lossless ambient music stem with the original gain, limiter and fade chain preserved. No narration or new sounds added.

Active playback/preloading now use killquest-opening-v173.mp4. Its video/subtitle stream remains byte-for-byte identical; duration remains44.25seconds. Full story rendering now also targets-21LUFS. Forest and startup hype videos remain unchanged.

Checked encoded loudness/true peak, exact audio hash against an independent encode of the clean normalized source, original video hash, playback/skipping/autoplay/focus, New Game/Forest/controller-selection transitions, and cinematic-loading/menu-music ordering. Syntax and diff checks passed. No browser/device listening or EXE build.
