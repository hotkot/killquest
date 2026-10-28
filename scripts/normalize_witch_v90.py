"""Split approved whole-sheet animations, fixed sheet scales, planted soles.
Do not scale individual poses by weapon/effect bounds. Torso x anchors are
reviewed separately from the off-center staff. Air poses keep head/torso level.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from scipy.ndimage import label,find_objects,binary_dilation
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'source-art/witch-v90';ART=ROOT/'dist/assets/characters';FX=ROOT/'dist/assets/effects'
SHEETS={
 'motion':(4,.842,['idle']*4+['walk']*8+['jump']*4,[160,170,165,165,190,195,195,190,200,205,205,200,185,205,195,205]),
 'casts':(6,1.158,['cast1']*6+['cast2']*6+['cast3']*6+['air-cast']*6,[111,101,84,88,99,118,126,120,104,95,124,117,85,76,67,105,106,130,116,146,132,120,122,130]),
 'powers':(4,.94,['push']*4+['slam']*4+['teleport']*4+['rage']*4,[220,195,181,180,195,160,155,190,195,192,200,195,170,160,140,200]),
 'support':(3,.770,['hurt']*4+['pickup']*4+['win']*4,[175,150,170,205,235,220,230,215,210,190,205,230])}
records={};poses={}
def clean(im,character=False):
 a=np.array(im.convert('RGBA'));a[:,:,3][a[:,:,3]<85]=0
 labs,n=label(a[:,:,3]>0);sizes=np.bincount(labs.ravel());boxes=find_objects(labs)
 keep=np.zeros_like(a[:,:,3],bool)
 if character:
  sizes[0]=0;keep=binary_dilation(labs==sizes.argmax(),iterations=1)&(a[:,:,3]>0)
  a[:,:,3][~keep]=0;a[a[:,:,3]==0]=0
  return Image.fromarray(a)
 for k in range(1,n+1):
  y,x=boxes[k-1];w=x.stop-x.start;h=y.stop-y.start
  if sizes[k]>=25 and max(w,h)/max(1,min(w,h))<22:keep|=labs==k
 a[:,:,3][~keep]=0;a[a[:,:,3]==0]=0
 return Image.fromarray(a)
for sheet,(rows,scale,clips,anchors) in SHEETS.items():
 raw=Image.open(SRC/(sheet+'.png'));w,h=raw.size;counts={}
 for idx,clip in enumerate(clips):
  col=idx%4;row=idx//4;bounds={'motion':[0,314,628,943,1254],'casts':[0,257,513,768,1037,1281,1536],'powers':[0,302,598,852,1122],'support':[0,363,699,1086]}[sheet]
  cell=clean(raw.crop((round(col*w/4)+2,max(0,bounds[row]-20),round((col+1)*w/4)-2,min(h,bounds[row+1]+20))),True)
  scale=.70 if sheet=='support' and row==2 else SHEETS[sheet][1]
  i=counts.get(clip,0);counts[clip]=i+1;anchor_x=anchors[idx]-2
  row_pad=bounds[row]-max(0,bounds[row]-20)
  # Fix head/upper torso baseline in poses that will follow scripted flight.
  face_y=None
  if sheet=='motion' and idx in [13,14]:face_y=[55,55][idx-13]-2
  if sheet=='casts' and idx>=18:face_y=[72,80,78,78,76,55][idx-18]-2
  if sheet=='powers' and idx in [4,5]:face_y=[116,130][idx-4]-2
  if sheet=='support' and idx==1:face_y=135-2
  if face_y is not None:face_y+=row_pad+2
  a=np.array(cell);ys,xs=np.where(a[:,:,3]>100);sole=int(ys.max())
  dy=408-round(sole*scale) if face_y is None else 209-round(face_y*scale)
  if sheet=='support' and idx==2:dy=408-round(sole*scale)
  image=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
  frame=Image.new('RGBA',(448,448));dx=224-round(anchor_x*scale);frame.alpha_composite(image,(dx,dy));key=f'witch-{clip}-{i:02}'
  frame.save(ART/(key+'.png'));poses[key]=frame;records[key]={'sheet':sheet,'cell':idx,'scale':scale,'anchor_x':anchor_x,'source_sole':sole,'offset':[dx,dy],'airborne':face_y is not None}
# Keep natural ready pose as recovery for teleport and victory holds.
# Portrait uses the exact approved character concept.
Image.open(SRC/'approved.png').save(ROOT/'dist/assets/ui/selene-select-art.png')
portrait=Image.open(SRC/'approved.png');head=portrait.crop((590,230,825,447));canvas=Image.new('RGBA',(128,128));head.thumbnail((120,120));canvas.alpha_composite(head,((128-head.width)//2,(128-head.height)//2));canvas.save(ROOT/'dist/assets/ui/selene-life-head.png')
raw=Image.open(SRC/'effects.png');w,h=raw.size
for row,clip in enumerate(['flame','burst','storm']):
 for i in range(4):
  cell=clean(raw.crop((round(i*w/4)+3,round(row*h/3)+3,round((i+1)*w/4)-3,round((row+1)*h/3)-3)))
  box=cell.getbbox();cell=cell.crop(box);out=Image.new('RGBA',(384,384));cell.thumbnail((364,364));out.alpha_composite(cell,((384-cell.width)//2,(384-cell.height)//2));out.save(FX/f'witch-fx-{clip}-{i:02}.png')
(SRC/'registration.json').write_text(json.dumps(records,indent=2)+'\n')
clips=list(dict.fromkeys(rec['sheet']+':'+key.split('-')[1] for key,rec in records.items()))
for sheet in SHEETS:
 keys=[k for k,r in records.items() if r['sheet']==sheet];preview=Image.new('RGB',(448*4,448*((len(keys)+3)//4)),'#20252c');d=ImageDraw.Draw(preview)
 for i,key in enumerate(keys):preview.paste(poses[key],(i%4*448,i//4*448),poses[key]);d.text((i%4*448+8,i//4*448+422),key,fill='white')
 preview.resize((896,preview.height//2)).save(SRC/(sheet+'-preview.jpg'),quality=94)
print('Normalized',len(records),'witch frames and 12 effects')

# Preserve the later approved crossing gait and forward-only heavy on rebuilds.
if (ROOT/'source-art/witch-v91/push-raw.png').exists():
 import runpy
 runpy.run_path(str(ROOT/'scripts/normalize_witch_v91.py'),run_name='__main__')
