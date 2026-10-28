from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,shutil
from scipy.ndimage import label,find_objects,binary_dilation
root=Path(__file__).resolve().parents[1];out=root/'dist/assets/characters';src=root/'source-art'
files={'a':'exec-4b00e4d1-d999-4547-bf3c-20bb67b81edd.png','b':'exec-b841ef5f-4660-4483-b2af-f7c0e05375fb.png','c':'exec-6d9263d2-b6e0-4427-97e4-7424bf5b29c6.png'}
# Artist-reviewed pelvis points, in raw sheet pixels. All are translated to the
# existing gameplay body anchor, never the weapon-biased bounding-box center.
anchors={
'a':[
[(101+181*i,104) for i in range(8)],
[(97+181*i,282) for i in range(8)],
[(98,469),(280,466),(472,465),(632,464),(833,462),(1009,466),(1188,466),(1372,466)],
[(98,685),(279,677),(472,656),(647,657),(830,658),(1013,663),(1195,662),(1375,661)],
[(99,842),(288,849),(493,846),(731,838),(942,860),(1160,847),(1371,832)],
[(105,1005),(283,1016),(454,1032),(656,995),(806,1028),(1021,1015),(1200,1027),(1371,1024)]],
'b':[
[(110,154),(275,114),(462,95),(637,107),(826,113),(1011,165),(1200,153),(1374,112)],
[(98,310),(282,300),(465,300),(650,301),(833,302),(1020,304),(1207,307),(1370,299)],
[(101,475),(282,472),(463,469),(644,478),(822,481),(1012,471),(1185,468),(1375,482)],
[(101,659),(283,668),(433,661),(617,669),(802,668),(984,686),(1183,690),(1370,671)],
[(94,824),(279,826),(460,825),(641,826),(825,826),(1001,826),(1195,826),(1374,826)],
[(96,1002),(280,1002),(465,1005),(644,1007),(821,1005),(999,1000),(1205,1000),(1377,1004)]],
'c':[
[(94,142),(276,143),(468,143),(645,143),(819,144),(1012,144),(1197,145),(1375,145)],
[(96,325),(279,326),(462,330),(628,358),(831,380),(1031,373),(1198,330),(1371,325)],
[(93,510),(271,540),(450,546),(637,550),(811,542),(1007,519),(1198,512),(1373,510)],
[(97,685),(280,685),(470,685),(655,673),(825,681),(1007,682),(1190,682),(1370,682)],
[(97,873),(284,873),(463,873),(640,874),(812,872),(996,870),(1190,872),(1371,872)]]}
rowlimits={'a':[188,375,557,751,923,1090],'b':[202,388,575,748,919,1090],'c':[239,420,604,782,968,1090]}
names={'a':['idle','walk','slash','rise','finisher','roll'],'b':['jump','air-slash','air-spin','air-finish','bow','air-bow'],'c':['rage','hurt','pickup','grapple','win']}
scales={'a':1.28,'b':1.28,'c':1.16};manifest={}
for sheet,file in files.items():
 raw=Path('/workspace/scratch/e77afc5b40f4/generated_images')/file
 dest=src/f'huntress-{sheet}-v43.png'
 if raw.exists():shutil.copy(raw,dest)
 im=Image.open(dest).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>80);sizes=np.bincount(labs.ravel());boxes=find_objects(labs)
 ids=[k for k in range(1,n+1) if sizes[k]>2500]
 rows=[[] for _ in rowlimits[sheet]]
 for k in ids:
  y,x=boxes[k-1];r=next((i for i,e in enumerate(rowlimits[sheet]) if y.stop<=e),5);rows[r].append(k)
 for r,clip in enumerate(names[sheet]):
  ks=sorted(rows[r],key=lambda k:boxes[k-1][1].start)
  assert len(ks)==len(anchors[sheet][r]),(sheet,r,len(ks))
  remap=list(range(len(ks)))
  if len(remap)==7:remap.append(6)
  for i,j in enumerate(remap):
   k=ks[j];mask=binary_dilation(labs==k,iterations=2);clean=a.copy();clean[:,:,3][~mask]=0
   cut=Image.fromarray(clean);box=cut.getbbox();cut=cut.crop(box);scale=scales[sheet];cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
   cx,cy=anchors[sheet][r][j];dx=224-round((cx-box[0])*scale);dy=300-round((cy-box[1])*scale)
   frame=Image.new('RGBA',(448,448));frame.alpha_composite(cut,(dx,dy));name=f'huntress-{clip}-{i:02}';frame.save(out/f'{name}.png');manifest[name]={'source':dest.name,'component':int(k),'anchor':[cx,cy],'scale':scale,'body_anchor':[224,300]}
# Start/end utility states connect back to the exact ready pose.
for clip in ['slash','rise','finisher','roll','pickup','grapple','win']:
 shutil.copy(out/'huntress-idle-00.png',out/f'huntress-{clip}-07.png')
(src/'huntress-registration.json').write_text(json.dumps(manifest,indent=2))
preview=Image.new('RGBA',(448*8,448*17),(24,31,39,255));d=ImageDraw.Draw(preview)
for r,clip in enumerate(sum(names.values(),[])):
 for i in range(8):preview.alpha_composite(Image.open(out/f'huntress-{clip}-{i:02}.png'),(i*448,r*448));d.text((i*448+10,r*448+10),f'{clip} {i}',fill='white')
preview.resize((1792,3808)).convert('RGB').save(src/'huntress-preview-v43.jpg',quality=90)
print('Normalized',len(manifest),'huntress frames.')

# Keep the later, approved passing/contact walk keys when rebuilding all clips.
if (src/"huntress-walk-v43.png").exists():
 import runpy
 runpy.run_path(str(root/"scripts/normalize_huntress_walk.py"),run_name="__main__")

# Preserve the later simple three-strike ground combo on full rebuilds.
if (src/"huntress-knives-v44.png").exists():
 import runpy
 runpy.run_path(str(root/"scripts/normalize_huntress_knives.py"),run_name="__main__")

# Keep ground-registered utility poses when rebuilding all huntress clips.
if (src/"huntress-pickup-v54").exists():
 import runpy
 runpy.run_path(str(root/"scripts/normalize_huntress_pickup_v54.py"),run_name="__main__")
