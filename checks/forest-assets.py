from pathlib import Path
from PIL import Image
root=Path('dist/assets/forest')
for i in range(8):
 im=Image.open(root/f'elder-{i}.png');box=im.getchannel('A').getbbox();assert im.size==(256,448);assert box[3]==438 and box[0]>0 and box[2]<256;assert 145<(box[3]-box[1])*224/448<=150.5
for name in ['stall','rock','cart','well']+[f'barricade-{i}' for i in range(4)]:
 f='prop-'+name+'.png' if name in ['stall','rock','cart','well'] else name+'.png';im=Image.open(root/f);box=im.getchannel('A').getbbox();assert im.size==(256,256);assert box[0]>0 and box[2]<256 and box[1]>0 and box[3]==240
for name in ['forest-a','forest-b','forest-c','forest-d','forest-e','forest-village','market','village-arena','arena-v63']:
 im=Image.open(root/(name+'.webp'));assert im.size==(1536,864)
print('PASS: elder has bandit-scale height, planted feet and transparent padding; props have clear gutters/ground anchors; all new background dimensions match.')
