from pathlib import Path
from PIL import Image
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'source-art/bruiser-repairs-v33.png').convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs)
ids=sorted(np.argsort(sizes)[-4:],key=lambda k:boxes[k-1][1].start)
scale=200/max(boxes[k-1][0].stop-boxes[k-1][0].start for k in ids[:3])
for k,index,cx in zip(ids,[2,3,4,20],[265,750,1250,1775]):
 arr=a.copy();arr[:,:,3][~binary_dilation(labs==k,iterations=2)]=0
 cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box)
 cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-box[0])*scale),408-cut.height))
 frame.save(root/f'source-art/uncentered/bandit-bruiser-{index:02}.png')
