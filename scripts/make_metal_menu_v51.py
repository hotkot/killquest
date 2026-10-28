"""Original KillQuest menu cues and metal/defeat fanfares, reproducible synthesis."""
from pathlib import Path
import wave, subprocess
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
# Three-bar 200 BPM power-metal lick: sixteenth-note runs, harmony, double kick.
beat=60/200;x=np.zeros((round(5*R),2))
phrases=[[76,78,79,83,79,78,76,74,71,74,76,78,79,83,86,83],[79,78,76,74,76,78,79,83,86,83,79,78,76,74,71,74],[76,79,83,88,86,83,79,76,74,76,79,83,86,88,90,88]]
for bar,phrase in enumerate(phrases):
 base=bar*4*beat
 for j,n in enumerate(phrase):
  at=base+j*beat/4;add(x,guitar(n,.14),at,-.35,.3);add(x,guitar(n+7,.14),at,.45,.12)
 for j in range(8):
  at=base+j*beat/2
  for n in [40,47]:add(x,guitar(n,.17,False),at,.25,.12)
  drums(x,at)
 for j in [1,3]:drums(x,base+j*beat,True)
add(x,guitar(88,1.4),3.6,-.3,.3);add(x,guitar(83,1.4),3.6,.4,.18)
for delay,g in [(.12,.16),(.24,.08)]:
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
  t=np.arange(round(.14*R))/R;s=(np.sin(2*np.pi*hz(n-12)*t)+.22*np.sin(2*np.pi*hz(n-12)*2.7*t))*np.minimum(t/.003,1)*np.exp(-t*36);add(x,s,i*d/max(1,len(notes)),0,.3)
 write(name,x)

# 16-bar 160 BPM fantasy-metal menu anthem: galloping stereo guitars, soaring
# harmonized leads, analog-style pad, bass and gated snare. Wrap delayed tails
# into the beginning for a continuous musical loop without fades.
beat=60/160;duration=16*4*beat;x=np.zeros((round(duration*R),2))
roots=[40,36,43,38]
melodies=[[64,67,71,76,74,71,67,69],[72,71,67,64,67,71,74,72],[67,71,74,79,78,74,71,74],[69,74,78,81,79,78,74,71]]
for bar in range(16):
 base=bar*4*beat;root=roots[(bar//2)%4]
 for j in range(4):
  for offset in [0,.5,.75]:
   at=base+(j+offset)*beat
   for pan,detune in [(-.8,-.04),(.8,.04)]:
    add(x,guitar(root+detune,.19,False),at,pan,.13)
    add(x,guitar(root+7+detune,.19,False),at,pan,.07)
  t=np.arange(round(beat*R))/R;add(x,np.sin(2*np.pi*hz(root-12)*t)*np.exp(-t*6),base+j*beat,0,.22)
  drums(x,base+j*beat,j%2==1)
  if j%2==0:drums(x,base+(j+.75)*beat)
 for j,n in enumerate(melodies[(bar//2)%4]):
  at=base+j*beat/2
  add(x,guitar(n,beat*.8),at,-.3,.17)
  if bar>=8:add(x,guitar(n+7,beat*.8),at,.45,.08)
  t=np.arange(round(.12*R))/R;add(x,rng.normal(0,1,len(t))*np.exp(-t*60),at,.6,.045)
 # Dark warm pad voicing, with soft attack/release per bar.
 t=np.arange(round(4*beat*R))/R;envelope=np.minimum(t/.12,1)*np.minimum((4*beat-t)/.12,1)
 for n in [root+12,root+19,root+27]:add(x,np.sin(2*np.pi*hz(n)*t)*envelope,base,-.2,.035)
for delay,g in [(.1875,.12),(.375,.06)]:x+=np.roll(x.copy()[:,::-1],round(delay*R),axis=0)*g
x=np.tanh(x*.9);x=x/max(abs(x).max(),1e-6)*.78
p=out/'killquest-menu.wav'
with wave.open(str(p),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((x*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-codec:a','libmp3lame','-b:a','192k',str(out/'killquest-menu.mp3')],check=True)
p.unlink()
