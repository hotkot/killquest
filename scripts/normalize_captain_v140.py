from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1]
# Shared anatomical anchors measured from the approved master; no per-frame scaling.
centers=[175,547,915,1294,175,550,915,1294,180,540,915,1294,175,540,915,1294,175,540,915,1294,180,540,915,1294]
for variant in ['crimson-lion','azure-griffin','ochre-stag']:
 path=root/f'source-art/captain-v140/{variant}.png'
 if not path.exists():continue
 a=np.array(Image.open(path).convert('RGBA'));labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs)
 ids=np.argsort(sizes)[-24:];assert min(sizes[ids])>5000
 # Group by vertical centers in six rows, then left-to-right. Complete components retain sword tips.
 ids=sorted(ids,key=lambda k:(boxes[k-1][0].start+boxes[k-1][0].stop)/2);ordered=[]
 for row in range(6):ordered.extend(sorted(ids[row*4:row*4+4],key=lambda k:boxes[k-1][1].start))
 preview=Image.new('RGBA',(2048,2688),(38,34,41,255));scale=1.10
 for i,k in enumerate(ordered):
  mask=(labs==k)|(binary_dilation(labs==k,iterations=2)&(labs==0));arr=a.copy();arr[~mask]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
  frame=Image.new('RGBA',(512,448));frame.alpha_composite(cut,(256-round((centers[i]*a.shape[1]/1448-box[0])*scale),408-cut.height));b=frame.getbbox();assert b[0]>2 and b[2]<510 and b[1]>2,(variant,i,b)
  frame.save(root/f'dist/assets/characters/commander-{variant}-{i:02}.png');preview.alpha_composite(frame,((i%4)*512,(i//4)*448))
 preview.convert('RGB').resize((1024,1344)).save(root/f'source-art/captain-v140/{variant}-preview.jpg')
 print(variant, '24 frames; shared scale1.10; body256 ground408; no edge contact')
