from pathlib import Path
from PIL import Image
from scipy.ndimage import label,binary_dilation
import numpy as np
root=Path(__file__).resolve().parents[1];im=Image.open(root/'source-art/containers-v36.png').convert('RGBA');a=np.array(im);cuts=[]
for i in range(8):
 x=int(i%4*im.width/4);y=int(i//4*im.height/2);arr=a[y:int((i//4+1)*im.height/2),x:int((i%4+1)*im.width/4)].copy();labs,n=label(arr[:,:,3]>100);sz=np.bincount(labs.ravel());sz[0]=0;mask=np.isin(labs,np.where(sz>50)[0]) if i in [2,6] else labs==sz.argmax();arr[:,:,3][~binary_dilation(mask,iterations=2)]=0;cut=Image.fromarray(arr);cuts.append(cut.crop(cut.getbbox()))
for row in range(2):
 scale=224/max(max(c.width,c.height) for c in cuts[row*4:row*4+4])
 for j in range(4):
  i=row*4+j;cut=cuts[i];cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(256,256));frame.alpha_composite(cut,((256-cut.width)//2,240-cut.height));frame.save(root/f'dist/assets/items/container-{i:02}.png')
