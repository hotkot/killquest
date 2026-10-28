import json,subprocess,hashlib
from pathlib import Path
p=Path('dist/assets/audio/killquest-menu-chug-v66.mp3')
meta=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(p)]))
assert abs(float(meta['format']['duration'])-120)<.1
assert meta['streams'][0]['channels']==2 and int(meta['streams'][0]['sample_rate'])==44100
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-af','loudnorm=I=-17:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
stats=json.loads(r.stderr[r.stderr.rindex('{'):]);assert -19<float(stats['input_i'])<-15;assert float(stats['input_tp'])<-.5
report=json.loads(Path('source-audio/menu-v66/mix-report.json').read_text());assert report['bpm']==112 and report['duration_seconds']==120
for name,expected in [('guitar-left',.075),('guitar-right',.075),('bass',.078),('drums',.088)]:assert abs(report['stems'][name]['active_rms']-expected)<.001;assert Path('source-audio/menu-v66/'+name+'.flac').exists()
assert hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(Path('dist/assets/audio/killquest-menu-balanced-v54.mp3').read_bytes()).digest()
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-']);import numpy as np
samples=np.frombuffer(raw,dtype='<f4').reshape(-1,2);assert float(abs(samples[[0,-1]]).max())<.025,'loop boundary must not click'
assert p.name in Path('dist/audio.js').read_text();assert 'creativecommons.org/licenses/by-sa/4.0/' in Path('dist/audio-credits.html').read_text()
print('PASS: new 120s/112BPM stereo track, four balanced stems, mixer routing, source attribution; measured',stats['input_i'],'LUFS,',stats['input_tp'],'dBTP,',stats['input_lra'],'LU range.')
