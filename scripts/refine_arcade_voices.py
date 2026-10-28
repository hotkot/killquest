"""Long vowel-led death cries and restrained arcade-style attack mastering."""
from pathlib import Path
import subprocess,wave,json
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import butter,sosfilt
root=Path(__file__).resolve().parents[1];src=root/'source-audio';out=root/'dist/assets/audio';R=44100

def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar',str(R),'-ac','1','-f','s16le','-']),dtype='<i2').astype(float)/32768

def save(name,x,peak):
 x=np.nan_to_num(x);x=x/max(np.abs(x).max(),1e-6)*peak;n=min(220,len(x)//8);x[:n]*=np.linspace(0,1,n);x[-n:]*=np.linspace(1,0,n)
 with wave.open(str(out/(name+'.wav')),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((x*32767).astype('<i2').tobytes())

def stretch(x,target):
 ratio=(len(x)/R)/target;filters=[]
 while ratio<.5:filters.append('atempo=0.5');ratio/=.5
 while ratio>2:filters.append('atempo=2');ratio/=2
 filters.append(f'atempo={ratio:.7f}')
 raw=subprocess.check_output(['ffmpeg','-v','error','-f','f32le','-ar',str(R),'-ac','1','-i','pipe:0','-af',','.join(filters),'-f','f32le','pipe:1'],input=x.astype('<f4').tobytes())
 return np.frombuffer(raw,dtype='<f4').astype(float)
for i in range(6):
 x=decode(src/f'long-cry-{i:02}.mp3');x-=x.mean();e=np.sqrt(uniform_filter1d(x*x,round(R*.009)));ids=np.flatnonzero(e>max(.005,e.max()*.025));x=x[max(0,ids[0]-round(R*.018)):min(len(x),ids[-1]+round(R*.07))]
 original=len(x)/R;target=[1.15,1.32,1.05,1.4,1.2,1.15][i]
 if original<target:
  # Keep consonantal onset/release at original tempo; prolong the voiced core.
  lead=min(round(R*.085),len(x)//5);tail=min(round(R*.11),len(x)//5);mid=x[lead:-tail]
  middle=stretch(mid,target-(lead+tail)/R)
  # Equal-power joins remove discontinuities introduced by local time stretching.
  def join(a,b):
   n=min(round(R*.006),len(a)//4,len(b)//4);t=np.linspace(0,1,n);return np.r_[a[:-n],a[-n:]*np.cos(t*np.pi/2)+b[:n]*np.sin(t*np.pi/2),b[n:]]
  x=join(join(x[:lead],middle),x[-tail:])
 x=sosfilt(butter(1,75,btype='highpass',fs=R,output='sos'),x);x=np.tanh(x*1.25)
 name=f'bandit-death-{i}' if i<4 else f'hero-death-{i-4}';save(name,x,.84)
 print(name,'source',round(original,3),'final',round(len(x)/R,3),'seconds')
for i in range(4):
 # Return to the unprocessed AI source so refining is reproducible, not cumulative.
 x=decode(src/f'ai-voice-{i:02}.mp3');e=np.sqrt(uniform_filter1d(x*x,round(R*.008)));ids=np.flatnonzero(e>max(.006,e.max()*.035));x=x[max(0,ids[0]-round(R*.016)):min(len(x),ids[-1]+round(R*.045))]
 x=sosfilt(butter(1,75,btype='highpass',fs=R,output='sos'),x);presence=sosfilt(butter(2,[800,3000],btype='bandpass',fs=R,output='sos'),x);x=np.tanh((x+presence*.18)*1.15)
 # A low-level short reflection gives body without burying the direct voice.
 delay=round(R*.032);x=np.r_[x,np.zeros(delay)]+np.r_[np.zeros(delay),x]*.025;save(f'hero-effort-{i}',x,.76)
p=out/'manifest.json';m=json.loads(p.read_text());m['voice_revision']='AI sustained death vowels with pitch-preserving core extension; punch/clarity pass on original short attacks';m['death_voice_source']='source-audio/long-cries-provenance.json';p.write_text(json.dumps(m,indent=2))
