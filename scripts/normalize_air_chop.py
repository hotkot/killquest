from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'source-art/hero-air-chop-v18.png').convert('RGBA').resize((1768,880),Image.Resampling.LANCZOS)
points=[(194,225),(660,286),(1140,300),(1520,282),(205,700),(640,710),(1100,700),(1530,682)]
xs=[0,460,930,1350,1768];ys=[0,465,880]
for i,(cx,cy) in enumerate(points):
 x=xs[i%4];y=ys[i//4];cut=im.crop((x,y,xs[i%4+1],ys[i//4+1]));a=np.array(cut);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;a[:,:,3][labs!=sizes.argmax()]=0;cut=Image.fromarray(a);box=cut.getbbox();cut=cut.crop(box);scale=.70;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-x-box[0])*scale),300-round((cy-y-box[1])*scale)));frame.save(root/f'source-art/uncentered/hero-air-chop-{i:02}.png')
p=root/'source-art/action-anchors.json';a=json.loads(p.read_text());a['hero-air-chop']=[[224,300]]*8;p.write_text(json.dumps(a,indent=2)+'\n')
