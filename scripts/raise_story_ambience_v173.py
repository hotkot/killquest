"""Match the New Game story intro ambience to the Forest intro's -21 LUFS."""
from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[1]
source=root/'source-audio/opening-video/ambient.wav'
prefix='volume=2.0,alimiter=limit=0.9,afade=t=out:st=43.2:d=1.05'
base='loudnorm=I=-21:TP=-2:LRA=8'
probe=subprocess.run(['ffmpeg','-hide_banner','-i',str(source),'-af',prefix+','+base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
measure=json.loads(probe.stderr[probe.stderr.rfind('{'):])
filters=prefix+','+base+''.join(':'+key+'='+measure[val] for key,val in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])+':linear=true'
output=root/'source-art/cinematic-archive/killquest-opening-v173.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(root/'source-art/cinematic-archive/killquest-opening-v171.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',filters,'-c:a','aac','-ar','48000','-b:a','128k','-t','44.25','-movflags','+faststart',str(output)],check=True)
probe=subprocess.run(['ffmpeg','-hide_banner','-i',str(output),'-vn','-af',base+':print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
encoded=json.loads(probe.stderr[probe.stderr.rfind('{'):]);assert -22<float(encoded['input_i'])< -20;assert float(encoded['input_tp'])< -2
(root/'source-audio/opening-video/loudness-v173.json').write_text(json.dumps({'target_lufs':-21,'peak_ceiling_dbtp':-2,'source_measurements':measure,'encoded_measurements':encoded,'filter':filters},indent=2)+'\n')
print('Encoded loudness:',encoded['input_i'],'LUFS; true peak:',encoded['input_tp'],'dBTP')
