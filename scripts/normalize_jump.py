from PIL import Image
from pathlib import Path
import json,numpy as np
from scipy.ndimage import label
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'source-art/hero-jump-v17.png').convert('RGBA');im.save(root/'source-art/hero-jump-v17.png');im=im.resize((2048,683),Image.Resampling.LANCZOS)
bounds=[0,272,536,786,1043,1295,1542,1810,2048];points=[(140,458),(365,477),(632,402),(882,330),(1138,319),(1387,366),(1634,487),(1920,456)]
for i,(cx,cy) in enumerate(points):
 frame=Image.new('RGBA',(400,400))
 if i in (0,7):frame.alpha_composite(Image.open(root/'source-art/uncentered/base-00.png').convert('RGBA'),(40,40))
 else:
  crop=im.crop((bounds[i],0,bounds[i+1],im.height));arr=np.array(crop);labs,n=label(arr[:,:,3]>8);sizes=np.bincount(labs.ravel());keep=sizes>35;keep[0]=False;arr[:,:,3][~keep[labs]]=0;crop=Image.fromarray(arr);box=crop.getbbox();crop=crop.crop(box);scale=.78;crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS);x=170-round((cx-bounds[i]-box[0])*scale);y=241-round((cy-box[1])*scale);frame.alpha_composite(crop,(x,y))
 frame.save(root/f'source-art/uncentered/hero-jump-{i:02}.png')
p=root/'source-art/action-anchors.json';a=json.loads(p.read_text());a['hero-jump']=[[170,241]]*8;p.write_text(json.dumps(a,indent=2)+'\n')

