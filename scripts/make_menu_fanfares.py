"""Original DragonQuest menu cues and metal/defeat fanfares, reproducible synthesis."""
from pathlib import Path
import wave
import numpy as np
from scipy.signal import butter,sosfilt
R=44100
out=Path(__file__).resolve().parents[1]/'dist/assets/audio'
rng=np.random.default_rng(491)
def hz(n):return 440*2**((n-69)/12)
def write(name,x):
 x=np.nan_to_num(x); x=x/max(1e-6,np.max(abs(x)))*.78
 fade=min(220,len(x)//4);x[:fade]*=np.linspace(0,1,fade)[:,None];x[-fade:]*=np.linspace(1,0,fade)[:,None]
 with wave.open(str(out/(name+'.wav')),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((x*32767).astype('<i2').tobytes())
def add(x,s,at,pan=0,gain=1):
 i=round(at*R);n=min(len(s),len(x)-i)
 if n>0:x[i:i+n]+=s[:n,None]*np.array([1-pan*.4,1+pan*.4])*gain
def guitar(n,d,lead=True):
 t=np.arange(round(d*R))/R;f=hz(n)*(1+.004*np.sin(2*np.pi*6*t)*np.minimum(t/.15,1))
 phase=np.cumsum(f)/R;v=sum(np.sin(2*np.pi*phase*k)/k**1.3 for k in range(1,13));v=np.tanh(v*(3 if lead else 5))
 v=sosfilt(butter(2,4200 if lead else 2500,fs=R,output='sos'),v)
 return v*np.minimum(t/.006,1)*np.exp(-t/(.7 if lead else .10))*np.minimum((d-t)/.035,1)
def drums(x,at,snare=False):
 t=np.arange(round(.24*R))/R
 if snare:s=rng.normal(0,1,len(t))*np.exp(-t*24)*.22+np.sin(2*np.pi*185*t)*np.exp(-t*30)*.2
 else:s=np.sin(2*np.pi*(48*t+1.7*(1-np.exp(-t*35))))*np.exp(-t*22)*.7
 add(x,s,at,gain=.55)
# Eight bars: rising shred phrases, harmonized run, bent sustained tonic; palm-muted backing.
beat=60/150;x=np.zeros((round(14*R),2))
phrases=[[64,67,69,71,76,74,71,69],[67,69,71,74,76,79,78,76],[76,74,71,69,67,69,71,74],[76,79,83,81,79,78,76,74]]
for bar in range(8):
 base=bar*4*beat
 for j,n in enumerate(phrases[bar%4]):
  at=base+j*beat/2;add(x,guitar(n,beat*.75),at,-.25,.3)
  if bar>=4:add(x,guitar(n+7,beat*.75),at,.55,.12)
 for j in range(8):
  at=base+j*beat/2
  for n in [40 if bar%4<2 else 43,47 if bar%4<2 else 50]:add(x,guitar(n,.22,False),at,.25,.13)
 for j in range(4):drums(x,base+j*beat,j%2==1)
 for j in range(8):
  t=np.arange(round(.10*R))/R;add(x,rng.normal(0,1,len(t))*np.exp(-t*75),base+j*beat/2,.6,.045)
add(x,guitar(76,1.7),12.8,-.2,.35);add(x,guitar(83,1.7),12.8,.4,.16)
# Stereo delay gives the solo a live amp tail.
for delay,g in [(.17,.18),(.34,.10)]:
 k=round(delay*R);x[k:]+=x[:-k,::-1].copy()*g
write('victory',x)
# Slow descending minor piano/bell lament, with dark sustained strings.
x=np.zeros((round(6*R),2))
for at,n in zip([0,.8,1.6,2.4],[64,62,59,52]):
 t=np.arange(round(3.3*R))/R;s=sum(np.sin(2*np.pi*hz(n)*k*t)*np.exp(-t*(1.5+k*.5))/k**2 for k in range(1,6))*np.minimum(t/.008,1)
 add(x,s,at,(at/2.4-.5),.45)
for n in [40,47,55]:
 t=np.arange(len(x))/R;s=np.sin(2*np.pi*hz(n)*t)*np.minimum(t/.7,1)*np.minimum((6-t)/2,1)*np.exp(-t*.2);add(x,s,0,0,.08)
k=round(.25*R);x[k:]+=x[:-k,::-1].copy()*.2;write('defeat',x)
for name,notes,d in [('menu-move',[79],.08),('menu-confirm',[67,74,79],.24),('menu-back',[74,67],.18)]:
 x=np.zeros((round((d+.15)*R),2))
 for i,n in enumerate(notes):
  t=np.arange(round(.14*R))/R;s=(np.sin(2*np.pi*hz(n)*t)+.22*np.sin(2*np.pi*hz(n)*2.7*t))*np.minimum(t/.003,1)*np.exp(-t*36);add(x,s,i*d/max(1,len(notes)),0,.3)
 write(name,x)
