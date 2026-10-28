/* Loading and the opening run concurrently; the title needs both to finish. */
(function(root){
 'use strict';
 let loaded=false,ended=false,shown=false,title=null,phase=()=>{};
 function reveal(){if(!loaded||!ended||shown)return;shown=true;document.getElementById('loadingScreen').hidden=true;document.body.classList.remove('booting');title();}
 function begin(onTitle,onPhase){title=onTitle;phase=onPhase;document.getElementById('menu').hidden=true;
  root.LoadingScreen.introReady.then(()=>{phase('cinematic');root.OpeningCinematic.play(()=>{ended=true;phase('loading');document.getElementById('loadingScreen').hidden=false;reveal();});}).catch(()=>{ended=true;phase('loading');document.getElementById('loadingScreen').hidden=false;reveal();});
 }
 root.BootFlow={begin,gameReady(){loaded=true;reveal();}};
})(globalThis);
