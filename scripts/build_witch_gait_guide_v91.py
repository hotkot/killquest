from PIL import Image,ImageDraw
from math import pi,cos,sin
out=Image.new('RGB',(448*4,448*3),'#20252c');d=ImageDraw.Draw(out)
for i in range(12):
 ox=(i%4)*448;oy=(i//4)*448;phase=2*pi*i/12
 d.line((ox+224,oy+170,ox+224,oy+285),fill='#9d87aa',width=18);d.ellipse((ox+199,oy+112,ox+249,oy+169),outline='#9d87aa',width=8)
 for offset,color in [(pi,'#00cfff'),(0,'#ff4455')]:
  t=(phase+offset)%(2*pi);ax=224+72*cos(t);ay=408-(max(0,-sin(t))*48)
  hx=224+(7 if offset==0 else -7);kx=(hx+ax)/2+22;ky=(285+ay)/2-8
  d.line((ox+hx,oy+285,ox+kx,oy+ky,ox+ax,oy+ay),fill=color,width=12)
  d.line((ox+ax-6,oy+ay,ox+ax+21,oy+ay),fill=color,width=12)
 d.text((ox+10,oy+10),str(i+1),fill='white');d.line((ox+65,oy+416,ox+382,oy+416),fill='#65707a',width=2)
from pathlib import Path
out.save(Path(__file__).resolve().parents[1]/'source-art/witch-v91/gait-guide.png')
