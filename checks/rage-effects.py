from pathlib import Path
from PIL import Image
import numpy as np
files=list(Path('dist/assets/effects').glob('rage-*.png'));assert len(files)==16
for p in files:
 a=np.array(Image.open(p));assert a.shape==(384,512,4) if 'blast' in p.name else a.shape==(96,96,4)
 alpha=a[:,:,3];assert alpha.max()>127 and alpha.min()==0
 assert not alpha[:6,:].any() and not alpha[-6:,:].any() and not alpha[:,:6].any() and not alpha[:,-6:].any(),p
print('PASS: 16 RGBA effect textures with transparent gutters and no edge clipping.')
