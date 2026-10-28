from PIL import Image,ImageDraw
from pathlib import Path
from scipy.ndimage import label,find_objects
import numpy as np,json
root=Path(__file__).resolve().parents[1];raw=np.array(Image.open(root/'source-art/townsfolk-v163/townsfolk-raw.png').convert('RGBA'));labs,n=label(raw[:,:,3]>30);sizes=np.bincount(labs.ravel());boxes=find_objects(labs);report={};board=Image.new('RGB',(2048,768),'#514947');d=ImageDraw.Draw(board)
for row,kind in enumerate(['laborer','villager','traveler']):
 ids=[k for k in range(1,n+1)if sizes[k]>1000 and row*256<=(boxes[k-1][0].start+boxes[k-1][0].stop)/2<(row+1)*256];ids.sort(key=lambda k:boxes[k-1][1].start);assert len(ids)==8,(kind,len(ids));tiles=[]
 for k in ids:
  a=raw.copy();a[labs!=k]=0;t=Image.fromarray(a);tiles.append(t.crop(t.getbbox()))
 scale=225/float(np.median([t.height for t in tiles]));entries=[]
 for i,(t,k)in enumerate(zip(tiles,ids)):
  a=np.array(t);yy,xx=np.where((a[:,:,3]>100)&(np.indices(a.shape[:2])[0]<t.height*.25));anchor=float(np.median(xx));res=t.resize((round(t.width*scale),round(t.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(448,448));offset=(round(224-anchor*scale),408-res.height);out.alpha_composite(res,offset);b=out.getbbox();assert b[0]>=16 and b[2]<=432 and b[1]>16 and b[3]<=408,(kind,i,b);out.save(root/f'dist/assets/characters/townsfolk-{kind}-{i:02}.png');ys,xs=boxes[k-1];entries.append({'frame':i,'source_component':int(k),'source_bounds':[xs.start,ys.start,xs.stop,ys.stop],'scale':scale,'head_anchor_x':anchor,'bounds':b,'foot_y':408});view=out.resize((300,300));x=i*256;y=row*256;board.paste(view,(x+128-150,y+238-round(408*300/448)),view);d.text((x+5,y+238),kind+' '+str(i),fill='white')
 report[kind]=entries
(root/'source-art/townsfolk-v164/normalization.json').write_text(json.dumps(report,indent=2));board.save(root/'source-art/townsfolk-v164/run-preview.png');print('Extracted24 complete character silhouettes from the full sheet, not nominal cells; removed neighboring fragments and restored cross-cell clothing/feet')
