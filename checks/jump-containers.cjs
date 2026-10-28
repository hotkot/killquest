const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);
vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.models=[TestCombat,ForestCombat,CityCombat];globalThis.height=jumpHeight;globalThis.bind=m=>scene.model=m;",c);
function make(Model,hero='kael'){const m=new Model(hero);c.bind(m);m.phase='explore';m.enemies=[];m.containers=[];m.encounterIndex=999;m.activeEncounter=null;m.p.x=600;m.p.y=555;return m;}
// Measured travel against pre-change distance, with the same 0.84-second jump.
for(const hero of ['kael','lyra','garran','selene'])for(const dir of [-1,1]){
 const m=make(c.models[0],hero);m.p.x=700;m.p.face=dir;m.jump();let elapsed=0,peak=0;
 while(m.p.state==='jump'&&elapsed<2){m.update(.01,new Set([dir>0?'ArrowRight':'ArrowLeft']));elapsed+=.01;peak=Math.max(peak,c.height(m.p));}
 const distance=Math.abs(m.p.x-700),old=(hero==='kael'?175:hero==='lyra'?195:155)*.83;
 assert(distance>old*1.55&&distance<old*1.8,hero+' jump distance '+distance);assert(elapsed>=.83&&elapsed<=.86);assert(peak>109&&peak<=110.01,'jump height changed');
}
// Real full-frame jumps clear all breakable container kinds in all three models.
for(const Model of c.models)for(const hero of ['kael','lyra','garran','selene'])for(const dir of [-1,1])for(const kind of ['crate','barrel','stump','sack','basket','barricade']){
 const m=make(Model,hero),prop=m.spawnContainer(800,555,kind);m.p.x=800-dir*80;m.p.face=dir;m.jump();
 for(let i=0;i<90;i++)m.update(.01,new Set([dir>0?'ArrowRight':'ArrowLeft']));
 assert((m.p.x-800)*dir>65,Model.name+' '+hero+' failed to jump '+kind+' '+dir);assert.equal(prop.hp,prop.maxHp);assert.equal(m.foods.length,0,'jumping dropped loot');
 // Landing returns to ordinary collision from either side.
 m.p.x=800+dir*100;m.p.y=555;m.p.state='idle';m.p.bulwarkDodgePass=false;m.resolveContainers(m.p,800-dir*100,555);assert((m.p.x-800)*dir<=-53.9,hero+' grounded container pass');
}
// No blanket collision disable: permanent scenery and non-player actors stay solid.
for(const Model of c.models)for(const hero of ['kael','lyra','garran','selene']){
 const m=make(Model,hero),prop=m.spawnContainer(800,555,'cart','none');prop.indestructible=true;m.p.x=720;m.jump();
 for(let i=0;i<90;i++)m.update(.01,new Set(['ArrowRight']));assert(m.p.x<=740.01,'jump bypassed permanent scenery');
 prop.indestructible=false;const enemy={x:900,y:555,state:'jump',t:.4};m.resolveContainers(enemy,700,555);assert(enemy.x<=740.01,'enemy gained player jump exception');
 // Dropping directly inside a container resolves to a legal ground point.
 m.p.x=800;m.p.y=555;m.p.state='jump';m.p.t=.70;m.update(.01,new Set());assert(Math.abs(m.p.x-800)>=59.99||m.p.y<=517.01||m.p.y>=574.99,'landed inside container');
}
// Independent co-op inputs: one airborne hero crosses while grounded ally is blocked.
const m=make(c.models[0],['kael','lyra','garran','selene']);m.spawnContainer(800,555,'crate');for(const p of m.players){p.x=720;p.y=555;}m.withPlayer(0,()=>m.jump());
for(let i=0;i<90;i++)m.update(.01,{playerInputs:m.players.map(()=>new Set(['ArrowRight']))});assert(m.players[0].x>860);for(const p of m.players.slice(1))assert(p.x<=740.01);
console.log('PASS jump travel +65% with unchanged height/timing; all four heroes, both directions, six container kinds across Test/Forest/City; no loot/damage on hop, grounded/landing collision, permanent scenery, enemies and independent co-op');
