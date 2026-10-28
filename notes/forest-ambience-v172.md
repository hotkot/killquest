# Audible Forest intro ambience

Raised the existing narration-free Forest cinematic bed from approximately-43.79LUFS to-21.03LUFS integrated (about22.8dB louder). Encoded true peak is-2.84dBTP, with safe headroom. Used measured two-pass loudness normalization from the clean lossless ambience source, avoiding repeated AAC processing and preserving the minor drone, wind, crackles, cart creak, dynamics and original fades.

New Forest video path is killquest-forest-v172.mp4 in playback and boot preloading. Video/subtitle stream is copied unchanged. Future full Forest renders also target-21LUFS. Other cutscenes and global volume settings are unchanged; narration remains absent.

Verified encoded loudness/true peak, exact AAC match to an independent clean-source normalization, identical video packet hash to the original cutscene, playback/skip/autoplay, Forest/New Game/controller-selection transitions, and cinematic/loading/music handoff. JavaScript syntax and diff checks passed. Browser/device listening was not available. No EXE build.
