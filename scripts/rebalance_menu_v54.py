"""Rebalance existing 120-second stems by active-block RMS, preserving section dynamics."""
from pathlib import Path
import numpy as np,subprocess,json,wave
root=Path(__file__).resolve().parents[1];source=root/'source-audio/menu-v53';out=root/'dist/assets/audio';report=root/'source-audio/menu-v54';report.mkdir(exist_ok=True)
R=44100
# The riff remains the lead, while bass and drums occupy comparable space;
# answering guitar and atmosphere remain quieter, audible supporting layers.
targets={'rhythm-guitars':.070,'bass':.065,'drums':.075,'support-guitar':.045,'atmosphere':.028}
mix=np.zeros((R*120,2),dtype=np.float32);metrics={}
for name,target in targets.items():
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source/(name+'.flac')),'-f','f32le','-'])
 x=np.frombuffer(raw,dtype='<f4').reshape(-1,2);assert len(x)==R*120
 blocks=x[:len(x)//(R//5)*(R//5)].reshape(-1,R//5,2)
 levels=np.sqrt(np.mean(blocks*blocks,axis=(1,2)));active=levels[levels>levels.max()*.15];before=float(np.median(active))
 gain=target/max(before,1e-7);gain=min(gain,.55/max(float(abs(x).max()),1e-7));mix+=x*gain
 metrics[name]={'active_rms_before':before,'active_rms_after':before*gain,'gain_db':float(20*np.log10(gain)),'target_active_rms':target}
 print(name,round(metrics[name]['gain_db'],2),'dB; active RMS',round(before*gain,4))
# One shared master gain keeps the revised balance, without clipping or flattening transients.
master=.78/max(float(abs(mix).max()),1e-7);mix*=master
fade=round(.005*R);mix[:fade]*=np.linspace(0,1,fade)[:,None];mix[-fade:]*=np.linspace(1,0,fade)[:,None]
p=out/'killquest-menu-balanced-v54.wav'
with wave.open(str(p),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-codec:a','libmp3lame','-b:a','192k',str(out/'killquest-menu-balanced-v54.mp3')],check=True);p.unlink()
(report/'mix-settings.json').write_text(json.dumps({'duration_seconds':120,'method':'median active 200ms block RMS with per-stem peak headroom; shared master gain','master_gain_db':float(20*np.log10(master)),'stems':metrics},indent=2)+'\n')
