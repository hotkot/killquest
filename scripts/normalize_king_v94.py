"""Calibrate King anatomy against idle, never weapon or crouched silhouette bounds.
Re-runnable from immutable shipped originals; all transforms share the foot pivot.
"""
from pathlib import Path
import json,shutil,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'source-art/king-scale-v94'; SRC=ART/'original'; DST=ROOT/'dist/assets/characters'
FACTORS={'idle':[1]*6,'walk':[1]*8,'sweep':[.80,.80,.79,.80,.80,.84,.79,.78],'slam':[1]*8,'charge':[.76,.77,.76,.78,.78,.85],'roar':[1]*6,'death':[1]*6}
def main():
 SRC.mkdir(parents=True,exist_ok=True); report={}; rows=[]
 for clip,scales in FACTORS.items():
  for n,scale in enumerate(scales):
   name=f'king-{clip}-{n:02}.png'; original=SRC/name
   if not original.exists():shutil.copy2(DST/name,original)
   im=Image.open(original).convert('RGBA')
   if scale==1:out=im.copy()
   else:
    small=im.resize((round(640*scale),round(512*scale)),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(640,512));out.alpha_composite(small,(round(320*(1-scale)),round(466*(1-scale))))
   out.save(DST/name)
   bounds=out.getchannel('A').point(lambda a:255 if a>32 else 0).getbbox()
   assert bounds and bounds[0]>1 and bounds[1]>1 and bounds[2]<639 and bounds[3]<=468,(name,bounds)
   report[name]={'scale':scale,'pivot':[320,466],'bounds':bounds,'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest()}
   rows.append((name,im,out))
 (ART/'normalization.json').write_text(json.dumps(report,indent=2)+'\n')
 for side,idx in [('before',1),('after',2)]:
  sheet=Image.new('RGB',(8*256,6*225),(29,31,36));draw=ImageDraw.Draw(sheet)
  for i,item in enumerate(rows):
   x=i%8*256;y=i//8*225;pic=item[idx].resize((256,205),Image.Resampling.LANCZOS)
   sheet.paste(pic,(x,y),pic);draw.text((x+5,y+207),item[0],fill='white')
  sheet.save(ART/f'{side}.jpg',quality=92)
 print(f'Checked {len(rows)} King frames; corrected oversized sweep and charge anatomy.')
if __name__=='__main__':main()
