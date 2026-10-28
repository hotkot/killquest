"""Two-minute original thrash arrangement with independently rendered stems."""
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfilt
import wave,subprocess
R=44100;rng=np.random.default_rng(521);beat=60/144;duration=72*4*beat
tracks={name:np.zeros((round(duration*R),2),dtype=np.float32) for name in ['rhythm-guitars','bass','drums','support-guitar','atmosphere']};mix=tracks['rhythm-guitars'];out=Path(__file__).resolve().parents[1]/'dist/assets/audio'
def hz(n):return 440*2**((n-69)/12)
def add(s,at,gain=1,pan=0,track="rhythm-guitars"):
 mix=tracks[track]
 i=round(at*R);n=min(len(s),len(mix)-i)
 if n>0:mix[i:i+n]+=s[:n,None]*gain*np.array([1-pan*.7,1+pan*.7])
def guitar(note,d,muted,detune):
 n=max(12,round(R/(hz(note)*detune)));size=round(d*R);cycle=rng.normal(0,1,n);cycle-=cycle.mean();parts=[]
 for _ in range(size//n+1):
  parts.append(cycle.copy());cycle=(cycle+np.roll(cycle,1))*.499
 x=np.concatenate(parts)[:size];t=np.arange(size)/R
 x*=np.minimum(t/.002,1)*np.exp(-t/(.048 if muted else .28))*np.minimum((d-t)/.012,1)
 # Bridge pickup, amp overdrive and a dark guitar cabinet.
 x=sosfilt(butter(1,115,'highpass',fs=R,output='sos'),x)
 x=np.tanh(x*16)
 x=sosfilt(butter(3,3100,fs=R,output='sos'),x)
 return x
# Four motifs: low-E chugs, chromatic pickup, syncopated power chords and descending turnaround.
patterns=[[(0,40,1),(.5,40,1),(.75,40,1),(1,40,1),(1.5,41,1),(1.75,40,1),(2,43,0),(2.75,40,1),(3,40,1),(3.5,46,1),(3.75,43,1)],[(0,40,1),(.5,40,1),(1,47,0),(1.75,46,1),(2,45,0),(2.75,43,1),(3,41,0),(3.75,40,1)],[(0,40,1),(.25,40,1),(1,40,1),(1.5,40,1),(2,43,0),(2.5,42,1),(3,41,0),(3.5,40,1)],[(0,40,0),(1,43,0),(2,41,0),(3,38,0),(3.5,39,1),(3.75,40,1)]]

sections=[(0,8,'intro'),(8,24,'main-riff'),(24,40,'power-chord-refrain'),(40,48,'half-time-breakdown'),(48,56,'bass-bridge'),(56,72,'final-reprise')]
for bar in range(72):
 base=bar*4*beat;section=next(name for lo,hi,name in sections if lo<=bar<hi)
 pattern=patterns[(bar//2)%4]
 if section=='power-chord-refrain':pattern=patterns[(bar//2+1)%4]
 if section=='half-time-breakdown':pattern=[(0,40,0),(1.5,40,1),(2,41,0),(3.5,38,1)]
 if section=='bass-bridge':pattern=[(0,40,0),(2,43 if bar%2 else 38,0)]
 guitarGain=.16 if section=='bass-bridge' else .22
 if section=='intro' and bar<4:guitarGain*=.65
 for pos,n,muted in pattern:
  at=base+pos*beat;d=.16 if muted else .32
  for pan,detune in [(-.9,.997),(.9,1.003)]:
   add(guitar(n,d,muted,detune),at,guitarGain,pan)
   if not muted:add(guitar(n+7,d,False,detune),at,guitarGain*.45,pan)
 # A separate centered bass line locks to the riff and walks into transitions.
 bassnotes=[28,28,31,28,28,35,29,27] if section!='bass-bridge' else [28,31,35,34,33,31,29,26]
 if section=='power-chord-refrain':bassnotes=[28,35,31,38,29,36,26,33]
 for j,n in enumerate(bassnotes):
  at=base+j*beat/2;t=np.arange(round(.23*R))/R
  if bar%4==3 and j>=6:n=[27,28][j-6]
  bass=np.sin(2*np.pi*hz(n)*t)+.27*np.sin(2*np.pi*hz(n)*2*t)+.10*np.sin(2*np.pi*hz(n)*3*t)
  bass=np.tanh(bass*1.3)*np.minimum(t/.005,1)*np.exp(-t*7)*np.minimum((.23-t)/.02,1)
  add(bass,at,.20 if section=='bass-bridge' else .16,track='bass')
 # Vary kick patterns; quieter intro, half-time snare and short tom fills.
 kickbeats=[0,1,2,3] if section=='intro' else [0,.75,1,1.5,2,2.75,3]
 if section=='half-time-breakdown':kickbeats=[0,.5,2,2.75]
 if section=='bass-bridge':kickbeats=[0,2]
 for pos in kickbeats:
  t=np.arange(round(.22*R))/R;kick=np.sin(2*np.pi*(46*t+1.8*(1-np.exp(-t*38))))*np.exp(-t*26)
  add(kick,base+pos*beat,.27,track='drums')
 for pos in ([2] if section in ['half-time-breakdown','bass-bridge'] else [1,3]):
  t=np.arange(round(.22*R))/R;snare=rng.normal(0,1,len(t))*np.exp(-t*25)+.6*np.sin(2*np.pi*180*t)*np.exp(-t*32)
  snare=sosfilt(butter(1,5000,fs=R,output='sos'),snare);add(snare,base+pos*beat,.11,track='drums')
 for j in range(8):
  t=np.arange(round(.08*R))/R;hat=sosfilt(butter(2,6000,'highpass',fs=R,output='sos'),rng.normal(0,1,len(t)))*np.exp(-t*70)
  add(hat,base+j*beat/2,.017 if section=='bass-bridge' else .024,.5,track='drums')
 if bar%8==7:
  for j,n in enumerate([55,52,48,45]):
   t=np.arange(round(.2*R))/R;tom=np.sin(2*np.pi*hz(n)*t)*np.exp(-t*20)
   add(tom,base+(3+j*.25)*beat,.13,-.5+j*.3,track='drums')
 if any(bar==lo for lo,hi,name in sections) or bar%8==0:
  t=np.arange(round(.8*R))/R;crash=sosfilt(butter(2,[1800,8000],'bandpass',fs=R,output='sos'),rng.normal(0,1,len(t)))*np.exp(-t*7)
  add(crash,base,.055,-.4,track='drums')
 # Quiet mid-register answering guitar only in selected phrases, avoiding shrill lead.
 if section in ['power-chord-refrain','final-reprise'] and bar%4>=2:
  for j,n in enumerate([52,55,54,50] if bar%2==0 else [52,50,47,52]):
   add(guitar(n,.34,False,1),base+(j+.25)*beat,.035,.4,track='support-guitar')
 if section in ['intro','bass-bridge']:
  for j,n in enumerate([40,47,43,47]):add(guitar(n,.5,False,1),base+j*beat,.025,-.3,track='support-guitar')
 # Low dark atmospheric fifths support section changes without a high MIDI melody.
 if section in ['intro','half-time-breakdown','bass-bridge'] or bar%4==0:
  t=np.arange(round(4*beat*R))/R;env=np.minimum(t/.3,1)*np.minimum((4*beat-t)/.3,1)
  for n in [40,47]:
   pad=np.sin(2*np.pi*hz(n)*t)+.15*np.sin(2*np.pi*hz(n)*1.003*t)
   add(pad*env,base,.018,-.25 if n==40 else .25,track='atmosphere')
# Wrap small room tails; arrange the end on the tonic to meet the opening riff.
for name in ['rhythm-guitars','support-guitar']:
 tracks[name]+=np.roll(tracks[name][:,::-1].copy(),round(.037*R),axis=0)*.06
mix=sum(tracks.values());mix=np.tanh(mix*.9);mix*=.72/max(abs(mix).max(),1e-6)
fade=round(.005*R);mix[:fade]*=np.linspace(0,1,fade)[:,None];mix[-fade:]*=np.linspace(1,0,fade)[:,None]
source=out.parents[2]/'source-audio/menu-v53';source.mkdir(parents=True,exist_ok=True)
def render(name,x,dest):
 p=dest/(name+'.wav')
 with wave.open(str(p),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(R);w.writeframes((np.clip(x,-.98,.98)*32767).astype('<i2').tobytes())
 return p
for name,x in tracks.items():
 p=render(name,x,source)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),str(source/(name+'.flac'))],check=True);p.unlink()
p=render('killquest-menu-thrash-v53',mix,out)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-codec:a','libmp3lame','-b:a','192k',str(out/'killquest-menu-thrash-v53.mp3')],check=True);p.unlink()
import json
(source/'arrangement.json').write_text(json.dumps({'duration_seconds':120,'bpm':144,'sections':[{'name':name,'start_seconds':round(lo*4*beat,3),'end_seconds':round(hi*4*beat,3)} for lo,hi,name in sections],'stems':list(tracks)},indent=2)+'\n')
print('Rendered original two-minute thrash arrangement and five independent stems.')
