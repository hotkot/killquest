from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1];src=root/'source-art';out=root/'dist/assets/characters'
raw=Path('/workspace/scratch/e77afc5b40f4/generated_images/exec-8f5f38e1-0344-4d67-a3f0-e0536b691230.png');dest=src/'huntress-walk-v43.png'
if raw.exists():shutil.copy(raw,dest)
im=Image.open(dest).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>80);sizes=np.bincount(labs.ravel());boxes=find_objects(labs);ids=sorted([k for k in range(1,n+1) if sizes[k]>10000],key=lambda k:boxes[k-1][1].start);assert len(ids)==4
anchors=[(278,390),(776,390),(1278,390),(1784,390)];scale=.3
manifest=json.loads((src/'huntress-registration.json').read_text())
# Four contact/passing keys are held for two frames each: knees visibly pass
# across the support leg twice per full cycle, with no synthetic foot sliding.
for i,j in enumerate([0,0,1,1,2,2,3,3]):
 k=ids[j];clean=a.copy();clean[:,:,3][~binary_dilation(labs==k,iterations=2)]=0;cut=Image.fromarray(clean);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);cx,cy=anchors[j];frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-box[0])*scale),300-round((cy-box[1])*scale)));name=f'huntress-walk-{i:02}';frame.save(out/f'{name}.png');manifest[name]={'source':dest.name,'component':int(k),'anchor':[cx,cy],'scale':scale,'body_anchor':[224,300],'key_pose':j}
(src/'huntress-registration.json').write_text(json.dumps(manifest,indent=2));preview=Image.new('RGBA',(448*4,448),(24,31,39,255))
for j in range(4):preview.alpha_composite(Image.open(out/f'huntress-walk-{j*2:02}.png'),(j*448,0))
preview.convert('RGB').save(src/'huntress-walk-preview-v43.jpg',quality=92)
print('Registered 4 crossing-leg gait keys across 8 frame slots')
