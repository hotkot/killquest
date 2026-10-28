from pathlib import Path
from PIL import Image,ImageDraw
import io,subprocess,json
root=Path(__file__).resolve().parents[1];art=root/'dist/assets/characters';folder=root/'source-art/npc-v160';baseline='96123d56674877d064e18e51ea83d498eee52cf9';audit=json.loads((folder/'heads.json').read_text());report={}
# Clip factors are measured from helmet landmarks, not whole alpha bounds:
# raised swords, long spears and crouching/falling poses must not define scale.
# Low-confidence template matches on turned/prone heads are rejected; those
# retain the validated clip's shared factor rather than stretching to stand up.
factors={'guard':[.95]*6+[.91]*5+[.95]*13,'bulwark':[.95]*24,'spearman':[.97]*24,'crossbowman':[1.05]*24,'commander':[1.05]*6+[1.04]*18}
for kind in factors:
 rows=[];board=Image.new('RGB',(1440,900),'#514947');d=ImageDraw.Draw(board)
 for j in range(30):
  key=f'rebel-{kind}-'+(f'{j:02}'if j<6 else f'combat-{j-6:02}');im=Image.open(io.BytesIO(subprocess.check_output(['git','show',f'{baseline}:dist/assets/characters/{key}.png'],cwd=root))).convert('RGBA');scale=1 if j<6 else factors[kind][j-6]
  # Upright idle/walk poses use helmet-to-floor height, excluding weapons.
  # This corrects individual short/tall stride frames as well as clip changes.
  if j<12:
   ref= audit[kind][0]['head'][1];head=audit[kind][j]['head'][1]
   scale=(408-ref)/(408-head)
  # Action poses retain their crouching/rotation and a shared clip correction.
  if scale!=1:
   w,h=im.size;resized=im.resize((round(w*scale),round(h*scale)),Image.Resampling.LANCZOS);frame=Image.new('RGBA',(w,h));frame.paste(resized,(round(w/2-w/2*scale),round(408-408*scale)));im=frame
  
  if scale!=1:
   import numpy as np
   a=np.array(im);yy,xx=np.where(a[:,:,3]>100);delta=407-int(yy.max());shifted=Image.new('RGBA',im.size);shifted.paste(im,(0,delta));im=shifted;a=np.array(im);a[409:]=0;im=Image.fromarray(a)
  im.save(art/(key+'.png'));rows.append({'key':key,'factor':scale,'foot':408,'canvas':list(im.size),'bounds':im.getbbox()})
  tile=im.resize((round(im.width*.66),296));x=j%8*180;y=j//8*225;board.paste(tile,(x+90-tile.width//2,y+210-round(408*.66)),tile);d.text((x+5,y+210),f'{key.split(kind+"-")[1]} x{scale}',fill='white')
 board.save(folder/(kind+'-after.png'));report[kind]=rows
(folder/'normalization.json').write_text(json.dumps(report,indent=2));print('Normalized150 rebel frames: reference idle size, individual upright stride correction, shared action-clip scale, foot408')
