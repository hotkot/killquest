# Selene magic-edge repair (v98)

Four affected files in `dist/assets/characters/`: witch-air-cast-03.png,
witch-cast2-03.png, witch-cast3-02.png and witch-rage-02.png.
The source sheets cropped flames at cell boundaries, including one beam that
was already truncated in the source artwork. Extra padding alone could not
recover those missing tips.

Built-in image generation edited the reference sheet. The integration script
extracts only the completed magic, preserving the original opaque character
pixels, body scale, animation order, timing and y408 pivot. Corrected canvases
are 768x448 with a 160px horizontal offset; player frame layouts account for
that width in menus and gameplay. Other frames remain unchanged. The source
normalizer reapplies this repair when regenerating assets.

Validation: original opaque character pixels outside the effect regions match
exactly; all effects have transparent outer margins. Reviewed the preview sheet.
Full renderer and Selene combat checks pass. Browser playtest unavailable.

## Image edit prompt

Edit target: this exact 1280x1024 transparent sprite repair sheet, 2 columns x 2 rows, each slot640x512. Preserve the four existing witch figures, all body/hand/staff positions and their exact sizes and locations. Repair ONLY the blue magical flame effects extending to the right of each figure. In every slot the blue flame currently ends at an ugly straight vertical crop edge: extend the flame naturally beyond that edge into the empty space, then finish it with a fully visible tapered curved pointed tip and a few little blue sparks, fading to transparency with at least 25px transparent margin before each slot edge. Top left: blue projectile diagonally down-right, finish its pointed tip. Top right: rightward hand-cast blue firebolt, finish its bright pointed tip. Bottom left: staff beam rightward, replace the vertical white cutoff with a complete narrowing magical burst finishing with a pointed tip. Bottom right: large staff firestorm, finish the curved flame tongue to the right. Keep all original bodies exactly unchanged. Clean sharp cel shaded 2D game sprite art, cyan white cores deep blue flame outlines. No background, no text, no extra characters, no rectangles, no clipped flat edges. Output same layout and same dimensions, true transparent background.
