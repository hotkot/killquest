from PIL import Image,ImageDraw
from pathlib import Path
from scipy.ndimage import label,find_objects
import numpy as np,json
root=Path(__file__).resolve().parents[1];folder=root/'source-art/townsfolk-v165';report={};allframes={}
def extract(path,rows,columns):
 raw=np.array(Image.open(path).convert('RGBA'));h,w=raw.shape[:2];labs,n=label(raw[:,:,3]>30);sizes=np.bincount(labs.ravel());boxes=find_objects(labs);clips=[]
 for row in range(rows):
  ids=[k for k in range(1,n+1)if sizes[k]>1500 and row*h/rows<=(boxes[k-1][0].start+boxes[k-1][0].stop)/2<(row+1)*h/rows];ids.sort(key=lambda k:boxes[k-1][1].start);assert len(ids)==columns,(str(path),row,len(ids));parts=[]
  for k in ids:
   a=raw.copy();a[labs!=k]=0;t=Image.fromarray(a);parts.append((t.crop(t.getbbox()),int(k)))
  clips.append(parts)
 return clips
def normalize(kind,clips):
 idle=clips['idle'];scale=232/float(np.median([im.height for im,k in idle]));entries=[];frames={}
 for clip,parts in clips.items():
  frames[clip]=[]
  seed=np.array(parts[0][0]);sy,sx=np.where((seed[:,:,3]>100)&(np.indices(seed.shape[:2])[0]>seed.shape[0]*.9));foot_ref=float((sx.min()+sx.max())/2);sy,sx=np.where((seed[:,:,3]>100)&(np.indices(seed.shape[:2])[0]<seed.shape[0]*.25));head_ref=float(np.median(sx))
  for i,(im,k)in enumerate(parts):
   a=np.array(im);yy,xx=np.where((a[:,:,3]>100)&(np.indices(a.shape[:2])[0]<im.height*.25));anchor=float(np.median(xx));
   if clip=='idle':
    fy,fx=np.where((a[:,:,3]>100)&(np.indices(a.shape[:2])[0]>im.height*.9));anchor=head_ref+float((fx.min()+fx.max())/2)-foot_ref
   im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(448,448));out.alpha_composite(im,(round(224-anchor*scale),408-im.height));b=out.getbbox();assert b[0]>=16 and b[2]<=432 and b[1]>=16 and b[3]<=408,(kind,clip,i,b);name='townsfolk-'+kind+('-idle'if clip=='idle'else'')+f'-{i:02}';out.save(root/f'dist/assets/characters/{name}.png');entries.append({'frame':i,'clip':clip,'source_component':k,'scale':scale,'bounds':b,'foot_y':408});frames[clip].append(out)
 report[kind]=entries;allframes[kind]=frames
for kind in ['baker','weaver','porter']:
 rows=extract(folder/(kind+'.png'),4,4);normalize(kind,{'run':rows[0]+rows[1],'idle':rows[2]+rows[3]})
rows=extract(folder/'original-idles.png',3,8)
for kind,idles in zip(['laborer','villager','traveler'],rows):normalize(kind,{'idle':idles})
(folder/'normalization.json').write_text(json.dumps(report,indent=2))
board=Image.new('RGB',(1600,6*260),'#514947');d=ImageDraw.Draw(board)
for row,kind in enumerate(['laborer','villager','traveler','baker','weaver','porter']):
 for col,im in enumerate(allframes[kind]['idle']):
  view=im.resize((300,300));x=col*200;y=row*260;board.paste(view,(x+100-150,y+238-round(408*300/448)),view);d.text((x+5,y+240),kind+' idle '+str(col),fill='white')
board.save(folder/'idle-preview.png')
board=Image.new('RGB',(1600,3*260),'#514947');d=ImageDraw.Draw(board)
for row,kind in enumerate(['baker','weaver','porter']):
 for col,im in enumerate(allframes[kind]['run']):
  view=im.resize((300,300));x=col*200;y=row*260;board.paste(view,(x+100-150,y+238-round(408*300/448)),view);d.text((x+5,y+240),kind+' run '+str(col),fill='white')
board.save(folder/'new-runs-preview.png');print('Normalized72 new frames: run24 + idle48, exact silhouette extraction, shared scale within each new character, fixed floor and head/body anchor.')
