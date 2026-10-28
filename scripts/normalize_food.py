from pathlib import Path
from PIL import Image
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json,shutil
root=Path(__file__).resolve().parents[1]
def cells(file,cols,rows):
 im=Image.open(root/'source-art'/file).convert('RGBA');a=np.array(im);out=[]
 for i in range(cols*rows):
  x=int(i%cols*im.width/cols);y=int(i//cols*im.height/rows);arr=a[y:int((i//cols+1)*im.height/rows),x:int((i%cols+1)*im.width/cols)].copy();labs,n=label(arr[:,:,3]>100);sz=np.bincount(labs.ravel());sz[0]=0;arr[:,:,3][~binary_dilation(labs==sz.argmax(),iterations=2)]=0;cut=Image.fromarray(arr);box=cut.getbbox();out.append((cut.crop(box),box,x,y))
 return out
poses=cells('hero-pickup-v35.png',4,2);scale=210/poses[0][0].height
for i,source in enumerate([0,1,3,3,4,5,6,7]):
 cut,box,x,y=poses[source];cx=[220,665,1090,1520,220,655,1090,1525][source]-x
 cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-box[0])*scale),408-cut.height));frame.save(root/f'source-art/uncentered/hero-pickup-{i:02}.png')
for i in [0,7]:shutil.copy(root/'source-art/uncentered/hero-idle-00.png',root/f'source-art/uncentered/hero-pickup-{i:02}.png')
anchors=json.loads((root/'source-art/action-anchors.json').read_text());anchors['hero-pickup']=[[224,300]]*8;(root/'source-art/action-anchors.json').write_text(json.dumps(anchors,indent=2))
# Locked idle endpoints use the source idle landmark rather than an inferred one.
walk=json.loads((root/'source-art/walk-anchors.json').read_text());anchors['hero-pickup'][0]=walk.get('hero-idle',anchors.get('hero-idle'))[0];anchors['hero-pickup'][7]=anchors['hero-pickup'][0];(root/'source-art/action-anchors.json').write_text(json.dumps(anchors,indent=2))
(root/'dist/assets/items').mkdir(exist_ok=True)
for i,(cut,box,x,y) in enumerate(cells('food-v34.png',3,2)):
 cut.thumbnail((112,112),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(128,128));frame.alpha_composite(cut,((128-cut.width)//2,120-cut.height));frame.save(root/f'dist/assets/items/food-{i:02}.png')
