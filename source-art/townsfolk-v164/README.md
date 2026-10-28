# Townsfolk border cleanup

The generated sheet's silhouettes do not fit exact256pixel columns: the laborer's fourth/fifth stride and the woman's trailing skirt cross nominal cell boundaries. Grid cropping therefore clipped their own clothing and included fragments of the previous pose in the next frame.

Use `scripts/normalize_townsfolk_v164.py` for current assets. It extracts each complete connected character from the full approved source sheet, orders the24characters into three8frame clips, then preserves the shared scale/body anchor/floor408 and generous448px canvas gutters. No sprite redraw or gameplay changes.

`normalization.json` records full source bounds and final frame bounds. `run-preview.png` displays every corrected pose. Regression checks require one complete character component per frame, no neighboring fragments and transparent gutters; existing movement and real scene lifecycle checks pass. Asset cache versions updated so browsers fetch the corrected frames.
