from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'source-art/hero-air-spin-v20.png').convert('RGBA').resize((1768,880),Image.Resampling.LANCZOS)
points=[(264,232),(672,232),(1098,240),(1594,234),(268,645),(660,644),(1104,687),(1580,684)]
xs=[0,490,940,1335,1768];ys=[0,430,880]
for i,(cx,cy) in enumerate(points):
 x=xs[i%4];y=ys[i//4];cut=im.crop((x,y,xs[i%4+1],ys[i//4+1]));a=np.array(cut);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;a[:,:,3][labs!=sizes.argmax()]=0;cut=Image.fromarray(a);box=cut.getbbox();cut=cut.crop(box);scale=.70;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-x-box[0])*scale),300-round((cy-y-box[1])*scale)));
 if i==0:frame=Image.open(root/'dist/assets/characters/hero-air-chop-06.png').convert('RGBA')
 if i==7:frame=Image.open(root/'dist/assets/characters/hero-heavy-03.png').convert('RGBA')
 frame.save(root/f'source-art/uncentered/hero-air-spin-{i:02}.png')
p=root/'source-art/action-anchors.json';a=json.loads(p.read_text());a['hero-air-spin']=[[224,300]]*8;p.write_text(json.dumps(a,indent=2)+'\n')
