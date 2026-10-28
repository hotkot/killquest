const fs=require('fs'),vm=require('vm'),assert=require('assert');
const c={Set,Map,Math,Number,document:{getElementById(){}},window:{}};vm.createContext(c);
vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.C=Combat;globalThis.B=BossCombat;globalThis.F=ForestCombat;globalThis.frame=heroFrame;globalThis.lift=rageHeight;",c);
function make(char='garran'){const m=new c.C(char);m.containers=[];m.enemies=[];m.pitEnabled=false;m.waveDelay=999;m.worldWidth=5000;m.p.x=2200;m.p.y=555;m.p.rage=100;return m;}
const enemy=(id,x,y=555,hp=500,kind='sword')=>({id,x,y,hp,maxHp:hp,kind,state:'idle',face:1,t:0,cool:99,training:true,walkDistance:0});
function step(m,time,dt=.01){for(let t=0;t<time-1e-8;t+=dt)m.update(Math.min(dt,time-t),new Set());}
for(const face of [-1,1])for(const dt of [.01,.20]){
 const m=make();m.p.face=face;const start=m.p.x;
 m.enemies=[enemy(1,start+face*70),enemy(2,start+face*640),enemy(3,start+face*1260),enemy(4,start-face*100),enemy(5,start+face*400,650),enemy(6,start+face*1600)];
 assert(m.rageAttack());assert.equal(m.p.rage,0);assert(!m.rageAttack());
 const charge=m.p.rageCharge;m.p.face=-face;m.attack();m.attack(true);m.jump();m.dodge();assert.equal(m.p.state,'rage');
 step(m,1.2,dt);assert.equal(m.p.face,face);assert(Math.abs(m.p.x-start-face*1280)<.001,'one-screen travel');assert.equal(c.lift(m.p),0,'charge stays grounded');
 for(const e of m.enemies.slice(0,3)){assert([300,265].includes(e.hp),'one 200-point hit plus at most one 35-point landing');assert.equal(e.throwOwner,0);assert.equal(e.face,face);}
 for(const e of m.enemies.slice(3))assert.equal(e.hp,500,'behind / other lane / beyond range untouched');
 assert.equal(charge.hits.size,3);step(m,1.5,dt);assert.equal(m.p.state,'idle');assert.equal(m.p.rageCharge,null);
 for(const e of m.enemies.slice(0,3))assert.equal(e.hp,265,'one charge and one landing, without duplicate damage');
}
for(const face of [-1,1]){
 const m=make();m.p.face=face;const x=m.p.x;
 const box=m.spawnContainer(x+face*500,555,'crate','life-potion');
 const arrow={x:x+face*350,y:555,vx:0,vy:0,life:10},behind={x:x-face*200,y:555,vx:0,vy:0,life:10},off={x:x+face*350,y:650,vx:0,vy:0,life:10};m.arrows=[arrow,behind,off];
 m.enemies=[enemy(1,x+face*100,555,65),enemy(2,x+face*600,555,125,'bruiser')];m.rageAttack();step(m,2.5);assert(box.broken);assert.equal(m.foods.length,1);assert.equal(m.foods[0].type,'life-potion');assert(!m.arrows.includes(arrow));assert(m.arrows.includes(behind)&&m.arrows.includes(off));assert.equal(m.kills,2);assert.equal(m.p.scoreKills,2);assert.equal(m.p.score,450);
}
// Permanent obstacles and pits stop the body, with no damage through the wall.
for(const face of [-1,1]){
 const m=make();m.p.face=face;const wall=m.spawnContainer(m.p.x+face*500,555,'crate');wall.indestructible=true;const beyond=enemy(1,m.p.x+face*800);m.enemies=[beyond];m.rageAttack();step(m,2,.2);assert(Math.abs(m.p.x-(2200+face*440))<.001);assert.equal(wall.hp,50);assert.equal(beyond.hp,500);
 const pit=make();pit.pitEnabled=true;vm.runInContext('globalThis.pit=PIT;',c);pit.p.x=c.pit.x-face*250;pit.p.y=c.pit.y;pit.p.face=face;pit.rageAttack();step(pit,2,.2);assert.equal(pit.p.hp,100);assert.equal(pit.p.lives,3);assert(!pit.inPit(pit.p.x,pit.p.y));
}
// Boss damage retains armor, independent owner/score, and standard arena bounds.
const b=make();const king=enemy(9,2600,555,1000,'king');b.enemies=[king];b.rageAttack();step(b,2);assert.equal(king.hp,800);assert(!['thrown','hurt','down'].includes(king.state));
const party=make();party.reset(['kael','lyra','garran']);party.worldWidth=1280;party.containers=[];party.enemies=[];party.pitEnabled=false;party.waveDelay=999;party.players.forEach((p,i)=>{p.x=200+i*30;p.y=555;p.rage=100;});party.enemies=[enemy(1,700,555,65)];party.command(2,'rage');assert.equal(party.players[0].rage,100);assert.equal(party.players[1].rage,100);step(party,3);assert.equal(party.players[2].scoreKills,1);assert.equal(party.players[0].scoreKills,0);assert(party.players[2].x<=1220);assert.equal(party.players[0].x,200);
const forest=new c.F(['kael','garran']);forest.phase='explore';forest.encounterIndex=99;forest.enemies=[];forest.containers=[];forest.players.forEach((p,i)=>{p.x=3000+i*200;p.y=555;p.state='idle';p.rage=100;});forest.command(1,'rage');step(forest,2);assert(forest.players[1].x-forest.players[0].x<=850.001);assert(forest.players[1].hp>0);
for(const t of [0,.15,.30,.50,.75,1.0,1.3,1.5]){const key=c.frame({character:'garran',state:'rage',t});assert(key.startsWith('knight-bash-'));assert(fs.existsSync('dist/assets/characters/'+key+'.png'));}
console.log('PASS: bilateral one-screen sweeps, frame-rate-independent contacts, front-only lane/range, once-only damage/launch/fall/score, destructibles/potion, arrow clearing, barriers/pits, boss armor, co-op ownership/leash, grounded normalized charge frames and recovery.');
const protectedKnight=make();const attacker=enemy(30,protectedKnight.p.x-70);Object.assign(attacker,{training:false,state:'attack',t:.47,face:1,ai:'commit'});protectedKnight.enemies=[attacker];protectedKnight.rageAttack();step(protectedKnight,.02);assert.equal(protectedKnight.p.hp,100,'full cast protects against attacks from behind');
