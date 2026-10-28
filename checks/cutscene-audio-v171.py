from pathlib import Path
import subprocess,json,tempfile
root=Path(__file__).resolve().parents[1]
def call(*args):return subprocess.check_output(['ffmpeg','-v','error',*map(str,args)],text=True).strip()
def digest(p,stream):return call('-i',p,'-map',stream,'-c','copy','-f','hash','-hash','sha256','-')
for old,new,audio,duration,filters in [('opening-v117','opening-v173','source-audio/opening-video/ambient.wav',44.25,json.loads((root/'source-audio/opening-video/loudness-v173.json').read_text())['filter']),('forest-v122','forest-v172','source-audio/forest-intro-v122/ambience-only-v171.wav',20,json.loads((root/'source-audio/forest-intro-v122/loudness-v172.json').read_text())['filter'])]:
 original=root/f'source-art/cinematic-archive/killquest-{old}.mp4';movie=root/f'source-art/cinematic-archive/killquest-{new}.mp4'
 assert digest(original,'0:v:0')==digest(movie,'0:v:0'),'visual stream changed'
 with tempfile.TemporaryDirectory() as folder:
  reference=Path(folder)/'ambience.m4a'
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(root/audio),'-af',filters,'-ar','48000','-c:a','aac','-b:a','128k','-t',str(duration),str(reference)],check=True)
  assert digest(reference,'0:a:0')==digest(movie,'0:a:0'),'soundtrack is not exactly the clean ambience source'
 assert digest(original,'0:a:0')!=digest(movie,'0:a:0'),'old narrated soundtrack retained'
 streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(movie)]))['streams'];assert [s['codec_type'] for s in streams]==['video','audio']
 print('PASS',new,'unchanged video/subtitles; exact clean ambience AAC; no narrated audio stream')
for name in ['dist/game.js','dist/loading-assets.js']:
 text=(root/name).read_text();assert 'killquest-opening-v117.mp4' not in text;assert 'killquest-forest-v122.mp4' not in text;assert 'killquest-opening-v175.mp4' in text;assert 'killquest-forest-v175.mp4' in text
for name in ['scripts/render_forest_intro_v122.py','scripts/render_opening_video.py']:
 text=(root/name).read_text();assert 'narration-normal-pauses.mp3' not in text;assert 'narration-original.mp3' not in text;compile(text,name,'exec')
print('PASS active playback/boot manifest reference clean videos; future renderers no longer consume narration')
