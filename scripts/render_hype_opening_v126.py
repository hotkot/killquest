from pathlib import Path
import subprocess,concurrent.futures,numpy as np,wave
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'source-art/hype-opening-v126';FPS=30;R=44100;bar=5/3;D=100/3
# Preserve the approved 33.333-second edit with the Ash and Iron soundtrack.
scenes=[(ROOT/'source-art/opening-v115/morvane-v115.png',2*bar,1),(ROOT/'source-art/opening-v115/village-v115.png',2*bar,-1),
(W/'kael.png',2*bar,1),(W/'lyra.png',2*bar,-1),(W/'garran-solo.png',2*bar,1),(W/'selene-solo.png',2*bar,-1),
(W/'kael.png',bar,-1),(W/'garran-group.png',bar,1),(W/'lyra.png',bar,-1),(W/'selene-group.png',bar,1),
(W/'garran-group.png',2*bar,-1),(ROOT/'dist/assets/ui/killquest-menu-v105.png',2*bar,1)]
def render(item):
 i,(path,seconds,direction)=item;frames=round(seconds*FPS)
 if (W/f'part-{i}.mp4').exists():return
 # Fast comic camera push/slide, a brief impact jolt, then a readable hold. No strobing.
 zoom=f"1.04+0.08*on/{frames}" if direction>0 else f"1.14-0.08*on/{frames}"
 x=f"(iw-iw/zoom)*({'.35+.25*on/'+str(frames) if direction>0 else '.65-.25*on/'+str(frames)})+5*sin(on*1.3)*exp(-on/5)"
 y="ih/2-ih/zoom/2+3*cos(on*1.5)*exp(-on/5)"
 vf=f"scale=1920:1080,zoompan=z='{zoom}':x='{x}':y='{y}':d=1:s=1280x720:fps={FPS},setsar=1,format=yuv420p"
 if i==11:vf+=',eq=brightness=-0.28:saturation=0.8'
 subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate',str(FPS),'-i',str(path),'-vf',vf,'-t',str(seconds),'-c:v','libx264','-preset','fast','-crf','21','-threads','2',str(W/f'part-{i}.mp4')],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,enumerate(scenes)))
(W/'concat.txt').write_text(''.join(f"file 'part-{i}.mp4'\n" for i in range(len(scenes))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(W/'concat.txt'),'-c','copy',str(W/'picture.mp4')],check=True)
filters=f"[0:v]subtitles={W/'titles.ass'}[base];[2:v]scale=930:-1[logo];[base][logo]overlay=(W-w)/2:190:enable='gte(t,30)',fade=t=out:st=32.95:d=0.38[v];[1:a]alimiter=limit=0.89:level=0,afade=t=out:st=32.7:d=0.633[a]"
output=ROOT/'dist/assets/cinematic/killquest-hype-v126.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(W/'picture.mp4'),'-i',str(ROOT/'source-audio/hype-opening-v126/approved-mix.wav'),'-i',str(ROOT/'dist/assets/ui/killquest-logo.png'),'-filter_complex',filters,'-map','[v]','-map','[a]','-t',str(D),'-c:v','libx264','-profile:v','baseline','-level:v','3.1','-pix_fmt','yuv420p','-r','30','-preset','fast','-crf','24','-threads','2','-c:a','aac','-ar','44100','-ac','2','-b:a','160k','-movflags','+faststart',str(output)],check=True)
for temporary in W.glob('*.mp4'):temporary.unlink()
print(output)
