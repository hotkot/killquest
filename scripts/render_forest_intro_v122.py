"""Render the current pixel-art intro with its retained narration-free soundtrack."""
from pathlib import Path
import subprocess,sys,shutil
root=Path(__file__).resolve().parents[1]
work=root/'source-art/intro-pixel-v175'
subprocess.run([sys.executable,str(work/'render.py'),'forest'],check=True)
output=root/'dist/assets/cinematic'/'killquest-forest-v175.mp4'
shutil.copy2(work/'forest'/'KillQuest-Forest-Intro.mp4',output)
print(output)
