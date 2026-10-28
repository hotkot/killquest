"""Install genuine AI Voice Generator output, trimmed and lightly mastered."""
from pathlib import Path
import subprocess,wave,json,io
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import butter,sosfilt,resample_poly
root=Path(__file__).resolve().parents[1];src=root/'source-audio';out=root/'dist/assets/audio';R=44100
banks={}
for i in range(10):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(src/f'ai-voice-{i:02}.mp3'),'-ar',str(R),'-ac','1','-f','s16le','-'])
 x=np.frombuffer(raw,dtype='<i2').astype(float)/32768;x-=x.mean();e=np.sqrt(uniform_filter1d(x*x,round(R*.008)))
 ids=np.flatnonzero(e>max(.006,e.max()*.035));assert len(ids)>0
 x=x[max(0,ids[0]-round(R*.022)):min(len(x),ids[-1]+round(R*.055))]
 x=sosfilt(butter(1,65,btype='highpass',fs=R,output='sos'),x);a=np.abs(x);x=np.sign(x)*np.where(a>.25,.25*(a/.25)**.85,a)
 banks[i]=x
for prefix in ['hero-effort','hero-pain','hero-death','bandit-death']:
 for p in out.glob(prefix+'-*.wav'):p.unlink()
roles={'hero-effort':[0,1,2,3],'hero-pain':[8,9],'hero-death':[8,9],'bandit-death':[4,5,6,7]}
for role,ids in roles.items():
 for j,i in enumerate(ids):
  x=banks[i].copy()
  if role=='hero-death':x=resample_poly(x,110,100)
  x=x/max(np.max(np.abs(x)),1e-8)*(.72 if role=='hero-effort' else .55 if role=='hero-pain' else .8)
  fade=min(round(R*.006),len(x)//10);x[:fade]*=np.linspace(0,1,fade);x[-fade:]*=np.linspace(1,0,fade)
  with wave.open(str(out/f'{role}-{j}.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((x*32767).astype('<i2').tobytes())
  print(role,j,round(len(x)/R,3),'seconds')
p=out/'manifest.json';m=json.loads(p.read_text());m['voice_variants']={k:len(v) for k,v in roles.items()};m['vocals']='AI Voice Generator TTS-generated vocalizations; deep barbarian / normal bandit; no procedural voice source';m['voice_revision']='real model-generated voice samples, trimmed silences and lightly compressed';m['voice_source']='source-audio/ai-voice-provenance.json';p.write_text(json.dumps(m,indent=2))
