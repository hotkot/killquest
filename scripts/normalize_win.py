from pathlib import Path
from PIL import Image
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json,shutil
root=Path(__file__).resolve().parents[1];im=Image.open(root/'source-art/hero-win-v41.png').convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-12:],key=lambda k:(int((boxes[k-1][0].start+boxes[k-1][0].stop)/2/(im.height/3)),boxes[k-1][1].start))
scale=210/(boxes[ids[0]-1][0].stop-boxes[ids[0]-1][0].start)
centers=[220,558,895,1240,220,560,896,1240,220,558,895,1240]
for i in range(12):
 # Hold the first raised pose instead of using the clipped raw top-right frame.
 source=4 if i==3 else i;k=ids[source];arr=a.copy();arr[:,:,3][~binary_dilation(labs==k,iterations=2)]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((centers[source]-box[0])*scale),408-cut.height));frame.save(root/f'source-art/uncentered/hero-win-{i:02}.png')
anchors=json.loads((root/'source-art/action-anchors.json').read_text());anchors['hero-win']=[[224,300]]*12
walk=json.loads((root/'source-art/walk-anchors.json').read_text());idle=(walk.get('hero-idle') or anchors['hero-idle'])[0]
for i in [0,11]:
 shutil.copy(root/'source-art/uncentered/hero-idle-00.png',root/f'source-art/uncentered/hero-win-{i:02}.png');anchors['hero-win'][i]=idle
(root/'source-art/action-anchors.json').write_text(json.dumps(anchors,indent=2))
