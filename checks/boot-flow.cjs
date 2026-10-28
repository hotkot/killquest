const vm=require('vm'),fs=require('fs'),assert=require('node:assert/strict');
const flush=()=>new Promise(r=>setImmediate(r));
function harness(){let introResolve,introReject,end,title=0;const phases=[],nodes={menu:{hidden:false},loadingScreen:{hidden:false}};const ctx={LoadingScreen:{introReady:new Promise((r,j)=>{introResolve=r;introReject=j})},OpeningCinematic:{play(done){end=done}},document:{getElementById:id=>nodes[id],body:{classList:{remove(){}}}}};ctx.globalThis=ctx;vm.runInNewContext(fs.readFileSync('dist/boot-flow.js','utf8'),ctx);ctx.BootFlow.begin(()=>title++,p=>phases.push(p));return {ctx,nodes,phases,introResolve,introReject,finish:()=>end(),get title(){return title}};}
(async()=>{
 const fast=harness();fast.introResolve();await flush();assert.deepEqual(fast.phases,['cinematic']);assert(fast.nodes.menu.hidden);fast.ctx.BootFlow.gameReady();assert.equal(fast.title,0);fast.finish();assert.equal(fast.title,1);assert(fast.nodes.loadingScreen.hidden);fast.ctx.BootFlow.gameReady();assert.equal(fast.title,1);
 const slow=harness();slow.introResolve();await flush();slow.finish();assert.equal(slow.title,0);assert(!slow.nodes.loadingScreen.hidden);assert(slow.nodes.menu.hidden);slow.ctx.BootFlow.gameReady();assert.equal(slow.title,1);assert(slow.nodes.loadingScreen.hidden);
 const early=harness();early.ctx.BootFlow.gameReady();assert.equal(early.title,0);early.introResolve();await flush();assert.equal(early.title,0);early.finish();assert.equal(early.title,1);
 const broken=harness();broken.introReject(Error('art unavailable'));await flush();assert.equal(broken.title,0);assert(!broken.nodes.loadingScreen.hidden);
 const opening=fs.readFileSync('dist/opening-cinematic.js','utf8');assert(!opening.includes('startMenuMusic('));assert(opening.includes('stopBackgroundMusic()'));
 console.log('PASS: cinematic masks loading; both completion orders, skip before readiness, early ready, intro failure, one title transition, and no menu music during opening.');
})().catch(e=>{console.error(e);process.exitCode=1});
