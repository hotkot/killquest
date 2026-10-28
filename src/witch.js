'use strict';
// Selene's simulation and sprite selection stay independent of Phaser.
const isWitch=p=>p.character==='selene';
const WITCH_CLIPS={idle:4,walk:12,jump:4,cast1:6,cast2:6,cast3:6,'air-cast':6,push:8,slam:4,teleport:4,rage:4,hurt:4,pickup:4,win:4};
const WITCH_STRIKES=[{duration:.44,impact:.21,linkAt:.40,damage:22,speed:600},{duration:.48,impact:.23,linkAt:.44,damage:27,speed:650},{duration:.58,impact:.29,linkAt:.56,damage:36,speed:720}];
const WITCH_PUSH={duration:.94,impact:.35,damage:35,range:210,depth:70};
const WITCH_SLAM={duration:.80,impact:.42,damage:50,range:230,depth:80};
const WITCH_RAGE={duration:2.6,release:.60,range:680,depth:110,damage:200};
// Keep the cast contact aligned with the first full forward-thrust pose.
function witchPushPose(t){return t<WITCH_PUSH.impact?animationIndex(t,WITCH_PUSH.impact,4):4+animationIndex(t-WITCH_PUSH.impact,WITCH_PUSH.duration-WITCH_PUSH.impact,4);}
function witchPushReaches(p,o,slam=false){const s=slam?WITCH_SLAM:WITCH_PUSH,dx=(o.x-p.x)*p.face;return Math.abs(o.y-p.y)<s.depth&&(slam?Math.abs(dx)<s.range:dx>=0&&dx<s.range);}
function witchFrame(p){let clip='idle',i=0;
 if(p.state==='idle')i=Math.floor((p.idleTime||0)/.22)%4;
 else if(p.state==='walk'){clip='walk';i=Math.floor(p.walkDistance/14)%12;}
 else if(p.state==='attack'){clip=p.witchHeavy?'push':'cast'+(p.step+1);i=p.witchHeavy?witchPushPose(p.t):animationIndex(p.t,WITCH_STRIKES[p.step].duration,6);}
 else if(p.state==='jump'){clip=p.airAttack?(p.airHeavy?'slam':'air-cast'):'jump';i=animationIndex(p.airAttack?p.airT:p.t,p.airAttack?(p.airHeavy?WITCH_SLAM.duration:WITCH_STRIKES[p.airStep].duration):JUMP_DURATION,p.airAttack&&!p.airHeavy?6:4);if(p.airLanding){clip='jump';i=3;}}
 else if(p.state==='dodge'){clip='teleport';i=animationIndex(p.t,.55,4);}
 else if(p.state==='rage'){clip='rage';i=p.t<.25?0:p.t<.60?1:p.t<2.15?2:3;}
 else if(p.state==='pickup'){clip='pickup';i=animationIndex(p.t,PICKUP_DURATION,4);}
 else if(p.state==='grab'){clip='push';i=p.t<.2?0:1;}
 else if(p.state==='throw'){clip='push';i=p.t<THROW_RELEASE?2:4;}
 else if(p.state==='victory'){clip='win';i=animationIndex(p.t,1.1,4);}
 else if(p.state==='respawn'){clip='jump';i=p.t<.75?2:3;}
 else if(['hurt','launched','down','dead'].includes(p.state)){clip='hurt';i=p.state==='hurt'?0:p.state==='launched'?1:p.state==='down'?(p.t<.55?2:3):2;}
 return frameKey('witch-'+clip,i);
}
function witchJumpHeight(p){
 if(p.airLanding){const u=clamp((p.t-p.airLandT)/.18,0,1);return p.airLandHeight*(1-u*u*(3-2*u));}
 if(p.airAttack){const d=p.airHeavy?WITCH_SLAM.duration:WITCH_STRIKES[p.airStep].duration;
  if(p.airHeavy)return Math.max(0,(p.airLift+15)*(1-clamp((p.airT-.10)/.32,0,1)));
  const u=clamp(p.airT/d,0,1);return p.airStep===2?p.airLift*(1-u*u*(3-2*u)):Math.max(65,p.airLift)+12*Math.sin(Math.PI*u);
 }
 return 110*Math.sin(Math.PI*clamp((p.t-.10)/.62,0,1));
}
function installWitchCombat(Combat){Object.assign(Combat.prototype,{
 attackWitch(heavy,input){const p=this.p;if(p.hp<=0||['dead','respawn','launched','down','pickup','rage','hurt','dodge','throw'].includes(p.state))return;
  if(p.state==='grab'){if(!heavy)this.throwGrab(input);return;}
  if(p.state==='jump'){
   if(p.airLanding)return;if(heavy){if(p.airHeavyUsed)return;p.airLift=jumpHeight(p);p.airAttack=p.airHeavy=p.airHeavyUsed=p.airUsed=true;p.airT=0;p.airStep=0;p.airHit=p.airQueue=false;return;}
   if(p.airHeavy)return;if(p.airAttack){if(p.airStep<2)p.airQueue=true;return;}
   if(!p.airUsed&&p.t<.54){p.airLift=jumpHeight(p);p.airAttack=p.airUsed=true;p.airHeavy=false;p.airStep=0;p.airT=0;p.airHit=p.airQueue=false;}return;
  }
  if(p.state==='attack'&&!heavy){if(!p.witchHeavy&&p.step<2)p.queue=true;return;}
  if(p.state==='attack'&&p.witchHeavy)return;
  if(!heavy&&(this.tryPickup()||this.tryGrab()))return;
  p.state='attack';p.t=0;p.step=0;p.witchHeavy=heavy;p.comboTravel=null;p.link=null;p.spinAttack=false;p.hit=p.queue=false;
  if(!heavy)soundCue('hero-effort',{x:p.x,gain:.65});
 },
 witchFx(kind,x,y,face=1,life=.5,extra={}){this.witchEffects??=[];this.witchEffects.push({kind,x,y,face,life,max:life,...extra});},
 witchHit(e,damage,face,launch=false,rage=false){const p=this.p;e.lastHitOwner=p.id;e.hp-=damage;this.hits++;this.comboTimer=2;if(!rage)p.rage=clamp(p.rage+RAGE_GAIN,0,100);
  this.witchFx('burst',e.x,e.y-50,face,.34,{width:110,height:100});soundCue('witch-impact',{x:e.x,gain:.7});
  if(e.kind!=='king'){if(launch){this.launchEnemy(e,face,230,25);e.throwNoRage=!!rage;if(e.hp<=0)e.flightDead=true;}else{e.state=e.hp<=0?'dead':'hurt';e.t=0;e.cool=.7;e.x=clamp(e.x+face*14,this.leftEdge(35),this.rightEdge(35));}}
  if(e.hp<=0&&(!launch||e.kind==='king')){this.recordEnemyDefeat(e,p.id);enemyDeathCue(e);}
 },
 witchPush(slam=false){const p=this.p,s=slam?WITCH_SLAM:WITCH_PUSH,reaches=o=>witchPushReaches(p,o,slam);
  this.damageContainers(s.damage,reaches);for(const e of this.enemies)if(e.hp>0&&!['entering','grabbed','thrown','down'].includes(e.state)&&reaches(e))this.witchHit(e,s.damage,slam?(e.x>=p.x?1:-1):p.face,true);
  if(slam)this.witchFx('burst',p.x,p.y-30,1,.52,{width:s.range*2.2,height:210});else this.witchFx('push',p.x+p.face*(s.range/2+15),p.y-85,p.face,.52,{width:s.range+30,height:150});soundCue('witch-impact',{x:p.x,gain:1,rate:.8});scene.cameras.main.shake(140,.008);
 },
 fireWitchFlame(air=false){const p=this.p,s=WITCH_STRIKES[air?p.airStep:p.step];this.witchFlames??=[];
  this.witchFlames.push({owner:p.id,x:p.x+p.face*48,y:p.y,z:air?jumpHeight(p)+90:90,vx:p.face*s.speed,vz:air?-440:0,face:p.face,damage:s.damage,life:1.05,age:0,step:air?p.airStep:p.step});
  soundCue('witch-cast',{x:p.x,rate:1+(air?p.airStep:p.step)*.07,gain:.75});
 },
 updateWitch(dt,input){const p=this.p;
  if(p.state==='dodge'){
   if(!p.teleported&&p.t>=.20){p.teleported=true;const start=p.x,target=clamp(start-p.face*190,this.leftEdge(60),this.rightEdge(60));
    for(let d=Math.min(8,Math.abs(target-start));Math.abs(target-p.x)>.01;){const old=p.x,next=p.x+Math.sign(target-p.x)*Math.min(d,Math.abs(target-p.x));if(this.pitEnabled&&this.inPit(next,p.y,25))break;p.x=next;this.resolveContainers(p,old,p.y);if(Math.abs(p.x-next)>.01||Math.abs(p.x-old)<.01)break;}
    this.witchFx('burst',start,p.y-65,p.face,.35,{width:90,height:190});this.witchFx('burst',p.x,p.y-65,p.face,.40,{width:90,height:190});soundCue('witch-teleport',{x:p.x});
   }
   if(p.t>=.55){p.state='idle';p.t=0;}return;
  }
  if(p.state==='attack'){
   const s=p.witchHeavy?WITCH_PUSH:WITCH_STRIKES[p.step];if(!p.hit&&p.t>=s.impact){p.hit=true;if(p.witchHeavy)this.witchPush();else this.fireWitchFlame();}
   if(!p.witchHeavy&&p.queue&&p.step<2&&p.t>=s.linkAt){p.step++;p.t=0;p.hit=p.queue=false;}
   else if(p.t>=s.duration){p.state='idle';p.t=0;p.witchHeavy=false;}return;
  }
  if(p.state==='jump'){
   if(p.airAttack){p.airT+=dt;const s=p.airHeavy?WITCH_SLAM:WITCH_STRIKES[p.airStep];
    if(!p.airHit&&p.airT>=s.impact){p.airHit=true;if(p.airHeavy){this.witchPush(true);soundCue('hero-effort',{x:p.x,gain:.7});}else this.fireWitchFlame(true);}
    if(!p.airHeavy&&p.airQueue&&p.airStep<2&&p.airT>=s.linkAt){p.airLift=jumpHeight(p);p.airStep++;p.airT=0;p.airHit=p.airQueue=false;}
    else if(p.airT>=s.duration){const h=jumpHeight(p);p.airAttack=false;p.airLanding=true;p.airLandT=p.t;p.airLandHeight=h;}
   }
   if(!p.airAttack&&(p.airLanding?p.t-p.airLandT>=.18:p.t>=JUMP_DURATION)){p.state='idle';p.t=0;}
   else{const move=movementFor(input);p.x+=move.x*155*dt;p.y+=move.y*100*dt;}return;
  }
  if(p.state==='rage'){
   const c=p.firestorm;p.face=c.face;
   if(p.t>=WITCH_RAGE.release){
    if(!p.hit){p.hit=true;this.witchFx('storm',c.x+c.face*WITCH_RAGE.range/2,c.y-100,c.face,1.65,{width:WITCH_RAGE.range+80,height:330,owner:p.id});soundCue('witch-storm',{x:p.x,gain:1});scene.cameras.main.shake(250,.012);}
    if(p.t<2.25){const reaches=o=>(o.x-c.x)*c.face>0&&(o.x-c.x)*c.face<WITCH_RAGE.range&&Math.abs(o.y-c.y)<WITCH_RAGE.depth;
     this.damageContainers(WITCH_RAGE.damage,o=>{if(c.props.has(o.id)||!reaches(o))return false;c.props.add(o.id);return true;});
     for(const e of this.enemies)if(e.hp>0&&!['entering','grabbed','thrown'].includes(e.state)&&!c.hits.has(e.id)&&reaches(e)){c.hits.add(e.id);this.witchHit(e,WITCH_RAGE.damage,c.face,true,true);}
     this.arrows=this.arrows.filter(a=>!reaches(a));
    }
   }
   if(p.t>=WITCH_RAGE.duration){p.state='idle';p.t=0;}return;
  }
 },
 updateWitchProjectiles(dt){this.witchFlames??=[];this.witchEffects??=[];
  for(const a of this.witchFlames){const ox=a.x,oz=a.z;a.x+=a.vx*dt;a.z+=a.vz*dt;a.age+=dt;a.life-=dt;
   const steps=Math.max(1,Math.ceil(Math.max(Math.abs(a.x-ox),Math.abs(a.z-oz))/12));let hit=false;
   for(let i=1;i<=steps&&!hit;i++){const u=i/steps,x=ox+(a.x-ox)*u,z=oz+(a.z-oz)*u;if(z< -20)break;
    // Stop at the first target in travel order, including solid scenery.
    const targets=[];for(const e of this.enemies)if(e.hp>0&&!['entering','grabbed','thrown'].includes(e.state)&&Math.abs(e.x-x)<30&&Math.abs(e.y-a.y)<27&&z+20>=5&&z-20<(e.kind==='dog'?85:e.kind==='king'?210:160))targets.push({e,x:e.x});
    for(const c of this.containers)if(!c.broken&&Math.abs(c.x-x)<(c.halfW??50)&&Math.abs(c.y-a.y)<30&&z<125&&z> -10)targets.push({c,x:c.x});
    const target=targets.sort((a,b)=>Math.abs(a.x-x)-Math.abs(b.x-x))[0];if(target){hit=true;a.life=0;this.withPlayer(a.owner,()=>{if(target.e)this.witchHit(target.e,a.damage,a.face);else this.damageContainers(a.damage,c=>c===target.c);});this.witchFx('burst',x,a.y-z,a.face,.28,{width:85,height:85});}
   }
   if(a.z<=0){a.life=0;this.witchFx('burst',a.x,a.y,a.face,.30,{width:100,height:65});}
  }
  this.witchFlames=this.witchFlames.filter(a=>a.life>0&&a.x>this.leftEdge()-120&&a.x<this.rightEdge()+120).slice(-40);
  for(const e of this.witchEffects)e.life-=dt;this.witchEffects=this.witchEffects.filter(e=>e.life>0).slice(-50);
 }
});}
function renderWitchEffects(view,m){view.witchViews??=new Map();const live=new Set([...(m.witchFlames||[]),...(m.witchEffects||[])]);
 for(const [a,s] of view.witchViews)if(!live.has(a)){s.destroy();view.witchViews.delete(a);}
 for(const a of live){const projectile=Object.hasOwn(a,'vx'),kind=projectile?'flame':a.kind==='storm'?'storm':a.kind==='push'?'flame':'burst';let sprite=view.witchViews.get(a);if(!sprite){sprite=view.add.sprite(0,0,'witch-fx-'+kind+'-00').setOrigin(.5,.5);view.witchViews.set(a,sprite);}
  const i=projectile?Math.floor(a.age*16)%4:a.kind==='storm'?Math.floor((a.max-a.life)*12)%4:animationIndex(a.max-a.life,a.max,4);
  sprite.setTexture(frameKey('witch-fx-'+kind,i)).setPosition(a.x,projectile?a.y-a.z:a.y).setFlipX(a.face<0).setDepth((projectile?a.y:a.y+(a.height||100)/2)+2).setDisplaySize(projectile?105+(a.step||0)*12:a.width,projectile?65+(a.step||0)*8:a.height).setAlpha(projectile?1:Math.min(1,a.life/.16));
  if(projectile)sprite.setRotation(Math.atan2(-a.vz,Math.abs(a.vx))*(a.face<0?-1:1));else sprite.setRotation(0);
 }
}
