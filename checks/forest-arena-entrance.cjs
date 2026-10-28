const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('dist/game.js','utf8');let sounds=[],shakes=0;
const ctx={Set,Map,Math,Number,window:{},document:{getElementById:()=>null},cue:(...args)=>sounds.push(args),shake:()=>shakes++};vm.createContext(ctx);
vm.runInContext(source.split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake:()=>shake(),flash(){}}}};soundCue=(...args)=>cue(...args);globalThis.F=ForestCombat;globalThis.height=enemyHeight;globalThis.pose=kingFrame;",ctx);
for(const chars of ['kael','lyra','garran','selene',['kael','lyra','garran','selene']]){
 const m=new ctx.F(chars);m.phase='explore';m.cameraX=m.fightLeft=11000;m.encounterIndex=8;
 m.players.forEach((p,i)=>{p.x=11700-i*180;p.y=[470,650,505,625][i];p.hp=80-i*5;p.rage=40;p.state='jump';p.airAttack=true;});
 const stats=m.players.map(p=>[p.hp,p.lives,p.score,p.rage]),supplies=m.containers.map(c=>c.hp);sounds=[];shakes=0;m.startArena();
 assert.equal(m.cameraX,11000);assert.equal(m.bossDialogue,null);assert(!m.isBoss);assert.equal(m.enemies.length,0);
 let jumped=false,landed=false,high=0,walked=0,oldCamera=m.cameraX;
 for(let i=0;i<700&&!m.bossDialogue;i++){
  const x=m.players[0].x;
  for(let j=0;j<m.players.length;j++)for(const action of ['light','heavy','jump','dodge','rage'])m.command(j,action);
  m.attack();m.jump();m.dodge();m.rageAttack();m.update(.02,new Set(['ArrowLeft']));
  assert(m.cameraX>=oldCamera&&m.cameraX-oldCamera<=4.40001,'continuous camera pan');oldCamera=m.cameraX;
  assert.deepEqual(m.players.map(p=>[p.hp,p.lives,p.score,p.rage]),stats,'entrance cannot deal damage or spend rage');
  assert(m.enemies.every(e=>e.kind==='king'),'no harassment before dialogue');
  if(m.players[0].x>x)walked++;
  if(m.phase==='arena-jump'){
   if(!jumped){assert.equal(m.cameraX,11520);assert(m.players.every(p=>p.x>=11880&&p.x<12300),'whole party inside before reveal');jumped=true;}
   high=Math.max(high,ctx.height(m.king));assert(ctx.pose(m.king).startsWith('king-slam-'));assert.equal(m.bossDialogue,null);
  }
  if(m.phase==='arena-land'){landed=true;assert(jumped);assert.equal(ctx.height(m.king),0);assert.equal(m.bossDialogue,null);}
 }
 assert(walked>10&&jumped&&landed&&high>190,JSON.stringify({chars,walked,jumped,landed,high,phase:m.phase,camera:m.cameraX,players:m.players.map(p=>[p.x,p.y,p.state])}));assert.equal(m.bossDialogue,'intro');assert.equal(m.phase,'explore');assert.equal(m.king.x,12520);assert.equal(shakes,1);assert.equal(sounds.filter(s=>s[0]==='boss-roar').length,1);
 assert.deepEqual(m.containers.map(c=>c.hp),supplies,'entrance preserves supplies');assert.equal(m.particles.length,0,'landing effects expire before dialogue');
 m.dialogueAge=1;m.dismissDialogue();assert.equal(m.bossDialogue,null);m.update(.02,new Set());assert.equal(m.reinforcementSerial,0);
 m.reset(chars);assert.equal(m.arenaEntry,null);assert(!m.arenaReached);assert(!m.isBoss);
}
// A spent player stays dead; a player with a pending respawn joins normally.
const m=new ctx.F(['kael','lyra','garran']);m.phase='explore';m.cameraX=m.fightLeft=11000;m.players.forEach((p,i)=>{p.x=11700-i*100;p.y=550});Object.assign(m.players[1],{hp:0,lives:0,state:'dead'});Object.assign(m.players[2],{hp:0,lives:1,state:'dead',lastSafeX:11400,lastSafeY:555});m.startArena();for(let i=0;i<700&&!m.bossDialogue;i++)m.update(.02,new Set());assert.equal(m.bossDialogue,'intro');assert.equal(m.players[1].hp,0);assert.equal(m.players[1].lives,0);assert.equal(m.players[1].state,'dead');assert.equal(m.players[2].hp,100);assert.equal(m.players[2].lives,1);assert(m.players[2].x>=11880);
console.log('PASS: continuous arena walk-in for all heroes and four players, safe prop lanes, off-screen jump/landing before dialogue, input lock, intact health/rage/supplies, one landing cue, no early reinforcements, respawn and replay.');
