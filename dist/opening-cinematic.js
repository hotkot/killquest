/* Rendered opening video, independent of background game loading. */
(function(root){
 'use strict';
 const url='assets/cinematic/killquest-hype-v126.mp4';let active=false,done=null,frame=0,previous=new Set();
 const $=id=>document.getElementById(id),video=()=>$('cineVideo'),mixer=()=>root.__bootAudioMixer;
 function sound(){if(!active)return;const m=mixer();m?.unlock();video().volume=m?.effectsEnabled===false?0:(m?.effectVolume??.8);video().muted=false;$('cineSound').hidden=true;video().play().catch(()=>{});}
 function finish(){if(!active)return;active=false;cancelAnimationFrame(frame);video().pause();$('openingCinematic').hidden=true;const callback=done;done=null;callback?.();}
 function poll(){if(!active)return;const pressed=new Set();for(const p of navigator.getGamepads?.()||[])if(p?.connected)for(const i of [0,1,9])if(p.buttons[i]?.pressed)pressed.add(p.index+':'+i);if(!document.hidden&&document.hasFocus()&&video().currentTime>.3&&[...pressed].some(k=>!previous.has(k))){finish();return;}previous=pressed;frame=requestAnimationFrame(poll);}
 function play(callback,{source=url,title='KillQuest opening cinematic'}={}){if(active)return;done=callback;active=true;previous=new Set();for(const p of navigator.getGamepads?.()||[])if(p?.connected)for(const i of [0,1,9])if(p.buttons[i]?.pressed)previous.add(p.index+':'+i);mixer()?.stopBackgroundMusic();const v=video();v.src=root.LoadingScreen?.media?.get(source)||source;$('openingCinematic').setAttribute?.('aria-label',title);v.setAttribute?.('aria-label',title+' with subtitles');v.currentTime=0;v.volume=mixer()?.effectsEnabled===false?0:(mixer()?.effectVolume??.8);v.muted=false;v.onended=finish;v.onerror=finish;$('openingCinematic').hidden=false;$('cineSkip').onclick=finish;$('cineSound').onclick=sound;$('cineSound').hidden=true;$('cineSkip').focus({preventScroll:true});v.play().catch(()=>{if(!active)return;v.muted=true;$('cineSound').hidden=false;v.play().catch(()=>{});});frame=requestAnimationFrame(poll);}
 window.addEventListener('keydown',e=>{if(!active)return;e.preventDefault();e.stopImmediatePropagation();if(!e.repeat&&['Escape','Enter',' '].includes(e.key)&&video().currentTime>.3)finish();else sound();},{capture:true});
 window.addEventListener('pointerdown',e=>{if(!active)return;sound();if(e.target.closest?.('#cineSkip')){e.preventDefault();e.stopImmediatePropagation();if(video().currentTime>.3)finish();}},{capture:true});
 function resume(){if(active&&!document.hidden&&document.hasFocus())video().play().catch(()=>{});}
 document.addEventListener('visibilitychange',()=>{if(active){if(document.hidden)video().pause();else resume();}});window.addEventListener('blur',()=>{if(active)video().pause();});window.addEventListener('focus',resume);
 root.OpeningCinematic={play,skip:finish,get blocking(){return active;},url};
})(globalThis);
