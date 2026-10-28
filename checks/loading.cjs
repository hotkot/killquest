const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const flush=()=>new Promise(r=>setImmediate(r));
function harness(failFetch=false){
 const nodes={},frames=[],releases=[];let revealed=false;
 const node=id=>nodes[id]??={style:{},hidden:false,textContent:'',setAttribute(k,v){this[k]=v}};
 const ctx={Map,Set,Promise,Array,Math,Blob,AbortSignal,URL:{createObjectURL:()=> 'blob:music'},setTimeout:()=>1,clearTimeout(){},requestAnimationFrame:f=>frames.push(f),location:{reload(){ctx.reloaded=true}},document:{getElementById:node,body:{classList:{remove(){revealed=true}}},fonts:{ready:Promise.resolve()}},KillQuestBootAssets:['assets/a.png','assets/audio/a.wav?v=witch-v90','assets/audio/music.mp3'],fetch:async()=>({ok:!failFetch,arrayBuffer:async()=>new ArrayBuffer(8)}),Image:class{set src(v){queueMicrotask(()=>this.onload())}decode(){return Promise.resolve()}},addEventListener(){}};
 ctx.window=ctx;ctx.globalThis=ctx;ctx.__bootAudioMixer={prepare:()=>new Promise(r=>releases.push(r))};
 for(const key of ['music','menuMusic'])ctx.__bootAudioMixer[key]=new class{constructor(){this.events={}}getAttribute(){return 'assets/audio/music.mp3'}addEventListener(k,f){this.events[k]=f}removeEventListener(k){delete this.events[k]}load(){queueMicrotask(()=>this.events.canplaythrough())}};
 vm.createContext(ctx);vm.runInContext(fs.readFileSync('dist/loading.js','utf8'),ctx);return {ctx,node,frames,releases,get revealed(){return revealed}};
}
(async()=>{
 const h=harness();let menu=false;h.ctx.LoadingScreen.spriteProgress(1);const p=h.ctx.LoadingScreen.sceneReady(()=>menu=true);await flush();assert(!menu&&!h.revealed);assert.equal(h.ctx.LoadingScreen.audio.size,1);assert.equal(h.node('loadingBar')['aria-valuenow'],95);h.releases[0]([{}]);await p;assert(!menu);assert.equal(h.frames.length,1);h.frames.shift()();assert(!menu);h.frames.shift()();assert(menu&&h.revealed);assert.equal(h.node('loadingBar')['aria-valuenow'],100);assert.equal(h.ctx.LoadingScreen.audio.size,0);
 const bad=harness(true);let escaped=false;await bad.ctx.LoadingScreen.sceneReady(()=>escaped=true);assert(!escaped&&!bad.revealed);assert.equal(bad.node('loadingRetry').hidden,false);bad.node('loadingRetry').onclick();assert(bad.ctx.reloaded);
 const imageFail=harness();imageFail.ctx.LoadingScreen.fail('Image failed');await flush();await imageFail.ctx.LoadingScreen.sceneReady(()=>{throw Error('must stay gated')});assert(!imageFail.revealed);
 const manifest={window:{}};vm.runInNewContext(fs.readFileSync('dist/loading-assets.js','utf8'),manifest);for(const url of manifest.window.KillQuestBootAssets)assert(fs.existsSync('dist/'+url.split('?')[0]),url);
 const game=fs.readFileSync('dist/game.js','utf8');assert(game.includes("function menuController(direction,confirm=false,cancel=false){if(mode==='loading')return;"));assert(game.includes("window.addEventListener('keydown',e=>{if(mode==='loading')return;"));
 console.log('PASS: staged readiness gate, no premature menu, audio prefetch/decode wait, music readiness, painted 100%, failure/retry, manifest paths and boot input guards.');
})().catch(e=>{console.error(e);process.exitCode=1});
