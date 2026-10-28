const fs=require('fs'),vm=require('vm'),assert=require('assert');const src=fs.readFileSync('dist/game.js','utf8'),sounds=[];
const c={document:{getElementById(){}},window:{},Math,Number,Set,Map,console,audioMixer:{play:(n)=>sounds.push(n)}};vm.createContext(c);
vm.runInContext(src.split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};mode='play';finish=()=>{};globalThis.Test=TestCombat;globalThis.Boss=BossCombat;globalThis.frame=heroFrame;globalThis.height=jumpHeight;globalThis.bind=m=>scene.model=m;globalThis.clips=WITCH_CLIPS;",c);
function make(chars='selene'){const m=new c.Test(chars);m.containers=[];m.allies=[];m.allySquad=null;m.enemies=[];m.squad=null;m.p.x=400;m.p.y=555;c.bind(m);return m;}
function foe(m,x,y=555,hp=500,kind='dagger'){const e={id:m.enemies.length+1,kind,x,y,hp,maxHp:hp,face:-1,state:'idle',t:0,cool:999,training:true,walkDistance:0,role:'pressure',side:1,lane:1,ai:'orbit',decision:99,retreat:0,lastAttack:-999};m.enemies.push(e);return e;}
function step(m,d,dt=.01){for(let t=0;t<d-1e-7;t+=dt)m.update(Math.min(dt,d-t),new Set());}
for(const face of [-1,1]){
 let m=make();m.p.face=face;const e=foe(m,400+face*330),back=foe(m,400-face*250),lane=foe(m,400+face*260,640);
 let count=0;const fire=m.fireWitchFlame;m.fireWitchFlame=function(...a){count++;return fire.apply(this,a);};m.attack();
 for(let i=0;i<145;i++){if(m.p.state==='attack'&&m.p.step<2)m.attack();m.update(.01,new Set());}step(m,1);
 assert.equal(count,3,'three projectile releases');assert.equal(e.hp,415,'22/27/36 chain');assert.equal(back.hp,500);assert.equal(lane.hp,500);assert.equal(m.p.state,'idle');assert.equal(m.p.rage,9);assert.equal(m.witchFlames.length,0);
 m=make();m.p.face=face;const frontHeavy=foe(m,400+face*120),rearHeavy=foe(m,400-face*120),offLane=foe(m,400+face*100,640);m.attack(true);step(m,.34);assert.equal(frontHeavy.hp,500,'heavy has a windup');step(m,.02);assert.equal(frontHeavy.state,'thrown');assert.equal(frontHeavy.face,face);assert.equal(frontHeavy.hp,465);assert.equal(rearHeavy.hp,500,'ground push never hits behind');assert.equal(offLane.hp,500,'ground push respects lane');const effect=m.witchEffects.find(a=>a.kind==='push');assert(effect&&effect.face===face&&(effect.x-m.p.x)*face>0,'forward flame rendering');step(m,1);assert.equal(frontHeavy.hp,440,'one direct hit plus landing damage');assert.equal(rearHeavy.hp,500);
 m=make();m.attack();step(m,.12);m.attack(true);assert(m.p.witchHeavy);step(m,.36);assert.equal(m.witchFlames.length,0,'heavy overrides light without shooting');
 m=make();m.p.face=face;const air=foe(m,400+face*150);m.jump();step(m,.25);m.attack();step(m,.22);assert(m.witchFlames.some(a=>a.vz<0&&a.vx*face>0));step(m,.8);assert(air.hp<500,'diagonal aerial projectile hits grounded enemy');
 m=make();m.p.face=face;const l=foe(m,270),r=foe(m,530);m.jump();step(m,.25);m.attack(true);step(m,.43);assert.equal(l.state,'thrown');assert.equal(r.state,'thrown');assert(c.height(m.p)<1,'slam contact is grounded');step(m,1);assert.equal(l.hp,425);assert.equal(r.hp,425);
 m=make();m.p.face=face;m.dodge();step(m,.21);assert.equal(m.p.x,400-face*190);assert.equal(m.p.face,face);assert(m.p.inv>0);step(m,.4);assert.equal(m.p.state,'idle');assert.equal(m.p.inv,0);
 m=make();m.p.face=face;const front=foe(m,400+face*300,555,80),behind=foe(m,400-face*100,555,80),out=foe(m,400+face*150,680,80),tough=foe(m,400+face*200,555,1000);
 m.p.rage=99;assert.equal(m.rageAttack(),false);m.p.rage=100;assert(m.rageAttack());assert.equal(m.p.rage,0);step(m,.61);assert(front.hp<=0);assert.equal(behind.hp,80);assert.equal(out.hp,80);assert.equal(tough.hp,800);assert(m.witchEffects.some(a=>a.kind==='storm'));step(m,2.2);assert.equal(tough.hp,775,'one storm contact plus landing');assert.equal(m.p.rage,0,'rage does not recharge itself');assert.equal(m.p.score,100);assert.equal(m.p.state,'idle');
}
// Swept projectiles cannot tunnel at a low frame rate or pass through a prop.
for(const dt of [.01,.20]){let m=make();const e=foe(m,650);m.attack();step(m,.8,dt);assert.equal(e.hp,478);assert.equal(m.p.rage,3);}
let m=make();const e=foe(m,700);const box=m.spawnContainer(550,555,'crate');m.attack();step(m,.9);assert.equal(e.hp,500);assert.equal(box.hp,28);
m=make();m.spawnContainer(300,555,'crate');m.dodge();step(m,.3);assert(m.p.x>=360,'backward teleport respects solid prop');
m=make();m.p.x=60;m.dodge();step(m,.3);assert.equal(m.p.x,60,'left screen boundary');
m=make();m.p.x=1200;m.p.face=-1;m.dodge();step(m,.3);assert.equal(m.p.x,1220,'right screen boundary');
// Pickup uses the shared kneeling interaction and never emits a projectile.
m=make();m.p.hp=50;m.foods=[{id:1,x:400,y:555,type:'food',kind:0,heal:25}];m.attack();assert.equal(m.p.state,'pickup');step(m,.9);assert.equal(m.p.hp,75);assert.equal(m.witchFlames.length,0);
// Fourth-player ownership, death/lives and reset lifecycle.
m=make(['kael','lyra','garran','selene']);m.players[3].x=500;m.players[3].y=555;const target=foe(m,800,555,20);m.command(3,'light');step(m,1);assert.equal(m.players[3].score,100);assert.equal(m.players[0].score,0);m.players[3].hp=0;step(m,.02);assert.equal(m.players[3].lives,2);m.reset(['kael','lyra','garran','selene']);assert.equal(m.players.length,4);assert.equal(m.witchEffects.length,0);assert.equal(m.witchFlames.length,0);
// All frame/state mappings ship real textures, with distinct ground casting clips.
m=make();for(const [clip,n] of Object.entries(c.clips))for(let i=0;i<n;i++)assert(fs.existsSync('dist/assets/characters/witch-'+clip+'-'+String(i).padStart(2,'0')+'.png'));
for(const state of ['idle','walk','jump','attack','dodge','rage','hurt','launched','down','dead','respawn','pickup','grab','throw','victory'])for(const t of [0,.2,.5,1,3]){Object.assign(m.p,{state,t,step:2,airStep:1,airT:t,airAttack:state==='jump',airHeavy:false,airLift:80});assert(fs.existsSync('dist/assets/characters/'+c.frame(m.p)+'.png'));}
console.log('PASS: Selene three-cast combos, forward/diagonal projectiles, heavy overrides, forward ground throw/landing and bilateral aerial throw, grounded aerial slam, backward safe teleport/invincibility, front-only lethal rage, once-only damage, frame-rate-independent collisions, prop blocking, pickups, P4 score/lives/reset and all frame paths.');

// Ground push and slam intentionally differ for props as well as enemies.
for(const face of [-1,1]){m=make();m.p.face=face;const front=m.spawnContainer(400+face*120,555,'crate'),rear=m.spawnContainer(400-face*120,555,'crate');m.attack(true);step(m,.4);assert.equal(front.hp,15);assert.equal(rear.hp,50);step(m,.5);assert.equal(front.hp,15,'one prop hit');}
// Twelve distance-driven walking keys retain the original 168px stride length.
m=make();m.p.state='walk';const walkKeys=new Set;for(let i=0;i<12;i++){m.p.walkDistance=i*14;walkKeys.add(c.frame(m.p));}assert.equal(walkKeys.size,12);m.p.walkDistance=168;assert.equal(c.frame(m.p),'witch-walk-00');
m.p.state='attack';m.p.witchHeavy=true;const pushKeys=new Set;for(let i=0;i<94;i++){m.p.t=i*.01;pushKeys.add(c.frame(m.p));}assert.equal(pushKeys.size,8);m.p.t=.35;assert.equal(c.frame(m.p),'witch-push-04','contact pose matches impact');
console.log('PASS: forward-only prop damage in both facings, twelve walk keys/unchanged stride, eight heavy poses and exact contact-frame alignment.');
