from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1]
a=np.array(Image.open(root/'source-art/city-spearman-v139/sheet.png').convert('RGBA'))
labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs)
ids=sorted(np.argsort(sizes)[-24:],key=lambda k:(boxes[k-1][0].start+boxes[k-1][0].stop)/2)
ordered=[]
for row in range(6):ordered.extend(sorted(ids[row*4:(row+1)*4],key=lambda k:boxes[k-1][1].start))
# One scale, feet y408, body x384. Wide frames retain the complete long spear.
scale=1.12
centers=[120,480,860,1240,120,480,860,1240,95,470,845,1185,104,470,860,1210,115,480,880,1235,125,490,850,1230]
preview=Image.new('RGBA',(768*4,448*6),(42,37,40,255))
for i,k in enumerate(ordered):
 mask=(labs==k)|(binary_dilation(labs==k,iterations=2)&(labs==0));arr=a.copy();arr[~mask]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box)
 cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(768,448));frame.alpha_composite(cut,(384-round((centers[i]-box[0])*scale),408-cut.height))
 assert frame.getbbox()[0]>1 and frame.getbbox()[2]<767,'clipped spear '+str(i)
 frame.save(root/f'dist/assets/characters/city-spearman-{i:02}.png');preview.alpha_composite(frame,((i%4)*768,(i//4)*448))
preview.convert('RGB').resize((1536,1344)).save(root/'source-art/city-spearman-v139/preview.jpg')
print('24 spearman frames; shared scale 1.12, 768x448 canvas, body384 / ground408; all spear tips inside frame')
