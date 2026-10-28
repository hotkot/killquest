"""Correct the oversized last walk row against the first twelve poses.

The last row was enlarged from a different source sheet. Calibrate helmet and
shoulder width independently of height; fitting full silhouettes recreates the
wide torso. Register all poses at x=224, sole y=408, retaining leg crossings.
"""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'source-art/garran-walk-v89'
ART=ROOT/'dist/assets/characters'
# v97: source row already has the correct vertical anatomy. Keep only the
# width correction; shortening these poses introduced a 10–18px height dip.
CALIBRATION={12:(.88,1),13:(.90,1),14:(.88,1),15:(.88,1)}
for i,(sx,sy) in CALIBRATION.items():
    name=f'knight-walk-{i:02}.png'
    original=Image.open(OUT/'original'/name).convert('RGBA')
    corrected=original.transform((448,448),Image.Transform.AFFINE,
        (1/sx,0,224-224/sx,0,1/sy,408-408/sy),Image.Resampling.BICUBIC)
    corrected.save(ART/name)
frames=[]
sheet=Image.new('RGB',(8*224,2*260),'#20252c');draw=ImageDraw.Draw(sheet)
for i in range(16):
    im=Image.open(ART/f'knight-walk-{i:02}.png').resize((336,336),Image.Resampling.LANCZOS)
    frame=Image.new('RGB',(336,336),'#20252c');frame.paste(im,(0,0),im)
    frames.append(frame)
    x=(i%8)*224-56;y=(i//8)*260-70
    sheet.paste(im,(x,y),im);draw.text(((i%8)*224+8,(i//8)*260+240),f'walk {i:02}',fill='white')
sheet.save(OUT/'walk-corrected.jpg',quality=94)
frames[0].save(OUT/'walk-corrected.gif',save_all=True,append_images=frames[1:],duration=85,loop=0)
