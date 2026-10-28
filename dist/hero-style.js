/* Pose-preserving comic rendering for the playable cast. Geometry and alpha
 * are immutable: this pass changes RGB shading only, never sprite coordinates. */
(function(root){
 'use strict';
 const TARGETS=/^(huntress-|knight-|witch-(?!fx-))/;
 const CONFIG={lyra:{ink:.95,soften:.60,saturation:1.10,levels:8},garran:{ink:.65,soften:.58,saturation:1.00,levels:9},selene:{ink:.72,soften:.56,saturation:1.01,levels:9}};
 const identity=key=>key.startsWith('huntress-')?'lyra':key.startsWith('knight-')?'garran':key.startsWith('witch-')?'selene':null;
 function process(data,width,height,hero){
  const cfg=CONFIG[hero];if(!cfg)return data.slice();
  const output=new Uint8ClampedArray(data),step=255/(cfg.levels-1);
  for(let y=1;y<height-1;y++)for(let x=1;x<width-1;x++){
   const i=(y*width+x)*4,a=data[i+3];if(a<32)continue;
   const r=data[i],g=data[i+1],b=data[i+2],lum=.2126*r+.7152*g+.0722*b;
   // Magical light keeps its smooth luminous falloff and its full original bounds.
   const magic=hero==='selene'&&b>145&&g>100&&b>r*1.4&&g>r*1.3;
   if(magic)continue;
   let sumR=r,sumG=g,sumB=b,count=1,edge=0,outline=false;
   for(const o of [-4,4,-width*4,width*4]){const j=i+o;
    if(data[j+3]<80){outline=true;continue;}
    const nr=data[j],ng=data[j+1],nb=data[j+2],nl=.2126*nr+.7152*ng+.0722*nb;
    const distance=Math.abs(r-nr)+Math.abs(g-ng)+Math.abs(b-nb);
    if(distance<95){sumR+=nr;sumG+=ng;sumB+=nb;count++;}
    if(nl<46&&lum>52&&distance>55)edge=Math.max(edge,(46-nl)/46);
   }
   let rgb=[r+(sumR/count-r)*cfg.soften,g+(sumG/count-g)*cfg.soften,b+(sumB/count-b)*cfg.soften];
   const mean=rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;
   rgb=rgb.map(v=>Math.max(0,Math.min(255,mean+(v-mean)*cfg.saturation)));
   const dark=outline?cfg.ink*.82:edge*cfg.ink*.43;
   for(let c=0;c<3;c++){
    const v=rgb[c];const flat=Math.round(v/step)*step;
    output[i+c]=(v*.10+flat*.90)*(1-dark);
   }
  }
  return output;
 }
 function canvasFor(image,hero,tile){
  const canvas=document.createElement('canvas');canvas.width=image.naturalWidth||image.width;canvas.height=image.naturalHeight||image.height;
  const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(image,0,0);
  const pixels=ctx.getImageData(0,0,canvas.width,canvas.height);const original=pixels.data.slice(),comic=process(original,canvas.width,canvas.height,hero);pixels.data.set(hero==='garran'&&tile?root.ArmorFinish.process(comic,canvas.width,canvas.height,tile,original):comic);ctx.putImageData(pixels,0,0);return canvas;
 }
 function armorTile(scene){
  if(!root.ArmorFinish||!scene.textures.exists?.('knight-steel-detail'))return null;
  if(scene.textures.__armorFinishTile)return scene.textures.__armorFinishTile;
  const canvas=document.createElement('canvas');canvas.width=canvas.height=256;const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(scene.textures.get('knight-steel-detail').getSourceImage(),0,0,256,256);
  return scene.textures.__armorFinishTile=root.ArmorFinish.buildTile(ctx.getImageData(0,0,256,256).data,256,256);
 }
 function apply(scene){
  if(scene.textures.__heroComicStyleApplied||!scene.textures?.getTextureKeys||typeof document.createElement!=='function')return;
  scene.textures.__heroComicStyleApplied=true;const tile=armorTile(scene);
  for(const key of scene.textures.getTextureKeys()){
   if(!TARGETS.test(key))continue;const hero=identity(key);if(!hero)continue;
   const old=scene.textures.get(key),image=old.getSourceImage();
   const canvas=canvasFor(image,hero,tile);
   scene.textures.remove(key);scene.textures.addCanvas(key,canvas);
  }
 }
 async function applyAsync(scene){
  if(scene.textures.__heroComicStyleApplied)return;
  let count=0;const tile=armorTile(scene);
  for(const key of scene.textures.getTextureKeys()){
   if(!TARGETS.test(key))continue;const hero=identity(key);if(!hero)continue;
   const canvas=canvasFor(scene.textures.get(key).getSourceImage(),hero,tile);
   scene.textures.remove(key);scene.textures.addCanvas(key,canvas);
   if(++count%6===0)await new Promise(resolve=>requestAnimationFrame(resolve));
  }
  scene.textures.__heroComicStyleApplied=true;
 }
 const api={process,apply,applyAsync,identity,config:CONFIG};root.HeroComicStyle=api;
 if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
