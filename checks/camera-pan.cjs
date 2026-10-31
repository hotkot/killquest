'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const c={Set,Map,Math,Number,document:{getElementById:()=>null},window:{}};
vm.createContext(c);
vm.runInContext(fs.readFileSync('dist/game.js','utf8').split('class BrawlScene')[0]+`
scene={cameras:{main:{shake(){},flash(){}}}};soundCue=()=>{};mode='play';
Combat.prototype.update=function(){};
globalThis.api={CityCombat,ForestCombat,panCameraForward,cityRoadCenter,bind:m=>scene.model=m};`,c);
const {CityCombat,ForestCombat,panCameraForward:pan,cityRoadCenter:road,bind}=c.api;
for(const hz of [30,60,120]){
 let x=0;for(let i=0;i<hz*2;i++){const previous=x;x=pan(x,5000,1/hz);assert(x-previous<=300/hz+1e-9);}
 assert(Math.abs(x-594)<7,'frame-rate independent pan');
}
assert.equal(pan(100,5000,60),109.9,'suspended frame must not jump');
assert.equal(pan(100,0,.02),100,'no backward scrolling');
assert.equal(pan(100,105,.02),105,'no target overshoot');
for(const dt of [0,-1,NaN,Infinity])assert.equal(pan(100,200,dt),100);
for(const Model of [ForestCombat,CityCombat])for(const heroes of [['kael'],['kael','lyra','garran','selene']]){
 const m=new Model(heroes);bind(m);m.phase='explore';m.enemies=[];m.containers=[];
 m.updateCivilians=()=>{};m.prepareCityEncounters=()=>{};
 m.encounterIndex=999;m.cityGroups=[];m.fightRight=m.worldWidth;
 // The rear hero disappears from the living party, changing its center abruptly.
 m.players.forEach((p,i)=>{p.x=i?1800:100;p.y=m.isCity?road(p.x):555;p.hp=100;});
 m.update(.02,new Set());
 if(heroes.length>1){m.players[0].hp=0;m.players[0].lives=0;}
 else m.p.x=5000;
 const start=m.cameraX;
 for(let i=0;i<200;i++){
  const x=m.cameraX,y=m.cameraY||0;
  m.update(.02,new Set());
  assert(m.cameraX>=x&&m.cameraX-x<=6+1e-8,Model.name+' horizontal snap');
  assert((m.cameraY||0)>=y&&(m.cameraY||0)-y<=3.6+1e-8,'vertical snap');
  assert.equal(m.fightLeft,m.cameraX);
 }
 assert(m.cameraX>start,'camera must catch up');
 // A respawn/rejoin behind the camera cannot pull the view backwards.
 const x=m.cameraX;m.players[0].hp=100;m.players[0].lives=3;m.players[0].x=0;
 m.update(.02,new Set());assert(m.cameraX>=x&&m.cameraX-x<=6+1e-8);
}
console.log('PASS bounded camera panning: Forest/City, solo/four-player, rear-player elimination/rejoin, target jumps, 30/60/120Hz, suspended frames, vertical speed, no rewind or overshoot.');
