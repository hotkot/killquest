"""Register artist-identified pelvis landmarks to one fixed body anchor."""
from PIL import Image,ImageDraw
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];src=root/'source-art/uncentered';out=root/'dist/assets/characters'
anchors={
'hero-attack':[(125,204),(142,199),(132,202),(96,199),(129,196),(123,201),(94,227),(124,211),(126,202),(124,201),(122,202),(128,209),(125,208),(130,208),(132,192),(140,222),(149,231),(124,207)],
'bandit-attack':[(135,198),(131,205),(133,226),(140,218),(120,215),(116,215),(167,207),(160,211)],
'base':[(130,201),(132,201),(140,199),(166,198),(173,243),(164,187),(203,249),(174,229),(184,234),(211,230),(192,239),(203,232),(214,246),(231,239),(181,237),(209,233),(202,244),(203,232),(132,206),(130,205),(172,208),(158,213),(189,213),(168,203)]}
# New walk landmarks are added after reviewing the generated cycles.
extra=root/'source-art/walk-anchors.json'
if extra.exists():anchors.update(json.loads(extra.read_text()))
anchors.pop('hero-attack',None);anchors.pop('bandit-attack',None)
anchors.update(json.loads((root/'source-art/action-anchors.json').read_text()))
metadata={}
for clip,points in anchors.items():
 for i,(cx,cy) in enumerate(points):
  name=f'{clip}-{i:02}';im=Image.open(src/f'{name}.png').convert('RGBA');frame=Image.new('RGBA',(448,448));target_y=cy+100 if clip=='hero-slide' else 300;dx,dy=224-cx,target_y-cy
  frame.alpha_composite(im,(dx,dy));frame.save(out/f'{name}.png')
  metadata[name]={'source_anchor':[cx,cy],'body_anchor':[224,target_y],'translation':[dx,dy]}
 cols=6 if clip in ['hero-attack','base'] else 4;rows=(len(points)+cols-1)//cols
 sheet=Image.new('RGBA',(448*cols,448*rows),(27,35,43,255));d=ImageDraw.Draw(sheet)
 for i in range(len(points)):
  x=i%cols*448;y=i//cols*448;sheet.alpha_composite(Image.open(out/f'{clip}-{i:02}.png'),(x,y));d.line((x+224,y+20,x+224,y+430),fill=(100,130,145));d.line((x+20,y+300,x+428,y+300),fill=(100,130,145))
 sheet.convert('RGB').save(out/f'{clip}-preview.jpg')
(root/'source-art/registration.json').write_text(json.dumps(metadata,indent=2))
print('Registered',len(metadata),'frames to fixed (224,300) body center.')
