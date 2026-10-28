from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects,binary_dilation
import numpy as np,json
root=Path(__file__).resolve().parents[1];src=root/'source-art/garran-v77';out=root/'dist/assets/characters'
def extract(name,rows):
 im=Image.open(src/(name+'.png')).convert('RGBA');a=np.array(im);lab,n=label(a[:,:,3]>32);areas=np.bincount(lab.ravel());slices=find_objects(lab)
 ids=[i for i in range(1,n+1) if areas[i]>1000]
 ids.sort(key=lambda i:(round(((slices[i-1][0].start+slices[i-1][0].stop)/2)/(im.height/rows)-.5),(slices[i-1][1].start+slices[i-1][1].stop)/2))
 if name=='combo':
  # Two source figures touch in row four column one. Hold the preceding clean contact pose.
  clean=[i for i in ids if slices[i-1][0].stop-slices[i-1][0].start<300];ids=clean[:12]+[clean[11]]+clean[12:15]
 cells=[]
 for k in ids:
  sy,sx=slices[k-1];l=max(0,sx.start-2);r=min(im.width,sx.stop+2);t=max(0,sy.start-2);b=min(im.height,sy.stop+2)
  v=a[t:b,l:r].copy();v[:,:,3]=np.where(binary_dilation(lab[t:b,l:r]==k,iterations=2),v[:,:,3],0);cells.append(Image.fromarray(v))
 return cells
def height(im):return np.ptp(np.where(np.array(im)[:,:,3]>32)[0])+1
report={}
def save(clip,cells,scale,width=448,correction=None):
 for j,im in enumerate(cells):
  factor=scale*(correction if correction and j>=12 else 1);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS);v=np.array(im);a=v[:,:,3]
  y=408-int(np.where(a>32)[0].max());gy=np.arange(im.height)[:,None]+y
  mask=(a>128)&(v[:,:,0]>180)&(v[:,:,1]>160)&(v[:,:,0]>v[:,:,2]*1.15)&(gy>240)&(gy<330)
  xs=np.where(mask)[1];anchor=np.median(xs) if len(xs)>30 else im.width/2;x=round(width/2-anchor)
  assert x>=4 and x+im.width<=width-4 and y>=4,(clip,j,x,y,im.size)
  canvas=Image.new('RGBA',(width,448));canvas.alpha_composite(im,(x,y));canvas.save(out/f'knight-{clip}-{j:02}.png');report[f'{clip}-{j:02}']={'scale':factor,'ground':408,'canvas':[width,448]}
idle=extract('idle',2);assert len(idle)==8;save('idle',idle,233/height(idle[0]))
walk=extract('walk',4);assert len(walk)==16;correction=np.median([height(i) for i in walk[:12]])/np.median([height(i) for i in walk[12:]]);save('walk',walk,234/np.median([height(i) for i in walk[:12]]),correction=correction)
combo=extract('combo',5);assert len(combo)==16;scale=234/height(combo[0]);save('slash',combo[:8],scale,640);save('stab',combo[8:],scale,640)
finish=extract('finisher',2);assert len(finish)==8;save('finisher',finish,234/height(finish[-1]),640)
back=extract('backstep',2);assert len(back)==8;save('backstep',back,234/height(back[0]))
for dst,source in [('slash-00','idle-00'),('stab-00','slash-07'),('finisher-00','stab-07'),('finisher-07','idle-00'),('backstep-00','idle-00'),('backstep-07','idle-00')]:
 im=Image.open(out/f'knight-{source}.png');width=640 if dst.split('-')[0] in ['slash','stab','finisher'] else 448;canvas=Image.new('RGBA',(width,448));canvas.alpha_composite(im,((width-im.width)//2,0));canvas.save(out/f'knight-{dst}.png')
for old in ['rise','block']:
 for p in out.glob(f'knight-{old}-*.png'):p.unlink()
(src/'registration.json').write_text(json.dumps({'frames':report,'walk_last_row_calibration':correction,'review':'Discarded malformed final combo row; held clean thrust contact at stab frame 4. Dedicated finisher used instead.'},indent=2)+'\n')
for clip,count in [('idle',8),('walk',16),('slash',8),('stab',8),('finisher',8),('backstep',8)]:
 sheet=Image.new('RGB',(8*288,((count+7)//8)*246),(28,31,35));d=ImageDraw.Draw(sheet)
 for i in range(count):
  im=Image.open(out/f'knight-{clip}-{i:02}.png');im.thumbnail((288,224));x=(i%8)*288+(288-im.width)//2;y=(i//8)*246;sheet.paste(im,(x,y),im);d.text(((i%8)*288+5,y+225),f'{clip} {i+1}',fill='white')
 sheet.save(src/(clip+'-preview.jpg'),quality=90)
print('Normalized',len(report),'reviewed frames')
