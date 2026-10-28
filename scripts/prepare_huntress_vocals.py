"""Cut AI Voice Generator takes, normalize, and add a quiet short reflection."""
from pathlib import Path
import subprocess,numpy as np
from scipy.io.wavfile import write
root=Path(__file__).resolve().parents[1];sr=24000
def read(name):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(root/'source-art'/name),'-f','f32le','-ac','1','-ar',str(sr),'-']),dtype=np.float32).copy()
def save(name,a):
 a=a[:max(1,np.where(np.abs(a)>.004)[0][-1]+int(.06*sr))];a*=.68/(np.max(np.abs(a))+1e-9);n=int(.075*sr);b=np.pad(a,(0,n*2));b[n:n+len(a)]+=a*.10;b[n*2:n*2+len(a)]+=a*.04
 b[:min(200,len(b))]*=np.linspace(0,1,min(200,len(b)));b[-min(600,len(b)):]*=np.linspace(1,0,min(600,len(b)));write(root/'dist/assets/audio'/f'{name}.wav',sr,(np.clip(b,-1,1)*32767).astype(np.int16))
a=read('lyra-vocals-v43.mp3');save('lyra-effort-0',a[:int(1.17*sr)]);save('lyra-effort-1',a[int(1.8*sr):int(2.66*sr)])
a=read('lyra-death-v43.mp3');save('lyra-pain-0',a);save('lyra-death-0',a)
save('lyra-warcry-0',read('lyra-rage-v43.mp3'))
