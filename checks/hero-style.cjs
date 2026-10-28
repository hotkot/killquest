const assert=require('node:assert/strict'),fs=require('node:fs'),style=require('../dist/hero-style.js');
const dir=process.argv[2];let frames=0,changed=0,magic=0;const start=performance.now();
for(const f of JSON.parse(fs.readFileSync(dir+'/frames.json'))){
 const before=fs.readFileSync(`${dir}/${f.key}.raw`),copy=Buffer.from(before),hero=style.identity(f.key),after=Buffer.from(style.process(before,f.w,f.h,hero));
 assert.equal(after.length,before.length);assert.deepEqual(before,copy);
 if(!hero){assert.deepEqual(after,before);frames++;continue;}
 let differs=false;
 for(let i=0;i<before.length;i+=4){assert.equal(after[i+3],before[i+3]);

  if(hero==='selene'&&before[i+2]>145&&before[i+1]>100&&before[i+2]>before[i]*1.4&&before[i+1]>before[i]*1.3){assert.equal(after[i],before[i]);assert.equal(after[i+1],before[i+1]);assert.equal(after[i+2],before[i+2]);magic++;}
  if(after[i]!==before[i]||after[i+1]!==before[i+1]||after[i+2]!==before[i+2])differs=true;
 }
 frames++;if(differs)changed++;
}
console.log(JSON.stringify({frames,changed,protectedMagicPixels:magic,seconds:+((performance.now()-start)/1000).toFixed(2)}));
const source=new Uint8ClampedArray([120,90,60,255,120,90,60,255,120,90,60,255,120,90,60,255]);let replacements=0;
global.document={createElement(){return {getContext(){return {drawImage(){},getImageData(){return {data:source.slice()}},putImageData(){}}}}}};
const textures=new Map(['hero-idle-00','huntress-idle-00','knight-idle-00','witch-idle-00','witch-fx-flame-00','bandit-idle-00'].map(k=>[k,{getSourceImage(){return {width:2,height:2}}}]));
const scene={textures:{getTextureKeys(){return [...textures.keys()]},get(k){return textures.get(k)},remove(k){textures.delete(k)},addCanvas(k,c){assert.equal(c.width,2);assert.equal(c.height,2);replacements++;textures.set(k,c)}}};
style.apply(scene);style.apply(scene);style.apply({textures:scene.textures});assert.equal(replacements,3);assert.equal(textures.size,6);assert(textures.get('hero-idle-00').getSourceImage);assert(textures.get('witch-fx-flame-00').getSourceImage);console.log('PASS: same texture keys and dimensions, originals/FX excluded, one-time processing across scene restarts.');
