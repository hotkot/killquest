from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1];folder=root/'source-art/rebel-combat-v156';art=root/'dist/assets/characters';report={}
for kind in ['guard','bulwark','spearman','crossbowman','commander']:
 a=np.array(Image.open(folder/(kind+'.png')).convert('RGBA'));labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());boxes=find_objects(labs);ids=[k for k in range(1,n+1) if sizes[k]>10000];center=lambda k:(boxes[k-1][0].start+boxes[k-1][0].stop)/2
 if kind=='commander':ids=sorted([k for k in ids if center(k)<260],key=lambda k:boxes[k-1][1].start);assert len(ids)==6
 else:
  edges=[0,198,390,573,770,925,1024] if kind=='spearman' else [0,270,540,785,1024];order=[]
  for row in range(len(edges)-1):
   parts=sorted([k for k in ids if edges[row]<=center(k)<edges[row+1]],key=lambda k:boxes[k-1][1].start)
   if kind=='bulwark' and row==1:
    assert len(parts)==5;parts=[parts[0],parts[1],parts[1],parts[1],parts[3],parts[4]]
   if kind=='crossbowman' and row==1:parts[2]=parts[1] # actual swept bolt is rendered separately
   assert len(parts)==(4 if kind=='spearman' else 6),(kind,row,len(parts));order.extend(parts)
  ids=order;assert len(ids)==24
  if kind=='spearman':ids[6]=ids[12];ids[7]=ids[13]
 heights=[boxes[k-1][0].stop-boxes[k-1][0].start for k in ids[:6]];target={'guard':234,'bulwark':234,'spearman':234,'crossbowman':220,'commander':245}[kind];scale=target/np.median(heights);rows=[]
 for i,k in enumerate(ids):
  mask=(labs==k)|(binary_dilation(labs==k,iterations=2)&(labs==0));arr=a.copy();arr[~mask]=0;im=Image.fromarray(arr);im=im.crop(im.getbbox());v=np.array(im);yy,xx=np.where((v[:,:,3]>100)&(np.indices(v.shape[:2])[0]>im.height*.9));anchor=float(np.median(xx)) if im.height>120 else im.width/2;im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);width=1024 if kind=='spearman' else 768;out=Image.new('RGBA',(width,448));out.alpha_composite(im,(round(width/2-anchor*scale),408-im.height));b=out.getbbox();assert b[0]>3 and b[2]<width-3 and b[1]>3 and b[3]<=408,(kind,i,b);out.save(art/f'rebel-{kind}-combat-{i:02}.png');rows.append({'frame':i,'source_component':int(k),'scale':float(scale),'bounds':b,'foot_y':408})
 if kind=='commander':
  a=np.array(Image.open(folder/'commander-actions.png').convert('RGBA'));labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());boxes=find_objects(labs);large=[k for k in range(1,n+1)if sizes[k]>10000];order=[]
  for row in range(3):order.extend(sorted([k for k in large if row*1024/3 <= (boxes[k-1][0].start+boxes[k-1][0].stop)/2 < (row+1)*1024/3],key=lambda k:boxes[k-1][1].start))
  assert len(order)==12,len(order);neutral=boxes[order[3]-1];scale=245/(neutral[0].stop-neutral[0].start)
  mapping=[0,1,2,3,4,5,5,3,6,7,7,3,8,8,4,9,10,11]
  for j,which in enumerate(mapping):
   k=order[which];mask=(labs==k)|(binary_dilation(labs==k,iterations=2)&(labs==0));arr=a.copy();arr[~mask]=0;im=Image.fromarray(arr);im=im.crop(im.getbbox());v=np.array(im);yy,xx=np.where((v[:,:,3]>100)&(np.indices(v.shape[:2])[0]>im.height*.9));anchor=float(np.median(xx))if im.height>150 else im.width/2;im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(768,448));out.alpha_composite(im,(round(384-anchor*scale),408-im.height));b=out.getbbox();assert b[0]>3 and b[2]<765 and b[1]>3 and b[3]<=408,(j,b);out.save(art/f'rebel-commander-combat-{j+6:02}.png');rows.append({'frame':j+6,'source_action':which,'scale':float(scale),'bounds':b,'foot_y':408})
 report[kind]=rows
(folder/'normalization.json').write_text(json.dumps(report,indent=2));print('Normalized',sum(len(v)for v in report.values()),'combat poses; common scale per role,768x448 (spears1024x448) with foot408')
