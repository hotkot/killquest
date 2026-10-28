'use strict';
const {app,BrowserWindow,Menu,protocol,net,session,dialog}=require('electron');
const path=require('node:path');
const {pathToFileURL,fileURLToPath}=require('node:url');
const fs=require('node:fs');
const resolveAsset=require('./asset-path.cjs');
app.setName('KillQuest');
protocol.registerSchemesAsPrivileged([{scheme:'killquest',privileges:{standard:true,secure:true,supportFetchAPI:true,corsEnabled:true,stream:true}}]);
let window;
if(!app.requestSingleInstanceLock())app.quit();
else{
 app.on('second-instance',()=>{if(window){if(window.isMinimized())window.restore();window.focus();}});
 app.whenReady().then(()=>{
  const root=path.join(__dirname,'game');
  protocol.handle('killquest',async request=>{
   const file=resolveAsset(root,request.url);
   if(!file)return new Response('Forbidden',{status:403});
   if(!fs.existsSync(file)||!fs.statSync(file).isFile())return new Response('Not found',{status:404});
   return net.fetch(pathToFileURL(file).toString());
  });
  session.defaultSession.setPermissionRequestHandler((_contents,_permission,callback)=>callback(false));
  session.defaultSession.webRequest.onBeforeRequest((details,callback)=>{
   let allowed=details.url.startsWith('killquest://game/')||details.url.startsWith('devtools:');
   if(details.url.startsWith('file:')){try{const relative=path.relative(root,fileURLToPath(details.url));allowed=!!relative&&!relative.startsWith('..')&&!path.isAbsolute(relative);}catch{allowed=false;}}
   callback({cancel:!allowed});
  });
  Menu.setApplicationMenu(null);
  window=new BrowserWindow({title:'KillQuest',width:1440,height:900,minWidth:640,minHeight:360,backgroundColor:'#090612',icon:path.join(__dirname,'icon.png'),show:false,autoHideMenuBar:true,webPreferences:{nodeIntegration:false,contextIsolation:true,sandbox:true,webSecurity:true}});
  window.once('ready-to-show',()=>window.show());
  window.webContents.setWindowOpenHandler(()=>({action:'deny'}));
  window.webContents.on('will-navigate',(event,url)=>{if(url!=='killquest://game/index.html')event.preventDefault();});
  window.webContents.on('before-input-event',(event,input)=>{
   if(input.type==='keyDown'&&!input.isAutoRepeat&&input.key==='F11'){event.preventDefault();window.setFullScreen(!window.isFullScreen());}
   if(input.type==='keyDown'&&input.alt&&input.key==='F4'){event.preventDefault();window.close();}
  });
  window.webContents.on('did-fail-load',(_e,code,description)=>{if(code!==-3)dialog.showErrorBox('KillQuest could not start',description);});
  window.loadURL('killquest://game/index.html');
 });
 app.on('window-all-closed',()=>app.quit());
}
