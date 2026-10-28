from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'source-art/city-guard-v128/sheet.png').convert('RGBA');a=np.array(im)
labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs)
ids=sorted(np.argsort(sizes)[-24:],key=lambda k:(boxes[k-1][0].start+boxes[k-1][0].stop)/2)
ordered=[]
for row in range(4):ordered.extend(sorted(ids[row*6:(row+1)*6],key=lambda k:boxes[k-1][1].start))
preview=Image.new('RGBA',(448*6,448*4),(42,37,40,255))
# Shared .88 scale across every pose, fixed foot anchor, torso-centered sword attacks.
centers=[128,390,640,900,1160,1420,128,390,600,880,1140,1410,125,370,610,870,1140,1390,125,370,630,900,1140,1390]
for i,k in enumerate(ordered):
 mask=binary_dilation(labs==k,iterations=2);arr=a.copy();arr[~mask]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box)
 cut=cut.resize((round(cut.width*.88),round(cut.height*.88)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((centers[i]-box[0])*.88),408-cut.height))
 frame.save(root/f'dist/assets/characters/city-guard-{i:02}.png');preview.alpha_composite(frame,((i%6)*448,(i//6)*448))
preview.convert('RGB').resize((1344,896)).save(root/'source-art/city-guard-v128/preview.jpg')
print('24 guard frames, shared scale .88, 448px canvases, foot anchor408')
