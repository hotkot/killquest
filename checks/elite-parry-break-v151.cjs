const fs=require('fs'),vm=require('vm'),assert=require('assert');const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.C=Combat;",c);
for(const hero of ['kael','lyra','garran','selene'])for(const variant of ['crimson-lion','azure-griffin','ochre-stag'])for(const face of [-1,1])for(const time of [.4,1.2]){
 const m=new c.C(hero);m.containers=[];m.pitEnabled=false;const e={id:1,kind:'commander',variant,x:600,y:555,face,hp:400,maxHp:400,state:'parry',t:time,cool:0,commanderStep:0,comboRemaining:0,parryCooldown:0};m.enemies=[e];Object.assign(m.p,{x:600-face*100,y:555,face});
 if(hero==='garran')m.knightImpact(25,160);else if(hero==='lyra')m.knifeImpact({damage:25,range:160});else if(hero==='selene')m.witchHit(e,25,face);else{m.attack();m.updatePlayer(.25,new Set());}
 assert(e.hp<400,hero+' rear damage');assert.equal(e.state,'idle');assert.equal(e.t,0);assert.equal(e.cool,.25);assert.equal(e.parryCooldown,5);assert.equal(e.x,600,'stagger immunity lost');assert.equal(e.comboRemaining,0);
 // Once guard is fully set, frontal hits still trigger the counter.
 Object.assign(e,{state:'parry',t:1.2});assert(m.guardBlocks(e,e.x+face*100));assert.equal(e.state,'counter');
 // A frontal hit during setup does not break his stance.
 Object.assign(e,{state:'parry',t:.4});assert(!m.guardBlocks(e,e.x+face*100));assert.equal(e.state,'parry');
 // No contact means no stance cancellation.
 Object.assign(m.p,{x:600-face*400,state:'idle'});Object.assign(e,{state:'parry',t:1.2});if(hero==='garran')m.knightImpact(25,160);else m.knifeImpact({damage:25,range:160});assert.equal(e.state,'parry');
}
console.log('PASS rear hits immediately drop setup/active parry across four heroes, all palettes and facings; damage/stagger immunity retained, standard parry cooldown applied, frontal counter/setup and misses unchanged.');
