"""Deterministic layered bow/string, flight and cloth sounds for Lyra."""
from pathlib import Path
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter,sosfilt
root=Path(__file__).resolve().parents[1]/'dist/assets/audio';sr=44100;rng=np.random.default_rng(43)
def noise(n,lo,hi):return sosfilt(butter(3,[lo,hi],fs=sr,btype='bandpass',output='sos'),rng.normal(0,1,n))
def save(name,a):
 a=np.tanh(a*1.2);a*=min(.86/(np.max(np.abs(a))+1e-9),1);write(root/(name+'.wav'),sr,(a*32767).astype(np.int16))
for i in range(3):
 t=np.arange(int(sr*.65))/sr;f=125+i*13
 string=sum(np.sin(2*np.pi*f*k*t)*np.exp(-t*(7+k*3))/k for k in range(1,9))*.16
 release=noise(len(t),1400,8000)*np.exp(-t*35)*.65
 flight=noise(len(t),800,6000)*np.sin(np.pi*np.minimum(1,t/.55))**2*np.exp(-t*4)*.17
 save(f'bow-{i}',string+release+flight)
t=np.arange(int(sr*1.0))/sr;a=noise(len(t),500,5000)*np.sin(np.pi*t)**2*.13
for shift in [0,.06,.12,.18,.24,.3,.36]:
 u=np.maximum(0,t-shift);env=np.exp(-u*19)*(t>=shift);a+=noise(len(t),1000,7500)*env*.15+np.sin(2*np.pi*170*u)*env*.08
save('arrow-rain-0',a)
t=np.arange(int(sr*.43))/sr;env=np.sin(np.pi*t/.43)**2
save('roll-0',noise(len(t),150,3800)*env*.35+np.sin(2*np.pi*70*t)*np.exp(-np.maximum(0,t-.29)*25)*(t>.29)*.13)
