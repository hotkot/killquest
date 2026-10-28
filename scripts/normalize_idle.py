from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label,find_objects
root=Path(__file__).resolve().parents[1];im=Image.open(root/'source-art/hero-idle-v26.png').convert('RGBA').resize((1774,887),Image.Resampling.LANCZOS);a=np.array(im);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-8:],key=lambda k:((boxes[k-1][0].start+boxes[k-1][0].stop)/2>=im.height/2,boxes[k-1][1].start));xs=[229,674,1118,1561,230,673,1118,1560]
for i,(k,cx) in enumerate(zip(ids,xs)):
 arr=a.copy();arr[:,:,3][labs!=k]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);scale=.52;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-box[0])*scale),408-cut.height));frame.save(root/f'source-art/uncentered/hero-idle-{i:02}.png')
p=root/'source-art/action-anchors.json';anchors=json.loads(p.read_text());anchors['hero-idle']=[[224,300]]*8;p.write_text(json.dumps(anchors,indent=2)+'\n')
