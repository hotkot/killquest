/* Opaque architectural quilting: joins follow low-error masonry/paving contours.
   Every output pixel comes wholly from one source. No transparency or crossfade. */
(function(root){
 function cut(a,b,w,h,left,right){const span=right-left+1,previous=new Float64Array(span),current=new Float64Array(span),parents=new Int16Array(span*h);let prev=previous,next=current;
  for(let y=0;y<h;y++){for(let k=0;k<span;k++){const p=(y*w+left+k)*4;let best=k;if(y){if(k&&prev[k-1]<prev[best])best=k-1;if(k+1<span&&prev[k+1]<prev[best])best=k+1;}const error=Math.abs(a[p]-b[p])+Math.abs(a[p+1]-b[p+1])+Math.abs(a[p+2]-b[p+2]);next[k]=error+(y?prev[best]:0);parents[y*span+k]=best;}[prev,next]=[next,prev];}
  let k=0;for(let n=1;n<span;n++)if(prev[n]<prev[k])k=n;const path=new Int16Array(h);for(let y=h-1;y>=0;y--){path[y]=left+k;k=parents[y*span+k];}return path;
 }
 function fit(generated,reference,w,h){const a=cut(generated,reference,w,h,Math.round(w*.125),Math.round(w*.405)),b=cut(generated,reference,w,h,Math.round(w*.595),Math.round(w*.875)),out=new Uint8ClampedArray(generated);for(let y=0;y<h;y++)for(let x=0;x<w;x++){const p=(y*w+x)*4;if(x<a[y]||x>b[y]){out[p]=reference[p];out[p+1]=reference[p+1];out[p+2]=reference[p+2];}out[p+3]=255;}return out;}
 root.CityJoinFit={fit};if(typeof module!=='undefined')module.exports=root.CityJoinFit;
})(typeof globalThis!=='undefined'?globalThis:this);
