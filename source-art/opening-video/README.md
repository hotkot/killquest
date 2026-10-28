# Rendered opening v117

44.25-second 1280×720 H.264/AAC intro, rendered with `scripts/render_opening_video.py`.

Uses the approved lower-arm third illustration and revised axe/grip fourth illustration, normal-speed deep narration with one second added after all 18 sentence/ellipsis boundaries, and an original quiet minor-key ambient drone. Narration is not time-stretched. Runtime video: `dist/assets/cinematic/killquest-opening-v117.mp4`.

The video covers concurrent game loading. Finishing/skipping reveals loading if needed, otherwise the Press Any Button screen. Menu theme starts only there. Browser autoplay restrictions use muted playback with Enable Sound and gesture unmuting; focus loss pauses the video. Volume follows effects settings. On-screen subtitles are burned into the video.

Old still-player media is retained in source-art/source-audio rather than deployed. The unused retired chug menu theme is retained in source-audio/retired-menu. Approved current menu theme unchanged.

Verified codec/duration, inspected rendered third-panel and title frames, tested video lifecycle/autoplay fallback, both loading completion orders, skip handling and controller menu. Live browser QA unavailable.
