from pathlib import Path
from PIL import Image
import numpy as np,json,shutil,hashlib
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1];src=root/'source-art';out=root/'dist/assets/characters'
raw=Path('/workspace/scratch/e77afc5b40f4/generated_images/exec-e6805df6-a70b-45a0-ad70-88fb341cd949.png');dest=src/'huntress-walk-eight-v43.png'
if raw.exists():shutil.copy(raw,dest)
im=Image.open(dest).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>80);sizes=np.bincount(labs.ravel());boxes=find_objects(labs)
ids=[k for k in range(1,n+1) if sizes[k]>10000];ids=sorted(ids,key=lambda k:(boxes[k-1][0].start//550,boxes[k-1][1].start));assert len(ids)==8
anchors=[(179,283),(535,283),(902,283),(1265,283),(181,822),(542,822),(908,822),(1273,822)];scale=.414
manifest=json.loads((src/'huntress-registration.json').read_text());hashes=[]
for i,k in enumerate(ids):
 clean=a.copy();clean[:,:,3][~binary_dilation(labs==k,iterations=2)]=0;cut=Image.fromarray(clean);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);cx,cy=anchors[i];frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-box[0])*scale),300-round((cy-box[1])*scale)));name=f'huntress-walk-{i:02}';frame.save(out/f'{name}.png');hashes.append(hashlib.sha256(frame.tobytes()).hexdigest());manifest[name]={'source':dest.name,'component':int(k),'anchor':[cx,cy],'scale':scale,'body_anchor':[224,300],'key_pose':i}
assert len(set(hashes))==8
(src/'huntress-registration.json').write_text(json.dumps(manifest,indent=2));preview=Image.new('RGBA',(448*8,448),(24,31,39,255))
for j in range(8):preview.alpha_composite(Image.open(out/f'huntress-walk-{j:02}.png'),(j*448,0))
preview.resize((1792,224)).convert('RGB').save(src/'huntress-walk-preview-v43.jpg',quality=92)
print('Registered 8 unique transparent walk poses')
