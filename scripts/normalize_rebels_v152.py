from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
root=Path(__file__).resolve().parents[1];folder=root/'source-art/rebels-v152';art=root/'dist/assets/characters';report={}
for kind in ['guard','bulwark','spearman','crossbowman','commander']:
 p=folder/(kind+'.png')
 if not p.exists():continue
 sheet=Image.open(p).convert('RGBA');cuts=[]
 for i in range(6):
  cell=sheet.crop((round(i%3*sheet.width/3),round(i//3*sheet.height/2),round((i%3+1)*sheet.width/3),round((i//3+1)*sheet.height/2)));arr=np.array(cell);ys,xs=np.where(arr[:,:,3]>100);box=(max(0,xs.min()-2),max(0,ys.min()-2),min(cell.width,xs.max()+3),min(cell.height,ys.max()+3));cuts.append(cell.crop(box))
 target={'spearman':293,'crossbowman':220,'commander':245}.get(kind,234);scale=target/np.median([im.height for im in cuts]);rows=[]
 for i,im in enumerate(cuts):
  arr=np.array(im);ys,xs=np.where((arr[:,:,3]>100)&(np.indices(arr.shape[:2])[0]>im.height*.9));anchor=float(np.median(xs));im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(448,448));out.alpha_composite(im,(round(224-anchor*scale),408-im.height));b=out.getbbox();assert b[0]>4 and b[2]<444 and b[1]>4 and b[3]<=408,(kind,i,b);out.save(art/f'rebel-{kind}-{i:02}.png');rows.append({'frame':i,'bounds':b,'scale':scale,'foot':408});
 report[kind]=rows
(folder/'normalization.json').write_text(json.dumps(report,indent=2));print('Normalized',len(report),'roles; shared per-role scales, foot408, full weapons')
