# Carion City moving scenery

116 bounded, source-color material animations across all twelve actual level panels: banners and awnings, source-shaped fire above the existing metal rims, lamp glow, distant painted smoke, and a small puddle reflection. Reproduce with `node scripts/bake_city_ambient_v176.cjs`.

The baker uses the original art and traced material polygons. Cloth attachment points, building geometry, metalwork, and the road stay fixed. Each patch replaces its static painted detail with an opaque interior and transparent feathered gutter; original scenery remains untouched. Fire uses a continuous inverse map to avoid strip seams. The existing solid architectural joins remain in front of the panel material layers.

The runtime follows the same panel transforms as the background, including all three descents. Frames use a model clock, freeze when the level is paused, and only switch textures when the frame changes. Horizontal and vertical visibility checks suppress offscreen drawing. All sprites belong to worldArt and are disposed on level changes. No movement speeds or collisions are changed.

Twelve frames per region; approximately 43 MiB decoded texture memory and 12 MiB compressed assets. All are in the loading manifest. Exact baked composites are retained under qa; browser playback has not been retested in this session.
