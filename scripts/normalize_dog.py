from pathlib import Path
from PIL import Image
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json
root=Path(__file__).resolve().parents[1];im=Image.open(root/'source-art/enemy-dog-v39.png').convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-16:],key=lambda k:(int((boxes[k-1][0].start+boxes[k-1][0].stop)/2/(im.height/4)),boxes[k-1][1].start))
scale=110/(boxes[ids[12]-1][0].stop-boxes[ids[12]-1][0].start)
for i,k in enumerate(ids):
 arr=a.copy();arr[:,:,3][~binary_dilation(labs==k,iterations=2)]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,((448-cut.width)//2,408-cut.height));frame.save(root/f'source-art/uncentered/enemy-dog-{i:02}.png')
anchors=json.loads((root/'source-art/action-anchors.json').read_text());anchors['enemy-dog']=[[224,300]]*16;(root/'source-art/action-anchors.json').write_text(json.dumps(anchors,indent=2))
