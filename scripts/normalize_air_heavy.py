from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label,find_objects
root=Path(__file__).resolve().parents[1];im=Image.open(root/'source-art/hero-air-heavy-v28.png').convert('RGBA').resize((1774,887),Image.Resampling.LANCZOS);a=np.array(im);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-8:],key=lambda k:((boxes[k-1][0].start+boxes[k-1][0].stop)/2>=im.height/2,boxes[k-1][1].start));pts=[(312,312),(788,304),(1131,309),(1522,296),(257,668),(675,691),(1148,736),(1545,684)]
for i,(k,(cx,cy)) in enumerate(zip(ids,pts)):
 arr=a.copy();arr[:,:,3][labs!=k]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);scale=.66;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));dy=300-round((cy-box[1])*scale) if i<4 else 408-cut.height;frame.alpha_composite(cut,(224-round((cx-box[0])*scale),dy))
 if i==6:
  cut=Image.open(root/'dist/assets/characters/hero-jump-06.png').convert('RGBA');box=cut.getchannel('A').getbbox();cut=cut.crop(box);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(box[0],408-cut.height))
 if i==7:frame=Image.open(root/'dist/assets/characters/hero-idle-00.png').convert('RGBA')
 frame.save(root/f'source-art/uncentered/hero-air-heavy-{i:02}.png')
p=root/'source-art/action-anchors.json';anchors=json.loads(p.read_text());anchors['hero-air-heavy']=[[224,300]]*8;p.write_text(json.dumps(anchors,indent=2)+'\n')
