"""Normalize reviewed 4x3 strips with shared body scale and torso/ground registration.
The generic sprite-strip helper assumes a horizontal strip and square output;
this variant preserves the established rectangular sword canvas and foot pivot.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json
root=Path(__file__).resolve().parents[1];src=root/'source-art/garran-v78';out=root/'dist/assets/characters';report={}
for clip in ['down','cross','thrust']:
 im=Image.open(src/(clip+'.png')).convert('RGBA');a=np.array(im);lab,n=label(a[:,:,3]>32);areas=np.bincount(lab.ravel());slices=find_objects(lab);ids=[i for i in range(1,n+1) if areas[i]>1000]
 ids.sort(key=lambda i:(round(((slices[i-1][0].start+slices[i-1][0].stop)/2)/(im.height/3)-.5),(slices[i-1][1].start+slices[i-1][1].stop)/2));assert len(ids)==12,(clip,len(ids))
 cells=[];heights=[]
 for k in ids:
  sy,sx=slices[k-1];l=max(0,sx.start-2);r=min(im.width,sx.stop+2);t=max(0,sy.start-2);b=min(im.height,sy.stop+2);v=a[t:b,l:r].copy();v[:,:,3]=np.where(binary_dilation(lab[t:b,l:r]==k,iterations=2),v[:,:,3],0)
  alpha=v[:,:,3];red=(alpha>128)&(v[:,:,0]>120)&(v[:,:,1]<v[:,:,0]*.6)&(v[:,:,2]<v[:,:,0]*.7);heights.append(int(np.where(alpha>32)[0].max()-np.where(red)[0].min()+1));cells.append(Image.fromarray(v))
 # Plume-to-feet measurement excludes the raised sword, avoiding body shrinkage.
 scale=234/float(np.median(heights));report[clip]={'shared_scale':scale,'source_body_heights':heights,'frames':[]}
 for j,cell in enumerate(cells):
  cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS);v=np.array(cell);alpha=v[:,:,3];y=408-int(np.where(alpha>32)[0].max());gy=np.arange(cell.height)[:,None]+y
  mask=(alpha>128)&(v[:,:,0]>180)&(v[:,:,1]>160)&(v[:,:,0]>v[:,:,2]*1.15)&(gy>240)&(gy<330);xs=np.where(mask)[1];anchor=np.median(xs) if len(xs)>30 else cell.width/2;x=round(320-anchor)
  assert x>=4 and x+cell.width<=636 and y>=4,(clip,j,x,y,cell.size)
  canvas=Image.new('RGBA',(640,448));canvas.alpha_composite(cell,(x,y));canvas.save(out/f'knight-{clip}-{j:02}.png');report[clip]['frames'].append({'translation':[x,y],'ground':408,'torso':320})
# Exact shared endpoints prevent a return to idle between queued strikes.
for dst,source in [('down-00','idle-00'),('cross-00','down-11'),('thrust-00','cross-11'),('thrust-11','idle-00')]:
 im=Image.open(out/f'knight-{source}.png');canvas=Image.new('RGBA',(640,448));canvas.alpha_composite(im,((640-im.width)//2,0));canvas.save(out/f'knight-{dst}.png')
for old in ['slash','stab','finisher']:
 for p in out.glob(f'knight-{old}-*.png'):p.unlink()
(src/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
sheet=Image.new('RGB',(6*320,6*246),(28,31,35));d=ImageDraw.Draw(sheet)
for row,clip in enumerate(['down','cross','thrust']):
 for i in range(12):
  im=Image.open(out/f'knight-{clip}-{i:02}.png');im.thumbnail((320,224));x=(i%6)*320;y=(row*2+i//6)*246;sheet.paste(im,(x,y),im);d.text((x+6,y+225),f'{clip} {i+1}',fill='white')
sheet.save(src/'combo-preview.jpg',quality=93)
print('Normalized 36 ground-combo frames, shared body scales, exact endpoint seams.')
