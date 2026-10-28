from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[1];data=json.loads((root/'source-art/townsfolk-v163/scene-fixture.json').read_text());board=Image.open(root/'dist/assets/quarter.png').convert('RGBA').resize((1280,720));rows=[]
for a in data['people']:rows.append((a['y'],a['x'],a['key'],.67,408/448,'characters'))
for a in data['enemies']:rows.append((a['y'],a['x'],a['key'],.77,408/448,'characters'))
a=data['player'];rows.append((a['y'],a['x'],a['key'],.84,408/448,'characters'))
a=data['cage'];rows.append((a['y'],a['x'],'prison-cage-00',340/512,240/256,'items'))
for y,x,key,scale,origin,folder in sorted(rows):
 im=Image.open(root/f'dist/assets/{folder}/{key}.png').convert('RGBA');im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);board.alpha_composite(im,(round(x-im.width/2),round(y-im.height*origin)))
board.convert('RGB').save(root/'source-art/townsfolk-v163/arena-preview.jpg',quality=92)
