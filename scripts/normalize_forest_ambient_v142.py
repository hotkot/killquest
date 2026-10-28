from pathlib import Path
from PIL import Image
import numpy as np
root=Path(__file__).resolve().parents[1]
for kind in ['fire','smoke']:
 im=Image.open(root/f'source-art/forest-ambient-v142/{kind}-sheet.png').convert('RGBA');w,h=im.width//3,im.height//2
 for i in range(6):
  cell=im.crop(((i%3)*w,(i//3)*h,(i%3+1)*w,(i//3+1)*h));a=np.array(cell);yy,xx=np.mgrid[:h,:w]
  # Transparent edge padding removes neighboring glow fringes, preserves soft internal alpha.
  feather=np.minimum.reduce([xx/18,(w-1-xx)/18,yy/12,(h-1-yy)/12,np.ones((h,w))]);a[:,:,3]=(a[:,:,3]*np.clip(feather,0,1)).astype('uint8')
  frame=Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS);frame.save(root/f'dist/assets/forest/ambient/{kind}-{i}.png')
 print(kind,'6 equally scaled 256x256 transparent frames')
