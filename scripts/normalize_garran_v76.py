from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json,shutil
root=Path(__file__).resolve().parents[1];source=root/'source-art/garran-v76';target=root/'dist/assets/characters'
files={
 'locomotion':('8edcdf1f-498c-4dd3-a325-d0efe914628b',['idle','walk','jump'],1.0),
 'swords':('5b7b4c87-465d-45d7-8a27-28ebf5046cc5',['slash','rise','finisher'],1.08),
 'aerial':('7c403f77-9184-40d4-8fcd-1a0a7b67b243',['air-slash','air-spin','air-finish'],1.06),
 'shield':('7bebd69e-ce5a-4397-9c9d-c110974a1c02',['bash','slam','block'],1.10),
 'utility':('5067837a-5f5f-4ada-9c2a-10fd5b596813',['hurt','pickup'],1.17),
 'special':('f2a8675f-86d1-4241-8d67-6db72ce35d9a',['win','rage'],.94)
}
# Grapple is generated separately because two figures touched in the discarded utility row.
if (source/'grapple.png').exists():files['grapple']=(None,['grapple'],.62)
report={}
for group,(raw,clips,scale) in files.items():
 path=source/(group+'.png')
 if raw and not path.exists():shutil.copyfile(root.parent.parent/'scratch/e77afc5b40f4/generated_images'/('exec-'+raw+'.png'),path)
 im=Image.open(path).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>32);areas=np.bincount(labs.ravel());sl=find_objects(labs);ids=[i for i in range(1,n+1) if areas[i]>1000]
 rows=6 if group=='utility' else len(clips)*2
 ids.sort(key=lambda i:(round(((sl[i-1][0].start+sl[i-1][0].stop)/2)/(im.height/rows)-.5),(sl[i-1][1].start+sl[i-1][1].stop)/2))
 assert len(ids)>=len(clips)*8,(group,len(ids))
 # Additional raw utility poses are deliberately excluded; one had a duplicate sword.
 ids=ids[:len(clips)*8]
 for j,k in enumerate(ids):
  clip=clips[j//8];idx=j%8;sy,sx=sl[k-1];l=max(0,sx.start-2);r=min(im.width,sx.stop+2);t=max(0,sy.start-2);b=min(im.height,sy.stop+2);pixels=a[t:b,l:r].copy();mask=binary_dilation(labs[t:b,l:r]==k,iterations=2);pixels[:,:,3]=np.where(mask,pixels[:,:,3],0)
  cell=Image.fromarray(pixels);cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS);v=np.array(cell);alpha=v[:,:,3];ys,xs=np.where((alpha>100)&(np.arange(cell.height)[:,None]>cell.height-40)&(v[:,:,0]<150)&(v[:,:,1]<145));anchor=float((np.percentile(xs,10)+np.percentile(xs,90))/2) if len(xs)>20 else cell.width/2
  x=round(224-anchor);x=max(4,min(444-cell.width,x));y=408-int(np.where(alpha>32)[0].max());assert cell.width<=440 and x>=4 and x+cell.width<=444 and y>=4,(group,j,x,y,cell.size)
  canvas=Image.new('RGBA',(448,448));canvas.alpha_composite(cell,(x,y));canvas.save(target/f'knight-{clip}-{idx:02}.png');report[f'{clip}-{idx:02}']={'scale':scale,'ground':408,'anchor_x':anchor,'source_bounds':[l,t,r,b]}
# Stabilize standing/walking torso centers rather than following the leading boot.
for clip in ['idle','walk']:
 for i in range(8):
  path=target/f'knight-{clip}-{i:02}.png';im=Image.open(path).copy();v=np.array(im);ys,xs=np.where((v[:,:,3]>128)&(v[:,:,0]>180)&(v[:,:,1]>160)&(v[:,:,0]>v[:,:,2]*1.15)&(np.arange(448)[:,None]>240)&(np.arange(448)[:,None]<330));dx=round(224-float(np.median(xs))) if len(xs)>30 else 0;l,t,r,b=im.getchannel('A').getbbox();assert l+dx>=3 and r+dx<=445
  centered=Image.new('RGBA',(448,448));centered.alpha_composite(im,(dx,0));centered.save(path);report[f'{clip}-{i:02}']['torso_shift_x']=dx
# Reviewed utility corrections and exact pose seams.
for dst,src in [('hurt-06','hurt-07')]:shutil.copyfile(target/('knight-'+src+'.png'),target/('knight-'+dst+'.png'))
originals=[Image.open(target/f'knight-pickup-{i:02}.png').copy() for i in range(8)]
for i,j in enumerate([0,4,1,2,2,5,6,7]):originals[j].save(target/f'knight-pickup-{i:02}.png')
for clip in ['slash','bash','pickup']:
 shutil.copyfile(target/'knight-idle-00.png',target/f'knight-{clip}-00.png')
for dst,src in [('rise-00','slash-07'),('finisher-00','rise-07'),('finisher-07','idle-00'),('bash-07','idle-00'),('slam-07','idle-00'),('block-07','idle-00'),('pickup-07','idle-00'),('air-spin-00','air-slash-07'),('air-finish-00','air-spin-07'),('win-00','idle-00'),('rage-00','idle-00'),('rage-07','idle-00')]:shutil.copyfile(target/('knight-'+src+'.png'),target/('knight-'+dst+'.png'))
(source/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
for group,(_,clips,_) in files.items():
 sheet=Image.new('RGB',(8*224,len(clips)*246),(28,31,35));d=ImageDraw.Draw(sheet)
 for row,clip in enumerate(clips):
  for i in range(8):
   im=Image.open(target/f'knight-{clip}-{i:02}.png').resize((224,224));sheet.paste(im,(i*224,row*246),im);d.text((i*224+5,row*246+225),clip+' '+str(i+1),fill='white')
 sheet.save(source/(group+'-preview.jpg'),quality=90)
print('Normalized',len(report),'Garran frames.')
