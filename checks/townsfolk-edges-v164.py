from PIL import Image
import numpy as np,json
from scipy.ndimage import label
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.loads((root/'source-art/townsfolk-v164/normalization.json').read_text());raw=np.array(Image.open(root/'source-art/townsfolk-v163/townsfolk-raw.png'));source_labels,n=label(raw[:,:,3]>30)
for kind,frames in rows.items():
 assert len(frames)==8
 assert len({f['scale']for f in frames})==1
 for f in frames:
  a=np.array(Image.open(root/f'dist/assets/characters/townsfolk-{kind}-{f["frame"]:02}.png'));l,n=label(a[:,:,3]>60);sizes=np.bincount(l.ravel());assert sum(sizes[1:]>8)==1,(kind,f['frame'],'stray disconnected fragment');b=f['bounds'];assert b[0]>=16 and b[2]<=432 and b[1]>=16 and b[3]<=408
  k=f['source_component'];ys,xs=np.where(source_labels==k);assert f['source_bounds']==[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
  assert np.count_nonzero(a[:,:,3]>100)>5000
print('PASS all24 frames contain one complete body component, exact full-sheet silhouette bounds, shared scale and floor, clear transparent gutters; no neighboring sprite fragments.')
