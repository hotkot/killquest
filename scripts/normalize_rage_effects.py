from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];out=root/'dist/assets/effects';out.mkdir(exist_ok=True)
im=Image.open(root/'source-art/rage-blast-v27.png').convert('RGBA');pts=[(174,380),(588,380),(1007,380),(1505,380),(207,823),(652,823),(1110,823),(1540,823)]
for i,(cx,cy) in enumerate(pts):
 bounds=[0,366,768,1240,1774] if i<4 else [0,470,915,1335,1774];x=bounds[i%4];y=0 if i<4 else 445;cut=im.crop((x,y,bounds[i%4+1],445 if i<4 else 887));box=cut.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox();cut=cut.crop(box);scale=.62;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(512,384));frame.alpha_composite(cut,(256-round((cx-x-box[0])*scale),307-round((cy-y-box[1])*scale)));frame.save(out/f'rage-blast-{i:02}.png')
im=Image.open(root/'source-art/rage-particles-v27.png').convert('RGBA')
for i in range(8):
 x=round(i%4*im.width/4);y=round(i//4*im.height/2);cut=im.crop((x,y,round((i%4+1)*im.width/4),round((i//4+1)*im.height/2)));box=cut.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox();cut=cut.crop(box);cut.thumbnail((80,80),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(96,96));frame.alpha_composite(cut,((96-cut.width)//2,(96-cut.height)//2));frame.save(out/f'rage-particle-{i:02}.png')
preview=Image.new('RGBA',(512*4,384*2),(25,30,38,255))
for i in range(8):preview.alpha_composite(Image.open(out/f'rage-blast-{i:02}.png'),((i%4)*512,(i//4)*384))
preview.convert('RGB').save(root/'source-art/rage-blast-preview.jpg')
