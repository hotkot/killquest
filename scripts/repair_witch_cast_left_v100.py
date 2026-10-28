"""Recover complete left silhouettes from source pixels outside nominal cells."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,re,shutil
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'source-art/witch-left-v100';SRC.mkdir(exist_ok=True);DST=ROOT/'dist/assets/characters'
raw=Image.open(ROOT/'source-art/witch-v90/casts.png').convert('RGBA');frames=[]
for key,left,dx,dy in [('witch-cast3-01',258,138,86),('witch-cast3-02',514,149,90)]:
 path=DST/(key+'.png');backup=SRC/(key+'-before.png')
 if not backup.exists():shutil.copy2(path,backup)
 original=Image.open(backup).convert('RGBA');cell=raw.crop((left-100,748,left+252,1057));a=np.array(cell);a[:,:,3][a[:,:,3]<85]=0
 labs,n=label(a[:,:,3]>0);sizes=np.bincount(labs.ravel());sizes[0]=0;mask=binary_dilation(labs==sizes.argmax(),iterations=1);a[:,:,3][~mask]=0;a[a[:,:,3]==0]=0
 expanded=Image.fromarray(a).resize((408,358),Image.Resampling.LANCZOS);extra=expanded.crop((0,0,116,358))
 width=max(640,original.width);offset=(width-original.width)//2;bodyOffset=(width-448)//2
 out=Image.new('RGBA',(width,448));out.alpha_composite(original,(offset,0));out.alpha_composite(extra,(bodyOffset+dx-116,dy));out.save(path);frames.append((key,original,out))
 p=ROOT/'dist/game.js';s=p.read_text();s=re.sub(r'"'+key+r'":\[1\.0,408,\d+\]',f'"{key}":[1.0,408,{width}]',s);p.write_text(s)
preview=Image.new('RGB',(1536,960),'#20252c');d=ImageDraw.Draw(preview)
for i,(key,before,after) in enumerate(frames):
 y=i*480;preview.paste(before,((768-before.width)//2,y),before);preview.paste(after,(768+(768-after.width)//2,y),after);d.text((10,y+450),key+' BEFORE',fill='white');d.text((778,y+450),key+' AFTER',fill='white')
preview.save(SRC/'comparison.jpg',quality=95)
print('Recovered hair, cape, staff and rear-leg pixels in both clipped final-cast poses.')
