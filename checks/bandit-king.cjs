const fs=require('fs'),vm=require('vm'),assert=require('assert'),events=[];let result=null;const ctx={Set,Map,Math,Number,console,document:{getElementById(){}},window:{},audioMixer:{play(n){events.push(n)}}};vm.createContext(ctx);const src=fs.readFileSync('dist/game.js','utf8');vm.runInContext(src.split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};mode='play';finish=win=>globalThis.result=win;globalThis.BossCombat=BossCombat;globalThis.ForestCombat=ForestCombat;globalThis.frame=kingFrame;globalThis.bind=m=>scene.model=m;",ctx);
function make(chars='kael'){const m=new ctx.BossCombat(chars);ctx.bind(m);ctx.result=null;m.dialogueAge=.3;m.dismissDialogue();m.reinforcementTimer=Infinity;return m;}
function step(m,time){for(let i=0;i<Math.ceil(time/.01);i++){m.update(.01,new Set());if(m.bossDialogue){m.dialogueAge=.3;m.dismissDialogue();}}}
let m=make();assert(m.isBoss&&!m.pitEnabled);assert.equal(m.enemies.length,1);assert.equal(m.enemies[0].kind,'king');assert.equal(m.king.hp,1600);assert.equal(m.containers.length,2);assert(m.containers.some(c=>c.loot==='life-potion'));step(m,1.7);assert.equal(m.king.bossAction,null);assert.equal(m.p.hp,100,'intro cannot deal damage');assert.equal(events.filter(n=>n==='boss-roar').length,1);
for(const action of ['sweep','slam','charge']){m=make();const e=m.king;e.x=600;e.y=555;m.p.x=action==='charge'?850:735;m.p.y=555;m.beginKingMove(e,action);step(m,action==='slam'?.9:.5);assert.equal(m.p.hp,100,'readable '+action+' windup');step(m,.7);assert(m.p.hp<100,action+' connects');const hp=m.p.hp;step(m,.2);assert.equal(m.p.hp,hp,'no per-frame repeated damage');assert(fs.existsSync('dist/assets/characters/'+ctx.frame(e)+'.png'));}
// Spatial evasion, jump clearance and invincible dodge protect independently.
for(const escape of ['lane','jump','dodge']){m=make();const e=m.king;e.x=600;m.p.x=735;m.p.y=555;m.beginKingMove(e,'slam');step(m,.85);if(escape==='lane')m.p.y=650;else if(escape==='jump'){m.jump();}else m.dodge();step(m,.25);assert.equal(m.p.hp,100,escape+' avoids slam');}
m=make();m.king.x=m.p.x+25;assert.equal(m.tryGrab(),false);m.attack(true);step(m,.58);assert.equal(m.king.state,'idle');assert.equal(m.king.bossAction,'roar');assert(m.king.hp<1600);assert(!['thrown','grabbed','down'].includes(m.king.state));
m=make();m.p.rage=100;m.king.x=350;m.king.y=555;m.rageAttack();step(m,1.8);assert(m.king.hp>0,'rage cannot kill boss outright');
m=make();m.king.hp=790;step(m,.01);assert.equal(m.king.phase,2);assert.equal(m.king.bossAction,'roar');const marker=events.filter(n=>n==='boss-roar').length;step(m,1.5);assert.equal(events.filter(n=>n==='boss-roar').length,marker,'phase change fires only once');
m=make(['kael','lyra']);assert.equal(m.king.hp,2400);m.king.x=600;m.players.forEach((p,i)=>{p.x=730;p.y=550+i*10;});m.beginKingMove(m.king,'sweep');step(m,.75);assert(m.players.every(p=>p.hp<100),'boss can damage either co-op player');
m.king.hp=0;m.king.lastHitOwner=1;step(m,1.5);assert.equal(ctx.result,true);assert.equal(m.kills,1);assert.equal(m.players[1].score,2500);assert.equal(m.players[0].score,0);assert.equal(m.enemies.length,1);step(m,3);assert.equal(m.kills,1);assert.equal(m.enemies.length,1,'no reinforcements after boss death');
m.reset(['kael','lyra']);assert.equal(m.king.hp,2400);assert.equal(m.king.phase,1);assert.equal(m.kills,0);assert(m.players.every(p=>p.lives===3));m.players.forEach(p=>{p.hp=0;p.lives=0;p.state='dead';p.t=1;});step(m,.1);assert.equal(ctx.result,false);
const forest=new ctx.ForestCombat();assert.equal(forest.enemies.length,0,'Forest remains enemy-free');console.log('PASS: isolated boss arena, health scaling, intro, readable three-move attacks, no repeated hits, lane/jump/dodge escapes, anti-grab/launch, rage survival, one enrage, co-op damage/credit, death/victory/defeat, no waves, restart and unchanged empty Forest.');
// Every player damage path must preserve the King's action, timer, cooldown and position.
for(const kind of ['light','heavy','air-light','air-heavy','knife','air-knife','arrow','rain','rage','respawn']){
 m=make();const e=m.king;e.x=600;e.y=555;m.p.x=500;m.p.y=555;m.p.face=1;m.containers=[];m.beginKingMove(e,'slam');e.actionTime=.4;e.t=.4;e.cool=.2;
 const before={x:e.x,y:e.y,t:e.t,cool:e.cool,hp:e.hp};
 if(kind==='knife'||kind==='air-knife'){m.p.airStep=2;m.knifeImpact({damage:20,range:180},false,kind==='air-knife');}
 else if(kind==='arrow'||kind==='rain')m.arrowHit(e,{damage:45,owner:0,face:1,rain:kind==='rain',rainCast:new Set()});
 else if(kind==='respawn')m.landRespawn();
 else if(kind==='rage'){m.p.rage=100;m.rageAttack();m.p.t=1.7;m.updatePlayer(.01,new Set());}
 else if(kind.startsWith('air-')){m.jump();m.attack(kind==='air-heavy');m.p.airT=.6;m.updatePlayer(.01,new Set());}
 else{m.attack(kind==='heavy');m.p.t=.6;m.updatePlayer(.01,new Set());}
 if(kind!=='respawn')assert(e.hp<before.hp,kind+' deals damage');
 for(const key of ['x','y','t','cool'])assert.equal(e[key],before[key],kind+' preserves '+key);
 assert.equal(e.state,'attack',kind+' cannot stagger');assert.equal(e.bossAction,'slam');assert.equal(e.actionTime,.4);
}
// Repeated shots during recovery cannot keep postponing the next attack.
m=make();m.king.x=600;m.p.x=745;m.p.y=555;m.king.bossAction=null;m.king.cool=.2;for(let i=0;i<25;i++){m.arrowHit(m.king,{damage:1,owner:0,face:1});m.update(.01,new Set());}assert.equal(m.king.bossAction,'sweep');
m=make();m.beginKingMove(m.king,'slam');m.king.hp=790;step(m,.2);assert.equal(m.king.bossAction,'slam','threshold damage cannot cancel an attack');step(m,1.8);assert.equal(m.king.bossAction,'roar','enrage starts after attack recovery');
console.log('PASS: ten damage/respawn paths cause no stagger, knockback or cooldown reset; sustained fire cannot suppress attacks; enrage waits for attack completion.');

// Dialogue freezes combat, consumes confirmation, and holds a midway death pose before victory.
for(const chars of ['kael',['kael','lyra']]){
 const d=new ctx.BossCombat(chars);ctx.bind(d);ctx.result=null;assert.equal(d.bossDialogue,'intro');const x=d.p.x;
 d.command(0,'jump');assert.equal(d.bossDialogue,'intro','held launch input cannot skip taunt');
 d.update(.5,new Set(['ArrowRight']));assert.equal(d.p.x,x);assert.equal(d.king.actionTime,0);d.command(d.players.length-1,'jump');assert.equal(d.bossDialogue,null);assert.equal(d.p.state,'idle','confirm never jumps');
 d.king.hp=0;for(let i=0;i<80;i++)d.update(.01,new Set());assert.equal(d.bossDialogue,'death');assert.equal(d.king.deathTime,.52);assert.equal(ctx.result,null);assert(ctx.frame(d.king).endsWith('02'),'midway wounded pose');
 d.update(5,new Set());assert.equal(d.king.deathTime,.52);assert.equal(ctx.result,null);d.command(0,'light');assert.equal(d.bossDialogue,null);assert(d.lastWordsDone);for(let i=0;i<100;i++)d.update(.01,new Set());assert.equal(ctx.result,true);assert.equal(d.kills,1);d.reset(chars);assert.equal(d.bossDialogue,'intro');assert(!d.lastWordsDone);
}
assert(src.includes('You! Who do you think you are?! I will cut you down like the peasants!'));assert(src.includes('...Ugh. She... will avenge me!'));
console.log('PASS: exact intro/final dialogue, blocked solo/co-op combat, guarded consumed confirmations, held midway death pose, delayed victory, once-only dialogue and restart.');

// The torso-height sword sweep intercepts jumps and aerial attacks for all fighters.
for(const character of ['kael','lyra','garran'])for(const face of [-1,1])for(const attack of [false,true]){
 m=make(character);const e=m.king;e.x=600;e.y=555;e.face=face;m.p.x=600+face*135;m.p.y=555;
 m.jump();m.p.t=.25;if(attack){m.attack();m.p.airT=.1;}
 m.beginKingMove(e,'sweep');e.actionTime=.69;m.updateEnemies(0);
 assert.equal(m.p.hp,82,character+' airborne sweep connects');
 m.p.inv=0;m.updateEnemies(0);assert.equal(m.p.hp,82,'same beat cannot hit twice');
}
for(const escape of ['lane','behind','invincible']){
 m=make();const e=m.king;e.x=600;e.y=555;e.face=1;m.p.x=735;m.p.y=555;m.jump();m.p.t=.25;
 if(escape==='lane')m.p.y+=100;if(escape==='behind')m.p.x=500;if(escape==='invincible')m.p.inv=1;
 m.beginKingMove(e,'sweep');e.face=1;e.actionTime=.69;m.updateEnemies(0);assert.equal(m.p.hp,100,escape+' still protects from airborne sweep');
}
console.log('PASS: both-facing sword sweep intercepts all three fighters in jumps/aerial attacks, once per beat; lane, facing and invincibility remain respected.');
