from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import map_coordinates,gaussian_filter,maximum_filter
from scipy.optimize import minimize
import json
root=Path(__file__).resolve().parents[1];folder=root/'source-art/forest-fire-v144';out=root/'dist/assets/forest/ambient'
spots={'roof-left':(30,25,190,138),'roof-center':(320,120,488,247),'door':(414,316,470,410),'transition-roof':(1000,170,1270,330),'transition-wall':(1170,286,1252,370)}
original=Image.open(root/'dist/assets/forest/village.webp').convert('RGB');report={}
for key,box in spots.items():
 assetFolder=folder if key.startswith('transition') else root/'source-art/village-fire-v143'; original=Image.open(root/('dist/assets/forest/forest-village.webp' if key.startswith('transition') else 'dist/assets/forest/village.webp')).convert('RGB'); ref=np.array(Image.open(assetFolder/f'{key}-reference.png').convert('RGB')).astype(float)/255;sheet=Image.open(assetFolder/f'{key}-sheet.png').convert('RGB');cw,ch=sheet.width/3,sheet.height/2;cells=[np.array(sheet.crop((round(i%3*cw),round(i//3*ch),round((i%3+1)*cw),round((i//3+1)*ch)))).astype(float)/255 for i in range(6)]
 # Register the stationary wood/stone context; generated panels can have extra surrounding crop.
 yy,xx=np.mgrid[3:ref.shape[0]-3:4,3:ref.shape[1]-3:4];tr=ref[yy,xx];mask=(tr[:,:,0]<.72)|(tr[:,:,1]>tr[:,:,0]*.85);xx=xx[mask];yy=yy[mask];target=tr[mask];gen=cells[0]
 def loss(p):
  sx,sy,tx,ty=p;x=xx*sx+tx;y=yy*sy+ty;valid=(x>=0)&(x<gen.shape[1]-1)&(y>=0)&(y<gen.shape[0]-1)
  if valid.mean()<.4:return 1
  sample=np.stack([map_coordinates(gen[:,:,c],[y[valid],x[valid]],order=1,mode='nearest') for c in range(3)],axis=-1)
  return np.mean(np.minimum(np.abs(sample-target[valid]),.4))+(1-valid.mean())*.025
 candidates=[]
 for scale in [.8,1,1.4,2.4]:
  p=[scale,scale,0,0];fit=minimize(loss,p,method='Powell',bounds=[(.55,3.5),(.55,3.5),(-120,120),(-100,130)],options={'maxiter':80,'xtol':.0005});candidates.append(fit)
 fit=min(candidates,key=lambda f:f.fun);sx,sy,tx,ty=fit.x;print(key,'registration',fit.x.round(3),'loss',round(fit.fun,4))
 w,h=box[2]-box[0],box[3]-box[1];base=np.array(original.crop(box)).astype(float);y,x=np.mgrid[:h,:w];factor=2 if key.startswith('transition') else 3;rx=x*factor;ry=y*factor
 # Freeze charred structural pixels. Only original luminous flame interiors and soft fringes change.
 r,g,b=base[:,:,0],base[:,:,1],base[:,:,2];hot=(r>185)&(g>60)&(r>g*1.08)&(b<g*.9);gate=gaussian_filter(maximum_filter(hot.astype(float),size=3),.65);gate*=np.clip((r-90)/80,0,1);gate*=np.clip((np.minimum.reduce([x,y,w-1-x,h-1-y])-1)/3,0,1)
 
 if key=='transition-roof':gate*=((x+box[0]>1040)&(x+box[0]<1185)&(y+box[1]<247))
 if key=='transition-wall':
  cavity=(x+box[0]>1197)&(x+box[0]<1227)&(y+box[1]>313)&(y+box[1]<341); gate=gaussian_filter(cavity.astype(float),.5); gate[:,(x[0]+box[0]>=1209)&(x[0]+box[0]<=1212)]=0
 frames=[base];valid=(rx*sx+tx>=0)&(rx*sx+tx<cw-1)&(ry*sy+ty>=0)&(ry*sy+ty<ch-1);gate*=valid
 for cell in cells:
  aligned=np.stack([map_coordinates(cell[:,:,c],[ry*sy+ty,rx*sx+tx],order=1,mode='nearest') for c in range(3)],axis=-1)*255
  # Match each location's original flame palette, without changing stationary wood or smoke.
  if hot.any():
   delta=np.median(base[hot],axis=0)-np.median(aligned[hot],axis=0);aligned=np.clip(aligned+delta*.65,0,255)
  frames.append(base*(1-gate[:,:,None])+aligned*gate[:,:,None])
 gate*=np.clip((box[0]+x)*.9375/160,0,1);alpha=np.rint(gate*255).clip(0,255).astype('uint8');Image.fromarray(alpha).save(folder/f'{key}-matte.png');
 atlas=Image.new('RGBA',(w*4,h*7));preview=Image.new('RGB',(w*4,h*2))
 for f in range(28):
  k=f//4;u=(f%4)/4;a=frames[k];b2=frames[(k+1)%7];a=np.rint(a*(1-u)+b2*u).clip(0,255).astype('uint8');im=Image.fromarray(np.dstack([a,alpha]));atlas.paste(im,((f%4)*w,(f//4)*h));
  if f%4==0:preview.paste(im,(((f//4)%4)*w,((f//4)//4)*h))
 atlas.save(out/f'fitted-{key}-v144.png');preview.resize((preview.width*2,preview.height*2)).save(folder/f'{key}-preview.png');report[key]={'box':box,'registration':fit.x.tolist(),'registration_loss':fit.fun,'changed_pixels':int((gate>.05).sum()),'frames':28}
(folder/'normalization.json').write_text(json.dumps(report,indent=2))
