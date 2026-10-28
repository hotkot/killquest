from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_opening

root=Path('dist/assets/characters');source=Path('source-art/lyra-slashes-v87')
for name,digest in json.loads((source/'preserved-other-player-frames.json').read_text()).items():
 assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,(name,'unrelated art changed')
idle=Image.open(root/'huntress-idle-00.png');ready=Image.new('RGBA',(640,448));ready.alpha_composite(idle,(96,0))
for name in ['slash-00','finisher-07']:
 assert np.array_equal(np.array(Image.open(root/('huntress-'+name+'.png'))),np.array(ready)),name
for target,origin in [('rise-00','slash-07'),('finisher-00','rise-07')]:
 assert (root/('huntress-'+target+'.png')).read_bytes()==(root/('huntress-'+origin+'.png')).read_bytes(),(target,'seam')
layout=json.loads(Path('source-art/player-scale-v86/normalization.json').read_text())['frames']
report=json.loads((source/'registration.json').read_text())
for clip in ['slash','rise','finisher']:
 assert .2<report[clip]['shared_scale']<3
 assert report[clip]['standing_reference_body_height']==219
 assert abs(report[clip]['normalized_witness_body_height']-219)<=2
 assert .85<report[clip]['normalized_witness_body_area']/layout['huntress-idle-00']['body_area']<1.18
 hashes=[]
 for i in range(8):
  name=f'huntress-{clip}-{i:02}';im=Image.open(root/(name+'.png'));a=np.array(im)
  assert a.shape==(448,640,4),name
  assert not a[:8,:,3].any() and not a[-8:,:,3].any() and not a[:,:8,3].any() and not a[:,-8:,3].any(),(name,'cut off')
  assert 400<=np.where(a[:,:,3]>32)[0].max()<=420,(name,'ground margin')
  assert layout[name]['factor']==1,(name,'new normalized body was rescaled again')
  assert layout[name]['canvas']==[640,448]
  hashes.append(hashlib.sha256(a.tobytes()).hexdigest())
 assert len(set(hashes))>=7,(clip,'duplicate motion frames')
 contact=np.array(Image.open(root/f'huntress-{clip}-04.png'))
 silver=(contact[:,:,3]>128)&(contact[:,:,:3].min(axis=2)>190)&(np.ptp(contact[:,:,:3].astype(int),axis=2)<45)
 assert silver.sum()>250,(clip,'missing visible cutting crescent')
print('PASS: 24 full grounded slash frames, shared idle anatomy calibration, visible contact crescents, exact combo seams, no double scaling and all other character art unchanged.')
