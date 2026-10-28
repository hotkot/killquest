/* Boot gate: Phaser owns its images; this owns DOM art, audio and readiness. */
(function(root){
 'use strict';
 const el=id=>document.getElementById(id),audio=new Map(),music=new Map(),retainedImages=[];
 let sprite=0,support=0,failed=false,ready=false;
 function progress(){const value=Math.min(99,Math.floor(sprite*70+support*25));el('loadingFill').style.width=value+'%';el('loadingPercent').textContent=value+'%';el('loadingBar').setAttribute('aria-valuenow',value);}
 function fail(message){if(failed)return;failed=true;el('loadingStatus').textContent=message||'Loading failed. Please retry.';el('loadingRetry').hidden=false;}
 el('loadingRetry').onclick=()=>location.reload();
 const pending=new Map();
 function load(url){if(!pending.has(url))pending.set(url,loadAsset(url));return pending.get(url);}
 async function loadAsset(url){
  if(/\.(wav|mp3|mp4)(\?|$)/.test(url)){
   const response=await fetch(url,{signal:AbortSignal.timeout(60000)});if(!response.ok)throw Error('Audio unavailable');
   const bytes=await response.arrayBuffer();if(url.includes('.wav'))audio.set(url,bytes);else music.set(url,URL.createObjectURL(new Blob([bytes],{type:url.includes('.mp4')?'video/mp4':'audio/mpeg'})));
  }else await new Promise((resolve,reject)=>{const image=new Image();retainedImages.push(image);const timer=setTimeout(()=>reject(Error('Image timeout')),60000);image.onload=()=>{clearTimeout(timer);(image.decode?image.decode():Promise.resolve()).then(resolve,reject)};image.onerror=()=>{clearTimeout(timer);reject(Error('Image unavailable'))};image.src=url;});
 }
 const isIntro=url=>url==='assets/cinematic/killquest-hype-v126.mp4'||url.includes('opening-narration-')||url.includes('killquest-logo.png')||url.includes('killquest-menu-v105.png');
 const urls=[...(root.KillQuestBootAssets||[])].sort((a,b)=>Number(isIntro(b))-Number(isIntro(a)));
 const introReady=Promise.all(urls.filter(isIntro).map(load));introReady.catch(()=>{});let next=0,done=0;
 const assets=Promise.all(Array.from({length:Math.min(6,urls.length)},async()=>{while(next<urls.length){const url=urls[next++];await load(url);support=++done/urls.length;progress();}}));
 // Attach rejection immediately; a Phaser load can take longer than support art.
 assets.catch(()=>fail('An asset could not be loaded. Check your connection and retry.'));
 function prepareMusic(track){return new Promise((resolve,reject)=>{
  const url=track.getAttribute('src')||track.src,blob=music.get(url)||music.get([...music.keys()].find(k=>url.endsWith(k)));
  if(!blob){reject(Error('Missing music'));return;}
  const timer=setTimeout(()=>finish(Error('Music timeout')),30000);
  function finish(error){clearTimeout(timer);track.removeEventListener('canplaythrough',loaded);track.removeEventListener('error',bad);error?reject(error):resolve();}
  function loaded(){finish()}function bad(){finish(Error('Music unavailable'))}
  track.addEventListener('canplaythrough',loaded,{once:true});track.addEventListener('error',bad,{once:true});track.preload='auto';track.src=blob;track.load();
 });}
 async function sceneReady(onReady){
  el('loadingStatus').textContent='Preparing weapons and voices…';
  try{
   await assets;if(failed)return;
   const mixer=root.__bootAudioMixer;
   if(mixer){const decoded=await mixer.prepare();if(decoded.some(b=>!b))throw Error('Sound decode failed');await Promise.all([prepareMusic(mixer.music),prepareMusic(mixer.menuMusic)]);}
   if(document.fonts)await document.fonts.ready;
   if(failed)return;audio.clear();ready=true;
   el('loadingFill').style.width='100%';el('loadingPercent').textContent='100%';el('loadingBar').setAttribute('aria-valuenow',100);el('loadingStatus').textContent='Ready for battle';
   // Paint completion, then release pointer, keyboard and controller menus together.
   requestAnimationFrame(()=>requestAnimationFrame(()=>{if(failed)return;if(!root.BootFlow){el('loadingScreen').hidden=true;document.body.classList.remove('booting');}onReady();}));
  }catch{fail('The game could not finish loading. Please retry.');}
 }
 root.LoadingScreen={audio,media:music,introReady,spriteProgress(p){sprite=Math.max(sprite,p);progress();if(p>=1)el('loadingStatus').textContent='Preparing the warband…';},sceneReady,fail,get ready(){return ready&&!failed;}};
 window.addEventListener('error',event=>{if(!ready&&event.target?.tagName==='SCRIPT')fail('A game file could not be loaded. Please retry.');},true);
})(globalThis);
