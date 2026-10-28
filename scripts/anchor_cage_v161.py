from pathlib import Path
from PIL import Image
import io,json,subprocess
root=Path(__file__).resolve().parents[1];baseline='a07f183f79c8453737153eef005a83213dc7b738';target=(239,448)
# Front platform landmark: stable ground pivot, independent of flying splinters.
landmarks={4:(239,420),5:(239,420),6:(197,439),7:(208,440),8:(198,430),9:(196,430),10:(220,430),11:(220,430)}
report=[]
for i,anchor in landmarks.items():
 im=Image.open(io.BytesIO(subprocess.check_output(['git','show',f'{baseline}:dist/assets/items/prison-cage-{i:02}.png'],cwd=root))).convert('RGBA');scale=1 if i<6 else .87;offset=(round(target[0]-anchor[0]*scale),round(target[1]-anchor[1]*scale));im=im.resize((round(512*scale),round(512*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(512,512));out.paste(im,offset);out.save(root/f'dist/assets/items/prison-cage-{i:02}.png');report.append({'frame':i,'source_anchor':anchor,'scale':scale,'offset':offset,'target_anchor':target})
(root/'source-art/cage-v161/anchors.json').write_text(json.dumps(report,indent=2))
# Fixed-position comparison at actual game scale.
board=Image.new('RGB',(1360,760),'#514947')
from PIL import ImageDraw
d=ImageDraw.Draw(board)
for j,i in enumerate([0,4,6,7,8,9,10,11]):
 im=Image.open(root/f'dist/assets/items/prison-cage-{i:02}.png').resize((340,340));x=j%4*340;y=j//4*380;board.paste(im,(x,y+20),im);d.text((x+8,y+8),str(i),fill='white');ax=x+239*340/512;ay=y+20+448*340/512;d.line((ax-6,ay,ax+6,ay),fill='red');d.line((ax,ay-6,ax,ay+6),fill='red')
board.save(root/'source-art/cage-v161/anchored-preview.png')
