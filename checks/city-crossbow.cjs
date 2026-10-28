const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);
vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.T=TestCombat;globalThis.F=ForestCombat;globalThis.C=CityCombat;globalThis.frame=banditFrame;globalThis.height=jumpHeight;globalThis.flightHeight=playerThrownHeight;globalThis.bind=m=>scene.model=m;",c);
function make(hero='kael'){const m=new c.T(hero);c.bind(m);m.containers=[];m.enemies=[];m.p.x=600;m.p.y=555;return m;}
function gunner(m,face=-1){const e={kind:'crossbowman',id:9020,x:face<0?1000:200,y:555,face,hp:95,maxHp:95,state:'idle',t:0,cool:0,walkDistance:0,loaded:true,reloadRemaining:0};m.enemies=[e];return e;}
function stepEnemies(m,t){for(let i=0;i<Math.round(t/.01);i++)m.updateEnemies(.01);}
function bolt(face=1,extra={}){return {kind:'bolt',x:600-face*150,y:555,z:112,vx:face*720,vy:0,life:2,damage:24,launch:true,throwDistance:235,...extra};}
// New enemy enters off-screen alongside the existing guards and Ironshield.
let m=new c.T('kael');c.bind(m);m.p.inv=999;assert.equal(m.enemies.length,13);assert.equal(m.enemies.filter(e=>e.kind==='guard').length,3);const entry=m.enemies.find(e=>e.kind==='crossbowman');assert(entry.x>1280&&entry.state==='entering');m.players.forEach(p=>p.inv=999);for(let i=0;i<800;i++)m.update(.01,new Set());assert(entry.x<1280&&entry.state!=='entering');
// Aim → single release → 1.9s stationary reload → next shot, with no auto fire.
for(const face of [-1,1]){m=make();m.p.inv=999;const e=gunner(m,face);let shots=0;const fire=m.fireCrossbow.bind(m);m.fireCrossbow=e=>{shots++;fire(e);};m.updateEnemies(.01);assert.equal(e.state,'attack');stepEnemies(m,.61);assert.equal(shots,0);stepEnemies(m,.02);assert.equal(shots,1);assert.equal(e.loaded,false);stepEnemies(m,.52);assert.equal(e.state,'reload');const x=e.x,y=e.y;stepEnemies(m,1.89);assert.equal(shots,1);assert.equal(e.state,'reload');assert.equal(e.x,x);assert.equal(e.y,y);stepEnemies(m,.02);assert(e.loaded);assert.equal(shots,1);stepEnemies(m,.9);assert.equal(shots,2);}
// Reload progress persists across a stagger; it can't instantly fire afterward.
m=make();m.p.inv=999;let e=gunner(m);e.loaded=false;e.state='reload';e.reloadRemaining=1.4;stepEnemies(m,.3);const remaining=e.reloadRemaining;e.state='hurt';e.t=0;stepEnemies(m,.35);assert(Math.abs(e.reloadRemaining-remaining)<.011);stepEnemies(m,.02);assert.equal(e.state,'reload');assert(e.reloadRemaining>1);assert.equal(m.arrows.length,0);
// Every hero is launched in bolt travel direction, lands down, then recovers.
for(const hero of ['kael','lyra','garran','selene'])for(const face of [-1,1]){
 m=make(hero);m.arrows=[bolt(face)];m.updateArrows(.3);assert.equal(m.p.hp,76);assert.equal(m.p.state,'launched');assert.equal(m.p.launchTo,600+face*235);assert.equal(m.arrows.length,0);for(let i=0;i<67;i++)m.updatePlayer(.01,new Set());assert.equal(m.p.state,'down');assert(Math.abs(m.p.x-(600+face*235))<.01);for(let i=0;i<90;i++)m.updatePlayer(.01,new Set());assert.equal(m.p.state,'idle');
 // A midair hit keeps its height at the instant of launch.
 m=make(hero);m.jump();m.p.t=.25;const h=c.height(m.p);m.arrows=[bolt(face)];m.updateArrows(.3);assert.equal(m.p.state,'launched');assert(Math.abs(c.flightHeight(m.p)-h)<1e-6);
 // Dodge/rage/respawn invincibility still prevents damage and launch.
 m=make(hero);m.p.inv=.5;m.arrows=[bolt(face)];m.updateArrows(.3);assert.equal(m.p.hp,100);assert.notEqual(m.p.state,'launched');
 m=make(hero);m.arrows=[bolt(face,{y:620})];m.updateArrows(.3);assert.equal(m.p.hp,100,'other lane hit');
}
// Garran frontal guard blocks; rear impacts launch him. Ordinary arrows still hurt.
for(const rear of [false,true]){m=make('garran');m.p.face=rear?1:-1;m.dodge();m.p.t=.1;m.arrows=[bolt(1)];m.updateArrows(.3);assert.equal(m.p.hp,rear?76:100);assert.equal(m.p.state==='launched',rear);}
m=make();m.arrows=[{x:450,y:555,vx:720,vy:0,life:1}];m.updateArrows(.3);assert.equal(m.p.hp,91);assert.equal(m.p.state,'hurt');
// First co-op player in the bolt path gets launched; the player behind is unharmed.
m=make(['kael','lyra']);m.players[0].x=500;m.players[1].x=650;m.players.forEach(p=>{p.y=555;p.inv=0;});m.arrows=[bolt(1,{x:350})];m.updateArrows(.6);assert.equal(m.players[0].hp,76);assert.equal(m.players[0].state,'launched');assert.equal(m.players[1].hp,100);
// Target and aim stay locked while firing; an injured crossbowman can be grabbed.
m=make(['kael','lyra']);m.players[0].x=600;m.players[0].y=555;m.players[1].x=100;m.players[1].y=555;m.players.forEach(p=>p.inv=999);e=gunner(m);m.updateEnemies(.01);const aim=e.aimX;m.players[1].x=950;stepEnemies(m,.65);assert.equal(e.targetPlayer,0);assert.equal(e.aimX,aim);assert.equal(e.face,-1);
m=make();e=gunner(m);e.x=630;e.state='reload';e.loaded=false;e.reloadRemaining=1;assert(m.tryGrab());assert.equal(e.state,'grabbed');m.throwGrab(new Set(['ArrowRight']));for(let i=0;i<80;i++)m.updatePlayer(.01,new Set());assert.equal(e.state,'thrown');
// Death uses normal life handling, not a throw that delays the death indefinitely.
m=make();m.p.hp=20;m.arrows=[bolt()];m.updateArrows(.3);assert(m.p.hp<=0);assert.notEqual(m.p.state,'launched');m.loseLife();assert.equal(m.p.lives,2);
// Reachable frames exist, HUD/score identifies him, and campaigns stay unchanged.
for(const state of ['idle','walk','entering','attack','reload','hurt','grabbed','thrown','down','dead','pitfall'])for(let t=0;t<2;t+=.05){const key=c.frame({kind:'crossbowman',state,t,walkDistance:t*100,reloadRemaining:1.9-t,lift:t*30});assert(fs.existsSync('dist/assets/characters/'+key+'.png'),key);}
m=make();e=gunner(m);assert(m.recordEnemyDefeat(e,0));assert.equal(m.p.score,225);assert(!m.recordEnemyDefeat(e,0));assert.equal(new c.C('kael').enemies.length,0);assert(!new c.F('kael').enemies.some(e=>e.kind==='crossbowman'));
console.log('PASS crossbowman entry, aim/single-shot/reload loop, reload interruption, all heroes both-direction bolt launch/down/recovery and airborne height continuity, invincibility/lane/shield/co-op contact, grab/throw, lethal life handling, frames/score, campaign isolation');
