// Supporting DOM art/audio; Phaser's own preload owns all scene textures.
const fs=require('fs'),vm=require('vm');const root='dist/';const audio=fs.readFileSync(root+'audio.js','utf8'),ctx={};vm.createContext(ctx);vm.runInContext(audio.slice(0,audio.indexOf('class GameAudio'))+';globalThis.variants=AUDIO_VARIANTS;',ctx);
const urls=new Set();for(const [family,count] of Object.entries(ctx.variants))for(let i=0;i<count;i++)urls.add(`assets/audio/${family}-${i}.wav?v=witch-v90`);
for(const n of ['slide','ui','victory','defeat','menu-move','menu-confirm','menu-back'])urls.add(`assets/audio/${n}.wav?v=witch-v90`);
for(const file of ['index.html','style.css','game.js','audio.js','opening-cinematic.js'])for(const m of fs.readFileSync(root+file,'utf8').matchAll(/["'](assets\/[^"']+\.(?:png|webp|jpg|mp3|mp4)(?:\?[^"']*)?)["']/g))if(fs.existsSync(root+m[1].split('?')[0]))urls.add(m[1]);
fs.writeFileSync(root+'loading-assets.js','window.KillQuestBootAssets='+JSON.stringify([...urls].sort(),null,1)+';\n');console.log('Boot supporting assets:',urls.size);
