from PIL import Image,ImageDraw,ImageFilter
import subprocess,io
from pathlib import Path
root=Path(__file__).resolve().parents[1]
base='96123d56674877d064e18e51ea83d498eee52cf9'
def original(i):return Image.open(io.BytesIO(subprocess.check_output(['git','show',f'{base}:dist/assets/items/prison-cage-{i:02}.png'],cwd=root))).convert('RGBA')
neutral=original(0)
# Only chest cloth within the bar openings moves. All cage hardware, bars,
# silhouettes, face, hands and feet remain byte-identical to the seed frame.
mask=Image.new('L',(512,512));d=ImageDraw.Draw(mask)
d.rectangle((218,263,258,280),fill=70);d.rectangle((280,251,302,280),fill=70)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for i in range(4):
 frame=Image.composite(original(i),neutral,mask) if i else neutral
 frame.save(root/f'dist/assets/items/prison-cage-{i:02}.png')
# Damaged boards do not change shape every half second.
damaged=original(4)
for i in [4,5]:damaged.save(root/f'dist/assets/items/prison-cage-{i:02}.png')
print('Locked cage geometry; subtle chest-only breathing; stable damaged pose')
