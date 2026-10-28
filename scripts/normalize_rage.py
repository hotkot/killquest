from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label,find_objects
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'source-art/hero-rage-v22.png').convert('RGBA').resize((1536,1024),Image.Resampling.LANCZOS);a=np.array(im);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-8:],key=lambda k:(boxes[k-1][0].start//600,boxes[k-1][1].start))
pts=[(252,391),(649,384),(999,355),(1275,378),(186,806),(576,807),(951,773),(1337,787)]
for i,(k,(cx,cy)) in enumerate(zip(ids,pts)):
 arr=a.copy();arr[:,:,3][labs!=k]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);scale=.64;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-box[0])*scale),300-round((cy-box[1])*scale)));frame.save(root/f'source-art/uncentered/hero-rage-{i:02}.png')
p=root/'source-art/action-anchors.json';anchors=json.loads(p.read_text());anchors['hero-rage']=[[224,300]]*8;p.write_text(json.dumps(anchors,indent=2)+'\n')
