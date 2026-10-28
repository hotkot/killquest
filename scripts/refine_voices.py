"""Softer, breathier formant voices with varied phrasing; no music changes."""
from pathlib import Path
import numpy as np,wave,json
from scipy.signal import butter,sosfilt,iirpeak,lfilter
out=Path(__file__).resolve().parents[1]/'dist/assets/audio';R=44100;rng=np.random.default_rng(62024)
for prefix in ['hero-effort','hero-pain','hero-death','bandit-effort','bandit-pain','bandit-death']:
 for p in out.glob(prefix+'-*.wav'):p.unlink()
counts={'hero-effort':12,'hero-pain':6,'hero-death':4,'bandit-death':6}
for family,count in counts.items():
 for i in range(count):
  death='death' in family;pain='pain' in family;d=(.46 if death else .18 if pain else .14)+rng.uniform(.01,.09);t=np.arange(round(d*R))/R
  pitch=(108 if family.startswith('bandit') else 82)+rng.uniform(-8,14);f=pitch*(1.03-rng.uniform(.12,.28)*t/d)+1.3*np.sin(2*np.pi*3*t+i);phase=2*np.pi*np.cumsum(f)/R
  glottal=sum(np.sin(k*phase+i*.22)/(k*k) for k in range(1,10));breath=sosfilt(butter(2,[300,1700],btype='bandpass',fs=R,output='sos'),rng.normal(0,1,len(t)))
  v=.3*glottal
  formants=[(360+(i%4)*65,3),(790+(i%3)*95,4),(1650+(i%4)*90,5)]
  for hz,q in formants:
   b,a=iirpeak(hz,q,fs=R);v+=lfilter(b,a,glottal+breath*.06)*1.6
  v=sosfilt(butter(2,1850,fs=R,output='sos'),v);envelope=np.sin(np.pi*t/d)**(1.15+(i%3)*.3)
  if i%4==2:envelope*=.65+.35*np.sin(2*np.pi*t/d+.3)**2
  v=(v+breath*.04)*envelope;v=v/max(np.max(np.abs(v)),1e-6)*(.48 if death else .26 if pain else .32)
  with wave.open(str(out/f'{family}-{i}.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((v*32767).astype('<i2').tobytes())
p=out/'manifest.json';m=json.loads(p.read_text());m['voice_variants']=counts;m['voice_revision']='soft harmonic source, reduced highs/roughness and loudness; randomized phrasing';p.write_text(json.dumps(m,indent=2))
print('Created',sum(counts.values()),'soft vocal variants; removed enemy effort and pain files.')
