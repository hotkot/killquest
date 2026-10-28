from pathlib import Path
from PIL import Image
import numpy as np,json
from scipy.ndimage import label,find_objects
root=Path(__file__).resolve().parents[1];im=Image.open(root/'source-art/hero-rage-v23.png').convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>8);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-12:],key=lambda k:(boxes[k-1][0].start//360,boxes[k-1][1].start))
pts=[(285,256),(658,257),(954,300),(1290,247),(284,620),(607,596),(963,642),(1287,635),(185,1010),(578,1005),(986,941),(1280,937)];frames=[]
for k,(cx,cy) in zip(ids,pts):
 arr=a.copy();arr[:,:,3][labs!=k]=0;cut=Image.fromarray(arr);box=cut.getbbox();cut=cut.crop(box);scale=.74;cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((cx-box[0])*scale),300-round((cy-box[1])*scale)));frames.append(frame)
# Preserve complete axes for source poses touching the generated sheet edge.
frames[2]=Image.open(root/'source-art/rage-reference-02.png').convert('RGBA');frames[3]=frames[4].copy();frames[7]=Image.open(root/'source-art/rage-reference-03.png').convert('RGBA');frames[11]=Image.open(root/'dist/assets/characters/base-00.png').convert('RGBA')
for i,frame in enumerate(frames):frame.save(root/f'source-art/uncentered/hero-rage-{i:02}.png')
p=root/'source-art/action-anchors.json';anchors=json.loads(p.read_text());anchors['hero-rage']=[[224,300]]*12;p.write_text(json.dumps(anchors,indent=2)+'\n')
im=Image.open(root/'source-art/arrow-v23.png').convert('RGBA');box=im.getchannel('A').point(lambda x:255 if x>8 else 0).getbbox();im=im.crop(box);im.thumbnail((320,64),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(336,80));frame.alpha_composite(im,((336-im.width)//2,(80-im.height)//2));frame.save(root/'dist/assets/arrow.png')
