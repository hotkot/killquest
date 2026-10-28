from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import numpy as np
for i in range(8):
 p=Path(f'dist/assets/items/container-{i:02}.png');a=np.array(Image.open(p));assert a.shape==(256,256,4)
 alpha=a[:,:,3];assert not alpha[:8].any() and not alpha[-8:].any() and not alpha[:,:8].any() and not alpha[:,-8:].any(),p
 labs,n=label(alpha>100);sizes=np.bincount(labs.ravel())[1:]
 if i not in [2,6]:assert len(sizes[sizes>20])==1,(p,'stray fragments outside static prop')
for i in range(6):
 a=np.array(Image.open(f'dist/assets/items/food-{i:02}.png'));assert a.shape==(128,128,4)
 assert not a[:4,:,3].any() and not a[-4:,:,3].any()
print('PASS: eight padded container frames, no stray pieces in static states, six transparent food sprites.')
