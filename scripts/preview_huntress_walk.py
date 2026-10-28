from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];frames=[]
for i in range(8):
 sprite=Image.open(root/f'dist/assets/characters/huntress-walk-{i:02}.png').convert('RGBA').resize((376,376),Image.Resampling.LANCZOS)
 canvas=Image.new('RGBA',(420,400),(24,31,39,255));d=ImageDraw.Draw(canvas);d.line((20,363,400,363),fill=(73,87,88));canvas.alpha_composite(sprite,(22,20));frames.append(canvas.convert('RGB'))
frames[0].save(root/'source-art/huntress-walk-game-scale-v43.gif',save_all=True,append_images=frames[1:],duration=85,loop=0)
print('Wrote .84-scale walk preview')
