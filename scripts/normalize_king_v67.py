"""Extract each whole connected figure; preserve blades crossing nominal grid gutters.
One scale per full animation strip, calibrated from the same approved body height.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1];source=root/'source-art/bandit-king-v67';target=root/'dist/assets/characters'
clips={'idle':(6,3,480),'walk':(8,4,450),'sweep':(8,2,270),'slam':(8,4,350),'charge':(6,3,395),'roar':(6,3,480),'death':(6,3,490)}
report={}
for clip,(count,cols,body_height) in clips.items():
 im=Image.open(source/(clip+'.png')).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>32);areas=np.bincount(labs.ravel());slices=find_objects(labs)
 ids=[i for i in range(1,n+1) if areas[i]>10000];assert len(ids)==count,(clip,len(ids),count)
 rows=count//cols
 ids.sort(key=lambda i:(round(((slices[i-1][0].start+slices[i-1][0].stop)/2)/(im.height/rows)-.5), (slices[i-1][1].start+slices[i-1][1].stop)/2))
 scale=260/body_height;info=[]
 for j,k in enumerate(ids):
  sy,sx=slices[k-1];l=max(0,sx.start-2);r=min(im.width,sx.stop+2);t=max(0,sy.start-2);b=min(im.height,sy.stop+2)
  pixels=a[t:b,l:r].copy();mask=binary_dilation(labs[t:b,l:r]==k,iterations=2);pixels[:,:,3]=np.where(mask,pixels[:,:,3],0)
  alpha=pixels[:,:,3];ys,xs=np.where((alpha>100)&(np.arange(b-t)[:,None]>b-t-body_height*.23)&(pixels[:,:,0]<140)&(pixels[:,:,1]<130))
  anchor_x=float((np.percentile(xs,10)+np.percentile(xs,90))/2) if len(xs)>20 else (r-l)/2
  anchor_x=max((r-l)-316/scale,min(316/scale,anchor_x))
  cell=Image.fromarray(pixels);cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
  x=round(320-anchor_x*scale);y=466-int(np.where(np.array(cell)[:,:,3]>32)[0].max())
  assert x>=4 and x+cell.width<=636 and y>=4,(clip,j,x,y,cell.size)
  canvas=Image.new('RGBA',(640,512));canvas.alpha_composite(cell,(x,y));canvas.save(target/f'king-{clip}-{j:02}.png');info.append({'bounds':canvas.getchannel('A').getbbox(),'source_anchor_x':anchor_x,'scale':scale})
 report[clip]=info
(source/'normalization.json').write_text(json.dumps(report,indent=2)+'\n')
# Review sheet is diagnostic only, kept alongside sources rather than shipped.
thumbs=[]
for clip,(count,_,_) in clips.items():
 for i in range(count):thumbs.append((clip,i,Image.open(target/f'king-{clip}-{i:02}.png').resize((240,192))))
sheet=Image.new('RGB',(8*240,6*218),(29,31,32));draw=ImageDraw.Draw(sheet)
for i,(clip,n,im) in enumerate(thumbs):
 x=i%8*240;y=i//8*218;sheet.paste(im,(x,y),im);draw.text((x+8,y+193),f'{clip} {n+1}',fill='white')
sheet.save(source/'preview.jpg',quality=90)
print('Normalized',len(thumbs),'frames with stable ground anchors.')

# Keep the reviewed anatomy calibration when regenerating source frames.
import runpy
runpy.run_path(str(root/"scripts/normalize_king_v94.py"),run_name="__main__")
