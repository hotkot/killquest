# Object ground shadows

The runtime ObjectShadows module adds a soft contact patch and a short ground projection of each object's actual sprite alpha. All current containers, destructible barriers, prisoner cages, solid scenery props and ground pickups use the same footprint anchors as their visible sprites. Shadows stay below actors and use world coordinates through City descents.

Projected textures are cached per sprite pose; changing damage/animation frames reuses those textures. Offscreen objects skip projection generation and drawing. Broken objects fade with their fragments; collected pickups and level resets dispose their shadow views. QA before/after composites and the Canvas/real-scene checks cover shape, tint, blending, anchor stability, culling, caching and cleanup. Browser playback has not been retested in this session.
