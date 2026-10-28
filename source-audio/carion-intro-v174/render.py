from pathlib import Path
from functools import lru_cache
import math,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent;FPS=24;D=34
SCENES=[('village',0,8,1),('warning',8,8,-1),('battle',16,10,1),('arrival',26,8,-1)]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(BOLD,30);tag=ImageFont.truetype(BOLD,18);chapter=ImageFont.truetype(BOLD,29)
LINES=[(.8,4.2,'You broke our chains.'),(4.3,7.7,'Now look—the people are rising.'),(8.6,15.6,'A rebellion is beginning.\nBut Carion City cannot wait.'),(16.6,20.8,'Bandits are ravaging its streets.'),(21,25.7,"They are fighting the Queen’s guard.\nOur rebels are still prisoners."),(26.6,30.8,'Get there quickly. Free our people.'),(31,33.7,'Give this rebellion a fighting chance.')]
@lru_cache(maxsize=4)
def picture(key):
 im=Image.open(W/(key+'.png')).convert('RGB');ratio=max(672/im.width,378/im.height);im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
 x=(im.width-672)//2;y=(im.height-378)//2
 return im.crop((x,y,x+672,y+378))
SHADE=Image.new('RGBA',(1280,720));sd=ImageDraw.Draw(SHADE)
for y in range(584,720):sd.line((0,y,1280,y),fill=(5,10,16,min(205,round((y-584)*1.65))))
def centered(d,text,y,f,color):
 b=d.textbbox((0,0),text,font=f,stroke_width=2);x=round((1280-(b[2]-b[0]))/2)
 d.text((x,y),text,font=f,fill=color,stroke_width=2,stroke_fill=(8,12,16))
def frame(n):
 t=n/FPS;key,start,seconds,direction=next(s for s in SCENES if s[1]<=t<s[1]+s[2]);u=(t-start)/seconds
 # Small whole-pixel camera movement keeps the pixel-art clusters crisp.
 x=16+round(direction*(u-.5)*16);im=picture(key).crop((x,9,x+640,369)).resize((1280,720),Image.Resampling.NEAREST).convert('RGBA')
 text=next((line for a,b,line in LINES if a<=t<b),None)
 if text:
  im=Image.alpha_composite(im,SHADE);d=ImageDraw.Draw(im);centered(d,'REBEL LEADER',603,tag,(195,203,145));rows=text.split('\n');y=664 if len(rows)==1 else 637
  for i,row in enumerate(rows):centered(d,row,y+i*34,font,(241,237,222))
 if t>=31:centered(ImageDraw.Draw(im),'CHAPTER II · CARION CITY',28,chapter,(229,204,153))
 im=im.convert('RGB');local=t-start;fade=min(1,local/.22,(seconds-local)/.22)
 if fade<1:im=Image.blend(Image.new('RGB',im.size),im,max(0,fade))
 return im
if '--stills' in sys.argv:
 contact=Image.new('RGB',(1280,720))
 for i,t in enumerate([5,12,23,32]):contact.paste(frame(t*FPS).resize((640,360),Image.Resampling.NEAREST),((i%2)*640,(i//2)*360))
 contact.save(W/'review.png');print(W/'review.png')
else:
 path=W/'KillQuest-Carion-City-Intro-Cinematic.mp4'
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-','-i',str(W/'score.m4a'),'-c:v','libx264','-profile:v','baseline','-level:v','3.1','-crf','20','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-t',str(D),'-movflags','+faststart','-metadata','title=KillQuest Carion City intro - cinematic preview',str(path)],stdin=subprocess.PIPE)
 try:
  for n in range(FPS*D):p.stdin.write(frame(n).tobytes())
 finally:p.stdin.close()
 if p.wait():raise SystemExit('Encoding failed')
 print(path)
