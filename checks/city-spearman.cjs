const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);
vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.T=TestCombat;globalThis.C=CityCombat;globalThis.F=ForestCombat;globalThis.frame=banditFrame;globalThis.hud=enemyHudTargets;globalThis.bind=m=>scene.model=m;",c);
function make(hero='kael'){const m=new c.T(hero);c.bind(m);m.enemies=[];m.containers=[];m.p.x=600;m.p.y=555;return m;}
function spear(m,face=-1,range=200){const e={id:9030,kind:'spearman',x:m.p.x-face*range,y:555,face,hp:110,maxHp:110,state:'idle',t:0,cool:0,hit:false,walkDistance:0};m.enemies=[e];return e;}
function enemies(m,time){for(let i=0;i<Math.round(time/.01);i++)m.updateEnemies(.01);}
let m=new c.T('kael');c.bind(m);m.p.inv=999;assert.equal(m.enemies.length,13);assert(m.enemies.some(e=>e.kind==='crossbowman'));assert(m.enemies.some(e=>e.kind==='bulwark'));const entered=m.enemies.find(e=>e.kind==='spearman');assert(entered&&entered.x>1280&&entered.state==='entering');m.p.inv=999;for(let i=0;i<800;i++)m.update(.01,new Set());assert(entered.x<1280&&entered.state!=='entering');
// Long spear reaches beyond sword range, waits for its extension, and hits once.
for(const hero of ['kael','lyra','garran','selene'])for(const face of [-1,1]){
 m=make(hero);let e=spear(m,face,230);m.updateEnemies(.01);assert.equal(e.state,'attack');enemies(m,.55);assert.equal(m.p.hp,100,'hit before extension');enemies(m,.02);assert.equal(m.p.hp,84,hero+' missing ranged poke '+face);assert.equal(m.p.state,'hurt');assert.equal(m.p.x,600+face*30);m.p.inv=0;enemies(m,.12);assert.equal(m.p.hp,84,'repeat damage within thrust');
 while(e.state==='attack')m.updateEnemies(.01);assert(e.cool>.85);enemies(m,.75);assert.notEqual(e.state,'attack','no recovery window');
}
// Exact active geometry: forward only, actual reach/depth, and a close shaft deadzone.
for(const [dx,dy,hit] of [[244,0,true],[246,0,false],[200,29,true],[200,31,false],[44,0,false],[-100,0,false]]){
 m=make();const e=spear(m,1);e.x=600-dx;e.y=555-dy;e.state='attack';e.t=.55;m.updateEnemies(.02);assert.equal(m.p.hp,hit?84:100,'tip geometry '+dx+','+dy);
}
// Sidestep, jump, invincibility and Garran's forward guard all counter the thrust.
for(const hero of ['kael','lyra','garran','selene']){
 m=make(hero);let e=spear(m);e.state='attack';e.t=.55;m.jump();m.p.t=.35;m.updateEnemies(.02);assert.equal(m.p.hp,100,'jump failed');
 m=make(hero);e=spear(m);e.state='attack';e.t=.55;m.p.inv=.5;m.updateEnemies(.02);assert.equal(m.p.hp,100,'invincibility failed');
}
for(const rear of [false,true]){m=make('garran');const e=spear(m,1);e.state='attack';e.t=.55;m.p.face=rear?1:-1;m.dodge();m.p.t=.1;m.updateEnemies(.02);assert.equal(m.p.hp,rear?84:100,'directional shield');}
// He approaches from afar, backs off when crowded, and doesn't retreat during windup.
m=make();let e=spear(m,-1,450);const far=e.x;enemies(m,.5);assert(e.x<far-30);m=make();e=spear(m,-1,90);const close=e.x;enemies(m,.5);assert(e.x>close+30);m=make();e=spear(m,-1,200);m.updateEnemies(.01);const windupX=e.x;m.p.x=e.x-70;enemies(m,.4);assert.equal(e.x,windupX);assert.equal(e.face,-1);m.p.x=e.x+80;enemies(m,.3);assert.equal(e.face,-1);assert.equal(m.p.hp,100,'turned and poked behind');
// Recovery can be punished by ordinary attacks, grabs and throws from either side.
for(const rear of [false,true]){m=make();e=spear(m,rear?1:-1,100);e.state='attack';e.t=.9;m.p.face=e.x>=m.p.x?1:-1;m.attack();for(let i=0;i<35;i++)m.updatePlayer(.01,new Set());assert(e.hp<110);assert.equal(e.state,'hurt');m=make();e=spear(m,rear?1:-1,32);assert(m.tryGrab());assert.equal(e.state,'grabbed');m.throwGrab(new Set(['ArrowRight']));for(let i=0;i<80;i++)m.updatePlayer(.01,new Set());assert.equal(e.state,'thrown');}
// Co-op target/facing stays locked once committed; cannot hit the player behind.
m=make(['kael','lyra']);m.players[1].x=100;m.players[1].y=555;e=spear(m);m.updateEnemies(.01);assert.equal(e.targetPlayer,0);m.players[1].x=e.x+20;enemies(m,.6);assert.equal(e.targetPlayer,0);assert.equal(e.face,-1);assert.equal(m.players[0].hp,84);assert.equal(m.players[1].hp,100);
// Name/score/asset states and campaign isolation.
m=make();e=spear(m);e.hp=50;assert.equal(c.hud(m)[0].name,'CARION SPEARMAN');assert(m.recordEnemyDefeat(e,0));assert.equal(m.p.score,225);assert(!m.recordEnemyDefeat(e,0));
for(const state of ['idle','walk','entering','attack','hurt','grabbed','thrown','down','dead','pitfall'])for(let t=0;t<1.5;t+=.05){const key=c.frame({kind:'spearman',state,t,walkDistance:t*100,lift:t*30});assert(fs.existsSync('dist/assets/characters/'+key+'.png'),key);}
assert.equal(new c.C('kael').enemies.length,0);assert(!new c.F('kael').enemies.some(e=>e.kind==='spearman'));
console.log('PASS spearman offscreen entry, all heroes both-direction ranged poke, extension timing/one hit/recovery, tip/depth/rear/close geometry, jump/invincibility/shield counters, approach/retreat/facing lock, stagger/grab/throw/co-op, HUD/score/frames, campaign isolation');
