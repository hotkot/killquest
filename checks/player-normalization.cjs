const fs=require('fs'),vm=require('vm'),assert=require('assert');
const audit=JSON.parse(fs.readFileSync('source-art/player-scale-v86/normalization.json'));
const source=fs.readFileSync('dist/game.js','utf8');
const c={document:{getElementById(){}},window:{},Math,Number,Set,Map};vm.createContext(c);
vm.runInContext(source.split('class BrawlScene')[0]+'\nglobalThis.visual=playerFrameVisual;globalThis.preview=playerPreviewRect;globalThis.layout=PLAYER_FRAME_LAYOUT;',c);
const frames=Object.entries(audit.frames);assert.equal(frames.length,535);assert.equal(Object.keys(c.layout).length,535);
const crypto=require('crypto'),groups=new Map;
for(const [key,rec] of frames){
 const bytes=fs.readFileSync('dist/assets/characters/'+key+'.png');
 assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),rec.sha256,'source artwork changed: '+key);
 const style=c.visual(rec.character,key);assert(style.scale>0&&style.scale<1);
 assert.equal(style.width,rec.canvas[0]);assert.equal(style.height,448);
 if(rec.airborne){const base=rec.character==='kael'?.84:.84*210/234,ground=rec.character==='lyra'?403:408;
  assert(Math.abs((300-style.origin*448)*style.scale-(300-ground)*base)<.00001,'airborne pelvis moved: '+key);
 }else assert(Math.abs((rec.sole_y-style.origin*448)*style.scale)<.00001,'sole moved from floor: '+key);
 const rect=c.preview(rec.character,key,448,448);
 assert(Math.abs(rect.width/rect.height-rec.canvas[0]/448)<.00001,'selection stretch: '+key);
 assert(Math.abs((rect.y+style.origin*448*rect.height/448)-424)<.00001,'selection floor: '+key);
 const prev=groups.get(rec.artwork);if(prev!==undefined)assert.equal(prev,rec.factor,'duplicate pose scale differs: '+key);else groups.set(rec.artwork,rec.factor);
}
// Compare bulky outliers to the reference body's mass, without measuring axes,
// raised swords, or total pose height. These used to be 29–49% larger in area.
for(const [key,idle] of [['hero-air-heavy-00','hero-idle-00'],['knight-cross-04','knight-idle-00']]){
 const pose=audit.frames[key],ref=audit.frames[idle];
 const ratio=pose.body_area*pose.factor**2/ref.body_area;assert(ratio>.85&&ratio<1.15,[key,ratio]);
}
for(const [key,idle] of [['hero-pickup-02','hero-idle-00'],['huntress-pickup-02','huntress-idle-00'],['knight-pickup-03','knight-idle-00']])assert.equal(audit.frames[key].factor,audit.frames[idle].factor,'crouch was enlarged to standing height');
const normal=c.preview('garran','knight-idle-00'),wide=c.preview('garran','knight-down-00');
assert(Math.abs(wide.width/normal.width-640/448)<.00001,'wide sword frames are squeezed');
for(const size of [[448,448],[320,448],[256,256]])for(const character of ['kael','lyra','garran']){const p=c.preview(character,character==='kael'?'hero-idle-00':character==='lyra'?'huntress-idle-00':'knight-idle-00',...size);assert(p.width>0&&p.height>0);}
console.log('PASS: all 535 player layouts, unchanged source artwork, shared-pose scales, grounded soles, preserved airborne pelvis, corrected body-mass outliers, natural crouches and aspect-correct selection previews.');
