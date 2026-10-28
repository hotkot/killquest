"""Offline artwork registration review. Metadata exported from actual game model."""
import json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
D=json.loads(subprocess.check_output(['node','scripts/export_city_pavement_v132.cjs'],cwd=R))
temp=tempfile.TemporaryDirectory();work=Path(temp.name)
# Half world scale keeps the 25,600 x 1,680 canvas manageable.
world=Image.new('RGB',(12800,840),'#34323b')
for t in D['layout']:
 im=Image.open(R/'dist/assets/city'/f"{t['key']}.webp").resize((1067,round(t['height']/2)))
 world.paste(im,(round(t['x']/2),round(t['y']/2)))
for i in range(1,12):
 left,right=D['layout'][i-1:i+1]
 ref=Image.new('RGBA',(768,720))
 for t,source_x,offset in [(left,left['width']-384,0),(right,0,384)]:
  src=Image.open(R/'dist/assets/city'/f"{t['key']}.webp").convert('RGBA')
  sx=src.width/t['width'];sy=src.height/t['height'];y=320 if t['descent'] and offset==0 else 0
  crop=src.crop((round(source_x*sx),round(y*sy),round((source_x+384)*sx),round((y+720)*sy))).resize((384,720))
  ref.paste(crop,(offset,0))
 gen=Image.open(R/'dist/assets/city'/f'join-{i:02}.webp').convert('RGBA').resize((768,720))
 (work/'gen').write_bytes(gen.tobytes());(work/'ref').write_bytes(ref.tobytes())
 subprocess.run(['node','-e',"const fs=require('fs'),fit=require('./dist/city-join-fit.js');fs.writeFileSync(process.argv[3],fit.fit(fs.readFileSync(process.argv[1]),fs.readFileSync(process.argv[2]),768,720));",str(work/'gen'),str(work/'ref'),str(work/'out')],cwd=R,check=True)
 im=Image.frombytes('RGBA',(768,720),(work/'out').read_bytes()).convert('RGB').resize((384,360))
 world.paste(im,(round(right['x']/2)-192,round(right['y']/2)))
for c in D['props']:
 kind=c['kind'];p=R/'dist/assets'
 if c.get('indestructible'):p=p/'forest'/f'prop-{kind}.png'
 elif kind in ['basket','sack','barricade']:p=p/'forest'/f'{kind}-0.png'
 else:p=p/'items'/f"container-{0 if kind=='barrel' else 4}.png"
 if not p.exists():
  p=next((R/'dist/assets/items').glob(f"container*{0 if kind=='barrel' else 4}*.png"))
 im=Image.open(p).convert('RGBA');size=round(c.get('size',128)/2);im=im.resize((size,size))
 world.paste(im,(round(c['x']/2-size/2),round(c['y']/2-size*240/256)),im)
d=ImageDraw.Draw(world)
for edge,color in [(1,'#00ffff'),(2,'#ffcc00')]:d.line([(round(p[0]/2),round(p[edge]/2)) for p in D['edges']],fill=color,width=2)
for c in D['props']:
 x,y=c['x']/2,c['y']/2;w=c.get('halfW',54 if c['kind']=='barrel' else 60)/2;top=c.get('top',38)/2;b=c.get('bottom',20)/2
 d.rectangle((x-w,y-top,x+w,y+b),outline='#ff66ff',width=1)
# Each panel includes its joins and every prop; rows follow vertical camera offset.
out=Image.new('RGB',(1280,12*430),'#171721');od=ImageDraw.Draw(out)
for i,t in enumerate(D['layout']):
 x=max(0,min(11520,round(t['x']/2)-105));y=min(480,max(0,round(t['y']/2)))
 out.paste(world.crop((x,y,x+1280,y+420)),(0,i*430));od.text((8,i*430+5),f"{i+1}: {t['key']} | cyan rear curb / yellow foreground / magenta prop footprint",fill='white')
out.save(R/'source-art/carion-route-v132/pavement-and-props.jpg',quality=90)
