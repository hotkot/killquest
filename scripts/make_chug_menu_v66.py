"""Iron at the Gate: original two-minute 112 BPM sampled-guitar menu groove.
Guitar performance samples: Skimel, CC BY-SA 4.0; see source-audio/menu-v66/CREDITS.md.
"""
from pathlib import Path
import numpy as np, subprocess, wave, json
from scipy.signal import butter,sosfilt,resample_poly
from functools import lru_cache
root=Path(__file__).resolve().parents[1];out=root/'source-audio/menu-v66';out.mkdir(exist_ok=True)
R=44100;BPM=112;beat=60/BPM;bars=56;duration=bars*4*beat;N=round(duration*R);rng=np.random.default_rng(6607)
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(out/'guitar-source.ogg'),'-ar',str(R),'-ac','1','-f','f32le','-'])
recording=np.frombuffer(raw,dtype='<f4');tracks={k:np.zeros((N,2),dtype=np.float32) for k in ['guitar-left','guitar-right','bass','drums']}
def filt(x,f,kind='lowpass',order=2):return sosfilt(butter(order,f,btype=kind,fs=R,output='sos'),x)
def add(name,s,at,gain=1,pan=0):
 i=round(at*R);start=max(0,-i);i=max(i,0);n=min(len(s)-start,N-i)
 if n>0:tracks[name][i:i+n]+=s[start:start+n,None]*gain*np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
def envelope(n,attack=.002,release=.025):
 e=np.ones(n);a=min(round(R*attack),n);b=min(round(R*release),n);e[:a]*=np.linspace(0,1,a);e[-b:]*=np.linspace(1,0,b);return e
@lru_cache(None)
def guitar(note,muted,variant,length):
 start=[3.365,3.545,3.735,3.915][variant] if muted else .115+variant*.003
 s=recording[round(start*R):round((start+(.14 if muted else 1.2))*R)]
 # Resample a real picked A2 power chord, rather than synthesizing bright lead tones.
 rate=2**((note-45)/12);s=resample_poly(s,1000,round(1000*rate));n=round(length*R)
 s=np.pad(s,(0,max(0,n-len(s))))[:n].copy();s=filt(filt(s,70,'highpass'),3600)
 s*=envelope(n,release=.025 if muted else .055)
 if muted:s*=np.exp(-np.arange(n)/R*7)
 s/=max(.05,float(abs(s).max()));return s.astype(np.float32)
# Original two-bar motifs: rests, syncopation, low D pedal and occasional chord answers.
A=[[(0,38,1),(2,38,1),(3,38,1),(6,38,1),(8,38,1),(10,38,1),(11,38,1),(14,41,0)],[(0,38,1),(3,38,1),(4,38,1),(7,38,1),(8,39,0),(11,38,1),(12,36,0),(15,38,1)]]
B=[[(0,38,0),(3,38,1),(4,38,1),(6,38,1),(8,43,0),(11,38,1),(12,41,0),(14,39,1)],[(0,38,1),(2,38,1),(5,38,1),(6,38,1),(8,36,0),(10,38,1),(12,39,0),(15,38,1)]]
C=[[(0,38,0),(4,38,1),(6,38,1),(8,39,0),(12,36,0)],[(0,38,1),(4,38,1),(7,38,1),(8,41,0),(12,39,0),(14,38,1)]]
sections=[(0,4,'entry'),(4,20,'groove'),(20,28,'chord-response'),(28,36,'half-time'),(36,40,'bass-pocket'),(40,52,'groove-return'),(52,56,'turnaround')]
for bar in range(bars):
 at=bar*4*beat;section=next(name for lo,hi,name in sections if lo<=bar<hi)
 pattern=(B if section=='chord-response' else C if section in ['half-time','bass-pocket'] else A)[bar%2]
 if section=='entry' and bar<2:pattern=[n for n in pattern if n[0]%4==0 or n[0]==14]
 if section=='turnaround' and bar>=54:pattern=[(0,38,1),(2,38,1),(4,36,0),(8,39,0),(12,38,0)]
 for j,(slot,note,muted) in enumerate(pattern):
  length=.12 if muted else (.46 if slot<=12 else .25)
  if section=='bass-pocket' and slot not in [0,8]:continue
  for side,pan,v in [('guitar-left',-.82,0),('guitar-right',.82,1)]:
   timing=(.004 if v else 0)+rng.uniform(-.0015,.0015)
   add(side,guitar(note,muted,(bar+j+v*2)%4,length),at+slot*beat/4+timing,.25*(.78 if section=='bass-pocket' else 1)*(1+rng.uniform(-.045,.045)),pan)
  # Picked bass locks to the guitar's low root, with an audible upper harmonic.
  hz=440*2**((note-12-69)/12);d=.17 if muted else length;t=np.arange(round(d*R))/R
  bass=np.sin(2*np.pi*hz*t)+.5*np.sin(2*np.pi*hz*2*t)+.13*np.sin(2*np.pi*hz*3*t)
  bass=np.tanh(bass*1.35)*np.exp(-t*4)*envelope(len(t),.003,.025)
  add('bass',bass,at+slot*beat/4,.19)
 # Drums stay solid and sparse, with kick accents following the chugs.
 kicks=[0,3,6,8,11,14] if bar%2==0 else [0,4,7,10,12]
 if section in ['half-time','bass-pocket']:kicks=[0,6,8,14]
 if section=='entry' and bar<2:kicks=[0,8]
 for slot in kicks:
  t=np.arange(round(.20*R))/R;phase=2*np.pi*(48*t+1.4*(1-np.exp(-t*42)))
  kick=(np.sin(phase)*np.exp(-t*23)+.12*filt(rng.normal(size=len(t)),3500)*np.exp(-t*160))*envelope(len(t),.001,.025)
  add('drums',kick,at+slot*beat/4,.42)
 for slot in ([8] if section in ['half-time','bass-pocket'] else [4,12]):
  t=np.arange(round(.22*R))/R;noise=filt(rng.normal(size=len(t)),[500,6500],'bandpass')
  snare=(noise*.68*np.exp(-t*24)+.6*np.sin(2*np.pi*185*t)*np.exp(-t*35)+.22*np.sin(2*np.pi*330*t)*np.exp(-t*38))*envelope(len(t),.001,.025)
  add('drums',snare,at+slot*beat/4,.28)
 for slot in range(0,16,2):
  t=np.arange(round(.075*R))/R;hat=filt(rng.normal(size=len(t)),[4500,10500],'bandpass')*np.exp(-t*70)*envelope(len(t),.001,.014)
  add('drums',hat,at+slot*beat/4,.035 if slot%4 else .026,.35)
 if bar in [4,20,28,40,52]:
  t=np.arange(round(.65*R))/R;crash=filt(rng.normal(size=len(t)),[2500,10500],'bandpass')*np.exp(-t*8)*envelope(len(t),.003,.05)
  add('drums',crash,at,.06,-.3)
 if bar in [19,27,35,51]:
  for j,note in enumerate([52,49,45]):
   t=np.arange(round(.15*R))/R;hz=440*2**((note-69)/12);tom=np.sin(2*np.pi*hz*t)*np.exp(-t*25)*envelope(len(t),.001,.02)
   add('drums',tom,at+(13+j)*beat/4,.18,-.4+j*.4)
# Independent stem balance. No atmosphere or bright lead competes with the riff.
targets={'guitar-left':.075,'guitar-right':.075,'bass':.078,'drums':.088};mix=np.zeros((N,2),np.float32);metrics={}
for name,x in tracks.items():
 blocks=x[:N//4410*4410].reshape(-1,4410,2);rms=np.sqrt(np.mean(blocks**2,axis=(1,2)));active=rms[rms>rms.max()*.18];gain=targets[name]/max(float(np.median(active)),1e-5);gain=min(gain,.75/max(float(abs(x).max()),1e-5));x*=gain;mix+=x;metrics[name]={'active_rms':float(np.median(active)*gain),'gain_db':float(20*np.log10(gain))}
 # Stems preserve the original arrangement for future mix adjustments.
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(R),'-ac','2','-i','-','-c:a','flac',str(out/(name+'.flac'))],stdin=subprocess.PIPE);proc.communicate(x.astype('<f4').tobytes());assert proc.returncode==0
mix=np.tanh(mix*1.1);mix*=.82/max(float(abs(mix).max()),1e-5)
# Gentle boundaries prevent clicks; composition returns to the opening low-D groove.
fade=round(.012*R);mix[:fade]*=np.linspace(0,1,fade)[:,None];mix[-fade:]*=np.linspace(1,0,fade)[:,None]
master=out/'iron-at-the-gate.wav'
with wave.open(str(master),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(master),'-af','loudnorm=I=-17:TP=-1.5:LRA=7','-ar',str(R),'-codec:a','libmp3lame','-b:a','192k',str(root/'dist/assets/audio/killquest-menu-chug-v66.mp3')],check=True)
master.unlink();(out/'mix-report.json').write_text(json.dumps({'title':'Iron at the Gate','bpm':BPM,'duration_seconds':duration,'bars':bars,'key':'D pedal','sections':sections,'stems':metrics,'loudness_target_lufs':-17,'guitar_source':'Skimel, CC BY-SA 4.0'},indent=2)+'\n')
print('Rendered',duration,'seconds;',metrics)
