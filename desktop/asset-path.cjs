'use strict';
const path=require('node:path');
module.exports=function resolveAsset(root,url){
 const parsed=new URL(url);
 if(parsed.protocol!=='killquest:'||parsed.hostname!=='game')return null;
 let pathname;
 try{pathname=decodeURIComponent(parsed.pathname);}catch{return null;}
 if(pathname.includes('\0')||pathname.includes('\\'))return null;
 const candidate=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
 const relative=path.relative(root,candidate);
 if(!relative||relative.startsWith('..')||path.isAbsolute(relative))return null;
 return candidate;
};
