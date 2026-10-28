"""Recover first-cast tip beyond its source grid cell; retain character pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,re,shutil
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'source-art/witch-fx-v99';SRC.mkdir(exist_ok=True)
key='witch-cast1-04';target=ROOT/'dist/assets/characters'/f'{key}.png';backup=SRC/'before.png'
if not backup.exists():shutil.copy2(target,backup)
original=Image.open(backup).convert('RGBA')
raw=Image.open(ROOT/'source-art/witch-v90/casts.png').convert('RGBA')
# Original cell x2..254, row y237..533; the actual firebolt extends past x254.
cell=raw.crop((2,237,286,533));a=np.array(cell);a[:,:,3][a[:,:,3]<85]=0;a[a[:,:,3]==0]=0
cell=Image.fromarray(a).resize((329,343),Image.Resampling.LANCZOS)
extra=cell.crop((292,0,329,343))
# Keep the connected flame cap; exclude fragments belonging to the next cell.
from scipy.ndimage import label,binary_dilation
pixels=np.array(extra);labels,n=label(pixels[:,:,3]>85);sizes=np.bincount(labels.ravel());sizes[0]=0
mask=binary_dilation(labels==sizes.argmax(),iterations=1);pixels[:,:,3][~mask]=0;pixels[pixels[:,:,3]==0]=0;extra=Image.fromarray(pixels)
out=Image.new('RGBA',(640,448));out.alpha_composite(original,(96,0));out.alpha_composite(extra,(96+404,93));out.save(target)
preview=Image.new('RGB',(1280,480),'#20252c');preview.paste(original,(96,0),original);preview.paste(out,(640,0),out);d=ImageDraw.Draw(preview);d.text((10,450),'Before: truncated at cell boundary',fill='white');d.text((650,450),'After: original source tip recovered',fill='white');preview.save(SRC/'comparison.jpg',quality=96)
p=ROOT/'dist/game.js';s=p.read_text();s=re.sub(r'"witch-cast1-04":\[1\.0,408,(448|640)\]','"witch-cast1-04":[1.0,408,640]',s);p.write_text(s)
print('Recovered complete first-cast flame tip; original 448x448 pixels preserved.')
