from PIL import Image
from pathlib import Path
import shutil
raw=Path('source-art/cage-v158/cage-raw.png')
im=Image.open(raw).convert('RGBA'); w,h=im.size
scale=440/(w/4)
for i in range(12):
 x=i%4;y=i//4
 tile=im.crop((round(x*w/4),round(y*h/3),round((x+1)*w/4),round((y+1)*h/3)))
 # Common scale; fixed slot center and floor, preserving relative motion.
 tile=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(512,512));frame.alpha_composite(tile,((512-tile.width)//2,480-tile.height))
 frame.save(f'dist/assets/items/prison-cage-{i:02}.png')
print('12 transparent cage frames; shared scale, floor480/512')
