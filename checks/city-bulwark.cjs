const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);
vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.T=TestCombat;globalThis.C=CityCombat;globalThis.F=ForestCombat;globalThis.frame=banditFrame;globalThis.stats=BULWARK;globalThis.bind=m=>scene.model=m;",c);
function make(hero='kael',rear=false){const m=new c.T(hero);c.bind(m);m.containers=[];m.p.x=600;m.p.y=555;m.p.face=1;m.enemies=[{kind:'bulwark',id:9010,x:700,y:555,face:rear?1:-1,hp:180,maxHp:180,state:'guard',t:0,cool:99,walkDistance:0,training:true,turnWait:0}];return m;}
function playerSteps(m,t){for(let i=0;i<Math.ceil(t/.01);i++)m.updatePlayer(.01,new Set());}
function enemies(m,t){for(let i=0;i<Math.round(t/.01);i++)m.updateEnemies(.01);}
let m=new c.T('kael');c.bind(m);m.p.inv=999;assert.equal(m.enemies.filter(e=>e.kind==='guard').length,3);const spawned=m.enemies.find(e=>e.kind==='bulwark');assert(spawned);assert(spawned.x>1280&&spawned.state==='entering');for(let i=0;i<500;i++)m.update(.01,new Set());assert(spawned.x>=42&&spawned.x<=1238&&spawned.state!=='entering');
// Full actual ground light/heavy and jump attack paths for every hero, from both sides.
for(const hero of ['kael','lyra','garran','selene'])for(const rear of [false,true])for(const attack of ['light','heavy','air-light','air-heavy']){
 m=make(hero,rear);const e=m.enemies[0];if(attack.startsWith('air')){m.jump();m.p.t=.15;}
 m.attack(attack.endsWith('heavy'));playerSteps(m,1.5);
 if(hero==='lyra'&&attack.endsWith('heavy')){for(let i=0;i<150;i++)m.updatePlayerArrows(.01);}if(hero==='selene'&&attack.endsWith('light')){for(let i=0;i<150;i++)m.updateWitchProjectiles(.01);}
 assert.equal(e.hp<180,rear,hero+' '+attack+' rear='+rear+' hp='+e.hp);if(!rear)assert(!['hurt','thrown','down'].includes(e.state),'front caused stagger');
}
// Facing is held for .70 seconds even in co-op; changing attack targets cannot snap it.
m=make('kael',true);let e=m.enemies[0];enemies(m,.69);assert.equal(e.face,1);assert(m.guardBlocks(e,800,true));assert(!m.guardBlocks(e,600,true));enemies(m,.02);assert.equal(e.face,-1);assert(m.guardBlocks(e,600,true));
m=make('kael',true);e=m.enemies[0];enemies(m,.4);m.p.x=800;enemies(m,.1);assert.equal(e.turnWait,0);m.p.x=600;enemies(m,.4);assert.equal(e.face,1);enemies(m,.31);assert.equal(e.face,-1);
m=make('kael',true);e=m.enemies[0];e.state='attack';e.t=.05;enemies(m,.8);assert.equal(e.face,1,'attack turned toward rear');assert.equal(m.p.hp,100,'thrust hit behind shield');while(e.state==='attack')m.updateEnemies(.01);assert.equal(e.face,1);enemies(m,.69);assert.equal(e.face,1);enemies(m,.02);assert.equal(e.face,-1);
// Frontal attacks remain guarded through attack wind-up, thrust and recovery.
for(const state of ['idle','walk','guard','attack','hurt']){m=make();e=m.enemies[0];e.state=state;for(const t of [0,.3,.57,1]){e.t=t;assert(m.guardBlocks(e,600,true));assert(!m.guardBlocks(e,800,true));}}
// Projectile direction is independent of the owner's current location.
m=make('lyra');e=m.enemies[0];m.p.x=800;m.arrowHit(e,{owner:0,damage:45,face:1});assert.equal(e.hp,180);m.arrowHit(e,{owner:0,damage:45,face:-1});assert.equal(e.hp,135);
// All rage specials bypass shields; grabs work from either side. Ordinary body impacts still respect facing.
for(const rear of [false,true])for(const hero of ['kael','lyra','garran','selene']){
 m=make(hero,rear);e=m.enemies[0];m.p.rage=100;m.rageAttack();for(let i=0;i<400;i++){m.updatePlayer(.01,new Set());m.updatePlayerArrows(.01);m.updateWitchProjectiles(.01);}
 assert.equal(e.hp<180,true,hero+' rage rear='+rear+' hp='+e.hp);
}
for(const rear of [false,true]){m=make('kael',rear);e=m.enemies[0];m.p.x=670;assert.equal(m.tryGrab(),true,'grab rear='+rear);{assert.equal(e.state,'grabbed');m.throwGrab(new Set(['ArrowRight']));playerSteps(m,.8);for(let i=0;i<150;i++){e.t+=.01;if(e.state==='thrown')m.updateThrown(e);}assert(e.hp<180);}}
for(const rear of [false,true]){m=make('kael',rear);e=m.enemies[0];m.damageLandingEnemies({x:700,y:555,throwFrom:600,face:1,throwOwner:0,fallDamage:55});assert.equal(e.hp,rear?125:180);}
// Actual thrust hits once, has a windup, and respects jumping, invincibility and player shield.
m=make();e=m.enemies[0];e.training=false;e.cool=0;m.updateEnemies(.01);assert.equal(e.state,'attack');enemies(m,.5);assert.equal(m.p.hp,100);enemies(m,.1);assert.equal(m.p.hp,82);enemies(m,.3);assert.equal(m.p.hp,82);assert(m.guardBlocks(e,600));
m=make('garran');e=m.enemies[0];e.state='attack';e.t=.55;e.hit=false;m.p.face=1;m.p.state='dodge';m.p.t=.1;m.updateEnemies(.02);assert.equal(m.p.hp,100);
// Walking and ordinary charges still collide; dodging through him is allowed.
m=make();e=m.enemies[0];m.p.x=800;m.resolveContainers(m.p,600,555);assert(m.p.x<=e.x-30);m.p.x=800;m.p.y=600;m.resolveContainers(m.p,600,600);assert.equal(m.p.x,800,'side lane should allow flanking');
// Co-op target reassignment has the same delay and a locked thrust target.
m=new c.T(['kael','lyra']);c.bind(m);m.containers=[];e={kind:'bulwark',id:1,x:700,y:555,face:1,hp:180,maxHp:180,state:'guard',t:0,cool:99,walkDistance:0,training:true};m.enemies=[e];m.players[0].x=1000;m.players[0].y=555;m.players[1].x=650;m.players[1].y=555;enemies(m,.4);assert.equal(e.targetPlayer,1);assert.equal(e.face,1);enemies(m,.31);assert.equal(e.face,-1);
// HUD/score/frame assets and campaign isolation.
m=make();e=m.enemies[0];assert(m.recordEnemyDefeat(e,0));assert.equal(m.p.score,350);assert(!m.recordEnemyDefeat(e,0));
for(const state of ['idle','walk','entering','attack','guard','hurt','grabbed','thrown','down','dead','pitfall'])for(let t=0;t<1.5;t+=.05){const key=c.frame({kind:'bulwark',state,t,walkDistance:t*120,lift:t*20,turnWait:.3});assert(fs.existsSync('dist/assets/characters/'+key+'.png'),key);}
assert.equal(new c.C('kael').enemies.length,0);assert(!new c.F('kael').enemies.some(e=>e.kind==='bulwark'));
console.log('PASS Ironshield: offscreen test entry; all heroes ordinary ground/air attacks front block and rear damage, all rage specials bypass shields; delayed turn/reset and attack facing lock; incoming projectile side; both-side grab/throw, directional body impact; windup/thrust and player block; physical flank; co-op targeting; score, all sprite states, campaign isolation');

// Actual dodge paths for all heroes, both directions, including backstep and teleport.
for(const hero of ['kael','lyra','garran','selene'])for(const dir of [-1,1]){
 m=make(hero);e=m.enemies[0];m.p.x=e.x-dir*32;m.p.face=['garran','selene'].includes(hero)?-dir:dir;m.dodge();
 for(let i=0;i<70;i++)m.update(.01,new Set());
 assert((m.p.x-e.x)*dir>30,hero+' dodge stopped at shield direction '+dir);
 m.p.state='idle';m.p.bulwarkDodgePass=false;const ox=e.x-dir*60;m.p.x=e.x+dir*60;m.p.y=e.y;m.resolveContainers(m.p,ox,e.y);assert((m.p.x-e.x)*dir<=-29,'normal walking lost body collision');
}
// Dodge-through permission never bypasses destructible or solid scenery.
for(const hero of ['kael','lyra','garran','selene']){
 m=make(hero);m.enemies=[];m.spawnContainer(700,555,'crate');m.p.x=620;m.p.face=['garran','selene'].includes(hero)?-1:1;m.dodge();
 for(let i=0;i<70;i++)m.update(.01,new Set());assert(m.p.x<=640.01,hero+' dodge passed through crate');
}
// Frontal grabs through each hero's actual light-attack command preserve throws.
for(const hero of ['kael','lyra','garran','selene']){m=make(hero);e=m.enemies[0];m.p.x=668;m.attack(false);assert.equal(m.p.state,'grab');assert.equal(e.state,'grabbed');m.attack(false,new Set(['ArrowRight']));playerSteps(m,.8);assert.equal(e.state,'thrown');}
console.log('PASS all four heroes dodge through Ironshields both ways, remain blocked by scenery and on normal walking; all heroes frontal light-input grab into throw');

// Jump through the physical guard body using real player/world updates, both ways.
for(const hero of ['kael','lyra','garran','selene'])for(const dir of [-1,1]){
 m=make(hero);e=m.enemies[0];m.p.x=e.x-dir*32;m.p.face=dir;m.jump();
 for(let i=0;i<90;i++)m.update(.01,new Set([dir>0?'ArrowRight':'ArrowLeft']));
 assert((m.p.x-e.x)*dir>30,hero+' jump stopped at Ironshield '+dir);assert.notEqual(m.p.state,'jump');
 const ox=e.x-dir*60;m.p.x=e.x+dir*60;m.p.y=e.y;m.resolveContainers(m.p,ox,e.y);assert((m.p.x-e.x)*dir<=-29,hero+' landing did not restore ground collision');
}
// Jumping also clears breakable containers; large permanent scenery stays solid.
for(const hero of ['kael','lyra','garran','selene']){
 m=make(hero);m.enemies=[];m.spawnContainer(700,555,'crate');m.p.x=620;m.jump();
 for(let i=0;i<90;i++)m.update(.01,new Set(['ArrowRight']));assert(m.p.x>760,hero+' jump could not clear crate');
}
// Landing directly over his body separates the player out of the grounded collider.
m=make();e=m.enemies[0];m.p.x=e.x;m.p.state='jump';m.p.t=.70;m.update(.01,new Set());assert(Math.abs(m.p.x-e.x)>=29.99||Math.abs(m.p.y-e.y)>=19.99,'landing left player inside Ironshield');
console.log('PASS all four heroes jump over Ironshields both directions; landing restores collision and separates overlap; breakable containers can be cleared');
