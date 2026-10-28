from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label
root=Path(__file__).resolve().parents[1]
points={
'sword':[(200,157),(512,157),(820,158),(1137,158),(197,476),(511,476),(816,475),(1137,477),(148,797),(474,793),(755,805),(1035,805),(144,1080),(465,1081),(779,1080),(1126,1080)],
'archer':[(201,153),(512,154),(822,154),(1134,154),(190,478),(505,478),(819,478),(1130,477),(172,776),(475,776),(790,776),(1082,780),(169,1093),(488,1080),(791,1065),(1130,1080)]}
p=root/'source-art/action-anchors.json';anchors=json.loads(p.read_text())
for kind,pts in points.items():
 im=Image.open(root/f'source-art/bandit-{kind}-v21.png').convert('RGBA').resize((1280,1280),Image.Resampling.LANCZOS)
 for i,(cx,cy) in enumerate(pts):
  x=(i%4)*320;y=(i//4)*320;cut=im.crop((x,y,x+320,y+320));a=np.array(cut);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;a[:,:,3][labs!=sizes.argmax()]=0;cut=Image.fromarray(a);box=cut.getbbox();cut=cut.crop(box);scale=.68;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-x-box[0])*scale),300-round((cy-y-box[1])*scale)));frame.save(root/f'source-art/uncentered/bandit-{kind}-{i:02}.png')
 anchors['bandit-'+kind]=[[224,300]]*16
p.write_text(json.dumps(anchors,indent=2)+'\n')

# Refined walking sheet: distinct contact and crossed-leg passing poses.
im=Image.open(root/'source-art/bandit-walks-v21.png').convert('RGBA').resize((1280,1280),Image.Resampling.LANCZOS)
pts=[(184,160),(514,157),(826,162),(1150,159),(187,480),(516,478),(832,478),(1152,478),(181,783),(511,783),(823,781),(1146,782),(182,1101),(509,1102),(823,1102),(1146,1103)]
for i,(cx,cy) in enumerate(pts):
 x=(i%4)*320;y=(i//4)*320;cut=im.crop((x,y,x+320,y+320));a=np.array(cut);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;a[:,:,3][labs!=sizes.argmax()]=0;cut=Image.fromarray(a);box=cut.getbbox();cut=cut.crop(box);scale=.68;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-x-box[0])*scale),300-round((cy-y-box[1])*scale)));kind='sword' if i<8 else 'archer';frame.save(root/f'source-art/uncentered/bandit-{kind}-{i%8:02}.png')
