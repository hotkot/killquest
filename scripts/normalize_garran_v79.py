"""Normalize reviewed 4x4 strips with shared body scale and torso/ground registration.
The generic sprite-strip helper assumes a horizontal strip and square output;
this variant preserves the established rectangular sword canvas and foot pivot.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json
root=Path(__file__).resolve().parents[1];src=root/'source-art/garran-v79';out=root/'dist/assets/characters';report={}
for clip in ['down','cross']:
 im=Image.open(src/(clip+'.png')).convert('RGBA');a=np.array(im);lab,n=label(a[:,:,3]>32);areas=np.bincount(lab.ravel());slices=find_objects(lab);ids=[i for i in range(1,n+1) if areas[i]>1000]
 ids.sort(key=lambda i:(round(((slices[i-1][0].start+slices[i-1][0].stop)/2)/(im.height/4)-.5),(slices[i-1][1].start+slices[i-1][1].stop)/2));assert len(ids)==16,(clip,len(ids))
 if clip=='cross':ids=[ids[i] for i in list(range(12))+[14,14,15,15]]  # Exclude the source's accidental second turn during recovery.
 if clip=='down':ids=[ids[1],ids[2],ids[0]]+ids[3:]  # Start vertical; then descend continuously instead of lifting first.
 cells=[];heights=[]
 for k in ids:
  sy,sx=slices[k-1];l=max(0,sx.start-2);r=min(im.width,sx.stop+2);t=max(0,sy.start-2);b=min(im.height,sy.stop+2);v=a[t:b,l:r].copy();v[:,:,3]=np.where(binary_dilation(lab[t:b,l:r]==k,iterations=2),v[:,:,3],0)
  alpha=v[:,:,3];red=(alpha>128)&(v[:,:,0]>120)&(v[:,:,1]<v[:,:,0]*.6)&(v[:,:,2]<v[:,:,0]*.7);heights.append(int(np.where(alpha>32)[0].max()-np.where(red)[0].min()+1));cells.append(Image.fromarray(v))
 # Plume-to-feet measurement excludes the raised sword, avoiding body shrinkage.
 scale=234/float(np.median(heights));report[clip]={'source_order':([1,2,0]+list(range(3,16))) if clip=='down' else list(range(12))+[14,14,15,15],'shared_scale':scale,'source_body_heights':heights,'frames':[]}
 for j,cell in enumerate(cells):
  cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS);v=np.array(cell);alpha=v[:,:,3];foot_alpha=alpha[:,:round(cell.width*.6)] if clip=='down' else alpha;y=408-int(np.where(foot_alpha>32)[0].max());gy=np.arange(cell.height)[:,None]+y
  mask=(alpha>128)&(v[:,:,0]>180)&(v[:,:,1]>160)&(v[:,:,0]>v[:,:,2]*1.15)&(gy>240)&(gy<330);xs=np.where(mask)[1];anchor=np.median(xs) if len(xs)>30 else cell.width/2;x=round(320-anchor)
  assert x>=4 and x+cell.width<=636 and y>=4,(clip,j,x,y,cell.size)
  canvas=Image.new('RGBA',(640,448));canvas.alpha_composite(cell,(x,y));canvas.save(out/f'knight-{clip}-{j:02}.png');report[clip]['frames'].append({'translation':[x,y],'ground':408,'torso':320})
# The raised start and low ending are deliberately retained in the first cut.
# Copy only the new spin endpoints; never alter the approved stab frames.
for dst,source in [('cross-00','down-15'),('cross-15','thrust-00')]:
 im=Image.open(out/f'knight-{source}.png');im.save(out/f'knight-{dst}.png')
(src/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
sheet=Image.new('RGB',(8*320,6*246),(28,31,35));d=ImageDraw.Draw(sheet)
for row,(clip,count) in enumerate([('down',16),('cross',16),('thrust',12)]):
 for i in range(count):
  im=Image.open(out/f'knight-{clip}-{i:02}.png');im.thumbnail((320,224));x=(i%8)*320;y=(row*2+i//8)*246;sheet.paste(im,(x,y),im);d.text((x+6,y+225),f'{clip} {i+1}',fill='white')
sheet.save(src/'combo-preview.jpg',quality=93)
print('Normalized 32 new cut/spin frames; preserved all twelve approved stab frames.')
