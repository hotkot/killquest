from PIL import Image
from scipy.ndimage import label
import numpy as np,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];report=json.loads((root/'source-art/townsfolk-v165/normalization.json').read_text())
for kind,rows in report.items():
 feet=[];heights=[]
 for r in rows:
  name='townsfolk-'+kind+('-idle'if r['clip']=='idle'else'')+f'-{r["frame"]:02}.png';a=np.array(Image.open(root/'dist/assets/characters'/name));labs,n=label(a[:,:,3]>60);sizes=np.bincount(labs.ravel());assert sum(sizes[1:]>8)==1,(name,'stray body fragment');assert not a[:16,:,3].any() and not a[:,0:16,3].any() and not a[:,432:,3].any() and not a[409:,:,3].any()
  if r['clip']=='idle':
   yy,xx=np.where((a[:,:,3]>100)&(np.indices(a.shape[:2])[0]>390));feet.append(float((xx.min()+xx.max())/2));yy,xx=np.where(a[:,:,3]>100);heights.append(int(yy.max()-yy.min()+1))
 assert max(feet)-min(feet)<5,(kind,'idle foot-center drift',feet)
 assert max(heights)/min(heights)<1.05,(kind,'idle scale drift',heights)
print('PASS all72 new frames: single complete silhouette, transparent gutters; all48 idle poses have stable planted feet and less than5% body-height variation.')
