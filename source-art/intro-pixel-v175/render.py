from pathlib import Path
from functools import lru_cache
import subprocess,sys
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent;FPS=24
MODE=sys.argv[1];D=44.25 if MODE=='story' else 20
SCENES=([('queen',0,8.625,1),('captives',8.625,8.5,-1),('kael-lyra',17.125,12.1666667,1),('garran-selene',29.2916667,14.9583333,-1)] if MODE=='story' else [('forest-path',0,5,1),('forest-cart',5,4,-1),('captives',9,6,1),('bandit-king',15,5,-1)])
LINES=([(0.2,8.4,'Queen Morvane would raise her dead kingdom.\nAnd the living would pay the price.'),(8.8,16.9,'Through the forest, her bandits hunt for souls.\nSouls to feed the rite.'),(17.3,21.2,'But four survivors follow their trail.'),(21.3,24.6,'An axe sworn to vengeance.'),(24.7,29.1,'A huntress who will not abandon her people.'),(29.5,33.1,'A shield against the darkness.'),(33.2,40.1,'And a flame to burn the dead queen’s dream to ash.'),(41,44.1,'STEEL · BLOOD · VENGEANCE')] if MODE=='story' else [(.6,4.5,'Beyond the trees… smoke stained the sky.'),(5.6,8.5,'The raiders had left a trail.'),(9.6,14.5,'They took the living. They burned the rest.'),(15.6,19.6,'At the village’s heart… their king waited.')])
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
@lru_cache(None)
def picture(key):
 im=Image.open(W/'art'/(key+'.png')).convert('RGB');r=max(672/im.width,378/im.height);im=im.resize((round(im.width*r),round(im.height*r)),Image.Resampling.LANCZOS);x=(im.width-672)//2;y=(im.height-378)//2;return im.crop((x,y,x+672,y+378))
shade=Image.new('RGBA',(1280,720));sd=ImageDraw.Draw(shade)
for y in range(585,720):sd.line((0,y,1280,y),fill=(5,9,15,min(205,round((y-585)*1.65))))
logo=Image.open(str(W.parents[1]/'dist/assets/ui/killquest-logo.png')).convert('RGBA');logo.thumbnail((850,350),Image.Resampling.LANCZOS)
def frame(n):
 t=n/FPS;key,start,seconds,direction=next(s for s in SCENES if s[1]<=t<s[1]+s[2]+.00001);u=(t-start)/seconds;x=16+round(direction*(u-.5)*16)
 im=picture(key).crop((x,9,x+640,369)).resize((1280,720),Image.Resampling.NEAREST).convert('RGBA')
 if MODE=='story' and t>=40.25:
  a=min(1,(t-40.25)/.35);im=Image.blend(im,Image.new('RGBA',im.size,(5,8,13,255)),.62*a)
  layer=Image.new('RGBA',im.size);layer.alpha_composite(logo,((1280-logo.width)//2,round((720-logo.height)/2-40)));layer.putalpha(layer.getchannel('A').point(lambda v:round(v*a)));im=Image.alpha_composite(im,layer)
 text=next((s for a,b,s in LINES if a<=t<b),None)
 if text:
  im=Image.alpha_composite(im,shade);d=ImageDraw.Draw(im);rows=text.split('\n');y=661 if len(rows)==1 else 626
  for i,row in enumerate(rows):
   box=d.textbbox((0,0),row,font=font,stroke_width=2);x=round((1280-(box[2]-box[0]))/2);d.text((x,y+i*35),row,font=font,fill=(241,237,222),stroke_width=2,stroke_fill=(8,12,16))
 im=im.convert('RGB');local=t-start;fade=min(1,local/.22,(seconds-local)/.22,(D-t)/.35)
 if fade<1:im=Image.blend(Image.new('RGB',im.size),im,max(0,fade))
 return im
if '--stills' in sys.argv:
 times=[4,12,24,35] if MODE=='story' else [3,7,12,17];out=Image.new('RGB',(1280,720))
 for i,t in enumerate(times):out.paste(frame(round(t*FPS)).resize((640,360),Image.Resampling.NEAREST),((i%2)*640,(i//2)*360))
 out.save(W/MODE/'review.png');print(W/MODE/'review.png')
else:
 path=W/MODE/('KillQuest-New-Game-Intro.mp4' if MODE=='story' else 'KillQuest-Forest-Intro.mp4')
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(W/MODE/'score.m4a'),'-c:v','libx264','-profile:v','baseline','-level:v','3.1','-crf','20','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-t',str(D),'-movflags','+faststart',str(path)],stdin=subprocess.PIPE)
 try:
  for n in range(round(FPS*D)):p.stdin.write(frame(n).tobytes())
 finally:p.stdin.close()
 if p.wait():raise SystemExit('Encoding failed')
 print(path)
