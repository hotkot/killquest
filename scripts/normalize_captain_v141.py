from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1]
for variant in ['crimson-lion','azure-griffin','ochre-stag']:
 a=np.array(Image.open(root/f'source-art/captain-v141/{variant}.png').convert('RGBA'));labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs)
 ids=sorted(np.argsort(sizes)[-12:],key=lambda k:(boxes[k-1][0].start+boxes[k-1][0].stop)/2);ordered=[]
 for row in range(3):ordered.extend(sorted(ids[row*4:row*4+4],key=lambda k:boxes[k-1][1].start))
 assert min(sizes[ids])>10000
 idle=boxes[ordered[4]-1];target=Image.open(root/f'dist/assets/characters/commander-{variant}-16.png').getbbox();scale=(target[3]-target[1])/(idle[0].stop-idle[0].start)
 preview=Image.new('RGBA',(2048,1344),(38,34,41,255))
 for i,k in enumerate(ordered):
  mask=(labs==k)|(binary_dilation(labs==k,iterations=2)&(labs==0));arr=a.copy();arr[~mask]=0;cut=Image.fromarray(arr);box=cut.getbbox();yy=boxes[k-1][0].stop;xs=np.where(labs[yy-8:yy]==k)[1];body=(xs.min()+xs.max())/2
  cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(512,448));frame.alpha_composite(cut,(256-round((body-box[0])*scale),408-cut.height));b=frame.getbbox();assert b[0]>2 and b[2]<510 and b[1]>2,(variant,i,b)
  frame.save(root/f'dist/assets/characters/commander-{variant}-combat-{i:02}.png');preview.alpha_composite(frame,((i%4)*512,(i//4)*448))
 preview.convert('RGB').resize((1024,672)).save(root/f'source-art/captain-v141/{variant}-preview.jpg');print(variant,round(scale,4),'12 complete frames: shared scale, foot408, body256')
