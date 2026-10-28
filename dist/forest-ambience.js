/* Painted scenery stays in world coordinates. All moving layers use the original
   palette, source-art masks and fixed attachment points, never camera offsets. */
(()=>{'use strict';
const PANELS=['forest-a','forest-b','forest-d','forest-e','forest-c','forest-village','market','village','village-arena','arena-v63'];
const FITTED_FIRES=[{key:'roof-left',x:30,y:25,w:160,h:113},{key:'roof-center',x:320,y:120,w:168,h:127},{key:'door',x:414,y:316,w:56,h:94},{key:'transition-roof',panel:'forest-village',x:1000,y:170,w:270,h:160},{key:'transition-wall',panel:'forest-village',x:1170,y:286,w:82,h:84}];
const CLEAN=['forest-village','market','village','village-arena','arena-v63'];
const layers=[];
const cloth=(panel,poly,mode='banner',extra={})=>layers.push({panel,kind:'cloth',poly,mode,...extra});
const water=(panel,poly)=>layers.push({panel,kind:'water',poly});
const fire=(panel,x,y,w,h)=>layers.push({panel,kind:'fire',x,y,w,h});
const smoke=(panel,x,y,w,h,alpha=.48)=>layers.push({panel,kind:'smoke',x,y,w,h,alpha});
water('forest-a',[[997,337],[1035,337],[1031,354],[1023,365],[1038,371],[1014,386],[1029,397],[1102,400],[1154,415],[1130,436],[1165,444],[1135,468],[1080,485],[1035,483],[1001,470],[1000,450],[969,445],[924,431],[937,413],[973,415],[987,404],[974,393],[985,379],[980,368]]);
water('forest-b',[[1140,303],[1194,302],[1170,318],[1196,324],[1190,345],[1245,350],[1243,370],[1205,383],[1229,395],[1245,413],[1196,435],[1250,443],[1309,457],[1290,469],[1210,457],[1168,446],[1110,447],[1075,438],[1029,430],[1017,407],[1001,399],[1012,381],[1010,369],[1060,363],[1080,356],[1094,348],[1093,333],[1107,327],[1124,326]]);
water('village-arena',[[784,382],[815,382],[814,395],[835,405],[822,419],[880,421],[916,432],[956,433],[980,445],[951,460],[951,476],[913,484],[875,478],[858,463],[846,445],[821,440],[796,435],[772,423],[778,408]]);
// Torn edges follow the actual painted silhouettes; poles/crossbars are excluded.
cloth('market',[[577,268],[631,282],[692,282],[737,276],[737,318],[728,337],[714,331],[703,342],[690,327],[680,340],[657,339],[645,330],[633,347],[616,332],[604,348],[592,326]],'awning');
cloth('market',[[533,284],[556,279],[551,324],[544,340],[539,322],[530,335]],'banner');
cloth('market',[[758,319],[801,327],[848,312],[854,319],[845,339],[826,343],[813,337],[807,351],[790,345],[778,354],[768,342],[751,350]],'awning');
cloth('market',[[1029,279],[1090,290],[1159,276],[1166,314],[1150,338],[1140,330],[1130,346],[1116,332],[1106,351],[1095,337],[1083,347],[1073,329],[1060,341],[1044,327]],'awning');
cloth('market',[[1292,280],[1361,278],[1466,266],[1484,260],[1476,313],[1468,328],[1452,318],[1437,336],[1424,329],[1407,340],[1397,326],[1381,339],[1362,329],[1346,346],[1334,334],[1315,341],[1308,323],[1292,336],[1280,317]],'awning');
cloth('village',[[179,245],[287,273],[402,270],[450,244],[475,277],[450,307],[427,315],[413,305],[402,319],[384,311],[370,323],[350,323],[332,314],[316,325],[290,310],[267,312],[255,297],[230,288]],'awning');
cloth('village',[[1285,145],[1338,157],[1335,250],[1328,270],[1318,251],[1310,266],[1301,253],[1292,267]],'banner');
cloth('village',[[1408,254],[1450,227],[1488,255],[1535,255],[1535,337],[1520,329],[1508,348],[1496,334],[1480,353],[1468,337],[1455,345],[1443,331],[1428,338],[1400,312],[1390,281]],'awning');
cloth('village-arena',[[586,96],[620,101],[654,95],[651,260],[645,285],[635,266],[624,292],[614,272],[605,286],[590,266]],'banner');
cloth('village-arena',[[919,99],[950,105],[978,97],[976,269],[965,294],[955,279],[947,300],[935,278],[924,289]],'banner');
cloth('village-arena',[[1237,76],[1274,83],[1272,126],[1265,142],[1256,132],[1249,146],[1238,131]],'banner');
cloth('village-arena',[[1055,174],[1094,163],[1092,181],[1083,184],[1077,190],[1065,187]],'awning');
cloth('village-arena',[[1451,51],[1496,40],[1490,55],[1478,62],[1466,58],[1453,66]],'awning');
cloth('village-arena',[[15,262],[105,291],[173,317],[237,322],[302,307],[299,331],[281,344],[266,339],[249,351],[234,343],[218,353],[201,341],[183,345],[163,332],[141,337],[121,322],[94,317],[64,298],[21,283]],'awning');
cloth('village-arena',[[1146,179],[1237,155],[1282,168],[1274,184],[1256,188],[1231,198],[1208,195],[1192,207],[1164,202],[1141,195]],'awning');
cloth('village-arena',[[1094,245],[1123,258],[1148,252],[1145,280],[1133,294],[1123,285],[1111,295],[1098,279]],'awning');
cloth('village-arena',[[1326,250],[1392,265],[1493,239],[1482,280],[1467,297],[1454,287],[1440,302],[1424,292],[1411,309],[1395,299],[1384,311],[1367,299],[1355,310],[1337,293]],'awning');
cloth('arena-v63',[[62,43],[101,55],[141,60],[129,292],[119,321],[108,308],[99,333],[88,313],[78,324],[70,299],[53,305]],'banner');
cloth('arena-v63',[[658,65],[700,79],[745,68],[737,255],[727,282],[718,269],[708,295],[699,278],[690,306],[682,279],[669,290],[663,267]],'banner');
cloth('arena-v63',[[395,209],[420,218],[445,204],[439,301],[428,321],[418,308],[408,324],[398,303]],'banner');
cloth('arena-v63',[[577,212],[600,223],[600,259],[593,281],[584,270],[576,279]],'banner');
cloth('arena-v63',[[622,234],[646,241],[644,283],[638,300],[628,286],[622,293]],'banner');
cloth('arena-v63',[[743,235],[769,241],[766,279],[757,294],[750,282],[744,289]],'banner');
cloth('arena-v63',[[795,214],[819,222],[818,265],[809,282],[802,268],[796,276]],'banner');
cloth('arena-v63',[[953,217],[977,228],[989,222],[989,310],[979,333],[969,322],[961,339],[951,318]],'banner');
cloth('arena-v63',[[1059,186],[1086,196],[1106,190],[1102,305],[1092,327],[1083,315],[1072,335],[1062,313]],'banner');
cloth('arena-v63',[[1433,120],[1465,129],[1494,117],[1490,246],[1478,270],[1467,258],[1458,276],[1446,255],[1439,265]],'banner');
cloth('arena-v63',[[185,725],[222,736],[258,748],[278,772],[284,862],[243,862],[234,820],[224,785],[203,768]],'banner',{foreground:true});
cloth('arena-v63',[[306,774],[331,781],[350,798],[378,797],[396,826],[402,863],[340,863],[330,835],[316,812]],'banner',{foreground:true});
for(const a of [[1100,353,28,49],[1340,274,36,58]])fire('forest-village',...a);
smoke('forest-village',1115,227,185,285,.40);smoke('forest-village',1370,222,155,260,.32);
smoke('market',752,225,130,245,.34);smoke('market',951,166,96,200,.28);
for(const a of [[115,119,137,84],[366,207,36,65],[421,213,52,82],[450,229,65,77],[558,267,37,66],[669,313,100,123],[791,338,86,58],[940,343,111,100],[443,397,31,70],[694,434,44,42],[1460,194,52,68]])fire('village',...a);
for(const a of [[400,180,170,270,.48],[681,265,200,330,.48],[971,300,170,290,.44],[1460,175,140,255,.36]])smoke('village',...a);
fire('village-arena',1251,294,43,48);smoke('village-arena',1375,174,120,245,.37);
for(const a of [[66,336,34,49],[477,315,31,41],[565,316,20,30],[635,309,17,28],[752,313,16,24],[845,316,24,38],[939,326,34,48],[1310,373,28,40],[1433,356,36,48],[367,84,21,30]])fire('arena-v63',...a);
smoke('arena-v63',365,91,109,195,.40);smoke('arena-v63',1367,190,163,270,.40);
const BRAZIERS=[{id:'left',x:66,y:343,w:110,h:80,poly:[[35,340],[91,340],[88,350],[78,358],[50,356],[38,349]]},{id:'hall-left',x:477,y:322,w:90,h:68,poly:[[450,319],[500,319],[493,331],[481,339],[465,336],[454,329]]},{id:'hall-right',x:939,y:333,w:100,h:72,poly:[[912,329],[968,329],[960,342],[943,348],[923,341]]},{id:'right',x:1433,y:365,w:105,h:78,poly:[[1400,365],[1460,365],[1451,378],[1430,385],[1411,377]]}];
for(const b of BRAZIERS){const l=layers.find(l=>l.panel==='arena-v63'&&l.kind==='fire'&&l.x===b.x);Object.assign(l,{y:b.y,w:b.w,h:b.h,brazierId:b.id});}
function polygon(ctx,p,ox=0,oy=0){ctx.moveTo(p[0][0]-ox,p[0][1]-oy);for(let i=1;i<p.length;i++)ctx.lineTo(p[i][0]-ox,p[i][1]-oy);ctx.closePath();}
function bounds(poly,pad=0){const x=Math.max(0,Math.floor(Math.min(...poly.map(p=>p[0]))-pad)),y=Math.max(0,Math.floor(Math.min(...poly.map(p=>p[1]))-pad));return{x,y,w:Math.min(1536-x,Math.ceil(Math.max(...poly.map(p=>p[0]))+pad-x)),h:Math.min(864-y,Math.ceil(Math.max(...poly.map(p=>p[1]))+pad-y))};}
function source(scene,key){return scene.textures.get(key).getSourceImage();}
function canvas(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return c;}
function prepareBackground(scene,panel){const key='ambient-bg-'+panel;if(scene.textures.exists(key))return key;const texture=scene.textures.createCanvas(key,1536,864),ctx=texture.context,original=source(scene,'level-'+panel);ctx.drawImage(original,0,0,1536,864);const patch=canvas(1536,864),pc=patch.getContext('2d');pc.drawImage(source(scene,'ambient-clean-'+panel),0,0,1536,864);const mask=canvas(1536,864),mc=mask.getContext('2d');const fade=mc.createLinearGradient(0,428,0,468);fade.addColorStop(0,'rgba(255,255,255,1)');fade.addColorStop(1,'rgba(255,255,255,0)');mc.fillStyle=fade;mc.fillRect(0,0,1536,468);mc.fillStyle='#fff';mc.strokeStyle='#fff';mc.lineWidth=12;mc.lineJoin='round';mc.filter='blur(2px)';mc.beginPath();for(const l of layers.filter(l=>l.panel===panel&&l.foreground))polygon(mc,l.poly);mc.fill();mc.stroke();pc.globalCompositeOperation='destination-in';pc.drawImage(mask,0,0);ctx.drawImage(patch,0,0);
 // Restore the exact river silhouette and banks below the water animation mask.
 for(const l of layers.filter(l=>l.panel===panel&&l.kind==='water')){ctx.save();ctx.beginPath();polygon(ctx,l.poly);ctx.clip();ctx.drawImage(original,0,0,1536,864);ctx.restore();}texture.refresh();return key;}
function prepareMoving(scene,l,index){const b=bounds(l.poly,10),seed=canvas(b.w,b.h),sc=seed.getContext('2d');sc.beginPath();polygon(sc,l.poly,b.x,b.y);sc.clip();sc.drawImage(source(scene,'level-'+l.panel),-b.x,-b.y,1536,864);l.bounds=b;l.frames=[];
 for(let f=0;f<16;f++){const key='ambient-layer-'+index+'-'+f;l.frames.push(key);if(scene.textures.exists(key))continue;const texture=scene.textures.createCanvas(key,b.w,b.h),ctx=texture.context,phase=f*Math.PI/8;
  if(l.kind==='water'){ctx.drawImage(seed,0,0);for(let y=0;y<b.h;y+=2){const dx=Math.sin(phase+y*.16)*2.2,dy=Math.sin(phase*2+y*.13)*1.2;ctx.drawImage(seed,0,y,b.w,Math.min(2,b.h-y),dx,y+dy,b.w,Math.min(2,b.h-y));}ctx.globalCompositeOperation='destination-in';ctx.drawImage(seed,0,0);ctx.globalCompositeOperation='source-over';}
  else if(l.mode==='awning'){for(let x=0;x<b.w;x+=3){const u=x/b.w,envelope=Math.sin(Math.PI*u),dy=Math.sin(phase+u*5)*2.4*envelope;ctx.drawImage(seed,x,0,Math.min(3,b.w-x),b.h,x,0,Math.min(3,b.w-x),b.h+dy);}}
  else{for(let y=0;y<b.h;y+=2){const v=Math.max(0,(y-10)/(b.h-20)),dx=(Math.sin(phase+v*6)-Math.sin(phase))*(v*v)*3.2;ctx.drawImage(seed,0,y,b.w,Math.min(2,b.h-y),dx,y,b.w,Math.min(2,b.h-y));}}
  texture.refresh();}
}
const api={layers,clean:CLEAN,fittedFires:FITTED_FIRES,braziers:BRAZIERS,
 preloadBake(scene){for(const key of CLEAN)scene.load.image('ambient-clean-'+key,'../source-art/forest-ambient-v142/'+key+'-clean.webp');for(const kind of ['fire','smoke'])for(let i=0;i<6;i++)scene.load.image('ambient-'+kind+'-'+i,'assets/forest/ambient/'+kind+'-'+i+'.png?v=forest-v142');},
 preload(scene){for(const b of BRAZIERS)scene.load.image('brazier-rim-'+b.id,'assets/forest/ambient/brazier-rim-'+b.id+'-v144.png');for(const f of FITTED_FIRES)scene.load.spritesheet('fitted-fire-'+f.key,'assets/forest/ambient/fitted-'+f.key+'-v144.png',{frameWidth:f.w,frameHeight:f.h});for(const key of CLEAN)scene.load.image('ambient-bg-'+key,'assets/forest/ambient/bg-'+key+(key==='village'?'-v143':key==='forest-village'?'-v144':'')+'.png?v=forest-v143');layers.forEach((l,i)=>{if(!l.poly)return;l.bounds=bounds(l.poly,10);l.atlas='ambient-atlas-'+i;scene.load.spritesheet(l.atlas,'assets/forest/ambient/layer-'+i+'.png?v=forest-v142',{frameWidth:l.bounds.w,frameHeight:l.bounds.h});});for(const kind of ['fire','smoke'])for(let i=0;i<6;i++)scene.load.image('ambient-'+kind+'-'+i,'assets/forest/ambient/'+kind+'-'+i+'.png?v=forest-v142');},
 prepare(scene){layers.forEach((l,i)=>{if(l.poly){l.bounds=bounds(l.poly,10);l.atlas='ambient-atlas-'+i;}});scene.ambientPrepared=!!scene.textures&&CLEAN.every(key=>scene.textures.exists('ambient-bg-'+key));},
 bake(scene){for(const panel of CLEAN)prepareBackground(scene,panel);layers.forEach((l,i)=>{if(!l.poly)return;prepareMoving(scene,l,i);l.atlas='ambient-atlas-'+i;if(!scene.textures.exists(l.atlas)){const b=l.bounds,atlas=scene.textures.createCanvas(l.atlas,b.w*4,b.h*4);l.frames.forEach((key,f)=>atlas.context.drawImage(source(scene,key),(f%4)*b.w,Math.floor(f/4)*b.h));atlas.refresh();}});scene.ambientPrepared=true;},
 background(scene,key){return scene.ambientPrepared&&CLEAN.includes(key)?'ambient-bg-'+key:'level-'+key;},
 setup(scene){scene.ambientViews=[];if(!scene.model.isForest)return;if(!scene.ambientPrepared)api.prepare(scene);if(!scene.ambientPrepared)return;layers.forEach((l,i)=>{if(['village','forest-village'].includes(l.panel)&&l.kind==='fire')return;const panel=PANELS.indexOf(l.panel),b=l.bounds,texture=l.poly?l.atlas:'ambient-'+l.kind+'-0',x=panel*1280-80+(b?b.x:l.x)*.9375,y=(b?b.y:l.y)*5/6,w=(b?b.w:l.w)*.9375,h=(b?b.h:l.h)*5/6;const sprite=scene.add.image(x,y,texture).setOrigin(l.poly?0:.5,l.poly?0:1).setDisplaySize(w,h).setDepth(l.foreground?900:-20+panel*.01+.005);scene.worldArt.push(sprite);let next=null;if(l.kind==='smoke'){next=scene.add.image(x,y,'ambient-smoke-1').setOrigin(.5,1).setDisplaySize(w,h).setDepth(-20+panel*.01+.0051).setAlpha(0);scene.worldArt.push(next);}let rim=null;if(l.brazierId){const b=BRAZIERS.find(b=>b.id===l.brazierId),box=bounds(b.poly),rx=panel*1280-80+box.x*.9375,ry=box.y*5/6;rim=scene.add.image(rx,ry,'brazier-rim-'+b.id).setOrigin(0,0).setDisplaySize(box.w*.9375,box.h*5/6).setDepth(-20+panel*.01+.0052);scene.worldArt.push(rim);}scene.ambientViews.push({sprite,next,rim,l,x,y,w,h,phase:i*.73,index:i});});for(const [i,f] of FITTED_FIRES.entries()){const panel=PANELS.indexOf(f.panel||'village'),x=panel*1280-80+f.x*.9375,y=f.y*5/6,w=f.w*.9375,h=f.h*5/6,sprite=scene.add.image(x,y,'fitted-fire-'+f.key).setOrigin(0,0).setDisplaySize(w,h).setDepth(-20+panel*.01+.006);scene.worldArt.push(sprite);scene.ambientViews.push({sprite,l:{kind:'fitted',panel:f.panel||'village',...f},x,y,w,h,phase:i*5.3});}},
 render(scene,m){const time=m.npcTime||0,camera=m.cameraX||0;for(const v of scene.ambientViews||[]){const visible=m.isForest&&v.x+v.w>camera-100&&v.x-v.w<camera+1380;v.sprite.setVisible(visible);if(v.next)v.next.setVisible(visible);if(v.rim)v.rim.setVisible(visible);if(!visible)continue;const {l,phase}=v;if(l.kind==='fitted'){v.sprite.setTexture('fitted-fire-'+l.key,Math.floor(time*14+phase)%28);continue;}if(l.poly){const frame=Math.floor(time*(l.kind==='water'?12:8)+phase)%16;v.sprite.setTexture(l.atlas,frame);}else{const frame=Math.floor(time*(l.kind==='fire'?11:3)+phase)%6;v.sprite.setTexture('ambient-'+l.kind+'-'+frame);v.sprite.setAlpha(l.kind==='smoke'?(l.alpha||.45)*(.94+.06*Math.sin(time+phase)):.91+.06*Math.sin(time*9+phase));if(l.kind==='smoke'){const blend=(time*3+phase)%1,alpha=(l.alpha||.45)*(.94+.06*Math.sin(time+phase)),x=v.x+Math.sin(time*.5+phase)*v.w*.012;v.sprite.setPosition(x,v.y).setAlpha(alpha*(1-blend));v.next.setTexture('ambient-smoke-'+((frame+1)%6)).setPosition(x,v.y).setAlpha(alpha*blend);}else v.sprite.setDisplaySize(v.w,v.h*(.97+.03*Math.sin(time*11+phase)));}}}
};globalThis.ForestAmbience=api;
})();
