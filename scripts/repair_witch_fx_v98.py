"""Repair cropped cast effects only. Original character pixels remain registered.
Generated sheet supplies completed magic, never replacement character anatomy.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,re
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'source-art/witch-fx-v98';DST=ROOT/'dist/assets/characters'
CONFIG={
 'witch-air-cast-03':((307,270,448,410),(390,300,580,450),(467,273),1),
 'witch-cast2-03':((310,140,448,280),(1045,190,1255,320),(470,158),1),
 'witch-cast3-02':((350,170,448,320),(315,710,640,850),(500,166),.7),
 'witch-rage-02':((320,165,448,330),(1000,695,1260,900),(440,151),1),
}
def blue(a):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
 return ((b>r*1.2)&(b>g*.85))|((b>200)&(g>180)&(r>150))
def main():
 sheet=Image.open(SRC/'repaired-sheet.png').convert('RGBA').resize((1280,1024),Image.Resampling.LANCZOS);report={};previews=[]
 for key,(region,crop,pos,sx) in CONFIG.items():
  original=Image.open(SRC/(key+'-before.png')).convert('RGBA');a=np.array(original);l,t,r,b=region
  roi=np.zeros(a.shape[:2],bool);roi[t:b,l:r]=True
  # These ROIs lie beyond her body. Keep brown/gold staff and skin intact.
  removed=roi&blue(a);a[:,:,3][removed]=0
  magic=np.array(sheet.crop(crop));magic[:,:,3][~blue(magic)]=0;fx=Image.fromarray(magic)
  if sx!=1:fx=fx.resize((round(fx.width*sx),fx.height),Image.Resampling.LANCZOS)
  out=Image.new('RGBA',(768,448));out.alpha_composite(Image.fromarray(a),(160,0));out.alpha_composite(fx,pos)
  # Restore every original non-effect pixel over the effect layer.
  body=np.array(original);body[:,:,3][removed]=0;out.alpha_composite(Image.fromarray(body),(160,0))
  out.save(DST/(key+'.png'));report[key]={'canvas':[768,448],'body_offset':[160,0],'original_effect_roi':region,'generated_crop':crop,'effect_position':pos,'effect_width_scale':sx}
  previews.append((key,out))
 (SRC/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
 preview=Image.new('RGB',(1536,2*480),'#20252c');d=ImageDraw.Draw(preview)
 for i,(key,out) in enumerate(previews):
  x=i%2*768;y=i//2*480;preview.paste(out,(x,y),out);d.text((x+10,y+450),key,fill='white')
 preview.save(SRC/'repaired-preview.jpg',quality=95)
 p=ROOT/'dist/game.js';s=p.read_text()
 for key in CONFIG:
  s=re.sub(r'"'+key+r'":\[1\.0,408,448\]',f'"{key}":[1.0,408,768]',s)
 p.write_text(s)
 print('Repaired four clipped magic poses; retained original bodies at identical scale and y408 ground pivot.')
if __name__=='__main__':main()
