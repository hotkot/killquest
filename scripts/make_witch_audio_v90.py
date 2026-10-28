"""Layered, filtered witchfire effects, deterministic and peak-normalized."""
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfilt
from scipy.io.wavfile import write
out=Path(__file__).resolve().parents[1]/'dist/assets/audio';sr=44100;rng=np.random.default_rng(90)
for name,duration,low,high in [('cast',.42,180,2600),('impact',.6,90,2100),('teleport',.62,280,3200),('storm',1.85,70,2200)]:
 t=np.arange(round(sr*duration))/sr;u=t/duration
 noise=sosfilt(butter(3,[low,high],btype='bandpass',fs=sr,output='sos'),rng.normal(0,1,len(t)))
 env=np.minimum(1,u*22)*(1-u)**1.5
 freq=190-110*u if name!='teleport' else 180+480*np.sin(np.pi*u)
 tone=np.sin(2*np.pi*np.cumsum(freq)/sr)*.14
 rumble=sosfilt(butter(2,160,fs=sr,output='sos'),rng.normal(0,1,len(t)))*.8
 sound=(noise*.9+tone+rumble)*env
 if name=='impact':sound+=np.sin(2*np.pi*60*t)*np.exp(-t*12)*.35
 if name=='storm':sound*=.7+.3*np.sin(2*np.pi*7*t)**2
 # Short stereo echo gives magic some space without masking combat.
 delay=round(.065*sr);right=np.r_[np.zeros(delay),sound[:-delay]]*.22+sound*.8
 stereo=np.stack([sound,right],axis=1);stereo*=.82/max(.001,np.max(np.abs(stereo)))
 write(out/f'witch-{name}-0.wav',sr,(stereo*32767).astype(np.int16))
