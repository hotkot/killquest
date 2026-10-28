const fs=require('fs'),vm=require('vm'),assert=require('assert');const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};vm.createContext(c);vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+"\nscene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';finish=()=>{};globalThis.T=TestCombat;globalThis.F=ForestCombat;globalThis.frame=banditFrame;globalThis.bind=m=>scene.model=m;",c);
function make(hero='kael'){const m=new c.T(hero);c.bind(m);m.containers=[];m.enemies=[];m.p.x=600;m.p.y=555;return m;}
function enemy(m,side=1){const e={kind:'guard',id:1,x:600+side*100,y:555,face:-side,hp:110,maxHp:110,state:'guard',t:0,cool:99,training:true,walkDistance:0,guardCooldown:99};m.enemies=[e];return e;}
let m=new c.T('kael');c.bind(m);m.p.inv=999;assert.equal(m.enemies.filter(e=>e.kind==='guard').length,3);assert(m.enemies.filter(e=>e.kind==='guard').every(e=>e.x>1280&&e.state==='entering'));for(let i=0;i<900;i++)m.update(.01,new Set());assert(m.enemies.every(e=>e.state!=='entering'&&e.x<1280));
for(const hero of ['kael','lyra','garran','selene']){m=make(hero);let e=enemy(m);assert(m.guardBlocks(e,600));assert(!m.guardBlocks(e,800));assert(!m.guardBlocks(e,600,true));e.t=.6;assert(!m.guardBlocks(e,600));e.t=0;m.attack();m.updatePlayer(.30,new Set());if(hero==='selene')m.witchHit(e,20,1);else if(hero==='garran')m.knightImpact(20,150);assert.equal(e.hp,110,hero+' light shield block');}
m=make('garran');let e=enemy(m);m.knightImpact(35,150,48,true);assert.equal(e.hp,75);assert.equal(e.state,'thrown');
m=make('selene');e=enemy(m);m.witchHit(e,40,1,true);assert.equal(e.hp,70);assert.equal(e.state,'thrown');
m=make('lyra');e=enemy(m);m.arrowHit(e,{owner:0,damage:35,face:1});assert.equal(e.hp,75);assert.equal(e.state,'thrown');
m=make();e=enemy(m);e.x=630;assert(m.tryGrab());assert.equal(e.state,'grabbed');
m=make();e=enemy(m);e.training=false;e.t=.77;m.updateEnemies(.02);assert.equal(e.state,'walk');assert.equal(e.ai,'commit');e.state='attack';e.t=.47;e.x=700;e.face=-1;e.hit=false;m.updateEnemies(.02);assert.equal(m.p.hp,85,'sword damage/timing');
m=make();e=enemy(m);assert(m.recordEnemyDefeat(e,0));assert.equal(m.p.score,200);assert(!m.recordEnemyDefeat(e,0));
for(const state of ['idle','walk','entering','attack','guard','hurt','grabbed','thrown','down','dead','pitfall'])for(let t=0;t<1.5;t+=.05){const key=c.frame({kind:'guard',state,t,walkDistance:t*120,lift:t*20});assert(fs.existsSync('dist/assets/characters/'+key+'.png'),key);}
assert.equal(new c.F('kael').enemies.filter(e=>e.kind==='guard').length,0);
console.log('PASS guard offscreen entry, all hero shield interactions, rear/recovery vulnerability, heavy counters, grab/throw, sword contact, score, animation states, Forest unchanged');
