"""Slice generated NPC/prop atlases, preserving alpha and stable ground anchors."""
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
out=root/'dist/assets/forest'
im=Image.open(root/'source-art/forest-v63/elder.png').convert('RGBA')
cells=[]
for i in range(4):
 cell=im.crop((i*im.width//4,0,(i+1)*im.width//4,im.height));alpha=cell.getchannel('A').point(lambda a:0 if a<16 else a);cell.putalpha(alpha);cells.append(cell.crop(alpha.getbbox()))
factor=300/max(c.height for c in cells)
frames=[]
for cell in cells:
 cell=cell.resize((round(cell.width*factor),round(cell.height*factor)),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(256,448));canvas.alpha_composite(cell,((256-cell.width)//2,438-cell.height));frames.append(canvas)
for i,j in enumerate([0,1,2,3,2,1,0,1]):frames[j].save(out/f'elder-{i}.png')
im=Image.open(root/'source-art/forest-v63/props.png').convert('RGBA')
# Generated artwork extends slightly beyond a nominal grid; use inspected gutters.
rows=[([(0,475),(475,895),(895,1350),(1350,im.width)],0,466), ([(0,463),(463,892),(892,1340),(1340,im.width)],466,im.height)]
for row,(columns,t,b) in enumerate(rows):
 cells=[]
 for l,r in columns:
  cell=im.crop((l,t,r,b));alpha=cell.getchannel('A').point(lambda a:0 if a<16 else a);cell.putalpha(alpha);cells.append(cell.crop(alpha.getbbox()))
 factor=220/max(c.width for c in cells)
 for i,cell in enumerate(cells):
  cell=cell.resize((round(cell.width*factor),round(cell.height*factor)),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(cell,((256-cell.width)//2,240-cell.height));canvas.save(out/(f'prop-{["stall","rock","cart","well"][i]}.png' if row==0 else f'barricade-{i}.png'))
