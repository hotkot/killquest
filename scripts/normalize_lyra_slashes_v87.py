"""Normalize three eight-pose slashes using each strip's neutral scale witness.

The ninth source cell is an upright scale reference, never a gameplay frame.
Use one anatomy scale per strip, fixed soles, and roomy rectangular canvases.
"""
from pathlib import Path
import json, shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, find_objects, binary_opening, binary_dilation

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source-art/lyra-slashes-v87'
OUT=ROOT/'dist/assets/characters'
W,H,GROUND=640,448,403
Y,X=np.mgrid[-4:5,-4:5];DISK=X*X+Y*Y<=16

def body_height(image):
    a=np.array(image);labs,_=label(binary_opening(a[:,:,3]>100,DISK))
    areas=np.bincount(labs.ravel());areas[0]=0
    ys=np.where(labs==areas.argmax())[0]
    return int(ys.max()-ys.min()+1)

idle=Image.open(OUT/'huntress-idle-00.png').convert('RGBA')
target_height=body_height(idle)
report={}
manifest=json.loads((ROOT/'source-art/huntress-registration.json').read_text())
for clip in ['slash','rise','finisher']:
    image=Image.open(SRC/(clip+'.png')).convert('RGBA')
    raw=np.array(image)
    labels,n=label(binary_opening(raw[:,:,3]>32))
    sizes=np.bincount(labels.ravel());boxes=find_objects(labels)
    ids=[i for i in range(1,n+1) if sizes[i]>1000]
    assert len(ids)==9,(clip,'expected nine complete isolated figures',len(ids))
    ids.sort(key=lambda i:(boxes[i-1][0].start+boxes[i-1][0].stop)/2)
    ordered=[]
    for row in range(3):
        ordered.extend(sorted(ids[row*3:(row+1)*3],key=lambda i:boxes[i-1][1].start))
    cells=[]
    for i,k in enumerate(ordered):
        sy,sx=boxes[k-1]
        l,r=max(0,sx.start-4),min(image.width,sx.stop+4)
        t,b=max(0,sy.start-4),min(image.height,sy.stop+4)
        assert l>=3 and r<=image.width-3 and t>=3 and b<=image.height-3,(clip,i,'source edge clips figure/effect')
        a=raw[t:b,l:r].copy()
        keep=binary_dilation(labels[t:b,l:r]==k,iterations=3)
        a[:,:,3]=np.where(keep,a[:,:,3],0)
        cells.append(Image.fromarray(a))
    witness=cells[8]
    a=np.array(witness)[:,:,3];ys=np.where(a>32)[0]
    preliminary=234/(ys.max()-ys.min()+1)
    test=witness.resize((round(witness.width*preliminary),round(witness.height*preliminary)),Image.Resampling.LANCZOS)
    scale=float(preliminary*target_height/body_height(test))
    normalized_witness=witness.resize((round(witness.width*scale),round(witness.height*scale)),Image.Resampling.LANCZOS)
    wl,wn=label(binary_opening(np.array(normalized_witness)[:,:,3]>100,DISK))
    wa=np.bincount(wl.ravel());wa[0]=0
    report[clip]={'shared_scale':scale,'standing_reference_body_height':target_height,
                  'normalized_witness_body_height':body_height(normalized_witness),
                  'normalized_witness_body_area':int(wa.max()),'frames':[]}
    for i,cell in enumerate(cells[:8]):
        cell=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
        v=np.array(cell);alpha=v[:,:,3]
        # Boots form a broad sole; ignore narrow blade/trail tips below them.
        widths=(alpha>32).sum(axis=1)
        sole=int(np.where(widths>=max(12,round(cell.width*.035)))[0].max())
        yy=np.arange(cell.height)[:,None]
        # Register the planted stance rather than weapon-biased full bounds.
        xs=np.where((alpha>100)&(yy>sole-22)&(yy<=sole))[1]
        anchor=(np.percentile(xs,10)+np.percentile(xs,90))/2
        x=round(W/2-anchor);y=GROUND-sole
        assert x>=8 and x+cell.width<=W-8 and y>=8 and y+cell.height<=H-8,(clip,i,x,y,cell.size)
        frame=Image.new('RGBA',(W,H));frame.alpha_composite(cell,(x,y))
        name=f'huntress-{clip}-{i:02}'
        frame.save(OUT/(name+'.png'))
        components,n=label(np.array(frame)[:,:,3]>100)
        counts=np.bincount(components.ravel())[1:]
        entry={'shared_scale':scale,'ground_anchor':GROUND,'body_anchor':[320,300],
               'translation':[x,y],'effect_components':int(sum(counts>50)),
               'source':str((SRC/(clip+'.png')).relative_to(ROOT)),
               'component':i,'action':{'slash':'diagonal sweep','rise':'turning horizontal slash','finisher':'crossed-blade slash'}[clip]}
        report[clip]['frames'].append(entry)
        manifest[name]=entry

for dst,src in [('slash-00','idle-00'),('rise-00','slash-07'),('finisher-00','rise-07'),('finisher-07','idle-00')]:
    image=Image.open(OUT/f'huntress-{src}.png')
    frame=Image.new('RGBA',(W,H));frame.alpha_composite(image,((W-image.width)//2,0))
    frame.save(OUT/f'huntress-{dst}.png')
    manifest['huntress-'+dst]['locked_to']='huntress-'+src
    manifest['huntress-'+dst]['effect_components']=1

(SRC/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'source-art/huntress-registration.json').write_text(json.dumps(manifest,indent=2)+'\n')
sheet=Image.new('RGB',(4*320,6*246),(28,31,35));d=ImageDraw.Draw(sheet)
frames=[];durations=[]
for row,clip in enumerate(['slash','rise','finisher']):
    times={'slash':[50,50,40,50,60,60,60,30], 'rise':[50,50,50,50,60,60,60,40],
           'finisher':[70,70,70,70,80,80,70,70]}[clip]
    for i in range(8):
        im=Image.open(OUT/f'huntress-{clip}-{i:02}.png')
        small=im.resize((320,224),Image.Resampling.LANCZOS)
        x=i%4*320;y=(row*2+i//4)*246;sheet.paste(small,(x,y),small)
        d.text((x+8,y+229),f'{clip} {i+1}',fill='white')
        bg=Image.new('RGB',(640,448),(28,31,35));bg.paste(im,(0,0),im)
        frames.append(bg);durations.append(times[i])
durations[-1]+=500
sheet.save(SRC/'combo-preview.jpg',quality=95)
frames[0].save(SRC/'combo-preview.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
print('Normalized 24 grounded slash frames using three standing scale witnesses and exact combo seams.')
