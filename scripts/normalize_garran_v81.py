"""Normalize dynamic downward and horizontal cut strips with shared body scale and torso/ground registration.
The generic sprite-strip helper assumes a horizontal strip and square output;
this variant preserves the established rectangular sword canvas and foot pivot.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects,binary_dilation,binary_opening
import numpy as np,json
root=Path(__file__).resolve().parents[1];src=root/'source-art/garran-v81';out=root/'dist/assets/characters';report={}
for clip,count,rows in [('down',8,2),('cross',12,4)]:
 im=Image.open(src/(clip+'.png')).convert('RGBA');a=np.array(im);core_threshold=240 if clip=='down' else 32;lab,n=label(binary_opening(a[:,:,3]>core_threshold));areas=np.bincount(lab.ravel());slices=find_objects(lab);ids=[i for i in range(1,n+1) if areas[i]>1000]
 ids.sort(key=lambda i:(round(((slices[i-1][0].start+slices[i-1][0].stop)/2)/(im.height/rows)-.5),(slices[i-1][1].start+slices[i-1][1].stop)/2));assert len(ids)==count,(clip,len(ids))
 if clip=='cross':ids=[ids[i] for i in list(range(9))+[8,10,11]]  # Hold the low follow-through instead of a spurious extra cut.
 cells=[];heights=[]
 for k in ids:
  sy,sx=slices[k-1];l=max(0,sx.start-4);r=min(im.width,sx.stop+4);t=max(0,sy.start-4);b=min(im.height,sy.stop+4);v=a[t:b,l:r].copy();v[:,:,3]=np.where(binary_dilation(lab[t:b,l:r]==k,iterations=3),v[:,:,3],0)
  alpha=v[:,:,3];red=(alpha>128)&(v[:,:,0]>120)&(v[:,:,1]<v[:,:,0]*.6)&(v[:,:,2]<v[:,:,0]*.7);heights.append(int(np.where(alpha>32)[0].max()-np.where(red)[0].min()+1));cells.append(Image.fromarray(v))
 # Plume-to-feet measurement excludes the raised sword, avoiding body shrinkage.
 scale=234/float(heights[0]);report[clip]={'source_order':list(range(8)) if clip=='down' else list(range(9))+[8,10,11],'core_threshold':core_threshold,'shared_scale':scale,'source_body_heights':heights,'frames':[]}
 for j,cell in enumerate(cells):
  cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS);v=np.array(cell);alpha=v[:,:,3]
  # Broad planted soles establish the ground; ignore a narrow low sword tip.
  row_width=(alpha>32).sum(axis=1);foot_base=int(np.where(row_width>=max(12,round(cell.width*.04)))[0].max());y=408-foot_base
  # Register the stance, allowing shoulders/chest to lean relative to the boots.
  gy=np.arange(cell.height)[:,None];xs=np.where((alpha>100)&(gy>foot_base-22)&(gy<=foot_base))[1];anchor=(np.percentile(xs,10)+np.percentile(xs,90))/2;x=round(320-anchor)
  assert x>=4 and x+cell.width<=636 and y>=4,(clip,j,x,y,cell.size)
  canvas=Image.new('RGBA',(640,448));canvas.alpha_composite(cell,(x,y));canvas.save(out/f'knight-{clip}-{j:02}.png');report[clip]['frames'].append({'translation':[x,y],'ground':408,'stance_center':320})
# Exact endpoints link two cuts to the approved stab without changing any stab PNG.
for dst,source in [('cross-00','down-07'),('cross-11','thrust-00')]:
 Image.open(out/f'knight-{source}.png').save(out/f'knight-{dst}.png')
(src/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
sheet=Image.new('RGB',(8*320,6*246),(28,31,35));d=ImageDraw.Draw(sheet)
for row,(clip,count) in enumerate([('down',8),('cross',12),('thrust',12)]):
 for i in range(count):
  im=Image.open(out/f'knight-{clip}-{i:02}.png');im.thumbnail((320,224));x=(i%8)*320;y=(row*2+i//8)*246;sheet.paste(im,(x,y),im);d.text((x+6,y+225),f'{clip} {i+1}',fill='white')
sheet.save(src/'combo-preview.jpg',quality=93)
print('Normalized 8 dynamic downward-cut poses and 12 horizontal-cut poses; preserved 12 stab frames.')
