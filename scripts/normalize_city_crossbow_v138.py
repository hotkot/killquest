from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'source-art/city-crossbow-v138/sheet.png').convert('RGBA');a=np.array(im)
labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs)
ids=sorted(np.argsort(sizes)[-30:],key=lambda k:(boxes[k-1][0].start+boxes[k-1][0].stop)/2)
ordered=[]
for row in range(5):ordered.extend(sorted(ids[row*6:(row+1)*6],key=lambda k:boxes[k-1][1].start))
preview=Image.new('RGBA',(448*6,448*5),(42,37,40,255))
# Shared .90 scale across every pose, fixed foot anchor and body-centered weapon poses.
# Detached generated bolt/blood flecks are excluded: runtime owns projectile/effect sprites.
centers=[120,350,580,805,1045,1270,110,340,565,795,1050,1275,128,360,580,815,1030,1270,129,355,580,815,1055,1270,125,355,580,805,1030,1255]
for i,k in enumerate(ordered):
 mask=binary_dilation(labs==k,iterations=2);arr=a.copy();arr[~mask]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box)
 cut=cut.resize((round(cut.width*.90),round(cut.height*.90)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((centers[i]-box[0])*.90),408-cut.height))
 frame.save(root/f'dist/assets/characters/city-crossbow-{i:02}.png');preview.alpha_composite(frame,((i%6)*448,(i//6)*448))
preview.convert('RGB').resize((1344,1120)).save(root/'source-art/city-crossbow-v138/preview.jpg')
print('30 crossbow frames, shared scale .90, 448px canvases, foot anchor408')
