"""Voice-only -3dB trim and two damped short echo taps; leave other audio intact."""
from pathlib import Path
import wave,json
import numpy as np
from scipy.signal import butter,sosfilt
root=Path(__file__).resolve().parents[1];src=root/'source-audio/dry-v12';out=root/'dist/assets/audio';R=44100
for p in src.glob('*.wav'):
 with wave.open(str(p)) as w:x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 dry=x*10**(-3/20);wet=sosfilt(butter(2,2600,fs=R,output='sos'),dry);result=np.zeros(len(x)+round(R*.19));result[:len(x)]+=dry
 for delay,level in [(.085,.13),(.17,.055)]:
  n=round(R*delay);result[n:n+len(x)]+=wet*level
 fade=round(R*.012);result[-fade:]*=np.linspace(1,0,fade);assert np.abs(result).max()<.9
 with wave.open(str(out/p.name),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(R);w.writeframes((result*32767).astype('<i2').tobytes())
p=out/'manifest.json';m=json.loads(p.read_text());m['vocal_mix']={'direct_gain_db':-3,'echo_taps_ms':[85,170],'echo_levels':[.13,.055],'echo_lowpass_hz':2600};p.write_text(json.dumps(m,indent=2))
print('Processed',len(list(src.glob('*.wav'))),'voices only: -3dB, damped 85/170ms echo.')
