"""Raise the clean Forest intro bed to an audible, subdued -21 LUFS."""
from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[1]
source=root/'source-audio/forest-intro-v122/ambience-only-v171.wav'
base='loudnorm=I=-21:TP=-2:LRA=8'
probe=subprocess.run(['ffmpeg','-hide_banner','-i',str(source),'-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
measure=json.loads(probe.stderr[probe.stderr.rfind('{'):])
filters=base+''.join(':'+key+'='+measure[val] for key,val in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])+':linear=true'
output=root/'source-art/cinematic-archive/killquest-forest-v172.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(root/'source-art/cinematic-archive/killquest-forest-v171.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',filters,'-c:a','aac','-ar','48000','-b:a','128k','-t','20','-movflags','+faststart',str(output)],check=True)
(root/'source-audio/forest-intro-v122/loudness-v172.json').write_text(json.dumps({'target_lufs':-21,'peak_ceiling_dbtp':-2,'source_measurements':measure,'filter':filters},indent=2)+'\n')
print(output)
