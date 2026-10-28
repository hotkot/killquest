"""Original 112 BPM E-minor thrash preview. Guitar recording: Skimel, CC BY-SA 4.0.
New slower riffs/arrangement; modeled bass and acoustic-style drums; no copied melodies. Not time-stretched.
"""
from pathlib import Path
import numpy as np,subprocess,wave,json
from scipy.signal import butter,sosfilt,resample_poly
from functools import lru_cache
W=Path(__file__).parent;ROOT=Path(__file__).resolve().parents[2];R=44100;BPM=112;beat=60/BPM;bars=28;D=bars*4*beat;N=round(D*R);rng=np.random.default_rng(129)
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'source-audio/menu-v66/guitar-source.ogg'),'-ar',str(R),'-ac','1','-f','f32le','-']),dtype='<f4')
tracks={name:np.zeros((N,2),dtype=np.float32) for name in ['guitar-L','guitar-R','bass','drums','room']}
def filt(x,f,kind='lowpass'):return sosfilt(butter(2,f,btype=kind,fs=R,output='sos'),x)
def envelope(n,attack=.0015,release=.015):
 e=np.ones(n);k=min(n,int(R*attack));j=min(n,int(R*release));e[:k]*=np.linspace(0,1,k);e[-j:]*=np.linspace(1,0,j);return e

def add(name,s,at,gain=1,pan=0):
 k=round(at*R);trim=max(0,-k);k=max(0,k);n=min(len(s)-trim,N-k)
 if n<=0:return
 tracks[name][k:k+n]+=s[trim:trim+n,None]*gain*np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
@lru_cache(None)
def guitar(note,muted,v,length):
 start=[3.365,3.545,3.735,3.915][v%4] if muted else .115+v*.003
 s=a[round(start*R):round((start+(.145 if muted else 1.2))*R)].copy();s=resample_poly(s,1000,round(1000*2**((note-45)/12)));n=round(length*R);s=np.pad(s,(0,max(0,n-len(s))))[:n];s=filt(filt(s,85,'highpass'),4700)
 if muted:s*=np.exp(-np.arange(n)/R*5)
 s*=envelope(n,release=.012 if muted else .035);return (s/max(abs(s).max(),.02)).astype(np.float32)
# Strict E natural minor: E F# G A B C D, including fifths in power chords.
# Voiced power-chord roots E, G, A, B, C have diatonic fifths; no F/Bb chromatic stabs.
A=[[(0,40,0),(4,40,1),(7,43,0),(10,40,1),(12,47,0)],[(0,40,1),(2,40,1),(4,45,0),(8,43,0),(12,40,0)],[(0,40,0),(4,40,1),(6,40,1),(9,48,0),(12,47,0)],[(0,45,0),(4,43,0),(8,40,1),(10,40,1),(14,40,0)]]
B=[[(0,48,0),(4,47,0),(8,40,1),(10,40,1),(12,43,0)],[(0,45,0),(4,47,0),(8,40,0),(14,40,1)],[(0,48,0),(4,43,0),(7,45,0),(10,47,0),(14,40,1)],[(0,47,0),(6,45,0),(10,43,0),(14,40,0)]]
C=[[(0,40,0),(8,43,0),(12,47,0)],[(0,48,0),(8,45,0)],[(0,43,0),(6,45,0),(10,47,0)],[(0,48,0),(8,47,0),(14,40,1)]]
allowed={4,6,7,9,11,0,2}
assert all(note%12 in allowed and (note+7)%12 in allowed for riff in [A,B,C] for pattern in riff for _,note,_ in pattern)
for bar in range(bars):
 at=bar*4*beat;half=False;bridge=16<=bar<20;last=bar==27
 pattern=(A if bar<8 or bar>=20 else B if bar<16 else C)[bar%4]
 if last:pattern=[(0,40,0),(4,40,1),(6,40,1),(8,40,0)]
 for j,(slot,note,muted) in enumerate(pattern):
  nextslot=pattern[j+1][0] if j+1<len(pattern) else 16;length=min(.165 if muted else .65,max(.065,(nextslot-slot)*beat/4-.008))
  if last and slot==8:length=2*beat
  for side in [0,1]:add('guitar-L' if side==0 else 'guitar-R',guitar(note,muted,(bar+j+side*2)%4,round(length,4)),at+slot*beat/4+(.004 if side else 0)+rng.uniform(-.0018,.0018),.32*rng.uniform(.94,1.03),-.86 if side==0 else .86)
  t=np.arange(round((.165 if muted else length)*R))/R;hz=440*2**((note-12-69)/12);pluck=(np.sin(2*np.pi*hz*t)+.5*np.sin(4*np.pi*hz*t)+.18*np.sin(6*np.pi*hz*t));s=np.tanh(pluck*1.3)*np.exp(-t*(7 if muted else 3))*envelope(len(t),.002,.02);add('bass',s,at+slot*beat/4,.23)
 # Heavy rock backbeat; kick follows the riff, leaving deliberate breathing room.
 kicks=[0,6,9,14] if bar%2==0 else [0,2,8,11]
 if bridge:kicks=[0,6,10]
 if bar>=24:kicks=[0,2,6,8,11,14]
 if last:kicks=[0,4,6,8]
 for slot in kicks:
  t=np.arange(round(.18*R))/R;phase=2*np.pi*(49*t+1.7*(1-np.exp(-t*43)));x=(np.sin(phase)*np.exp(-t*26)+.16*filt(rng.normal(size=len(t)),[1800,4700],'bandpass')*np.exp(-t*160))*envelope(len(t),.0007,.025);add('drums',x,at+slot*beat/4+rng.uniform(-.001,.001),.51*rng.uniform(.92,1.03))
 for slot in ([8] if half else [4,12]):
  if last and slot>8:continue
  t=np.arange(round(.24*R))/R;noise=filt(rng.normal(size=len(t)),[700,7500],'bandpass');body=(np.sin(2*np.pi*182*t)*np.exp(-t*35)+.33*np.sin(2*np.pi*331*t)*np.exp(-t*29));x=(noise*.55*np.exp(-t*27)+body*.75)*envelope(len(t),.001,.025);when=at+slot*beat/4+rng.uniform(-.0015,.0025);add('drums',x,when,.35);add('room',x,when+.027,.032,-.15)
 for slot in range(0,16,2):
  if last and slot>=8:continue
  t=np.arange(round(.075*R))/R;x=filt(rng.normal(size=len(t)),[4200,10000],'bandpass')*np.exp(-t*65)*envelope(len(t),.001,.015);add('drums',x,at+slot*beat/4,.035*rng.uniform(.75,1.15),.32)
 if bar in [0,4,8,12,16,20,24,27]:
  t=np.arange(round(.8*R))/R;metal=sum(np.sin(2*np.pi*f*t+rng.uniform(0,6)) for f in [3811,4523,5719,6947,8191])/5;x=(filt(rng.normal(size=len(t)),[2600,10500],'bandpass')*.6+metal*.15)*np.exp(-t*6)*envelope(len(t),.002,.03);add('drums',x,at,.075,-.35)
 if bar in [7,15,19,23,26]:
  for j,slot in enumerate([12,13,14,15]):
   t=np.arange(round(.16*R))/R;f=[170,145,120,95][j];x=(np.sin(2*np.pi*(f*t+.08*(1-np.exp(-t*35))))*np.exp(-t*25)+.08*filt(rng.normal(size=len(t)),2400)*np.exp(-t*35))*envelope(len(t),.001,.02);add('drums',x,at+slot*beat/4,.22,-.55+j*.35)
# Mild room, controlled low end and independently balanced rhythm section.
mix=np.zeros((N,2),np.float32);metrics={};targets={'guitar-L':.075,'guitar-R':.075,'bass':.076,'drums':.10,'room':.009}
for name,x in tracks.items():
 blocks=x[:N//4410*4410].reshape(-1,4410,2);rms=np.sqrt(np.mean(blocks**2,axis=(1,2)));active=rms[rms>rms.max()*.2];gain=min(targets[name]/max(np.median(active),1e-5),.8/max(abs(x).max(),1e-5));mix+=x*gain;metrics[name]=float(gain)
mix=np.tanh(mix*1.08);mix*=.9/max(abs(mix).max(),1e-5);mix[:180]*=np.linspace(0,1,180)[:,None];mix[-int(R*.5):]*=np.linspace(1,0,int(R*.5))[:,None]
with wave.open(str(W/'master.wav'),'wb') as f:f.setparams((2,2,R,0,'NONE','not compressed'));f.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(W/'master.wav'),'-af','loudnorm=I=-14:TP=-1.2:LRA=7','-ar',str(R),'-c:a','libmp3lame','-b:a','256k','-metadata','title=KillQuest — Ash and Iron — E Minor Preview','-metadata','artist=KillQuest; sampled guitar by Skimel','-metadata','copyright=Music remix CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/','-metadata','comment=Original 112 BPM E natural minor riffs and arrangement. No chromatic riffs. Guitar sample: Skimel, https://commons.wikimedia.org/wiki/File:Distorted_guitar_Palm_mute_off_and_on.ogg . Cropped, transposed, EQ, double-tracked. Preview only, not implemented.',str(W/'KillQuest-Ash-and-Iron-E-Minor-Preview.mp3')],check=True)
(W/'mix-report.json').write_text(json.dumps({'bpm':BPM,'duration':D,'stems':metrics,'sections':['0-17.14 main groove','17.14-34.29 riff answer','34.29-42.86 heavy bridge','42.86-60 main riff return and ending']},indent=2))
print('Rendered',D,'seconds')
