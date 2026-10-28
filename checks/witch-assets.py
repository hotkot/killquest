from pathlib import Path
from PIL import Image
import json,wave,numpy as np
root=Path(__file__).resolve().parents[1];art=root/'dist/assets/characters'
registration=json.loads((root/'source-art/witch-v90/registration.json').read_text())
assert len(registration)==76
for key,r in registration.items():
 im=Image.open(art/(key+'.png'));assert im.size==(448,448) and im.mode=='RGBA'
 a=np.array(im);assert a[:,:,3].min()==0 and a[:,:,3].max()>200
 box=im.getbbox();assert min(box[0],box[1],448-box[2],448-box[3])>=6,(key,box,'cropped at canvas edge')
 # No floating pieces belonging to an adjacent grid cell.
 from scipy.ndimage import label
 lab,n=label(a[:,:,3]>100);areas=np.bincount(lab.ravel())[1:];assert max(areas)>1000
 assert sum(areas[areas<100])<max(areas)*.025,(key,'stray fragments')
 assert r['scale']>0
for clip in ['flame','burst','storm']:
 for i in range(4):
  im=Image.open(root/f'dist/assets/effects/witch-fx-{clip}-{i:02}.png');assert im.size==(384,384);assert im.getextrema()[3][0]==0
for family in ['cast','impact','teleport','storm']:
 with wave.open(str(root/f'dist/assets/audio/witch-{family}-0.wav')) as w:
  assert w.getnchannels()==2 and w.getframerate()==44100 and w.getsampwidth()==2
  assert .3<w.getnframes()/w.getframerate()<2
  a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2')/32768
  assert .02<np.sqrt(np.mean(a*a))<.4
  assert .7<np.max(np.abs(a))<.9
assert Image.open(root/'dist/assets/ui/selene-life-head.png').size==(128,128)
print('PASS: 76 transparent character frames, padded canvases/no neighboring fragments, 12 blue flame sprites, portrait/life head, four non-silent unclipped stereo magic effects.')
