const fs=require('fs'),assert=require('assert');
const style=require('../dist/hero-style.js'),armor=require('../dist/armor-finish.js');
const dir=process.argv[2];if(!dir)throw Error('Provide raw-frame QA directory');
const tile=armor.buildTile(fs.readFileSync(dir+'/tile.raw'),256,256);
let changed=0;
for(const f of JSON.parse(fs.readFileSync(dir+'/frames.json'))){
 const raw=new Uint8ClampedArray(fs.readFileSync(`${dir}/${f.key}.raw`)),saved=raw.slice();
 const base=style.process(raw,f.w,f.h,'garran'),out=armor.process(base,f.w,f.h,tile,raw);
 assert.deepStrictEqual(raw,saved,'source mutated');assert.equal(out.length,raw.length);
 let count=0;
 for(let i=0;i<out.length;i+=4){
  assert.equal(out[i+3],raw[i+3],'alpha changed');
  const diff=out[i]!==base[i]||out[i+1]!==base[i+1]||out[i+2]!==base[i+2];
  if((base[i]+base[i+1]+base[i+2])/3<72)assert(!diff,'ink changed');
  if(raw[i+3]<250)assert(!diff,'contour changed');
  if(diff)count++;
 }
 assert(count>0,`${f.key} has no steel treatment`);changed+=count;
 assert.deepStrictEqual(out,armor.process(base,f.w,f.h,tile,raw),'not deterministic');
 if(/knight-(idle-00|walk-04|down-03|cross-04|thrust-04|bash-03|win-04|pickup-03)$/.test(f.key)){
  fs.writeFileSync(`${dir}/${f.key}.before`,base);fs.writeFileSync(`${dir}/${f.key}.after`,out);
 }
}
console.log('PASS all 149 frames: immutable alpha/contours/ink, unchanged source, deterministic steel finish;',changed,'metal pixels');
