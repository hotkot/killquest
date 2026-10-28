"""Render the current pixel-art intro with its retained narration-free soundtrack."""
from pathlib import Path
import subprocess,sys,shutil
root=Path(__file__).resolve().parents[1]
work=root/'source-art/intro-pixel-v175'
subprocess.run([sys.executable,str(work/'render.py'),'story'],check=True)
output=root/'dist/assets/cinematic'/'killquest-opening-v175.mp4'
shutil.copy2(work/'story'/'KillQuest-New-Game-Intro.mp4',output)
print(output)
