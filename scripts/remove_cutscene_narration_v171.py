"""Remux existing cutscene video with clean music/ambience, never the narrated mix."""
from pathlib import Path
import subprocess, numpy as np, wave
from scipy.signal import butter,sosfilt
root=Path(__file__).resolve().parents[1]
R=24000;duration=20;n=R*duration;t=np.arange(n)/R;rng=np.random.default_rng(122)
a=np.zeros(n)
# Same deterministic ambience as render_forest_intro_v122.py, without its voice bus.
for f,g in [(73.416,.009),(110,.005),(146.832,.003)]:a+=np.sin(2*np.pi*f*t+.15*np.sin(t*.4))*g
noise=rng.normal(size=n);wind=sosfilt(butter(2,[140,1700],btype='bandpass',fs=R,output='sos'),noise)
a+=wind*.007*(.7+.3*np.sin(t*.7))
for at in rng.uniform(9,19.5,90):
 k=round(at*R);count=min(900,len(a)-k);a[k:k+count]+=rng.normal(size=count)*np.exp(-np.arange(count)/R*120)*.012
mask=np.clip(1-abs(t-5.6)/.6,0,1);a+=np.sin(2*np.pi*(310*t+1.4*np.sin(t*21)))*mask*.007
a*=np.clip(t/.3,0,1)*np.clip((duration-t)/.6,0,1)
clean=root/'source-audio/forest-intro-v122/ambience-only-v171.wav'
with wave.open(str(clean),'wb') as f:f.setparams((1,2,R,0,'NONE','not compressed'));f.writeframes((np.clip(a,-.92,.92)*32767).astype('<i2').tobytes())
for old,new,audio,seconds,filters in [
 ('killquest-forest-v122.mp4','killquest-forest-v171.mp4',clean,20,'anull'),
 ('killquest-opening-v117.mp4','killquest-opening-v171.mp4',root/'source-audio/opening-video/ambient.wav',44.25,'volume=2.0,alimiter=limit=0.9,afade=t=out:st=43.2:d=1.05')]:
 folder=root/'source-art/cinematic-archive'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(folder/old),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',filters,'-c:a','aac','-b:a','128k','-t',str(seconds),'-movflags','+faststart',str(folder/new)],check=True)
 print(new)
