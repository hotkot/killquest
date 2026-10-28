from pathlib import Path
from PIL import Image
import shutil
root=Path(__file__).resolve().parents[1]
raw=Path('/workspace/scratch/e77afc5b40f4/generated_images/exec-e342737f-9e43-45a4-89df-f6870ae364e4.png')
source=root/'source-art/life-potion-v47.png'
if raw.exists():shutil.copy(raw,source)
im=Image.open(source).convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((112,112),Image.Resampling.LANCZOS)
frame=Image.new('RGBA',(128,128));frame.alpha_composite(im,((128-im.width)//2,120-im.height));frame.save(root/'dist/assets/items/life-potion.png')
print('Prepared life potion sprite, 128px RGBA.')
