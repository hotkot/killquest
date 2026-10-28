from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,io,subprocess
from scipy.signal import fftconvolve
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).resolve().parents[1];out=root/'source-art/npc-v160';art=root/'dist/assets/characters'
heads={'guard':(187,176,243,223),'bulwark':(182,180,239,233),'spearman':(203,170,266,219),'crossbowman':(211,189,269,248),'commander':(181,179,244,242)}
def gray(im):
 a=np.array(im.convert('RGBA'),dtype=np.float64)/255;return (a[:,:,:3].mean(2)*a[:,:,3]+.18*(1-a[:,:,3])).astype(np.float64)
def original(key):return Image.open(io.BytesIO(subprocess.check_output(['git','show',f'96123d56674877d064e18e51ea83d498eee52cf9:dist/assets/characters/{key}.png'],cwd=root))).convert('RGBA')
def match(kind):
 ref=original(f'rebel-{kind}-00').crop(heads[kind]);templates=[]
 for scale in np.arange(.75,1.351,.05):
  for angle in [-120,-90,-60,-30,0,30,60,90,120,150,180]:
   im=ref.resize((round(ref.width*scale*.5),round(ref.height*scale*.5)),Image.Resampling.LANCZOS).rotate(angle,Image.Resampling.BICUBIC,expand=True)
   t=gray(im);t-=t.mean();norm=np.sqrt((t*t).sum());templates.append((float(scale),angle,t,norm))
 rows=[];board=Image.new('RGB',(1440,900),'#514947');d=ImageDraw.Draw(board)
 for j in range(30):
  key=f'rebel-{kind}-'+(f'{j:02}'if j<6 else f'combat-{j-6:02}');im=original(key);a=gray(im.resize((im.width//2,224),Image.Resampling.LANCZOS));best=(-1,None)
  for scale,angle,t,norm in templates:
   h,w=t.shape;ones=np.ones((h,w),dtype=np.float64);s=fftconvolve(a,ones,mode='valid');ss=fftconvolve(a*a,ones,mode='valid');denom=np.sqrt(np.maximum(ss-s*s/(h*w),1e-5))*norm
   corr=fftconvolve(a,t[::-1,::-1],mode='valid')/np.maximum(denom,1e-5)
   yy,xx=np.unravel_index(corr.argmax(),corr.shape);score=float(corr[yy,xx])
   if score>best[0]:best=(score,(scale,angle,int(xx*2),int(yy*2),w*2,h*2))
  score,(scale,angle,x,y,w,h)=best;rows.append(dict(key=key,scale=round(scale,2),angle=angle,score=round(score,3),head=[x,y,w,h]))
  tile=im.resize((round(im.width*.6),269));px=j%8*180;py=j//8*225;ix=px+90-tile.width//2;iy=py+210-round(408*.6);board.paste(tile,(ix,iy),tile);d.rectangle((ix+x*.6,iy+y*.6,ix+(x+w)*.6,iy+(y+h)*.6),outline='yellow');d.text((px+3,py+210),f'{j-6 if j>=6 else "i"+str(j)} {scale:.2f} {score:.2f}',fill='white')
 board.save(out/(kind+'-heads.png'));return kind,rows
report=dict(ThreadPoolExecutor(5).map(match,heads));(out/'heads.json').write_text(json.dumps(report,indent=2));print({k:[(r['key'].split(k+'-')[1],r['scale'],r['score'])for r in v if r['scale']!=1 or r['score']<.6]for k,v in report.items()})
