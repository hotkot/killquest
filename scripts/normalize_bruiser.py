from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1]
def normalize(src,clip,count,cols,scale,centers):
 im=Image.open(root/'source-art'/src).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs)
 ids=sorted(np.argsort(sizes)[-count:],key=lambda k:(int((boxes[k-1][0].start+boxes[k-1][0].stop)/2/(im.height/(count/cols))),boxes[k-1][1].start))
 for i,k in enumerate(ids):
  mask=binary_dilation(labs==k,iterations=2);arr=a.copy();arr[:,:,3][~mask]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
  frame=Image.new('RGBA',(448,448));cx=centers[i] if centers else (box[0]+box[2])/2
  frame.alpha_composite(cut,(224-round((cx-box[0])*scale),408-cut.height));frame.save(root/f'source-art/uncentered/{clip}-{i:02}.png')
 anchors=json.loads((root/'source-art/action-anchors.json').read_text());anchors[clip]=[[224,300]]*count;(root/'source-art/action-anchors.json').write_text(json.dumps(anchors,indent=2))
normalize('bandit-bruiser-v32.png','bandit-bruiser',24,6,.86,[130,380,642,899,1153,1409,128,380,640,896,1147,1400,128,382,640,898,1158,1400,128,382,640,898,1158,1400])
if (root/'source-art/hero-knockdown-v31.png').exists():normalize('hero-knockdown-v31.png','hero-knockdown',8,4,.61,[250,690,1180,1590,250,700,1170,1590])
# Approved individual repair replaces the duplicated-weapon walking pose.
repair=root/'source-art/bruiser-walk-fix-v32.png'
if repair.exists():
 im=Image.open(repair).convert('RGBA');arr=np.array(im);labs,n=label(arr[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;mask=binary_dilation(labs==sizes.argmax(),iterations=2);arr[:,:,3][~mask]=0;im=Image.fromarray(arr);box=im.getbbox();cut=im.crop(box);scale=200/cut.height
 cut=cut.resize((round(cut.width*scale),200),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((625-box[0])*scale),208));frame.save(root/'source-art/uncentered/bandit-bruiser-03.png')
# Keep the four anatomy/weapon redraws when rebuilding the original clip.
import runpy
if (root/'source-art/bruiser-repairs-v33.png').exists():
 runpy.run_path(str(root/'scripts/normalize_bruiser_repairs.py'))
