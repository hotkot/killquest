"""Chesty barbarian exclamations, audible enemy death cries and flesh-cut layers."""
from pathlib import Path
import numpy as np,wave,json
from scipy.signal import butter,sosfilt,iirpeak,lfilter
R=44100;rng=np.random.default_rng(7409);out=Path(__file__).resolve().parents[1]/'dist/assets/audio'
def band(x,lo,hi):return sosfilt(butter(2,[lo,hi],btype='bandpass',fs=R,output='sos'),x)
def write(name,x,peak):
 x=np.nan_to_num(x);x=x/max(np.max(np.abs(x)),1e-8)*peak
 n=min(180,len(x)//5);x[:n]*=np.linspace(0,1,n);x[-n:]*=np.linspace(1,0,n)
 with wave.open(str(out/(name+'.wav')),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((x*32767).astype('<i2').tobytes())
for family,count in [('hero-effort',12),('bandit-death',6)]:
 for i in range(count):
  hero=family.startswith('hero');d=(.24 if hero else .65)+rng.uniform(.02,.12);t=np.arange(round(d*R))/R
  f=(78+rng.uniform(-6,14))*(1.2-.22*t/d) if hero else (155+rng.uniform(-15,35))*(1.45-.8*t/d)
  f=f+2*np.sin(2*np.pi*(4 if hero else 7)*t);phase=2*np.pi*np.cumsum(f)/R
  source=sum(np.sin(k*phase+(k%2)*.12)/(k**1.18) for k in range(1,22));breath=band(rng.normal(0,1,len(t)),400,3400)
  source*=.91+.09*np.sin(2*np.pi*(24 if hero else 33)*t)
  v=source*.24
  forms=[(460+(i%4)*30,3),(970+(i%3)*65,4),(2200+(i%4)*70,5)] if hero else [(720+(i%3)*50,3),(1250+(i%2)*100,4),(2600+(i%3)*90,5)]
  for hz,q in forms:
   b,a=iirpeak(hz,q,fs=R);v+=lfilter(b,a,source+breath*.11)*2.5
  v=np.tanh(v*1.2);v=sosfilt(butter(2,3300,fs=R,output='sos'),v)
  envelope=np.minimum(1,t/.018)*np.minimum(1,(d-t)/(.09 if hero else .3))*np.exp(-t*(1.4 if hero else .4))
  consonant=breath*np.exp(-t*65)*.12;v=(v+consonant)*envelope
  write(f'{family}-{i}',v,.76 if hero else .82)
for i in range(6):
 d=.20+i*.012;t=np.arange(round(d*R))/R;n=rng.normal(0,1,len(t));wet=band(n,220,1900);tear=band(n,1600,6200)
 # Dense wet transient followed by irregular fibrous tearing, with a body thud.
 a=(1-np.exp(-t*600))*np.exp(-t*22);mod=.35+.65*(np.sin(2*np.pi*(35+i*7)*t+.5)**2)
 phase=2*np.pi*np.cumsum(75+130*np.exp(-t*50))/R
 x=wet*a*mod*.9+tear*np.exp(-t*48)*.35+np.sin(phase)*np.exp(-t*30)*.35
 for at,g in [(.017,.15),(.041,.12),(.078,.08)]:x+=band(rng.normal(0,1,len(t)),300,2500)*np.exp(-np.abs(t-at)*170)*g
 write('flesh-'+str(i),x,.78)
p=out/'manifest.json';m=json.loads(p.read_text());m['voice_revision']='chesty harmonic/formant opening exclamations and strained falling enemy death cries; stronger vocal mix';m['effect_variants']={'flesh':6};p.write_text(json.dumps(m,indent=2))
print('Rebuilt 18 prominent vocal samples and added six wet slicing layers.')
