"""Extract generated Forest atlas cells, preserve alpha and align ground anchors."""
from PIL import Image
from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=root/'source-art/forest-v61/sprites.png'
im=Image.open(src).convert('RGBA')
rows=[(0,330),(330,538),(538,765),(765,1024)]
for row,(top,bottom) in enumerate(rows):
 cells=[]
 for col in range(4):
  cell=im.crop((col*384,top,(col+1)*384,bottom))
  # Ignore barely visible ambient alpha outside the drawn silhouette.
  alpha=cell.getchannel('A');alpha=alpha.point(lambda a:0 if a<16 else a);cell.putalpha(alpha)
  box=alpha.getbbox();cells.append(cell.crop(box))
 factor=(300/max(c.height for c in cells)) if row==0 else (220/max(c.width for c in cells))
 for col,cell in enumerate(cells):
  size=(round(cell.width*factor),round(cell.height*factor));cell=cell.resize(size,Image.Resampling.LANCZOS)
  canvas=Image.new('RGBA',(256,448) if row==0 else (256,256));foot=438 if row==0 else 240
  canvas.alpha_composite(cell,((canvas.width-cell.width)//2,foot-cell.height))
  kind=['elder','stump','sack','basket'][row]
  canvas.save(root/f'dist/assets/forest/{kind}-{col}.png')
# Four-frame symmetric breathing/blink loop, anchored on the same feet.
for i,frame in enumerate([0,1,2,3,2,1,0,3]):
 Image.open(root/f'dist/assets/forest/elder-{frame}.png').save(root/f'dist/assets/forest/elder-loop-{i}.png')
for i in range(8):
 Image.open(root/f'dist/assets/forest/elder-loop-{i}.png').save(root/f'dist/assets/forest/elder-{i}.png')
 (root/f'dist/assets/forest/elder-loop-{i}.png').unlink()
