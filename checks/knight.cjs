const fs=require('fs'),vm=require('vm'),assert=require('assert');const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);const source=fs.readFileSync('dist/game.js','utf8');vm.runInContext(source.split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.C=Combat;globalThis.B=BossCombat;globalThis.frame=heroFrame;globalThis.height=jumpHeight;globalThis.bind=m=>scene.model=m;",c);
const enemy=(id,x,y=555,hp=200)=>({id,kind:'sword',x,y,hp,maxHp:hp,state:'idle',t:0,cool:99,training:true,walkDistance:0});
function make(){const m=new c.C('garran');c.bind(m);m.pitEnabled=false;m.containers=[];m.enemies=[];m.waveDelay=999;m.p.x=600;m.p.y=555;return m;}
function step(m,t,input=new Set()){for(let i=0;i<Math.ceil(t/.01);i++)m.update(.01,input);}
let m=make(),e=enemy(1,700,555,1000);m.enemies=[e];m.attack();m.attack();let queued=false;const clips=new Set;for(let i=0;i<250;i++){clips.add(c.frame(m.p).split('-').slice(0,-1).join('-'));if(m.p.step===1&&!queued){m.attack();queued=true;}m.update(.01,new Set());}assert.equal(e.hp,912);assert.equal(m.p.state,'idle');for(const clip of ['down','cross','thrust'])assert(clips.has('knight-'+clip));
for(const face of [-1,1]){m=make();m.p.face=face;e=enemy(1,600+face*100);const back=enemy(2,600-face*100);m.enemies=[e,back];m.attack(true);m.attack();assert(m.p.bash&&!m.p.queue);step(m,1.5);assert.equal(e.hp,140);assert.equal(back.hp,200);assert(Math.abs(m.p.x-600-face*240)<1);assert.equal(m.p.state,'idle');}
m=make();const box=m.spawnContainer(720,555,'crate');m.attack(true);step(m,1);assert.equal(box.hp,15,'one contact per prop per bash');assert(m.p.x<=660,'charge respects container collision');
m=make();m.attack();m.attack(true);assert(m.p.bash,'heavy replaces light instead of advancing its combo');
for(const face of [-1,1]){m=make();m.p.face=face;m.enemies=[enemy(1,480),enemy(2,720),enemy(3,860)];m.jump();step(m,.25);const h=c.height(m.p);m.attack(true);assert(m.p.airHeavy);assert(Math.abs(c.height(m.p)-h)<1e-6);m.attack();assert(!m.p.airQueue);step(m,1.5);assert.equal(m.enemies[0].hp,133);assert.equal(m.enemies[1].hp,133);assert.equal(m.enemies[2].hp,175,'outside slam radius, but caught by the thrown enemy landing');assert.equal(c.height(m.p),0);}
m=make();m.enemies=[enemy(1,700,555,1000)];m.jump();step(m,.22);m.attack();m.attack();queued=false;for(let i=0;i<190;i++){if(m.p.airStep===1&&!queued){m.attack();queued=true;}m.update(.01,new Set());}assert.equal(m.enemies[0].hp,905);assert.equal(m.p.state,'idle');
// A backstep retreats without turning and protects its front during the active dodge.
m=make();m.dodge();const x=m.p.x;step(m,.2,new Set(['ArrowRight']));assert(m.p.x<x-40);assert.equal(m.p.face,1);assert.equal(m.p.state,'dodge');assert(m.shieldBlocks(m.p,m.p.x+50));assert(!m.shieldBlocks(m.p,m.p.x-50));const t=m.p.t;m.dodge();assert.equal(m.p.t,t);m.attack();m.jump();assert.equal(m.p.state,'dodge');step(m,.26);assert(!m.shieldBlocks(m.p,m.p.x+50),'lowering recovery is vulnerable');step(m,.2);assert.equal(m.p.state,'idle');
for(const face of [-1,1]){m=make();m.p.face=face;const start=m.p.x;m.dodge();step(m,.59,new Set(['ArrowLeft']));assert(Math.abs(m.p.x-(start-face*135))<1);assert.equal(m.p.face,face);}
for(const side of [1,-1]){m=make();m.dodge();e=enemy(1,600+side*70);Object.assign(e,{training:false,state:'attack',t:.47,face:-side,ai:'commit'});m.enemies=[e];m.updateEnemies(.02);assert.equal(m.p.hp,side===1?100:85);}
m=make();m.dodge();m.p.t=.48;e=enemy(1,670);Object.assign(e,{training:false,state:'attack',t:.47,face:-1,ai:'commit'});m.enemies=[e];m.updateEnemies(.02);assert.equal(m.p.hp,85);
for(const side of [1,-1]){m=make();m.dodge();m.arrows=[{x:600+side*30,y:555,vx:-side*500,vy:0,life:1}];m.updateArrows(.04);assert.equal(m.p.hp,side===1?100:91);assert.equal(m.arrows.length,0);}
m=make();m.p.rage=100;m.enemies=[enemy(1,480,555,65),enemy(2,720,555,65)];m.rageAttack();step(m,3);assert.equal(m.enemies[0].hp,65,'directional rage leaves enemies behind untouched');assert(m.enemies[1].hp<=0);assert.equal(m.kills,1);assert.equal(m.p.scoreKills,1);
m=make();m.p.hp=50;const food=m.spawnContainer(600,555,'barrel');m.damageContainers(99,c=>c===food);m.attack();assert.equal(m.p.state,'pickup');step(m,.9);assert.equal(m.p.hp,75);assert.equal(m.foods.length,0);
const b=new c.B('garran');c.bind(b);b.bossDialogue=null;b.reinforcementTimer=Infinity;b.king.x=700;b.p.x=600;b.p.y=555;b.attack(true);step(b,.5);assert(b.king.hp<1600);assert(!['thrown','down','hurt'].includes(b.king.state),'boss retains armor');
const party=new c.C(['kael','lyra','garran']);assert.equal(party.players.length,3);assert.equal(party.players[2].character,'garran');party.withPlayer(2,()=>party.attack(true));assert(party.players[2].bash);assert.equal(party.players[0].state,'idle');
console.log('PASS: three ground/air strikes, shield charge in both directions and once-only prop collision, heavy override, bilateral aerial launch/fall damage, continuous jump height, directional backstep guard/recovery/no refresh, melee/arrows, rage kills/credit, pickup, boss armor and independent third fighter.');

// Shield charge protects its front throughout wind-up and travel, without back immunity.
for(const side of [1,-1]){m=make();m.attack(true);e=enemy(1,600+side*70);Object.assign(e,{training:false,state:'attack',t:.47,face:-side,ai:'commit'});m.enemies=[e];m.updateEnemies(.02);assert.equal(m.p.hp,side===1?100:85);}
for(const side of [1,-1]){m=make();m.attack(true);m.arrows=[{x:600+side*30,y:555,vx:-side*500,vy:0,life:1}];m.updateArrows(.04);assert.equal(m.p.hp,side===1?100:91);}
m=make();m.attack(true);m.p.t=.64;assert(m.shieldBlocks(m.p,700));m.p.t=.70;assert(!m.shieldBlocks(m.p,700),'bash recovery exposes the front');
console.log('PASS: deterministic backward displacement, unchanged forward facing, guard recovery, and shield-bash frontal melee/arrow immunity with rear vulnerability.');

for(let i=0;i<8;i++){const key=vm.runInContext(`knightFrame({state:'walk',walkDistance:${[0,26,48,66,88,114,136,154][i]},character:'garran'})`,c);assert.equal(key,'knight-walk-'+String(i).padStart(2,'0'));}console.log('PASS: all eight deliberate walking poses are reachable, including both leg crossings.');

// Each drawn ground frame is reachable and the three hits land on their drawn contact frames.
for(const face of [-1,1]){
 m=make();m.p.face=face;m.enemies=[enemy(1,600+face*110,555,1000)];m.attack();m.attack();let queuedThird=false;const seen=new Set(),contacts=[];let hp=1000;
 for(let i=0;i<230;i++){if(m.p.step===1&&!queuedThird){m.attack();queuedThird=true;}if(m.p.state==='attack')seen.add(c.frame(m.p));m.update(.005,new Set());if(m.enemies[0].hp!==hp){hp=m.enemies[0].hp;contacts.push([m.p.step,c.frame(m.p)]);}}
 // Finish the final recovery after collecting the complete chain.
 for(let i=0;i<230;i++){if(m.p.state==='attack')seen.add(c.frame(m.p));m.update(.005,new Set());if(m.enemies[0].hp!==hp){hp=m.enemies[0].hp;contacts.push([m.p.step,c.frame(m.p)]);}}
 for(const [clip,count] of [['down',8],['cross',9],['thrust',12]])for(let i=0;i<count;i++)assert(seen.has('knight-'+clip+'-'+String(i).padStart(2,'0')),'skipped '+clip+' '+i);
 assert.deepEqual(contacts,[[0,'knight-down-04'],[1,'knight-cross-04'],[2,'knight-thrust-06']]);assert.equal(hp,912);assert.equal(m.p.state,'idle');
}
console.log('PASS: preserved first cut / horizontal body-rotation cut / unchanged stab, all 29 frames, three correctly timed contacts, both directions, and recovery.');

function comboDuration(character){const m=new c.C(character);c.bind(m);m.enemies=[];m.containers=[];m.pitEnabled=false;m.waveDelay=999;m.attack();const queued=new Set();let time=0;while(time<4){if(m.p.state==='attack'&&m.p.step<2&&!queued.has(m.p.step)){m.attack();queued.add(m.p.step);}m.update(.001,new Set());time+=.001;if(m.p.state==='idle')return time;}throw Error('combo did not finish');}
const durations=['kael','lyra','garran'].map(comboDuration);assert(Math.abs(durations[2]-durations[0])<.08,durations);assert(Math.abs(durations[2]-durations[1])<.08,durations);console.log('PASS: measured full combo durations Kael/Lyra/Garran:',durations.map(n=>n.toFixed(3)).join(' / '),'seconds.');

for(const face of [-1,1]){m=make();m.p.face=face;const start=m.p.x;m.attack();step(m,.3);assert.equal(m.p.state,'attack');assert(Math.abs(m.p.x-start-face*18)<.01,'first cut steps forward');m=make();m.p.face=face;const wall=m.spawnContainer(600+face*65,555,'crate');m.attack();step(m,.3);assert((m.p.x-600)*face<=5.01,'first cut respects prop collision');}
const firstTiming=vm.runInContext('KNIGHT_STRIKES[0]',c),kaelChain=vm.runInContext('COMBO_LINKS[0].exitAt',c);assert(Math.abs(firstTiming.linkAt-kaelChain)<=.011);assert(firstTiming.impact<.24);console.log('PASS: earlier first contact, Kael-like first chain timing, 18px step in both directions and container blocking.');
