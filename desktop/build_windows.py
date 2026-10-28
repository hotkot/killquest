"""Build the offline Windows portable ZIP from a verified official Electron x64 runtime."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,shutil,json,struct,sys
root=Path(__file__).resolve().parents[1]
cache=Path(sys.argv[1]);destination=Path(sys.argv[2]);version='44.7.2'
runtime=cache/'electron-win64.zip';sums=(cache/'SHASUMS256.txt').read_text()
expected=next(line.split()[0] for line in sums.splitlines() if line.strip().endswith(f'electron-v{version}-win32-x64.zip'))
assert hashlib.sha256(runtime.read_bytes()).hexdigest()==expected,'Electron runtime checksum mismatch'
folder=destination/'KillQuest-Windows-x64';folder.mkdir(parents=True,exist_ok=True)
with ZipFile(runtime) as z:
 assert z.testzip() is None;z.extractall(folder)
(folder/'electron.exe').rename(folder/'KillQuest.exe')
app=folder/'resources/app';app.mkdir(parents=True,exist_ok=True)
for name in ['main.cjs','asset-path.cjs','package.json']:shutil.copy2(root/'desktop'/name,app/name)
shutil.copytree(root/'dist',app/'game',dirs_exist_ok=True)
shutil.copy2(root/'dist/assets/ui/life-head.png',app/'icon.png')
shutil.copy2(root/'desktop/README.txt',folder/'READ-ME.txt')
(folder/'resources/default_app.asar').unlink(missing_ok=True)
pe=(folder/'KillQuest.exe').read_bytes();assert pe[:2]==b'MZ';offset=struct.unpack_from('<I',pe,0x3c)[0];assert pe[offset:offset+4]==b'PE\0\0';assert struct.unpack_from('<H',pe,offset+4)[0]==0x8664
for source in (root/'dist').rglob('*'):
 if source.is_file():
  target=app/'game'/source.relative_to(root/'dist')
  assert hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest(),source
manifest={'game_version':'v56','electron_version':version,'platform':'win32','architecture':'x64','source_commit':sys.argv[3] if len(sys.argv)>3 else 'v56','runtime_sha256':expected,'entrypoint':'KillQuest.exe','offline':True}
(folder/'build-info.json').write_text(json.dumps(manifest,indent=2)+'\n')
archive=destination/'KillQuest-Windows-x64-v56.zip'
with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(folder.rglob('*')):
  if p.is_file():z.write(p,Path(folder.name)/p.relative_to(folder))
with ZipFile(archive) as z:
 assert z.testzip() is None
 assert folder.name+'/KillQuest.exe' in z.namelist()
print(json.dumps({'archive':str(archive),'size_mb':round(archive.stat().st_size/1024/1024,1),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'checks':'official runtime checksum; Windows x64 PE; exact asset copies; ZIP integrity'}))
