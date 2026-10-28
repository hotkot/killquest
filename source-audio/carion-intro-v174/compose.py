from pathlib import Path
import numpy as np, subprocess, wave, json
from scipy.signal import butter,sosfilt,resample_poly
from functools import lru_cache
W=Path(__file__).resolve().parent
R=44100; BPM=128; beat=60/BPM; N=34*R; rng=np.random.default_rng(297)
source=Path(__file__).resolve().parents[1]/'menu-v66/guitar-source.ogg'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-ar',str(R),'-ac','1','-f','f32le','-']),dtype='<f4')
tracks={n:np.zeros((N,2),np.float32) for n in ['rhythm','bass','drums','lead','room']}
def filt(x,f,kind='lowpass'):return sosfilt(butter(2,f,btype=kind,fs=R,output='sos'),x)
def env(n,release=.025):
 e=np.ones(n);k=min(n,90);j=min(n,round(R*release));e[:k]*=np.linspace(0,1,k);e[-j:]*=np.linspace(1,0,j);return e
def add(name,s,t,g=1,pan=0):
 k=round(t*R);n=min(len(s),N-k)
 if n>0 and k>=0:tracks[name][k:k+n]+=s[:n,None]*g*np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
@lru_cache(None)
def guitar(note,muted,v,d):
 start=[3.365,3.545,3.735,3.915][v%4] if muted else .115+v*.003
 s=a[round(start*R):round((start+(.145 if muted else 1.5))*R)].copy()
 s=resample_poly(s,1000,round(1000*2**((note-45)/12)))
 n=round(d*R);s=np.pad(s,(0,max(0,n-len(s))))[:n];s=filt(filt(s,85,'highpass'),4800)
 if muted:s*=np.exp(-np.arange(n)/R*4)
 s*=env(n);return (s/max(abs(s).max(),.02)).astype(np.float32)
def bass(note,d):
 t=np.arange(round(d*R))/R;f=440*2**((note-12-69)/12)
 return np.tanh(1.5*(np.sin(2*np.pi*f*t)+.33*np.sin(4*np.pi*f*t)))*np.exp(-t*3)*env(len(t))
def drum(kind):
 d={'kick':.2,'snare':.25,'hat':.09,'crash':1.1,'tom':.22}[kind];t=np.arange(round(d*R))/R;n=rng.normal(size=len(t))
 if kind=='kick':s=np.sin(2*np.pi*(49*t+1.7*(1-np.exp(-t*43))))*np.exp(-t*25)+.1*filt(n,[1900,4800],'bandpass')*np.exp(-t*150)
 elif kind=='snare':s=.65*filt(n,[700,7800],'bandpass')*np.exp(-t*26)+.8*np.sin(2*np.pi*182*t)*np.exp(-t*32)
 elif kind=='hat':s=filt(n,[4400,11000],'bandpass')*np.exp(-t*70)
 elif kind=='tom':s=np.sin(2*np.pi*125*t)*np.exp(-t*22)+.12*filt(n,2200)*np.exp(-t*30)
 else:s=filt(n,[2800,11000],'bandpass')*np.exp(-t*5)*.6
 return s*env(len(t))
# Original riff vocabulary: low E pedal, short answering chord stabs,
# offbeat rests and descending turnarounds. No quoted melody or riff.
A=[(0,40,0),(3,40,1),(4,40,1),(6,43,0),(8,45,0),(11,40,1),(12,40,1),(14,38,0)]
B=[(0,40,0),(2,40,1),(3,40,1),(6,40,1),(8,47,0),(10,45,0),(13,43,0),(15,40,1)]
C=[(0,45,0),(3,45,1),(4,45,1),(7,48,0),(8,43,0),(11,43,1),(12,43,1),(14,38,0)]
D=[(0,40,0),(3,40,1),(4,40,1),(6,43,0),(9,45,0),(12,47,0),(14,38,0)]
patterns=[A,B,A,D,A,B,C,D,C,D,A,B,A,D,C,D,A,[(0,40,0)]]
for bar,pattern in enumerate(patterns):
 at=bar*4*beat;final=bar==17
 for j,(slot,note,muted) in enumerate(pattern):
  nextslot=pattern[j+1][0] if j+1<len(pattern) else 16
  d=34-at if final else min(.12 if muted else .5,(nextslot-slot)*beat/4-.015)
  for side in [-1,1]:
   add('rhythm',guitar(note,muted,(bar+j+(side+1))%4,round(d,4)),at+slot*beat/4+(.005 if side==1 else 0),.34*rng.uniform(.96,1.03),side*.87)
  add('bass',bass(note,d),at+slot*beat/4,.28)
 # Hook is carried by the rhythm guitars. Short low-register lead answers
 # appear at phrase ends, leaving space for the riff and on-screen story.
 if bar in [3,7,11,15]:
  for j,note in enumerate([64,67,69,67,66,64]):
   t=at+(9+j)*beat/4;d=beat*.46
   add('lead',guitar(note,False,j%4,round(d,4)),t,.09,-.18)
   add('room',guitar(note,False,j%4,round(d,4)),t+.14,.014,.5)
 if bar in [12,14,16]:
  for j,note in enumerate([64,67,71,69]):
   t=at+j*beat;d=beat*.7
   add('lead',guitar(note,False,j%4,round(d,4)),t,.065,-.15)
 if final:
  add('drums',drum('kick'),at,.58);add('drums',drum('crash'),at,.12,-.3)
  continue
 # Strong backbeat, syncopated kick, quieter eighth-note hats.
 for slot in ([0,3,6,8,11,14] if bar%2==0 else [0,2,6,8,10,15]):add('drums',drum('kick'),at+slot*beat/4,.56)
 for slot in [4,12]:
  hit=drum('snare');add('drums',hit,at+slot*beat/4,.39)
  add('room',hit,at+slot*beat/4+.026,.025,.1)
 for slot in range(0,16,2):add('drums',drum('hat'),at+slot*beat/4,.045*rng.uniform(.8,1.12),.35)
 if bar in [0,4,8,12,16]:add('drums',drum('crash'),at,.10,-.35)
 if bar in [7,15]:
  for j in range(4):add('drums',drum('tom'),at+(12+j)*beat/4,.20,-.5+j*.3)
mix=np.zeros((N,2),np.float32);report={}
for name,target in {'rhythm':.125,'bass':.095,'drums':.115,'lead':.035,'room':.009}.items():
 x=tracks[name];rms=np.sqrt(np.mean(x.reshape(-1,4410,2)**2,axis=(1,2)));active=rms[rms>rms.max()*.15]
 gain=min(target/max(np.median(active),1e-5),.82/max(abs(x).max(),1e-5));mix+=x*gain;report[name]=float(gain)
mix=np.tanh(mix*1.08);mix*=.92/max(abs(mix).max(),1e-5)
mix[:180]*=np.linspace(0,1,180)[:,None];mix[-round(.7*R):]*=np.linspace(1,0,round(.7*R))[:,None]
with wave.open(str(W/'master.wav'),'wb') as f:f.setparams((2,2,R,0,'NONE','not compressed'));f.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(W/'master.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=7','-ar',str(R),'-c:a','aac','-b:a','256k','-metadata','title=KillQuest — Break the Gates','-metadata','artist=KillQuest; guitar sample by Skimel','-metadata','copyright=CC BY-SA 4.0; guitar source https://commons.wikimedia.org/wiki/File:Distorted_guitar_Palm_mute_off_and_on.ogg',str(W/'score.m4a')],check=True)
(W/'arrangement.json').write_text(json.dumps({'bpm':BPM,'duration':34,'tonality':'E-centered guitar riff with G, A and D answering stabs','mix':report,'provenance':'Original riffs and arrangement; transposed guitar recording by Skimel, CC BY-SA 4.0; modeled bass and drums. No quoted music.'},indent=2))
print('Rendered original riff-led thrash preview, 34 seconds, 128 BPM')
