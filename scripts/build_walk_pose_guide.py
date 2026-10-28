from PIL import Image,ImageDraw
from pathlib import Path
import math
im=Image.new('RGB',(1280,1280),(245,245,240));d=ImageDraw.Draw(im)
for i in range(16):
 ox=(i%4)*320;oy=(i//4)*320;cx=ox+150;hy=oy+175;ground=oy+285
 phase=i/16
 if phase<.5:nx=40-160*phase;ny=0;fx=-40+160*phase;fy=16*math.sin(phase*2*math.pi)
 else:nx=-40+160*(phase-.5);ny=16*math.sin((phase-.5)*2*math.pi);fx=40-160*(phase-.5);fy=0
 d.rectangle((cx-25,oy+75,cx+25,hy),fill=(155,155,155));d.ellipse((cx-17,oy+34,cx+17,oy+68),fill=(155,155,155));d.line((ox+45,ground,ox+270,ground),fill=(90,90,90),width=2)
 for hx,dx,lift,col in [(cx-6,fx,fy,(35,100,210)),(cx+6,nx,ny,(210,45,45))]:
  ax=cx+dx;ay=ground-8-lift;vx=ax-hx;vy=ay-hy;dist=math.hypot(vx,vy);midX=(ax+hx)/2;midY=(ay+hy)/2;bend=math.sqrt(max(0,57**2-(dist/2)**2));kx=midX+vy/dist*bend;ky=midY-vx/dist*bend
  d.line((hx,hy,kx,ky,ax,ay),fill=col,width=10);d.line((ax-6,ay+6,ax+18,ay+6),fill=col,width=9)
 d.text((ox+10,oy+8),str(i+1),fill=(0,0,0))
im.save(Path(__file__).resolve().parents[1]/'source-art/walk-pose-guide-v30.png')
