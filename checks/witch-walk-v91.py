"""Verify the traced gait's foot order and the final art's preserved geometry."""
from pathlib import Path
from PIL import Image
import numpy as np,json
root=Path(__file__).resolve().parents[1];src=root/'source-art/witch-v91'
guide=Image.open(src/'gait-checked.png').convert('RGBA');final=Image.open(src/'walk-raw.png').convert('RGBA').resize(guide.size)
w,h=guide.size;delta=[];overlap=[]
for i in range(12):
 box=(round(i%4*w/4),round(i//4*h/3),round((i%4+1)*w/4),round((i//4+1)*h/3));a=np.array(guide.crop(box)).astype(float);b=np.array(final.crop(box))
 r,g,blue=a[:,:,:3].transpose(2,0,1);yy,xx=np.mgrid[:a.shape[0],:a.shape[1]];lower=yy>a.shape[0]*.57;leg=lower&(a[:,:,3]>120)
 near=leg&(r>150)&(r>g*2)&(r>blue*1.4);far=leg&(g>100)&(blue>140)&(r<g*.6)
 delta.append(float(np.mean(xx[near])-np.mean(xx[far])))
 old=lower&(a[:,:,3]>120);new=lower&(b[:,:,3]>120);iou=np.count_nonzero(old&new)/np.count_nonzero(old|new);overlap.append(iou);assert iou>.70,(i,iou,'recolor changed foot geometry')
assert delta[0]>80 and delta[6]<-80,'opposite footfall order'
assert abs(delta[3])<30 and abs(delta[9])<30,'both passing poses overlap'
assert max(delta)-min(delta)>200,'full stride through both halves'
reg=json.loads((root/'source-art/witch-v90/registration.json').read_text())
assert len({reg[f'witch-walk-{i:02}']['scale'] for i in range(12)})==1,'per-frame scale drift'
# Unrelated poses must remain byte-for-byte unchanged from before the revision.
import hashlib
for name,digest in json.loads((src/'unchanged-poses.json').read_text()).items():
 assert hashlib.sha256((root/'dist/assets/characters'/name).read_bytes()).hexdigest()==digest,name+' changed unexpectedly'
print(f'PASS: opposite footfalls, both passing poses, full stride, final leg geometry (minimum IoU {min(overlap):.2f}), one shared walk scale, all unrelated witch poses unchanged.')
