/* Bake bounded source-color animation; no generated replacement scenery.
   Runtime only switches small preloaded atlases, never filters whole screens. */
const fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
require('child_process').execFileSync(process.execPath,[path.join(__dirname,'bake_city_joins_v178.cjs')],{stdio:'inherit'});
const {createCanvas,loadImage,ImageData}=require('@napi-rs/canvas');
const api=require('../dist/city-ambience.js');const root=path.resolve(__dirname,'..');
const out=path.join(root,'dist/assets/city/ambient'),qa=path.join(root,'source-art/city-ambient-v178/qa');fs.mkdirSync(out,{recursive:true});fs.mkdirSync(qa,{recursive:true});
function distance(x,y,poly){let inside=false,d=Infinity;for(let i=0,j=poly.length-1;i<poly.length;j=i++){
 const [ax,ay]=poly[j],[bx,by]=poly[i],dx=bx-ax,dy=by-ay,t=Math.max(0,Math.min(1,((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy||1)));d=Math.min(d,Math.hypot(x-ax-t*dx,y-ay-t*dy));if((ay>y)!==(by>y)&&x<(bx-ax)*(y-ay)/(by-ay)+ax)inside=!inside;
 }return inside?d:-d;}
function sample(a,w,h,x,y,c){x=Math.max(0,Math.min(w-1,x));y=Math.max(0,Math.min(h-1,y));const ix=Math.floor(x),iy=Math.floor(y),nx=Math.min(w-1,ix+1),ny=Math.min(h-1,iy+1),u=x-ix,v=y-iy;return a[(iy*w+ix)*4+c]*(1-u)*(1-v)+a[(iy*w+nx)*4+c]*u*(1-v)+a[(ny*w+ix)*4+c]*(1-u)*v+a[(ny*w+nx)*4+c]*u*v;}
for(const name of fs.readdirSync(out))if(/^\d+\.png$/.test(name)&&Number(name.split('.')[0])>=api.layers.length)fs.unlinkSync(path.join(out,name));
const sources=new Map(),atlases=new Map(),metrics=[];
(async()=>{
for(const l of api.layers){
 if(!sources.has(l.panel)){const img=await loadImage((l.join?path.join(root,'source-art/city-ambient-v178',l.panel+'.png'):path.join(root,'dist/assets/city',l.panel+'.webp'))),c=createCanvas(l.refWidth,l.refHeight);c.getContext('2d').drawImage(img,0,0,l.refWidth,l.refHeight);sources.set(l.panel,c);}
 const c=createCanvas(l.w,l.h),ctx=c.getContext('2d');ctx.drawImage(sources.get(l.panel),-l.x,-l.y);const original=ctx.getImageData(0,0,l.w,l.h).data,mask=new Float32Array(l.w*l.h),warm=new Float32Array(mask.length);
 let hotCount=0;
 for(let y=0;y<l.h;y++)for(let x=0;x<l.w;x++){const j=y*l.w+x,i=j*4,d=distance(x+l.x+.5,y+l.y+.5,l.poly);mask[j]=Math.max(0,Math.min(1,d/4));const r=original[i],g=original[i+1],b=original[i+2];warm[j]=r>125&&g>53&&r>g*1.12&&g>b*1.22?Math.min(1,(r-g-12)/24)*mask[j]:0;if(warm[j]>.3)hotCount++;}
 const base=new Uint8ClampedArray(original),flame=createCanvas(l.w,l.h),fc=flame.getContext('2d'),flameData=new Uint8ClampedArray(original.length);
 if(l.kind==='fire')for(let y=0;y<l.h;y++)for(let x=0;x<l.w;x++){const j=y*l.w+x,i=j*4,k=warm[j];if(k<=0)continue;
  let left=x-1,right=x+1;while(left>0&&warm[y*l.w+left]>.04)left--;while(right<l.w-1&&warm[y*l.w+right]>.04)right++;
  for(let q=0;q<3;q++){const bg=(original[(y*l.w+left)*4+q]+original[(y*l.w+right)*4+q])/2;base[i+q]=original[i+q]*(1-k)+bg*k;flameData[i+q]=original[i+q];}flameData[i+3]=Math.round(k*255);
 }
 if(l.kind==='fire')fc.putImageData(new ImageData(flameData,l.w,l.h),0,0);
 const atlas=createCanvas(l.w*4,l.h*3),ac=atlas.getContext('2d');
 for(let f=0;f<12;f++){
  const p=f*Math.PI/6,bytes=new Uint8ClampedArray(original),frame=createCanvas(l.w,l.h),ct=frame.getContext('2d');
  if(l.kind==='fire'){
   const anchor=l.h-8,rendered=new Uint8ClampedArray(base);
   // Inverse-map every pixel once. Forward-drawing overlapping strips creates
   // bright horizontal seams, especially at the brazier's attachment point.
   for(let y=0;y<l.h;y++)for(let x=0;x<l.w;x++){
    const i=(y*l.w+x)*4,v=Math.max(0,(anchor-y)/Math.max(1,anchor-8));
    const sx=x-Math.sin(p*2+v*6)*v*2.2,sy=anchor+(y-anchor)/(1+.11*Math.sin(p+v*4));
    const alpha=sample(flameData,l.w,l.h,sx,sy,3)/255*(.94+.055*Math.sin(p*2+v*3));
    for(let q=0;q<3;q++)rendered[i+q]=base[i+q]*(1-alpha)+sample(flameData,l.w,l.h,sx,sy,q)*alpha;
   }ct.putImageData(new ImageData(rendered,l.w,l.h),0,0);
  }else{
   for(let y=0;y<l.h;y++)for(let x=0;x<l.w;x++){const j=y*l.w+x,i=j*4,k=mask[j];if(!k)continue;let dx=0,dy=0,gain=1;
    if(l.kind==='cloth'){
     const u=x/l.w,v=Math.max(0,(y-8)/Math.max(1,l.h-16)),pin=l.mode==='awning'?Math.sin(Math.PI*u)*v:v*v;
     dx=(Math.sin(p+v*6+u*2)-Math.sin(p+u*2))*2.8*pin*k;
     dy=l.mode==='awning'?Math.sin(p+u*7)*2.7*pin*k:Math.sin(p+u*5)*.65*v*k;
     gain=1+Math.sin(p+u*8+v*5)*.035*pin*k;
    }else if(l.kind==='smoke'){
     const edge=Math.sin(Math.PI*x/(l.w-1))*Math.sin(Math.PI*y/(l.h-1));dx=Math.sin(p+y*.024)*4*edge;dy=Math.cos(p+x*.018)*2.5*edge;
    }else if(l.kind==='water'){dx=Math.sin(p+y*.75)*2.1*k;dy=Math.cos(p*2+x*.11)*.65*k;gain=1+.045*Math.sin(p*2+x*.17+y*.7)*k;
    }else if(l.kind==='light'){gain=1+(.15*Math.sin(p)+.045*Math.sin(p*3))*(warm[j]>0?1:0)*k;}
    for(let q=0;q<3;q++)bytes[i+q]=sample(original,l.w,l.h,x+dx,y+dy,q)*gain;
   }ct.putImageData(new ImageData(bytes,l.w,l.h),0,0);
  }
  // Transparent gutter / feather contains every changed pixel. The unchanged
  // source outside the object stays visible, including poles, rims and paving.
  const result=ct.getImageData(0,0,l.w,l.h),data=result.data;
  for(let y=0;y<l.h;y++)for(let x=0;x<l.w;x++){const j=y*l.w+x,i=j*4,edge=Math.min(x,y,l.w-1-x,l.h-1-y);data[i+3]=Math.round(Math.min(1,Math.max(0,(edge-1)/5))*(l.kind==='cloth'?mask[j]:l.kind==='light'?(warm[j]>0?mask[j]:0):1)*255);}
  ct.putImageData(result,0,0);ac.drawImage(frame,f%4*l.w,Math.floor(f/4)*l.h);
 }
 fs.writeFileSync(path.join(out,l.index+'.png'),atlas.toBuffer('image/png'));atlases.set(l.index,atlas);metrics.push({index:l.index,panel:l.panel,kind:l.kind,pixels:l.w*l.h*12,hotCount});
}
// Review exact baked frames at material scale and whole-panel scale.
for(const key of ['market','residential','prison','gates-descent','citadel','citadel-link','join-01','join-03','join-08','join-11']){
 const source=sources.get(key),c=createCanvas(source.width,source.height),ctx=c.getContext('2d');ctx.drawImage(source,0,0);for(const l of api.layers.filter(l=>l.panel===key).sort((a,b)=>(a.kind==='fire'?2:a.kind==='light'?-2:0)-(b.kind==='fire'?2:b.kind==='light'?-2:0))){const f=5,a=atlases.get(l.index);ctx.drawImage(a,f%4*l.w,Math.floor(f/4)*l.h,l.w,l.h,l.x,l.y,l.w,l.h);}fs.writeFileSync(path.join(qa,key+'.png'),c.toBuffer('image/png'));
}
const contact=createCanvas(1280,432*3),cc=contact.getContext('2d');for(const [i,key]of ['market','residential','prison','gates-descent','citadel','citadel-link'].entries()){const im=await loadImage(path.join(qa,key+'.png'));cc.drawImage(im,0,0,im.width,im.height,(i%2)*640,Math.floor(i/2)*432,640,Math.round(im.height/im.width*640));}fs.writeFileSync(path.join(qa,'contact.jpg'),contact.toBuffer('image/jpeg'));
fs.writeFileSync(path.join(root,'source-art/city-ambient-v178/bake-report.json'),JSON.stringify({layers:metrics.length,textureMiB:metrics.reduce((a,l)=>a+l.pixels*4,0)/1024/1024,regions:metrics},null,2));
const manifest=path.join(root,'dist/loading-assets.js');let text=fs.readFileSync(manifest,'utf8');text=text.replace(/\n "assets\/city\/ambient\/[^"\n]+",/g,'');text=text.replace('window.KillQuestBootAssets=[','window.KillQuestBootAssets=[\n'+api.layers.map(l=>' "assets/city/ambient/'+l.index+'.png?v=city-ambient-v178",').join('\n'));fs.writeFileSync(manifest,text);
console.log('Baked',metrics.length,'painted material animations;',Math.round(metrics.reduce((a,l)=>a+l.pixels*4,0)/1024/1024),'MiB texture memory.');console.log('Fire boxes with insufficient source flame:',metrics.filter(l=>l.kind==='fire'&&l.hotCount<3));
})().catch(e=>{console.error(e);process.exit(1)});
