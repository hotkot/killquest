from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label,find_objects
root=Path(__file__).resolve().parents[1]
specs={
'hero-grapple':('hero-grapple-v24.png',.55,[(180,269),(576,269),(1000,270),(1370,332),(252,756),(635,768),(1028,756),(1396,732)]),
'bandit-dagger-grapple':('bandit-dagger-grapple-v24.png',.58,[(256,255),(687,254),(1096,250),(1530,278),(229,669),(627,710),(1024,757),(1515,784)]),
'bandit-sword-grapple':('bandit-sword-grapple-v24.png',.54,[(280,226),(693,228),(1100,247),(1548,301),(242,660),(626,694),(1036,758),(1514,760)]),
'bandit-archer-grapple':('bandit-archer-grapple-v24.png',.52,[(221,261),(609,279),(913,237),(1354,256),(212,777),(570,820),(900,856),(1322,878)])}
p=root/'source-art/action-anchors.json';anchors=json.loads(p.read_text())
for clip,(file,scale,pts) in specs.items():
 im=Image.open(root/'source-art'/file).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-8:],key=lambda k:((boxes[k-1][0].start+boxes[k-1][0].stop)/2>=im.height/2,boxes[k-1][1].start))
 for i,(k,(cx,cy)) in enumerate(zip(ids,pts)):
  arr=a.copy();arr[:,:,3][labs!=k]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));dx=224-round((cx-box[0])*scale);dy=300-round((cy-box[1])*scale)
  if clip.startswith('bandit-') and i>=6:dy=408-cut.height
  frame.alpha_composite(cut,(dx,dy))
  if clip=='hero-grapple' and i==7:frame=Image.open(root/'dist/assets/characters/base-00.png').convert('RGBA')
  frame.save(root/f'source-art/uncentered/{clip}-{i:02}.png')
 anchors[clip]=[[224,300]]*8
p.write_text(json.dumps(anchors,indent=2)+'\n')
