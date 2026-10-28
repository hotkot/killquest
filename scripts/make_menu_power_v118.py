"""Short low-D transition chord; sampled Skimel guitar, CC BY-SA 4.0.
Source/license: source-audio/menu-v66/CREDITS.md. No time-stretched menu music.
"""
from pathlib import Path
import subprocess, numpy as np, wave
from scipy.signal import resample_poly, butter, sosfilt
root=Path(__file__).resolve().parents[1]; R=44100; n=int(1.3*R)
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(root/'source-audio/menu-v66/guitar-source.ogg'),'-ar',str(R),'-ac','1','-f','f32le','-'])
a=np.frombuffer(raw,dtype='<f4'); mix=np.zeros((n,2))
for side,offset in enumerate([.115,.121]):
 s=a[int(offset*R):int((offset+1.1)*R)].copy()
 s=resample_poly(s,1000,round(1000*2**(-7/12)))[:int(.95*R)]
 s=sosfilt(butter(2,[75,3800],btype='bandpass',fs=R,output='sos'),s)
 t=np.arange(len(s))/R;s*=np.exp(-t*2.7);s[:132]*=np.linspace(0,1,132);s[-2205:]*=np.linspace(1,0,2205)
 delay=int(side*.008*R);mix[delay:delay+len(s),side]+=s
 for d,g in [(.055,.11),(.093,.07),(.151,.035)]:
  k=delay+int(d*R);count=min(len(s),n-k);mix[k:k+count,1-side]+=s[:count]*g
# A brief low root reinforces the impact without a bright synth lead.
t=np.arange(n)/R; bass=np.sin(2*np.pi*73.416*t)*np.exp(-t*12);bass[:132]*=np.linspace(0,1,132)
mix+=bass[:,None]*.045;mix*=.89/max(abs(mix).max(),.01)
with wave.open(str(root/'dist/assets/audio/menu-power-0.wav'),'wb') as f:
 f.setnchannels(2);f.setsampwidth(2);f.setframerate(R);f.writeframes((mix*32767).astype('<i2').tobytes())
