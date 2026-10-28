/* Steel material shader for existing Garran canvases. RGB only; immutable ink,
 * alpha, canvas bounds and sprite geometry. Runs once while assets prepare. */
(function(root){
 'use strict';
 const clamp=(n,l,h)=>Math.max(l,Math.min(h,n));
 function buildTile(data,width,height){
  const values=new Float32Array(width*height);let sum=0,square=0;
  for(let p=0;p<values.length;p++){const i=p*4,v=(data[i]+data[i+1]+data[i+2])/3;values[p]=v;sum+=v;square+=v*v;}
  const mean=sum/values.length,sd=Math.max(3,Math.sqrt(square/values.length-mean*mean));
  for(let p=0;p<values.length;p++)values[p]=clamp((values[p]-mean)/(sd*2.4),-1,1);
  return {values,width,height};
 }
 function process(data,width,height,tile,source=data){
  const out=new Uint8ClampedArray(data);if(!tile?.values?.length)return out;
  const count=width*height,mask=new Uint8Array(count),seeds=new Uint8Array(count),seen=new Uint8Array(count),queue=new Int32Array(count);
  for(let p=0;p<count;p++){
   const i=p*4,r=source[i],g=source[i+1],b=source[i+2],v=(r+g+b)/3,spread=Math.max(r,g,b)-Math.min(r,g,b);
   // Silver is neutral/cool; warm cloth, leather, wood, gold and red are excluded.
   // Preserve anti-aliased contour pixels and dark drawn lines exactly.
   if(source[i+3]<250||v<78||spread>Math.max(18,v*.16)||r-b>Math.max(16,v*.13)||g-b>Math.max(12,v*.09))continue;
   mask[p]=1;if(v>105&&v<225&&r-b<15&&g-b<11)seeds[p]=1;
  }
  for(let start=0;start<count;start++){
   if(!mask[start]||seen[start])continue;let head=0,tail=1,minX=width,minY=height,maxX=0,maxY=0,seedCount=0;queue[0]=start;seen[start]=1;
   while(head<tail){const p=queue[head++],x=p%width,y=Math.floor(p/width);seedCount+=seeds[p];minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);
    for(const q of [x? p-1:-1,x+1<width?p+1:-1,y?p-width:-1,y+1<height?p+width:-1])if(q>=0&&mask[q]&&!seen[q]){seen[q]=1;queue[tail++]=q;}
   }
   // Tiny bright fabric flecks and linework do not become textured metal.
   if(tail<18||seedCount<3||seedCount/tail<.055)continue;
   const bw=Math.max(8,maxX-minX+1),bh=Math.max(8,maxY-minY+1);
   for(let n=0;n<tail;n++){
    const p=queue[n],i=p*4,x=p%width,y=Math.floor(p/width),u=Math.floor((x-minX)/bw*(tile.width-1)),v=Math.floor((y-minY)/bh*(tile.height-1));
    const detail=tile.values[v*tile.width+u],luma=(data[i]+data[i+1]+data[i+2])/3;
    if(luma<72)continue; // Comic-pass outlines remain byte-identical as well.
    const gain=1+detail*.17,patina=Math.max(0,-detail)*3.3,gloss=Math.max(0,luma-185)*.055;
    out[i]=clamp(data[i]*gain-gloss+patina*.55,0,255);
    out[i+1]=clamp(data[i+1]*gain-gloss-patina*.1,0,255);
    out[i+2]=clamp(data[i+2]*gain-gloss-patina*.7,0,255);
   }
  }
  return out;
 }
 const api={buildTile,process};root.ArmorFinish=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
