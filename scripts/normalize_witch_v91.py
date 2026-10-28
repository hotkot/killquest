"""Re-register Selene's revised walk and forward heavy, preserving anatomy scale.

Each clip has ONE scale. Align hips independently of the off-center staff and
plant soles at y408. Neighboring-cell fragments never survive extraction.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from scipy.ndimage import label,binary_dilation,find_objects
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'source-art/witch-v91';ART=ROOT/'dist/assets/characters'
regfile=ROOT/'source-art/witch-v90/registration.json'
records=json.loads(regfile.read_text());backup=SRC/'registration-before.json'
if not backup.exists():backup.write_text(json.dumps(records,indent=2)+'\n')
# Shared anatomy sizes calibrated against witch-idle-00's head-to-sole distance.
CLIPS={
 'push':{'rows':2,'count':8,'scale':.630,'hips':[216,254,169,135,182,190,185,174],'padding':100},
 'walk':{'rows':3,'count':12,'scale':.79,'hips':[230]*12,'padding':10},
}
for clip,cfg in CLIPS.items():
 path=SRC/(clip+'-raw.png')
 if not path.exists():continue
 raw=Image.open(path).convert('RGBA');w,h=raw.size;frames=[]
 if clip=='walk':
  faces=[];heights=[]
  for j in range(cfg['count']):
   l=round(j%4*w/4);t=round(j//4*h/cfg['rows']);r=round((j%4+1)*w/4);b=round((j//4+1)*h/cfg['rows']);a=np.array(raw.crop((l,t,r,b))).astype(float)
   rr,gg,bb=a[:,:,:3].transpose(2,0,1);skin=(a[:,:,3]>100)&(rr>150)&(rr>gg*1.13)&(gg>bb*1.12)&(gg>80)
   labs,n=label(skin);sizes=np.bincount(labs.ravel());boxes=find_objects(labs)
   candidates=[(ys,xs) for k,(ys,xs) in enumerate(boxes,1) if sizes[k]>90 and ys.start>(b-t)*.10 and ys.start<(b-t)*.4 and xs.start>(r-l)*.4]
   candidates.sort(key=lambda p:p[0].start);ys,xs=candidates[0];faces.append((xs.start+xs.stop)/2)
   heights.append(np.where(a[:,:,3]>100)[0].max()-ys.start)
  cfg['scale']=round(216/float(np.median(heights)),6)
  cfg['hips']=[cx-18/cfg['scale'] for cx in faces]

 for i in range(cfg['count']):
  col=i%4;row=i//4;x0=round(col*w/4);y0=round(row*h/cfg['rows']);x1=round((col+1)*w/4);y1=round((row+1)*h/cfg['rows']);pad=cfg['padding'];left=max(0,x0-pad);top=max(0,y0-12)
  cell=raw.crop((left,top,min(w,x1+pad),min(h,y1+12)));a=np.array(cell);a[:,:,3][a[:,:,3]<85]=0
  labs,n=label(a[:,:,3]>0);sizes=np.bincount(labs.ravel());sizes[0]=0;mask=binary_dilation(labs==sizes.argmax(),iterations=1)&(a[:,:,3]>0);a[:,:,3][~mask]=0;a[a[:,:,3]==0]=0
  ys,xs=np.where(a[:,:,3]>100);sole=int(ys.max());scale=cfg['scale'];anchor_x=cfg['hips'][i]+x0-left
  image=Image.fromarray(a);box=image.getbbox();image=image.crop(box);image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
  frame=Image.new('RGBA',(448,448));dx=224-round((anchor_x-box[0])*scale);dy=408-round((sole-box[1])*scale);frame.alpha_composite(image,(dx,dy));key=f'witch-{clip}-{i:02}';frame.save(ART/(key+'.png'));frames.append(frame)
  records[key]={'sheet':'witch-v91/'+clip,'cell':i,'scale':scale,'anchor_x':anchor_x,'source_sole':sole,'offset':[dx,dy],'airborne':False}
 preview=Image.new('RGB',(448*4,448*cfg['rows']),'#20252c');d=ImageDraw.Draw(preview)
 for i,frame in enumerate(frames):preview.paste(frame,(i%4*448,i//4*448),frame);d.text((i%4*448+8,i//4*448+422),f'{clip} {i:02}',fill='white')
 preview.resize((896,preview.height//2)).save(SRC/(clip+'-preview.jpg'),quality=95)
 renders=[]
 for frame in frames:
  im=Image.new('RGB',(448,448),'#20252c');im.paste(frame,(0,0),frame);renders.append(im.resize((336,336)))
 renders[0].save(SRC/(clip+'-preview.gif'),save_all=True,append_images=renders[1:],duration=65 if clip=='walk' else 95,loop=0)
regfile.write_text(json.dumps(records,indent=2)+'\n')
print('Registered revised',', '.join(k for k in CLIPS if (SRC/(k+'-raw.png')).exists()))

# Preserve completed flame tips and wider canvases when rebuilding source strips.
if (ROOT/"source-art/witch-fx-v98/repaired-sheet.png").exists():
 import runpy
 runpy.run_path(str(ROOT/"scripts/repair_witch_fx_v98.py"),run_name="__main__")

if (ROOT/"source-art/witch-fx-v99/before.png").exists():
 runpy.run_path(str(ROOT/"scripts/repair_witch_first_cast_v99.py"),run_name="__main__")

if (ROOT/"source-art/witch-left-v100/witch-cast3-01-before.png").exists():
 runpy.run_path(str(ROOT/"scripts/repair_witch_cast_left_v100.py"),run_name="__main__")
