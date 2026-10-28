const fs=require('fs'),{createCanvas,loadImage}=require('@napi-rs/canvas'),crypto=require('crypto');
(async()=>{
const root=process.cwd(),folder=root+'/source-art/garran-arm-v147',sheet=await loadImage(root+'/source-art/garran-arm-v146/sheet.png');
const c=createCanvas(448,448),ctx=c.getContext('2d');
// Registration of the corrected seventh cell uses its helmet, matching the shipped frame.
// Original sheet 1792x896; corrected sheet preserves this layout.
const s=.6;ctx.drawImage(sheet,896,448,448,448,232-(1148-896)*s,174-(465-448)*s,448*s,448*s);
const fixed=ctx.getImageData(0,0,448,448),original=await loadImage(root+'/dist/assets/characters/knight-walk-06.png');
ctx.clearRect(0,0,448,448);ctx.drawImage(original,0,0);const old=ctx.getImageData(0,0,448,448);old.data.set(require('pngjs').PNG.sync.read(fs.readFileSync(root+'/dist/assets/characters/knight-walk-06.png')).data);
// Only the arm and blade region is accepted from the generated correction.
const m=createCanvas(448,448),mc=m.getContext('2d');mc.beginPath();mc.moveTo(125,245);mc.lineTo(219,245);mc.lineTo(222,306);mc.lineTo(306,357);mc.lineTo(305,366);mc.lineTo(197,320);mc.lineTo(125,320);mc.closePath();mc.fill();const mask=mc.getImageData(0,0,448,448).data;
for(let i=0;i<old.data.length;i+=4)if(mask[i+3])old.data.set(fixed.data.subarray(i,i+4),i);
const prior=require('pngjs').PNG.sync.read(require('child_process').execFileSync('git',['show','4b958475a1d6b43b353719b0be7e38551d51d316:dist/assets/characters/knight-walk-06.png']));for(let y=0;y<285;y++)for(let x=0;x<165;x++){const i=(y*448+x)*4;old.data.set(prior.data.subarray(i,i+4),i);}
fs.writeFileSync(folder+'/candidate.png',require('pngjs').PNG.sync.write({width:448,height:448,data:Buffer.from(old.data)}));
})();
