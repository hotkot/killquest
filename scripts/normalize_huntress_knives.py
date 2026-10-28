"""Register the simple v44 knife chain; lock the two handoff poses exactly."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json,shutil
root=Path(__file__).resolve().parents[1];src=root/'source-art';out=root/'dist/assets/characters'
raw=Path('/workspace/scratch/e77afc5b40f4/generated_images/exec-fd824bc8-f50b-494f-b10d-4fd7947ad958.png');dest=src/'huntress-knives-v44.png'
if raw.exists():shutil.copy(raw,dest)
a=np.array(Image.open(dest).convert('RGBA'));labs,n=label(a[:,:,3]>80);sizes=np.bincount(labs.ravel());boxes=find_objects(labs)
ids=[k for k in range(1,n+1) if sizes[k]>10000];rows=[[],[],[]]
for k in ids:
 y,x=boxes[k-1];cy=(y.start+y.stop)/2;rows[0 if cy<270 else 1 if cy<525 else 2].append(k)
assert all(len(row)==8 for row in rows)
centers=[[150,400,651,905,1158,1416,1658,1917],[150,401,646,894,1157,1406,1657,1915],[142,398,646,900,1156,1418,1670,1920]]
baseline=int(np.where(np.array(Image.open(out/'huntress-idle-00.png'))[:,:,3]>8)[0].max());scale=.98;manifest=json.loads((src/'huntress-registration.json').read_text())
for r,clip in enumerate(['slash','rise','finisher']):
 for i,k in enumerate(sorted(rows[r],key=lambda k:boxes[k-1][1].start)):
  mask=binary_dilation(labs==k,iterations=2);clean=a.copy();clean[:,:,3][~mask]=0;cut=Image.fromarray(clean);box=cut.getbbox();cut=cut.crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
  foot=int(np.where(np.array(cut)[:,:,3]>8)[0].max());frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(224-round((centers[r][i]-box[0])*scale),baseline-foot));name=f'huntress-{clip}-{i:02}';frame.save(out/f'{name}.png')
  manifest[name]={'source':dest.name,'component':int(k),'anchor':[centers[r][i],box[1]+foot/scale-(baseline-300)/scale],'scale':scale,'body_anchor':[224,300],'ground_anchor':baseline,'action':['horizontal slash','diagonal cut','forward thrust'][r]}
# Start/finish ready pose and exact row-to-row handoffs. The raw sheet's last
# diagonal-cut cell touches the canvas edge, so use the complete next load pose.
for target,origin in [('slash-00','idle-00'),('rise-00','slash-07'),('rise-07','finisher-00'),('finisher-07','idle-00')]:
 shutil.copy(out/f'huntress-{origin}.png',out/f'huntress-{target}.png');manifest['huntress-'+target]['locked_to']='huntress-'+origin
(src/'huntress-registration.json').write_text(json.dumps(manifest,indent=2))
sheet=Image.new('RGBA',(448*8,490*3),(24,31,39,255));draw=ImageDraw.Draw(sheet)
for r,clip in enumerate(['slash','rise','finisher']):
 for i in range(8):
  sheet.alpha_composite(Image.open(out/f'huntress-{clip}-{i:02}.png'),(i*448,r*490+35));draw.text((i*448+12,r*490+8),f'{r+1} / {i+1:02}',fill='white')
sheet.resize((2048,840)).convert('RGB').save(src/'huntress-knives-preview-v44.jpg',quality=94)
frames=[]
for clip in ['slash','rise','finisher']:
 for i in range(8):
  im=Image.new('RGBA',(448,448),(24,31,39,255));im.alpha_composite(Image.open(out/f'huntress-{clip}-{i:02}.png'));frames.append(im.resize((376,376)).convert('RGB'))
frames[0].save(src/'huntress-knives-loop-v44.gif',save_all=True,append_images=frames[1:],duration=[48]*8+[52]*8+[68]*8,loop=0)
print('Registered 24 grounded knife poses with two exact combo handoffs.')
