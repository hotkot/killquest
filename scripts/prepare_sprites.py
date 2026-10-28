"""Isolate each frame, discard neighboring fragments, preserve shared scale and foot pivot."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
ap=argparse.ArgumentParser();ap.add_argument('image');ap.add_argument('name');ap.add_argument('--columns',type=int,required=True);ap.add_argument('--rows',type=int,required=True);ap.add_argument('--height',type=float,default=215);ap.add_argument('--standing-reference',action='store_true');a=ap.parse_args()
root=Path(__file__).resolve().parents[1];out=root/'dist/assets/characters';out.mkdir(parents=True,exist_ok=True)
im=Image.open(a.image).convert('RGBA');w,h=im.size;frames=[]
ar=np.array(im);lab,n=label(ar[:,:,3]>100);counts=np.bincount(lab.ravel());counts[0]=0
ids=np.argsort(counts)[-(a.columns*a.rows):]
components=[]
for component in ids:
 main=lab==component;ys,xs=np.where(main)
 components.append((float(np.mean(ys)),float(np.mean(xs)),component))
components.sort()
ordered=[]
for row in range(a.rows):ordered.extend(sorted(components[row*a.columns:(row+1)*a.columns],key=lambda t:t[1]))
for _,__,component in ordered:
 main=lab==component;ys,xs=np.where(main);box=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
 keep=binary_dilation(main,iterations=2);clean=ar.copy();clean[~keep]=0
 feet=main&(np.indices(main.shape)[0]>ys.max()-14);fy,fx=np.where(feet)
 frames.append((Image.fromarray(clean).crop(box),float(np.median(fx))-box[0],box))
scale=a.height/(frames[0][0].height if a.standing_reference else np.median([f.height for f,_,_ in frames]))
scale=min(scale,min(292/max(f.width,f.height) for f,_,_ in frames))
for i,(f,pivot,box) in enumerate(frames):
 f=f.resize((round(f.width*scale),round(f.height*scale)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(320,320));x=round(160-pivot*scale);x=max(12,min(x,308-f.width));frame.alpha_composite(f,(x,308-f.height));frame.save(out/f'{a.name}-{i:02}.png')
preview=Image.new('RGBA',(320*a.columns,320*a.rows),(27,35,43,255))
for i in range(len(frames)):
 f=Image.open(out/f'{a.name}-{i:02}.png');preview.alpha_composite(f,((i%a.columns)*320,(i//a.columns)*320))
preview.convert('RGB').save(out/f'{a.name}-preview.jpg')
print(json.dumps({'name':a.name,'frames':len(frames),'shared_scale':scale}))
