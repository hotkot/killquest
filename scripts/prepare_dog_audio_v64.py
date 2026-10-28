from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1];folder=root/'source-art/dog-audio-v64/selected'
clips=[('dog-bark',i,folder/f'Dog Bark {i+1}.wav',0,.36,1) for i in range(3)]
clips += [('dog-growl',i,root/'source-art/dog-audio-v64/growl.ogg',0,.62,.94+i*.08) for i in range(2)]
clips += [('dog-hurt',0,folder/'Sad Dog.wav',.6,.4,1.08),('dog-hurt',1,folder/'Sad Dog 1.wav',1.2,.42,1.05),('dog-death',0,folder/'Sad Dog.wav',1.8,1.2,.94),('dog-death',1,folder/'Sad Dog 1.wav',2.1,1.25,.95)]
clips += [('dog-bite',i,root/f'dist/assets/audio/flesh-{i}.wav',0,.18,1.13) for i in range(2)]
for name,i,source,start,duration,rate in clips:
 filters=f'aresample=44100,highpass=f=90,lowpass=f=6000,afftdn=nf=-28,asetrate=44100*{rate},aresample=44100,apad,atrim=duration={duration},afade=t=in:d=0.008,afade=t=out:st={max(0,duration-.06)}:d=0.06,loudnorm=I=-21:TP=-3:LRA=7'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',str(source),'-t',str(duration),'-ar','44100','-ac','1','-af',filters,'-c:a','pcm_s16le',str(root/f'dist/assets/audio/{name}-{i}.wav')],check=True)
