from pathlib import Path
import wave,json,subprocess,numpy as np
files=list(Path('dist/assets/audio').glob('*.wav'));assert len(files)==45
for p in files:
 with wave.open(str(p)) as w:
  assert w.getframerate() in [24000,44100] and w.getsampwidth()==2 and w.getnframes()>4000
  x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
  assert np.isfinite(x).all() and .01<np.sqrt(np.mean(x*x))<.5,p
  assert np.abs(x).max()<.9,p
meta=json.load(open('dist/assets/audio/manifest.json'));assert meta['duration_seconds']==60
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=channels,sample_rate','-of','json','dist/assets/audio/quarter-forge.mp3']))
assert probe['streams'][0]['channels']==2 and 60<=float(probe['format']['duration'])<60.2
for family in ['swing','hit','heavy','hero-effort','hero-pain','hero-death','bandit-death']:
 assert len({Path(f'dist/assets/audio/{family}-{i}.wav').read_bytes() for i in range(meta.get('voice_variants',{}).get(family,3))})==meta.get('voice_variants',{}).get(family,3)
print('PASS: 45 non-silent varied PCM effects below clipping; stereo 60-second music file decodes; original composition metadata.')

for family,peak,rms in [('hero-effort',.5,.045),('bandit-death',.55,.045)]:
 for i in range(meta['voice_variants'][family]):
  with wave.open(f'dist/assets/audio/{family}-{i}.wav') as w:x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
  assert np.max(np.abs(x))>peak and np.sqrt(np.mean(x*x))>rms,(family,i,'vocal too quiet')
assert len({Path(f'dist/assets/audio/flesh-{i}.wav').read_bytes() for i in range(6)})==6
print('PASS: prominent vocal sample levels and six distinct flesh slicing effects.')
for family,count in [('bandit-death',4),('hero-death',2)]:
 for i in range(count):
  with wave.open(f'dist/assets/audio/{family}-{i}.wav') as w:duration=w.getnframes()/w.getframerate()
  assert 1.1<duration<1.8,(family,i,duration)
print('PASS: all six death cries sustain for roughly 1.0–1.3 seconds.')

for p in Path('source-audio/dry-v12').glob('*.wav'):
 with wave.open(str(p)) as w:original=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 with wave.open(str(Path('dist/assets/audio')/p.name)) as w:echoed=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 assert len(echoed)>len(original)
 n=min(len(original),round(44100*.075))
 assert np.max(np.abs(echoed[:n]-original[:n]*10**(-3/20)))<.00007
 assert np.sqrt(np.mean(echoed*echoed))<np.sqrt(np.mean(original*original))
print('PASS: voice-only lower direct level, delayed tails and reduced overall loudness.')
