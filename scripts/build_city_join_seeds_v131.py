from PIL import Image,ImageDraw
from pathlib import Path
root=Path(__file__).resolve().parents[1];keys=['outskirts','outskirts-link','gates','gates-descent','market','market-link','residential','residential-descent','prison','prison-descent','citadel','citadel-link'];w=25600/12;drops=[3,7,9];seeds=[]
for i in range(1,12):
 left=Image.open(root/f'dist/assets/city/{keys[i-1]}.webp').convert('RGB').resize((round(w),1040 if i-1 in drops else 720));right=Image.open(root/f'dist/assets/city/{keys[i]}.webp').convert('RGB').resize((round(w),1040 if i in drops else 720))
 y=320 if i-1 in drops else 0
 seed=Image.new('RGB',(768,720));seed.paste(left.crop((left.width-384,y,left.width,y+720)),(0,0));seed.paste(right.crop((0,0,384,720)),(384,0));seed.save(root/f'source-art/carion-route-v131/join-seeds/join-{i:02}.png');seeds.append(seed.resize((256,240)))
preview=Image.new('RGB',(256*3,260*4))
for i,im in enumerate(seeds):preview.paste(im,((i%3)*256,(i//3)*260));ImageDraw.Draw(preview).text(((i%3)*256+5,(i//3)*260+240),str(i+1),fill='white')
preview.save(root/'source-art/carion-route-v131/join-seeds/preview.jpg')
