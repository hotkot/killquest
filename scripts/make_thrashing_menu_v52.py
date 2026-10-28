"""Original low-register riff-driven thrash menu music, physically plucked guitar model."""
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfilt
import wave,subprocess
R=44100;rng=np.random.default_rng(521);beat=60/144;duration=16*4*beat
mix=np.zeros((round(duration*R),2));out=Path(__file__).resolve().parents[1]/'dist/assets/audio'
def hz(n):return 440*2**((n-69)/12)
def add(s,at,gain=1,pan=0):
 i=round(at*R);n=min(len(s),len(mix)-i)
 if n>0:mix[i:i+n]+=s[:n,None]*gain*np.array([1-pan*.7,1+pan*.7])
def guitar(note,d,muted,detune):
 n=max(12,round(R/(hz(note)*detune)));size=round(d*R);cycle=rng.normal(0,1,n);cycle-=cycle.mean();parts=[]
 for _ in range(size//n+1):
  parts.append(cycle.copy());cycle=(cycle+np.roll(cycle,1))*.499
 x=np.concatenate(parts)[:size];t=np.arange(size)/R
 x*=np.minimum(t/.002,1)*np.exp(-t/(.048 if muted else .28))*np.minimum((d-t)/.012,1)
 # Bridge pickup, amp overdrive and a dark guitar cabinet.
 x=sosfilt(butter(1,115,'highpass',fs=R,output='sos'),x)
 x=np.tanh(x*16)
 x=sosfilt(butter(3,3100,fs=R,output='sos'),x)
 return x
# Four motifs: low-E chugs, chromatic pickup, syncopated power chords and descending turnaround.
patterns=[[(0,40,1),(.5,40,1),(.75,40,1),(1,40,1),(1.5,41,1),(1.75,40,1),(2,43,0),(2.75,40,1),(3,40,1),(3.5,46,1),(3.75,43,1)],[(0,40,1),(.5,40,1),(1,47,0),(1.75,46,1),(2,45,0),(2.75,43,1),(3,41,0),(3.75,40,1)],[(0,40,1),(.25,40,1),(1,40,1),(1.5,40,1),(2,43,0),(2.5,42,1),(3,41,0),(3.5,40,1)],[(0,40,0),(1,43,0),(2,41,0),(3,38,0),(3.5,39,1),(3.75,40,1)]]
for bar in range(16):
 base=bar*4*beat;pattern=patterns[(bar//2)%4]
 for pos,n,muted in pattern:
  at=base+pos*beat;d=.16 if muted else .32
  for pan,detune in [(-.9,.997),(.9,1.003)]:
   add(guitar(n,d,muted,detune),at,.22,pan)
   if not muted:add(guitar(n+7,d,False,detune),at,.10,pan)
  t=np.arange(round(d*R))/R;add(np.sin(2*np.pi*hz(n-12)*t)*np.minimum(t/.004,1)*np.exp(-t*9),at,.19)
 for j in range(4):
  at=base+j*beat;t=np.arange(round(.22*R))/R
  kick=np.sin(2*np.pi*(46*t+1.8*(1-np.exp(-t*38))))*np.exp(-t*26)
  add(kick,at,.3)
  if j%2:
   snare=rng.normal(0,1,len(t))*np.exp(-t*25)+.6*np.sin(2*np.pi*180*t)*np.exp(-t*32)
   snare=sosfilt(butter(1,5000,fs=R,output='sos'),snare);add(snare,at,.12)
 for j in range(8):
  t=np.arange(round(.08*R))/R;hat=sosfilt(butter(2,6000,'highpass',fs=R,output='sos'),rng.normal(0,1,len(t)))*np.exp(-t*70)
  add(hat,base+j*beat/2,.025,.5)
# Small cabinet room, wrap tails to preserve loop continuity, no high-register lead.
mix+=np.roll(mix[:,::-1].copy(),round(.037*R),axis=0)*.06
mix=np.tanh(mix*.9);mix*=.72/max(abs(mix).max(),1e-6)
p=out/'killquest-menu-thrash-v52.wav'
with wave.open(str(p),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-codec:a','libmp3lame','-b:a','192k',str(out/'killquest-menu-thrash-v52.mp3')],check=True)
p.unlink();print('Original riff-driven stereo thrash loop:',round(duration,3),'seconds, 144 BPM')
