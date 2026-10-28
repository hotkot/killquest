"""Original sample synthesis and EDM/metal composition. No external recordings."""
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfilt,iirpeak,lfilter
import wave,subprocess,json
R=44100; rng=np.random.default_rng(9127);out=Path(__file__).resolve().parents[1]/'dist/assets/audio';out.mkdir(exist_ok=True)
def time(d):return np.arange(round(d*R))/R
def noise(d):return rng.normal(0,1,len(time(d)))
def filt(x,f,kind='lowpass'):return sosfilt(butter(2,f,kind,fs=R,output='sos'),x)
def env(t,a=.005,decay=12):return np.minimum(1,t/a)*np.exp(-t*decay)
def save(name,x,music=False):
 x=np.nan_to_num(x);peak=np.max(np.abs(x));x=x/max(peak,1e-6)*(.88 if music else .8)
 fade=min(len(x)//4,220);ramp=np.linspace(0,1,fade);x[:fade]*=ramp[:,None] if x.ndim==2 else ramp;x[-fade:]*=ramp[::-1,None] if x.ndim==2 else ramp[::-1]
 p=out/(name+'.wav')
 with wave.open(str(p),'wb') as w:w.setnchannels(2 if x.ndim==2 else 1);w.setsampwidth(2);w.setframerate(R);w.writeframes((x*32767).astype('<i2').tobytes())
 if music:
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-codec:a','libmp3lame','-b:a','160k',str(out/(name+'.mp3'))],check=True);p.unlink()
def swing(d=.3,heavy=False):
 t=time(d);n=filt(noise(d),1800 if heavy else 3500,'highpass');s=n*np.sin(np.pi*np.clip(t/d,0,1))**2*np.exp(-t*2);body=filt(noise(d),750)*env(t,.012,8);return s*.32+body*(.8 if heavy else .4)
def hit(d=.32,heavy=False):
 t=time(d);phase=2*np.pi*np.cumsum(45+120*np.exp(-t*40))/R;thump=np.sin(phase)*env(t,.002,24 if heavy else 35);crack=filt(noise(d),1500,'highpass')*env(t,.001,90);metal=sum(np.sin(2*np.pi*f*t+rng.random()*6)*np.exp(-t*rate) for f,rate in [(731,24),(1193,18),(2027,30),(3121,40)]);return thump*.9+crack*.45+metal*.07
for i in range(3):
 save('swing-'+str(i),swing(.25+i*.025));save('hit-'+str(i),hit());save('heavy-'+str(i),hit(.5,True)+swing(.5,True)*.15)
save('slide',filt(noise(.36),2200)*np.sin(np.pi*time(.36)/.36)**1.5)
def grunt(d,pitch,pain=False,death=False):
 t=time(d);f=pitch*(1.12-.3*t/d)+5*np.sin(2*np.pi*24*t);phase=np.cumsum(f)/R;glottal=(1-(phase%1))**5-.16;breath=filt(noise(d),2500)*.12;src=glottal+breath
 v=np.zeros(len(t));formants=[(720,5),(1150,6),(2400,8)] if pain else [(420,4),(900,5),(2100,7)]
 for hz,q in formants:
  b,a=iirpeak(hz,q,fs=R);v+=lfilter(b,a,src)
 v=np.tanh(v*9)*(np.sin(np.pi*np.clip(t/d,0,1))**.6)*np.exp(-t*(1.2 if death else 2));return v+breath*.04
for role,pitch in [('hero',86),('bandit',133)]:
 for action,d in [('effort',.22),('pain',.29),('death',.62)]:
  for i in range(3):save(role+'-'+action+'-'+str(i),grunt(d+i*.025,pitch*(.95+i*.07),action!='effort',action=='death'))
save('ui',hit(.12)*.15)
# 32 bars / 60 seconds at 128 BPM: chug riff, electronic bass, break, melodic climax.
bpm=128;beat=60/bpm;bars=32;duration=bars*4*beat;music=np.zeros((round(duration*R),2),dtype=np.float64)
def add(x,start,gain=1,pan=0):
 idx=round(start*R);n=min(len(x),len(music)-idx)
 if n<=0:return
 # Wrap release tails to the start for a seamless compositional loop.
 music[idx:idx+n,0]+=x[:n]*gain*np.sqrt((1-pan)/2);music[idx:idx+n,1]+=x[:n]*gain*np.sqrt((1+pan)/2)
 if n<len(x):music[:len(x)-n,0]+=x[n:]*gain*np.sqrt((1-pan)/2);music[:len(x)-n,1]+=x[n:]*gain*np.sqrt((1+pan)/2)
def guitar(f,d,chug=True,detune=1):
 t=time(d);x=sum(np.sin(2*np.pi*f*detune*k*t+rng.random()*6)*np.exp(-t*(1.3+k*.8))/k for k in range(1,18));x+=sum(np.sin(2*np.pi*f*1.5*detune*k*t)/k*np.exp(-t*(2+k)) for k in range(1,9))*.6
 x=np.tanh(x*3.2);x=filt(x,5200);e=np.minimum(1,t/.002)*np.exp(-t*(14 if chug else 2.7));return x*e+filt(noise(d),3200,'highpass')*env(t,.001,130)*.09
def bass(f,d):
 t=time(d);p=f*t;carrier=(p%1)*2-1;mod=np.sin(2*np.pi*f*.5*t);x=np.tanh(carrier*2+mod);return filt(x,600)*np.minimum(1,t/.003)*np.exp(-t*5)
def kick():
 t=time(.34);ph=2*np.pi*np.cumsum(48+150*np.exp(-t*35))/R;return np.sin(ph)*env(t,.001,12)+filt(noise(.34),4000,'highpass')*env(t,.001,110)*.08
def snare():
 t=time(.27);return (filt(noise(.27),1100,'highpass')*.65+np.sin(2*np.pi*184*t)*.35)*env(t,.001,18)
def hat(opened=False):
 d=.25 if opened else .08;t=time(d);return filt(noise(d),6500,'highpass')*env(t,.001,15 if opened else 60)
roots=[82.4069,82.4069,65.4064,73.4162];riff=[0,0,0,3,0,0,6,5]
for bar in range(bars):
 root=roots[(bar//2)%4];section=bar//8;start=bar*4*beat;breakdown=section==2
 for k in range(8):
  at=start+k*beat/2;f=root*2**(riff[k]/12);islong=k in [3,7]
  if not breakdown or k in [0,3,6]:
   add(guitar(f,.55 if islong else .25,not islong,.996),at,.23,-.7);add(guitar(f,.55 if islong else .25,not islong,1.004),at+.003,.23,.7)
  add(bass(root if k%2==0 else f,.28),at,.22,0)
 for k in range(4):
  at=start+k*beat
  if not breakdown or k in [0,2]:add(kick(),at,.72)
  if k in [1,3]:add(snare(),at,.37)
 for k in range(8 if breakdown else 16):add(hat(k%8==7),start+k*beat/(2 if breakdown else 4),.09 if k%2==0 else .045,(k%3-1)*.4)
 if section in [1,3]:
  melody=[12,15,19,17,15,14,12,10];notes=[82.4069*2**(n/12) for n in melody]
  for k in range(4):
   f=notes[(bar*2+k)%8];t=time(.7);x=(np.sin(2*np.pi*f*t)+np.sin(2*np.pi*f*2*t)*.25+np.sin(2*np.pi*f*1.003*t)*.4)*np.sin(np.pi*np.minimum(t/.7,1))**.5
   add(x,start+k*beat,.10,.2);add(x,start+k*beat+beat*.75,.025,-.4)
 # Crash at phrase starts, tom/snare turnaround at phrase ends.
 if bar%8==0:
  t=time(1.2);add(filt(noise(1.2),3500,'highpass')*env(t,.001,4),start,.10,-.2)
 if bar%8==7:
  for k in range(4):add(snare(),start+3*beat+k*beat/4,.16,(-1)**k*.25)
# Gentle saturation/limiting, short spatial room on drums/riffs, no vocal track.
for delay,gain in [(round(R*.031),.055),(round(R*.071),.035)]:music+=np.roll(music,delay,axis=0)*gain
music=np.tanh(music*1.25);save('quarter-forge',music,True)
for name,notes in [('victory',[164.81,207.65,246.94]),('defeat',[82.4,77.78,65.4])]:
 x=np.zeros(round(R*.9))
 for i,f in enumerate(notes):g=guitar(f,.55,False);at=round(i*.13*R);n=min(len(g),len(x)-at);x[at:at+n]+=g[:n]*.5
 save(name,x)
(out/'manifest.json').write_text(json.dumps({'composer':'Original procedural composition','title':'Quarter Forge','bpm':128,'duration_seconds':duration,'bars':32,'style':'distorted power-chord riffs / electronic bass / dance drums','vocals':'synthetic formant grunts, not recorded actors','sample_rate':R},indent=2))
print('Generated',len(list(out.glob('*.wav'))),'SFX samples and',duration,'seconds of original music.')
