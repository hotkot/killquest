from PIL import Image,ImageDraw
from pathlib import Path
import numpy as np,json
root=Path(__file__).resolve().parents[1];im=Image.open(root/'source-art/townsfolk-v163/townsfolk-raw.png').convert('RGBA');w,h=im.size;report={};board=Image.new('RGB',(1280,660),'#514947');d=ImageDraw.Draw(board)
for row,kind in enumerate(['laborer','villager','traveler']):
 tiles=[]
 for col in range(8):
  t=im.crop((round(col*w/8),round(row*h/3),round((col+1)*w/8),round((row+1)*h/3)));a=np.array(t);a[a[:,:,3]<30]=0;t=Image.fromarray(a);tiles.append(t.crop(t.getbbox()))
 scale=225/float(np.median([t.height for t in tiles]));entries=[]
 for i,t in enumerate(tiles):
  a=np.array(t);yy,xx=np.where((a[:,:,3]>100)&(np.indices(a.shape[:2])[0]<t.height*.25));anchor=float(np.median(xx));res=t.resize((round(t.width*scale),round(t.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(448,448));offset=(round(224-anchor*scale),408-res.height);out.alpha_composite(res,offset);b=out.getbbox();assert b[0]>3 and b[2]<445 and b[1]>3 and b[3]<=408,(kind,i,b);out.save(root/f'dist/assets/characters/townsfolk-{kind}-{i:02}.png');entries.append({'frame':i,'scale':scale,'head_anchor_x':anchor,'bounds':b,'foot_y':408});view=out.resize((300,300));x=i*160;y=row*220;board.paste(view,(x+80-150,y+208-round(408*300/448)),view);d.text((x+5,y+207),kind+' '+str(i),fill='white')
 report[kind]=entries
(root/'source-art/townsfolk-v163/normalization.json').write_text(json.dumps(report,indent=2));board.save(root/'source-art/townsfolk-v163/run-preview.png');print('24 frames normalized: shared scale per civilian, stable head/body center, foot408, 448px canvas')
