"""Audit every player pose and generate non-destructive display normalization.

Anatomy-reviewed action calibrations use each fighter's approved idle as the
reference. Never fit a pose's full weapon/limb bounds to a standing height.
Shared artwork gets a shared scale; ground poses register to the actual soles,
while airborne poses retain their pelvis anchor and scripted jump trajectory.
"""
from pathlib import Path
from collections import defaultdict
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_opening, binary_dilation, label

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'dist/assets/characters'
OUT = ROOT / 'source-art/player-scale-v86'
OUT.mkdir(exist_ok=True)
GROUPS = {
 'witch': {clip:1 for clip in ['idle','walk','jump','cast1','cast2','cast3','air-cast','push','slam','teleport','rage','hurt','pickup','win']},
 'hero': {'air-chop':.91,'air-heavy':.88,'air-spin':.92,'grapple':1,'heavy':.95,
          'idle':1,'jump':1,'knockdown':.97,'link-one':1,'link-two':1,'pickup':1,
          'rage':.92,'rise':1,'slash':1,'slide':1,'spin':1,'walk':.975,'win':.96},
 'huntress': {'air-bow':1,'air-finish':.92,'air-slash':.90,'air-spin':.90,'bow':.96,
              'finisher':1,'grapple':1,'hurt':1,'idle':1,'jump':.94,'pickup':1,
              'rage':.95,'rise':1,'roll':1,'slash':1,'walk':1.04,'win':1},
 'knight': {'air-finish':1,'air-slash':1,'air-spin':1,'backstep':1,'bash':.88,
            'cross':.86,'down':1,'grapple':.96,'hurt':.95,'idle':1,'jump':.95,
            'pickup':1,'rage':1,'slam':.93,'thrust':.98,'walk':1,'win':1},
}
CHARACTERS = {'hero': ('kael', .84, 408), 'huntress': ('lyra', .84*210/234, 403),
              'knight': ('garran', .84*210/234, 408), 'witch': ('selene', .84*210/234, 408)}
yy, xx = np.mgrid[-4:5,-4:5]
DISK = xx*xx + yy*yy <= 16
records, artworks = {}, defaultdict(list)

def body_measure(image):
    a = np.array(image)
    mask = a[:,:,3] > 100
    labs, _ = label(binary_opening(mask, DISK))
    sizes = np.bincount(labs.ravel()); sizes[0] = 0
    body = labs == sizes.argmax()
    near = binary_dilation(body, iterations=5) & (a[:,:,3] > 32)
    return int(sizes.max()), int(np.where(near)[0].max())

paths = sorted(p for who in GROUPS for p in ART.glob(who+'-*.png'))
paths += [ART / f'base-{i:02}.png' for i in range(6)]
for path in paths:
    name = path.stem
    who, clip, idx = ('hero','base',int(name[-2:])) if name.startswith('base-') else (name.split('-')[0], name.split('-',1)[1].rsplit('-',1)[0], int(name[-2:]))
    char, base_scale, ground = CHARACTERS[who]
    image = Image.open(path).convert('RGBA')
    crop = image.crop(image.getbbox())
    identity = hashlib.sha256(str(crop.size).encode()+crop.tobytes()).hexdigest()
    factor = GROUPS[who].get(clip,1)
    priority = 30 if clip.startswith('air-') else 40
    if clip in ['idle','base']:
        factor, priority = 1, 100
    # Later sheets contain independent pose groups and exact older recovery keys.
    if who == 'hero' and clip == 'air-heavy' and idx >= 6: factor, priority = 1, 60
    if who == 'hero' and clip == 'jump' and 2 <= idx <= 5: factor = .95
    if who == 'hero' and clip == 'rage' and idx == 2: factor = .86
    if who == 'hero' and clip == 'rage' and idx == 11: factor, priority = 1, 60
    # v89: last-row walk artwork is anatomically corrected at source.
    if who == 'knight' and clip == 'walk': factor = 1
    if who == 'knight' and clip in ['bash','pickup','win','rage'] and idx in [0,7]: factor, priority = 1, 60
    if who == 'knight' and clip == 'slam' and idx == 7: factor, priority = 1, 60
    area, foot = body_measure(image)
    airborne = clip.startswith('air-') or clip == 'jump'
    if clip == 'rage' and who != 'huntress':
        airborne = (2 <= idx <= 6) if who == 'hero' else (idx in [2,3])
    if who == 'hero' and clip == 'knockdown' and idx < 3: airborne = True
    if who == 'huntress' and clip == 'hurt' and idx in [1,2,3]: airborne = True
    if who == 'knight' and clip == 'hurt' and idx in [0,1,2]: airborne = True
    if who == 'witch': airborne = False  # baked common floor/head registration; flight remains scripted
    # Garran's established sole registration already excludes low sword tips.
    source_ground = ground if who in ['knight','witch'] else foot + (1 if who == 'hero' else 0)
    if clip == 'idle': source_ground = ground
    rec = {'character':char,'clip':clip,'index':idx,'canvas':list(image.size),
           'factor':factor,'priority':priority,'airborne':airborne,'sole_y':source_ground,
           'body_area':area,'artwork':identity,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    records[name] = rec
    artworks[identity].append(name)

for names in artworks.values():
    priority = max(records[name]['priority'] for name in names)
    factors = [records[name]['factor'] for name in names if records[name]['priority'] == priority]
    factor = round(float(np.median(factors)),5)
    for name in names:
        records[name]['factor'] = factor

layout = {}
left, right, above, below = [], [], [], []
for name, rec in records.items():
    who = 'hero' if name.startswith('base-') else name.split('-')[0]
    char, base_scale, ground = CHARACTERS[who]
    factor = rec['factor']
    # Scaling around the pelvis preserves airborne body centers; grounded
    # poses scale around their soles and continue to meet the world floor.
    origin = 300 + (ground-300)/factor if rec['airborne'] else rec['sole_y']
    origin = round(origin,5)
    rec['origin_y'] = origin
    layout[name] = [factor, origin, rec['canvas'][0]]
    image = Image.open(ART/(name+'.png'));a=np.array(image);ys,xs=np.where(a[:,:,3]>8)
    scale = base_scale*factor
    left.append((image.width/2-xs.min())*scale)
    right.append((xs.max()-image.width/2)*scale)
    above.append((origin-ys.min())*scale)
    below.append((ys.max()-origin)*scale)
zoom = round(min(1,210/max(left+right),390/max(above),20/max(1,max(below))),5)
(OUT/'normalization.json').write_text(json.dumps({'groups':GROUPS,'preview_zoom':zoom,'frames':records},indent=2)+'\n')
game = ROOT/'dist/game.js'
s = game.read_text()
block = '// PLAYER_NORMALIZATION_BEGIN\nconst PLAYER_FRAME_LAYOUT='+json.dumps(layout,separators=(',',':'))+';\nconst PLAYER_PREVIEW_ZOOM='+str(zoom)+';\n// PLAYER_NORMALIZATION_END'
if '// PLAYER_NORMALIZATION_BEGIN' in s:
    start=s.index('// PLAYER_NORMALIZATION_BEGIN');end=s.index('// PLAYER_NORMALIZATION_END',start)+len('// PLAYER_NORMALIZATION_END')
    s=s[:start]+block+s[end:]
else:
    line=s.index('\n',s.index('const PLAYER_VISUALS='))
    s=s[:line+1]+block+'\n'+s[line+1:]
game.write_text(s)

for who, (char,base_scale,ground) in CHARACTERS.items():
    groups = defaultdict(list)
    for name,rec in records.items():
        if rec['character']==char and not name.startswith('base-'): groups[rec['clip']].append(name)
    sheet=Image.new('RGB',(5*288,len(groups)*200),(28,31,35));d=ImageDraw.Draw(sheet)
    for row,(clip,names) in enumerate(groups.items()):
        # All frames use the SAME game-space pixel scale, including 640px sword canvases.
        chosen=[f'{who}-idle-00']+[names[k] for k in [0,len(names)//3,2*len(names)//3,-1]]
        for col,name in enumerate(chosen):
            rec=records[name];im=Image.open(ART/(name+'.png'))
            scale=base_scale*rec['factor']*.78
            im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
            x=col*288+144-im.width//2;y=row*200+170-round(rec['origin_y']*scale)
            sheet.paste(im,(x,y),im)
            d.line((col*288+5,row*200+170,col*288+283,row*200+170),fill='#46535c')
            d.text((col*288+8,row*200+181),('idle reference' if col==0 else name.replace(who+'-',''))+f" x{rec['factor']}",fill='white')
    sheet.save(OUT/(who+'-normalized.jpg'),quality=94)
print(f'Generated layouts for {len(records)} playable frames; preview zoom {zoom}. Artwork and timings unchanged.')
