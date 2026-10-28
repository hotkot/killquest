from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,re
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1];folder=root/'source-art/garran-walk-v145';art=root/'dist/assets/characters'
a=np.array(Image.open(folder/'sheet.png').convert('RGBA'));labs,n=label(a[:,:,3]>100);sizes=np.bincount(labs.ravel());sizes[0]=0;boxes=find_objects(labs);ids=sorted(np.argsort(sizes)[-8:],key=lambda k:(boxes[k-1][0].start+boxes[k-1][0].stop)/2);ordered=[]
for row in range(2):ordered.extend(sorted(ids[row*4:(row+1)*4],key=lambda k:boxes[k-1][1].start))
heights=[boxes[k-1][0].stop-boxes[k-1][0].start for k in ordered];scale=234/np.median(heights)
def helmet_center(arr):
 yy,xx=np.mgrid[:arr.shape[0],:arr.shape[1]];rgb=arr[:,:,:3].astype(float);mask=(arr[:,:,3]>100)&(yy>arr.shape[0]*.12)&(yy<arr.shape[0]*.28)&(xx>arr.shape[1]*.35)&(xx<arr.shape[1]*.83)&((rgb.max(2)-rgb.min(2))<32)&(rgb.mean(2)>90)
 return np.median(xx[mask])
reference=np.array(Image.open(art/'knight-walk-00.png').convert('RGBA'));refbox=Image.fromarray(reference).getbbox();target_head=refbox[0]+helmet_center(reference[refbox[1]:refbox[3],refbox[0]:refbox[2]])
frames=[];report=[]
for i,k in enumerate(ordered):
 mask=(labs==k)|(binary_dilation(labs==k,iterations=2)&(labs==0));arr=a.copy();arr[~mask]=0;im=Image.fromarray(arr);box=im.getbbox();cut=im.crop(box);head=helmet_center(np.array(cut));cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);f=Image.new('RGBA',(448,448));f.alpha_composite(cut,(round(target_head-head*scale),408-cut.height));b=f.getbbox();assert b[0]>3 and b[2]<445 and b[1]>3 and b[3]==408,(i,b);f.save(art/f'knight-walk-{i:02}.png');frames.append(f);report.append({'frame':i,'bounds':b,'scale':scale,'helmet_x':target_head,'sole_y':408})
preview=Image.new('RGB',(4*280,2*290),(38,35,43));d=ImageDraw.Draw(preview);gifs=[]
for i,f in enumerate(frames):
 image=f.resize((336,336),Image.Resampling.LANCZOS);bg=Image.new('RGB',(336,336),(38,35,43));bg.paste(image,(0,0),image);gifs.append(bg);cropped=f.crop((90,150,360,420)).resize((270,270),Image.Resampling.LANCZOS);preview.paste(cropped,((i%4)*280,(i//4)*290),cropped);d.text(((i%4)*280+5,(i//4)*290+274),['CONTACT','WEIGHT','CROSS','LIFT','CONTACT','WEIGHT','CROSS','LIFT'][i],fill='white')
preview.save(folder/'preview.jpg');gifs[0].save(folder/'walk.gif',save_all=True,append_images=gifs[1:],duration=[150,125,105,125]*2,loop=0)
(folder/'normalization.json').write_text(json.dumps(report,indent=2))
# Keep source layout/audit synchronized with the now-eight-frame clip.
p=root/'source-art/player-scale-v86/normalization.json';audit=json.loads(p.read_text())
for i in range(16):
 key=f'knight-walk-{i:02}'
 if i>=8:audit['frames'].pop(key,None);continue
 rec=audit['frames'][key];sha=hashlib.sha256((art/(key+'.png')).read_bytes()).hexdigest();rec.update(sha256=sha,artwork=sha,sole_y=408,origin_y=408,factor=1.0,body_area=int((np.array(frames[i])[:,:,3]>100).sum()))
p.write_text(json.dumps(audit,indent=2))
p=root/'dist/game.js';s=p.read_text();match=re.search(r'const PLAYER_FRAME_LAYOUT=(\{.*?\});',s);layout=json.loads(match.group(1))
for i in range(8,16):layout.pop(f'knight-walk-{i:02}',None)
s=s[:match.start(1)]+json.dumps(layout,separators=(',',':'))+s[match.end(1):];p.write_text(s)
print('8 frames; shared scale',round(scale,4),'helmet x',target_head,'heights',heights,'sole408; audit/layout535frames')
