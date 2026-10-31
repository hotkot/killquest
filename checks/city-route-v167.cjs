// Isolated geometry regression: combat population disabled; campaign coverage lives in carion-campaign-v167.cjs.
const fs=require('fs'),vm=require('vm'),assert=require('assert');let finished=0;
const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);const src=fs.readFileSync('dist/game.js','utf8');vm.runInContext(src.split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>globalThis.done();globalThis.C=CityCombat;globalThis.F=ForestCombat;globalThis.layout=CITY_LAYOUT;globalThis.road=cityRoadCenter;globalThis.bounds=cityRoadBounds;globalThis.pavement=cityPavement;globalThis.width=CITY_WIDTH;globalThis.forestWidth=FOREST_WIDTH;globalThis.bind=m=>scene.model=m;globalThis.regions=CAMPAIGN_LEVELS;globalThis.playable=campaignPlayable;",c);c.done=()=>finished++;
function make(heroes='kael'){const m=new c.C(heroes);const reset=m.reset.bind(m);m.reset=(...args)=>{reset(...args);m.enemies=[];m.cityGroups=[];m.cityEncounters=[];};m.enemies=[];m.cityGroups=[];m.cityEncounters=[];c.bind(m);return m;}
function step(m,t,input=new Set()){for(let i=0;i<Math.ceil(t/.02);i++)m.update(.02,input);if(m.phase==='dialogue'){for(let j=0;j<4;j++){m.villageDialogueAge=.3;m.dismissDialogue();}}}
assert.equal(c.width,c.forestWidth*2);assert(c.playable('carion'));assert(!c.playable('temple'));
let m=make();assert.equal(m.enemies.length,0);assert.equal(m.phase,'entrance');step(m,3);assert.equal(m.phase,'explore');assert(Math.abs(m.p.x-320)<.01);assert.equal(m.p.rage,0);
// A full playable traverse using actual movement and heavy strikes to clear central barricades.
let lastCamera=0;for(let i=0;i<11000&&!m.complete;i++){const blockage=m.containers.find(c=>!c.broken&&!c.indestructible&&Math.abs(c.y-m.p.y)<45&&c.x>m.p.x&&c.x-m.p.x<140);if(blockage&&m.p.state==='idle'||blockage&&m.p.state==='walk')m.attack(true);let targetY=c.road(Math.min(25599,m.p.x+100));for(const b of m.containerBounds()){if(b.r>m.p.x&&b.l<m.p.x+180&&targetY>b.t-12&&targetY<b.b+12){const [top,bottom]=c.bounds(Math.max(m.p.x,b.l+5));targetY=b.b+14<bottom?b.b+14:b.t-14;}}const safe=c.bounds(m.p.x+40);targetY=Math.max(safe[0]+10,Math.min(safe[1]-10,targetY));const dy=targetY-m.p.y;const input=new Set(['ArrowRight']);if(dy>9)input.add('ArrowDown');else if(dy< -9)input.add('ArrowUp');m.update(.02,input);assert(m.roadContains(m.p.x,m.p.y),'left painted street');assert(m.cameraX>=lastCamera,'camera rewound');lastCamera=m.cameraX;assert.equal(m.enemies.length,0,'enemy spawned');}
assert(m.complete,'could not traverse city');assert.equal(finished,1);
// Backtracking is bounded by the furthest camera position. Allow the camera
// to catch up after the fixture teleports the player; normal movement is continuous.
m=make();step(m,3);m.p.x=6000;m.p.y=555;m.update(.02,new Set());step(m,20);const edge=m.cameraX;step(m,8,new Set(['ArrowLeft']));assert.equal(m.cameraX,edge);assert(m.p.x>=edge+60);
// Solid props block, survive damage; containers block until destroyed and food appears only then.
m=make();step(m,3);const prop=m.containers.find(c=>c.indestructible),hp=prop.hp;m.damageContainers(10000,c=>c===prop);assert.equal(prop.hp,hp);assert(!prop.broken);const crate=m.containers.find(c=>!c.indestructible&&c.loot==='food');assert.equal(m.foods.length,0);m.damageContainers(1000,c=>c===crate);assert(crate.broken);assert.equal(m.foods.length,1);
// Four players stay together, camera never abandons the rear player, reset restores empty rage.
m=make(['kael','lyra','garran','selene']);step(m,3);m.players[0].x=2000;m.update(.02,new Set());assert(Math.max(...m.players.map(p=>p.x))-Math.min(...m.players.map(p=>p.x))<=850);assert(m.cameraX<=Math.min(...m.players.map(p=>p.x))-80);m.reset();assert.equal(m.players.length,4);assert(m.players.every(p=>p.rage===0));assert.equal(m.enemies.length,0);
console.log('PASS City: 25,600px, 3s entry, entire traversal with movement/destruction, zero spawns, forward-only camera/rear clamp, food/solid props, four-player tether/reset, completion and region eligibility');
for(const hero of ['kael','lyra','garran','selene']){const city=make(hero),forest=new c.F(hero);for(const m of [city,forest]){c.bind(m);m.phase='explore';m.enemies=[];m.containers=[];m.p.x=600;m.p.y=555;m.p.state='idle';for(let i=0;i<50;i++)m.update(.02,new Set(['ArrowRight']));}assert(Math.abs(city.p.x-forest.p.x)<.001,hero+' city movement was slowed');assert(Math.abs(city.p.x-600-(hero==='lyra'?245:220))<.001);}
console.log('PASS unchanged walk speed for all four heroes: City matches Forest exactly');

// Bends guide horizontal input diagonally; movement and airborne/dash actions stay on pavement.
// Initialize the view at each teleported test location so this tests local descent tracking.
for(const tile of Array.from(c.layout).filter(t=>t.descent)){m=make();step(m,3);m.p.x=tile.x+tile.width*.15;m.p.y=c.road(m.p.x);m.cameraX=Math.max(0,m.p.x-520);m.cameraY=Math.max(0,m.p.y-555);m.p.state='idle';m.containers=[];step(m,7,new Set(['ArrowRight']));assert(m.p.x>tile.x+tile.width*.65,'horizontal input snagged on descending curb');assert(m.roadContains(m.p.x,m.p.y));const before=m.p.x;for(let i=0;i<650;i++){const input=new Set(['ArrowRight']);if(c.road(m.p.x+100)-m.p.y>8)input.add('ArrowDown');m.update(.02,input);assert(m.roadContains(m.p.x,m.p.y));}assert(m.p.x>before+1000);assert(m.p.y>tile.y+750);assert(m.cameraY>tile.y+100);}
for(const hero of ['kael','lyra','garran','selene']){m=make(hero);step(m,3);m.containers=[];const t=c.layout[7];m.p.x=t.x+t.width*.4;m.p.y=c.road(m.p.x);m.p.lastSafeX=m.p.x;m.p.lastSafeY=m.p.y;m.p.state='idle';m.dodge();step(m,.8,new Set(['ArrowRight']));assert(m.roadContains(m.p.x,m.p.y));m.p.state='idle';m.p.rage=100;m.rageAttack();step(m,3);assert(m.roadContains(m.p.x,m.p.y));m.beginRespawn();step(m,1.5);assert(m.roadContains(m.p.x,m.p.y));}
console.log('PASS three real descents guide input along curbs, vertical camera, wall-safe dodges/rage/respawns for all heroes');
m=make(['kael','lyra','garran','selene']);step(m,3);m.containers=[];
for(let i=0;i<13000&&!m.complete;i++){const inputs=m.players.map(p=>{const k=new Set(['ArrowRight']),d=c.road(p.x+100)-p.y;if(d>8)k.add('ArrowDown');else if(d< -8)k.add('ArrowUp');return k;});m.update(.02,{playerInputs:inputs});for(const p of m.players){assert(m.roadContains(p.x,p.y));assert(p.y-m.cameraY<710&&p.y-m.cameraY>220,'vertical camera abandoned party');}}
assert(m.complete,'four-player descent traversal failed');console.log('PASS full four-hero traversal: independent movement speeds, three bends, legal feet and party visible through vertical camera follow');
// Independent visual landmarks from the reviewed pavement artwork (world units).
for(const [panel,u,top,bottom] of [[0,.4,452,655],[2,.5,512,660],[3,.5,618,790],[4,.5,444,660],[7,.6,676,826],[8,.5,456,668],[9,.6,688,874],[10,.5,456,662]]){
 const tile=c.layout[panel],b=c.bounds(tile.x+tile.width*u);assert(Math.abs(b[0]-(tile.y+top+8))<.01);assert(Math.abs(b[1]-(tile.y+bottom-8))<.01);
}
// Every object's complete ground footprint must fit the road, not just its center.
m=make();step(m,3);
for(const prop of m.containers){const w=prop.halfW??(prop.kind==='barrel'?54:60),t=prop.top??38,b=prop.bottom??20;
 for(let x=prop.x-w;x<=prop.x+w;x+=2){const edge=c.bounds(x);assert(prop.y-t>=edge[0]+2,prop.kind+' base behind rear curb at '+prop.x);assert(prop.y+b<=edge[1]-2,prop.kind+' base in foreground rubble at '+prop.x);}
}
// Walk every connector in both directions and along both street edges. No fake
// center narrowing, and no border prop collision exists in the open pavement.
for(let seam=1;seam<12;seam++)for(const lane of [.2,.8])for(const dir of [-1,1]){
 m=make();step(m,3);m.containers=[];const center=seam*c.layout[0].width,start=center-dir*350;let x=start;const yAt=x=>{const [a,b]=c.bounds(x);return a+(b-a)*lane;};let actor={x,y:yAt(x)};
 for(let j=0;j<350;j++){const oldX=actor.x,oldY=actor.y;actor.x+=dir*2;actor.y=yAt(actor.x);m.resolveContainers(actor,oldX,oldY);assert(Math.abs(actor.x-(oldX+dir*2))<.001,'invisible join wall '+seam);assert(m.roadContains(actor.x,actor.y));}
}
// Route and props resolve together: repeatedly pushing diagonally against either
// face of every solid can never project a player inside it or off the pavement.
m=make();step(m,3);
for(const prop of m.containers.filter(p=>p.indestructible))for(const side of [-1,1]){
 const w=prop.halfW,t=prop.top,b=prop.bottom;const actor={x:prop.x+side*(w+6),y:prop.y};actor.y=Math.max(c.bounds(actor.x)[0],Math.min(c.bounds(actor.x)[1],actor.y));
 for(let j=0;j<80;j++){const ox=actor.x,oy=actor.y;actor.x-=side*4;actor.y+=j<40?2:-2;m.resolveContainers(actor,ox,oy);assert(m.roadContains(actor.x,actor.y));assert(!(actor.x>prop.x-w+.01&&actor.x<prop.x+w-.01&&actor.y>prop.y-t+.01&&actor.y<prop.y+b-.01),'clipped inside solid '+prop.x);}
}
console.log('PASS traced artwork landmarks, all prop footprints on pavement, 44 bidirectional edge-lane join crossings, combined curb/prop collision stress');
m=make(['kael','lyra','garran','selene']);step(m,3);
for(let tick=0;tick<14000&&!m.complete;tick++){
 const inputs=m.players.map((p,index)=>{const k=new Set(['ArrowRight']);let ty=c.road(p.x+100);
  for(const box of m.containerBounds())if(box.r>p.x&&box.l<p.x+180&&ty>box.t-12&&ty<box.b+12){const [top,bottom]=c.bounds(Math.max(p.x,box.l+5));ty=box.b+14<bottom?box.b+14:box.t-14;}
  const b=c.bounds(p.x+40);ty=Math.max(b[0]+10,Math.min(b[1]-10,ty));if(ty-p.y>9)k.add('ArrowDown');else if(ty-p.y< -9)k.add('ArrowUp');
  if(['idle','walk'].includes(p.state)&&m.containers.some(b=>!b.broken&&!b.indestructible&&b.x>p.x&&b.x-p.x<140&&Math.abs(b.y-p.y)<45))m.command(index,'heavy',k);return k;
 });m.update(.02,{playerInputs:inputs});for(const p of m.players)assert(m.roadContains(p.x,p.y));
}
assert(m.complete,'four-player traverse with all props failed');console.log('PASS all four heroes traverse complete city with actual solid props and breakable containers');
// Regress the actual snag: horizontal or outward-diagonal input at either exact
// curb must advance in both directions, across every panel/join/sample corner.
m=make();step(m,3);m.containers=[];
let edgeChecks=0;
for(let start=400;start<c.width-400;start+=29)for(const edge of [0,1])for(const dir of [-1,1])for(const outward of [false,true]){
 const oldY=c.bounds(start)[edge],actor={x:start+dir*4,y:oldY+(outward?(edge?4:-4):0)},budget=outward?Math.sqrt(32):4;
 m.resolveContainers(actor,start,oldY);
 assert((actor.x-start)*dir>1,'curb snag at '+start+' edge '+edge+' direction '+dir);
 assert(m.roadContains(actor.x,actor.y),'curb slide left pavement');
 assert(Math.hypot(actor.x-start,actor.y-oldY)<=budget+.001,'curb slide accelerated');edgeChecks++;
}
// No direction changes or path-following test automation: hold Right through all
// three descents and joins, starting at either edge. Both must remain traversable.
for(const hero of ['kael','lyra','garran','selene'])for(const edge of [0,1]){
 m=make(hero);step(m,3);m.containers=[];m.p.y=c.bounds(m.p.x)[edge];let old=m.p.x;
 for(let tick=0;tick<8500&&!m.complete;tick++){m.update(.02,new Set(['ArrowRight']));assert(m.p.x>old+.2,'held-right curb deadlock '+hero+' at '+old);old=m.p.x;assert(m.roadContains(m.p.x,m.p.y));}
 assert(m.complete,'held-right traversal failed '+hero);
}
console.log('PASS '+edgeChecks+' exact-curb movement/speed checks, both directions and outward diagonals; all heroes hold Right through entire city from either edge');
