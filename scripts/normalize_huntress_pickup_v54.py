"""Ground-register Lyra's existing pickup poses without changing their art or scale."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil
root=Path(__file__).resolve().parents[1];out=root/'dist/assets/characters';src=root/'source-art/huntress-pickup-v54';src.mkdir(exist_ok=True)
baseline=int(np.where(np.array(Image.open(out/'huntress-idle-00.png'))[:,:,3]>8)[0].max())
manifest=json.loads((root/'source-art/huntress-registration.json').read_text());rows=[]
preview=Image.new('RGBA',(448*4,448*2),(27,24,34,255));draw=ImageDraw.Draw(preview)
for i in range(8):
 name=f'huntress-pickup-{i:02}';raw=src/(name+'-original.png');dest=out/(name+'.png')
 if not raw.exists():shutil.copy2(dest,raw)
 im=Image.open(raw).convert('RGBA');alpha=np.array(im)[:,:,3];foot=int(np.where(alpha>8)[0].max());shift=baseline-foot
 frame=Image.new('RGBA',(448,448));frame.alpha_composite(im,(0,shift));frame.save(dest)
 # Ground registration supersedes pelvis-centering for this grounded utility action.
 entry=manifest[name];entry.update(ground_anchor=baseline,ground_shift_y=shift,body_anchor=[224,300+shift],registration='grounded pickup',normalization_source=str(raw.relative_to(root)))
 rows.append({'frame':name,'old_foot_y':foot,'new_foot_y':baseline,'shift_y':shift})
 x=i%4*448;y=i//4*448;preview.alpha_composite(frame,(x,y));draw.line((x,y+baseline,x+448,y+baseline),fill='#69caca',width=2);draw.text((x+10,y+10),str(i),fill='white')
(root/'source-art/huntress-registration.json').write_text(json.dumps(manifest,indent=2)+'\n')
(src/'registration.json').write_text(json.dumps(rows,indent=2)+'\n');preview.resize((1344,672)).convert('RGB').save(src/'preview.png')
print('Grounded pickup frames at',baseline,':',[r['shift_y'] for r in rows])
