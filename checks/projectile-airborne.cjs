const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');const ctx={Set,Map,Math,Number,window:{},document:{getElementById:()=>null}};vm.createContext(ctx);vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};globalThis.C=Combat;globalThis.height=jumpHeight;globalThis.contact=projectileBodyContact;",ctx);
const make=hero=>{const m=new ctx.C(hero);m.enemies=[];m.containers=[];m.pitEnabled=false;m.p.x=600;m.p.y=555;m.p.rage=30;return m;};
const arrow=(face=1,z=80,y=555)=>({x:600-face*110,y,z,vx:face*1000,vy:0,vz:0,life:1});
for(const hero of ['kael','lyra','garran','selene'])for(const face of [-1,1]){
 let m=make(hero);m.jump();m.p.t=.22;assert(ctx.height(m.p)>45&&ctx.height(m.p)<75);m.arrows=[arrow(face)];m.updateArrows(.22);assert.equal(m.p.hp,91,hero+' lower airborne body gets hit');assert.equal(m.p.rage,27);assert.equal(m.arrows.length,0);
 m=make(hero);m.jump();m.p.t=.41;assert(ctx.height(m.p)>100);m.arrows=[arrow(face)];m.updateArrows(.22);assert.equal(m.p.hp,100,'arrow below airborne feet misses');assert.equal(m.arrows.length,1);
 m.arrows=[arrow(face,180)];m.updateArrows(.22);assert.equal(m.p.hp,91,'elevated projectile intersects airborne torso');
 m=make(hero);m.jump();m.p.t=.22;m.arrows=[arrow(face,80,610)];m.updateArrows(.22);assert.equal(m.p.hp,100,'different lane misses');
 m=make(hero);m.jump();m.p.t=.22;m.p.inv=.5;m.arrows=[arrow(face)];m.updateArrows(.22);assert.equal(m.p.hp,100,'explicit invincibility remains');
}
// The same generic update handles a future high/diagonal projectile with its own damage.
let m=make('kael');m.jump();m.p.t=.41;const bolt={x:490,y:555,z:300,vx:1100,vy:0,vz:-1000,damage:23,hitRadius:10,life:1};m.updateHostileProjectiles([bolt],.2);assert.equal(m.p.hp,77);assert.equal(bolt.life,0);
// First actual collision wins; a shield behind another player cannot intercept through them.
m=new ctx.C(['kael','garran']);m.players.forEach(p=>{p.y=555;p.inv=0});m.players[0].x=500;m.players[1].x=600;m.players[1].face=-1;m.withPlayer(1,()=>m.dodge());m.arrows=[{x:400,y:555,vx:1000,vy:0,life:1}];m.updateArrows(.3);assert.equal(m.players[0].hp,91);assert.equal(m.players[1].hp,100);
// Arrows and flames can hit thrown enemies in the air, preserving their flight until landing.
for(const magic of [false,true]){
 m=make(magic?'selene':'lyra');const e={id:1,kind:'sword',x:700,y:555,hp:300,maxHp:300,state:'thrown',t:.25,throwFrom:700,throwTo:900,throwOwner:0,face:1,fallDamage:25,fallApplied:false};m.enemies=[e];
 if(magic){m.witchFlames=[{owner:0,x:600,y:555,z:220,vx:1000,vz:0,face:1,damage:22,life:1,age:0,step:0}];m.updateWitchProjectiles(.2);assert.equal(e.hp,278);}
 else{m.playerArrows=[{owner:0,x:600,y:555,z:220,vx:1000,vy:0,vz:0,face:1,damage:45,life:1}];m.updatePlayerArrows(.2);assert.equal(e.hp,255);}
 assert.equal(e.state,'thrown');assert.equal(e.t,.25);assert.equal(e.throwTo,900);assert.equal(e.fallApplied,false);
}
console.log('PASS: both-facing arrows hit all airborne heroes on body intersection, pass underneath/other lanes, respect invincibility, elevated/diagonal future projectiles and first-contact shield order; arrows/flames hit airborne enemies without resetting flight.');
