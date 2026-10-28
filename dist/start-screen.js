/* Title gate: consume the opening press, never pass it into a menu action. */
(function(root){
 'use strict';
 let active=false,onContinue=null,latch=false,enteredAt=0,previous=new Set(),heldKeys=new Set(),pointerHeld=false;
 const screen=()=>document.getElementById('startScreen');
 const mixer=()=>root.__bootAudioMixer;
 function begin(){if(!active)return;active=false;latch=true;enteredAt=performance.now();mixer()?.holdMenuMusic?.(1000);mixer()?.startMenuMusic();mixer()?.play?.('menu-power',{gain:1.8});screen().hidden=true;const callback=onContinue;onContinue=null;callback?.();}
 function show(callback,{waitForRelease=false}={}){onContinue=callback;active=true;latch=waitForRelease;enteredAt=performance.now();screen().hidden=false;screen().focus({preventScroll:true});mixer()?.holdMenuMusic?.();}
 function gesture(event){
  if(event.type==='keydown')heldKeys.add(event.code||event.key);else pointerHeld=true;
  // A gesture during downloads may authorize music when the title appears.
  if(root.LoadingScreen&&!root.LoadingScreen.ready){mixer()?.unlock();return;}
  if(!active&&!latch)return;
  if(event.type==='keydown'&&event.repeat){event.preventDefault();event.stopImmediatePropagation();return;}
  event.preventDefault();event.stopImmediatePropagation();
  if(active&&!latch)begin();
 }
 window.addEventListener('keydown',gesture,{capture:true});
 window.addEventListener('pointerdown',gesture,{capture:true});
 window.addEventListener('keyup',event=>heldKeys.delete(event.code||event.key),{capture:true});
 window.addEventListener('pointerup',()=>{pointerHeld=false;},{capture:true});
 window.addEventListener('pointercancel',()=>{pointerHeld=false;},{capture:true});
 window.addEventListener('blur',()=>{heldKeys.clear();pointerHeld=false;});
 // Pointerdown reveals the menu; discard its following click as well.
 window.addEventListener('click',event=>{if(latch){event.preventDefault();event.stopImmediatePropagation();}},{capture:true});
 function poll(){
  const pressed=new Set();for(const pad of navigator.getGamepads?.()||[])if(pad?.connected)pad.buttons.forEach((b,i)=>{if(b.pressed||b.value>.5)pressed.add(pad.index+':'+i)});
  if(active&&!latch&&!document.hidden&&document.hasFocus()&&[...pressed].some(key=>!previous.has(key)))begin();
  if(latch&&pressed.size===0&&heldKeys.size===0&&!pointerHeld&&performance.now()-enteredAt>250)latch=false;
  previous=pressed;requestAnimationFrame(poll);
 }
 requestAnimationFrame(poll);
 root.StartScreen={show,get blocking(){return active||latch;}};
})(globalThis);
