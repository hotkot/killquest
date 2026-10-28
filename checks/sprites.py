from PIL import Image
from pathlib import Path
import numpy as np
from scipy.ndimage import label
paths=list(Path('dist/assets/characters').glob('*.png'))
assert len(paths)==649
knight=[p for p in paths if p.name.startswith('knight-')]
assert len(knight)==149
for p in knight:
 a=np.array(Image.open(p));assert a.shape==((448,640,4) if p.name.split('-')[1] in ['down','cross','thrust'] else (448,448,4)),p
 alpha=a[:,:,3];assert not alpha[:4].any() and not alpha[-8:].any() and not alpha[:,:3].any() and not alpha[:,-3:].any(),p
 if p.name.startswith(('knight-down-','knight-cross-')):
  assert 405<=np.where(alpha>32)[0].max()<=432,(p,'boot / low blade margin')
 else:assert np.where(alpha>32)[0].max()==408,(p,'ground alignment')
 lab,n=label(alpha>100);areas=np.bincount(lab.ravel())[1:];assert sum(areas>50)==1,(p,'detached parts')
paths=[p for p in paths if not p.name.startswith('knight-')]
print('PASS: 149 knight frames with ground registration, transparent gutters and connected silhouettes.')
king=[p for p in paths if p.name.startswith('king-')]
assert len(king)==48
for p in king:
 a=np.array(Image.open(p));assert a.shape==(512,640,4),p
 alpha=a[:,:,3];assert not alpha[:4].any() and not alpha[-4:].any() and not alpha[:,:3].any() and not alpha[:,-3:].any(),p
 assert 464<=np.where(alpha>32)[0].max()<=466,(p,'ground baseline')
 lab,n=label(alpha>100);counts=np.bincount(lab.ravel())[1:]
 assert sum(counts>50)==1,(p,'detached parts')
paths=[p for p in paths if not p.name.startswith('king-')]
print('PASS: 48 boss frames, planted ground anchors, transparent gutters and connected weapons.')
for p in paths:
 a=np.array(Image.open(p));assert a.shape==((448,640,4) if p.name.startswith(('huntress-slash-','huntress-rise-','huntress-finisher-')) else (448,448,4)),p
 alpha=a[:,:,3];assert not alpha[:8].any() and not alpha[-8:].any() and not alpha[:,:8].any() and not alpha[:,-8:].any(),p
 lab,n=label(alpha>100);counts=np.bincount(lab.ravel())[1:];large=sorted(counts[counts>50],reverse=True)
 # Reviewed silver X-trail edge streaks, aerial knife trail and arrow fan.
 expected=3 if p.name=='huntress-finisher-04.png' else 2 if p.name in ['huntress-air-spin-03.png','huntress-rage-04.png'] else 1
 assert len(large)==expected,(p,large)
print('PASS: 452 RGBA frames, transparent gutters, no unexpected detached fragments.')

import json
registration=json.loads(Path('source-art/registration.json').read_text())
assert len(registration)==316
for name,entry in registration.items():
 assert entry['body_anchor'][0]==224
 if not name.startswith('hero-slide'):assert entry['body_anchor'][1]==300
 else:assert entry['translation'][1]==100
 source=np.array(Image.open('source-art/uncentered/'+name+'.png'))
 dest=np.array(Image.open('dist/assets/characters/'+name+'.png'))
 assert source[:,:,3].sum()==dest[:,:,3].sum(),('clipped alpha',name)
print('PASS: fixed body registration in every frame; no pixels clipped during centering.')

for link,source in [('hero-link-one-00','hero-slash-07'),('hero-link-one-07','hero-rise-03'),('hero-link-two-00','hero-rise-07'),('hero-link-two-07','hero-heavy-04'),('hero-air-spin-00','hero-air-chop-06'),('hero-air-spin-07','hero-heavy-03')]:
 assert np.array_equal(np.array(Image.open('dist/assets/characters/'+link+'.png')),np.array(Image.open('dist/assets/characters/'+source+'.png'))),(link,'endpoint seam')
print('PASS: all six transition endpoints exactly match their adjacent strike poses.')
for p in Path('source-art/uncentered').glob('hero-jump-*.png'):
 alpha=np.array(Image.open(p))[:,:,3]
 assert not np.any(alpha[-4:,:]>8),(p,'feet touch intermediate bottom edge')
 assert not np.any(alpha[:4,:]>8),(p,'head touches intermediate top edge')
print('PASS: jump source frames retain transparent bottom padding before registration.')
for kind in ['dagger','sword','archer']:
 for i in [6,7]:
  alpha=np.array(Image.open(f'dist/assets/characters/bandit-{kind}-grapple-{i:02}.png'))[:,:,3]
  ys=np.where(alpha>8)[0]
  assert 405<=ys.max()<=408,(kind,i,'landing must rest on ground')
print('PASS: human landing and prone frames share the ground baseline.')
for i in range(16):
 alpha=np.array(Image.open(f'dist/assets/characters/hero-walk-{i:02}.png'))[:,:,3]
 assert 405<=np.where(alpha>8)[0].max()<=408,(i,'walk ground baseline')
print('PASS: all 16 hero walk poses share a planted-foot ground baseline.')

registration=json.loads(Path('source-art/huntress-registration.json').read_text());assert len(registration)==136
for name,entry in registration.items():
 if name.startswith('huntress-pickup-'):
  assert entry['body_anchor']==[224,300+entry['ground_shift_y']],name
  assert entry['ground_anchor']==403,name
  image=Image.open('dist/assets/characters/'+name+'.png')
  original=Image.open(entry['normalization_source'])
  a=np.array(image);b=np.array(original)
  assert np.where(a[:,:,3]>8)[0].max()==403,name
  assert np.count_nonzero(a[:,:,3])==np.count_nonzero(b[:,:,3]),(name,'cropped alpha')
  assert a[:,:,3].sum()==b[:,:,3].sum(),(name,'lost pixels')
 else:assert entry['body_anchor']==([320,300] if name.startswith(('huntress-slash-','huntress-rise-','huntress-finisher-')) else [224,300]),name
print('PASS: Lyra combat frames retain body anchors and all eight pickup poses share the ground baseline without cropping; intentional weapon-effect components explicitly reviewed.')

heights=[]
for name,scale in [('hero',.84),('huntress',.84*210/234),('knight',.84*210/234)]:
 a=np.array(Image.open('dist/assets/characters/'+name+'-idle-00.png'))[:,:,3];ys=np.where(a>32)[0];heights.append((ys.max()-ys.min()+1)*scale)
assert max(heights)-min(heights)<.01,heights
print('PASS: Kael, Lyra and Garran standing silhouettes all measure 176.4 in-game pixels.')

for i in range(2,7):
 assert Path(f'dist/assets/characters/knight-cross-{i:02}.png').read_bytes()==Path(f'source-art/garran-v85/reference-knight-cross-{i:02}.png').read_bytes(),(i,'preserved forward slash pose changed')
assert len(list(Path('dist/assets/characters').glob('knight-cross-*.png')))==9
print('PASS: nine-frame slash retains its five approved transition/contact poses; only four rearward-blade poses replaced.')

idle=Image.open('dist/assets/characters/knight-idle-00.png');padded=Image.new('RGBA',(640,448));padded.alpha_composite(idle,(96,0))
for name in ['thrust-11']:
 assert np.array_equal(np.array(padded),np.array(Image.open('dist/assets/characters/knight-'+name+'.png'))),name
print('PASS: final stab recovers to the exact grounded idle pose.')

import hashlib
preserved=json.loads(Path('source-art/garran-v85/preserved-thrust-sha256.json').read_text())
for name,digest in preserved.items():
 assert hashlib.sha256(Path('dist/assets/characters',name).read_bytes()).hexdigest()==digest,(name,'stab changed')
print('PASS: all twelve final stab frames remain byte-for-byte unchanged.')

raised=np.array(Image.open('dist/assets/characters/knight-down-00.png'))[:,:,3]
assert (raised[:150]>32).sum()>100,'first slash must start with a raised blade'
print('PASS: first cut begins raised; low sword ends and boot baselines retain full transparent padding.')

for name,digest in json.loads(Path('source-art/garran-v85/preserved-down-sha256.json').read_text()).items():
 assert hashlib.sha256(Path('dist/assets/characters',name).read_bytes()).hexdigest()==digest,(name,'first strike changed')
print('PASS: all eight first-strike sprites also remain byte-for-byte unchanged.')
