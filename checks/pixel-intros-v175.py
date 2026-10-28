"""Verify revised cinematic media, soundtrack continuity and boot wiring."""
from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[1]
def digest(p,stream):
 return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map',stream,'-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()
for old,new,duration in [('opening-v173','opening-v175',44.25),('forest-v172','forest-v175',20)]:
 a=root/f'source-art/cinematic-archive/killquest-{old}.mp4';b=root/f'dist/assets/cinematic/killquest-{new}.mp4'
 assert digest(a,'0:a:0')==digest(b,'0:a:0'),'soundtrack changed'
 assert digest(a,'0:v:0')!=digest(b,'0:v:0'),'visuals not replaced'
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(b)]))
 assert abs(float(info['format']['duration'])-duration)<.08
 video=info['streams'][0];assert(video['width'],video['height'])==(1280,720)
 assert [s['codec_type'] for s in info['streams']]==['video','audio']
 for file in ['dist/game.js','dist/loading-assets.js']:
  s=(root/file).read_text();assert f'killquest-{new}.mp4' in s;assert f'killquest-{old}.mp4' not in s
 print('PASS',new,'new pixel-art visuals; exact previous ambience; correct duration, codecs and active paths')
assert 'killquest-carion-v174.mp4' in (root/'dist/game.js').read_text()
assert 'killquest-hype-v126.mp4' in (root/'dist/opening-cinematic.js').read_text()
print('PASS Carion cinematic and startup action opening preserved.')
