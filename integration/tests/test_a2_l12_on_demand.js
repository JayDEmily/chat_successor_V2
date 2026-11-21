// Disposable network-intercepted Chrome fixture; no real ChatGPT requests or Sends.
'use strict';
const fs=require('fs'),os=require('os'),path=require('path');
const puppeteer=require('puppeteer-core');
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'l12-refresh-fixture-'));
const jsPath=path.resolve(__dirname,'..','chrome_reader','readback.js');
const project='g-p-11111111111111111111111111111111';
const chat='11111111-1111-1111-1111-111111111111';
const url='https://chatgpt.com/g/'+project+'/c/'+chat;
(async()=>{
let browser;
try {
 browser=await puppeteer.launch({
  headless:true,
  executablePath:process.env.CHROME_BIN || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  userDataDir:profile,
  args:['--disable-background-networking','--no-first-run','--no-default-browser-check','--disable-extensions','--no-proxy-server']
 });
 const page=await browser.newPage();
 await page.setRequestInterception(true);
 let intercepted=0,externalBlocked=0;
 page.on('request', req=>{
  if(req.url()===url){
    intercepted++;
    req.respond({status:200,contentType:'text/html',body:'<!doctype html><html><body><main><button id="send">Send</button></main><script>window.sendCount=0;document.querySelector("#send").addEventListener("click",()=>window.sendCount++);</script></body></html>'});
  } else {externalBlocked++;req.abort();}
 });
 await page.goto(url,{waitUntil:'domcontentloaded'});
 await page.evaluate((p)=>{
  window.chrome=window.chrome||{};
  window.chrome.runtime={getManifest:()=>({content_scripts:[{matches:['https://chatgpt.com/g/'+p+'*']}]})};
  window.setInterval=()=>0;
 },project);
 await page.addScriptTag({path:jsPath});
 const selector='button.chat-succession-source-refresh';
 await page.waitForSelector(selector,{timeout:3000});
 const first=await page.evaluate(()=>{
   const a=JSON.parse(document.querySelector('input.chat-succession-readback').value);
   return {observedAt:a.observedAt,phase:a.phase,project:a.project,chat:a.chat,
    count:document.querySelectorAll('button.chat-succession-source-refresh').length,
    readonly:document.querySelector('input.chat-succession-readback').readOnly,
    sendCount:window.sendCount};
 });
 await new Promise(r=>setTimeout(r,30));
 // With periodic renewal intentionally disabled, passive waiting must
 // not be mistaken for a fresh readback of the saved source.
 const idleAt=await page.evaluate(()=>
   JSON.parse(document.querySelector('input.chat-succession-readback').value).observedAt);
 await page.evaluate(sel=>document.querySelector(sel).click(),selector);
 const second=await page.evaluate(()=>{
   const a=JSON.parse(document.querySelector('input.chat-succession-readback').value);
   return {observedAt:a.observedAt,phase:a.phase,project:a.project,chat:a.chat,
   count:document.querySelectorAll('button.chat-succession-source-refresh').length,
   sendCount:window.sendCount};
 });
 const ax=await page._client().send('Accessibility.getFullAXTree');
 const buttonVisibleInAX=ax.nodes.some(x=>x.role?.value==='button' && x.name?.value==='Chat Succession refresh source readback');
 await page.evaluate(sel=>{history.replaceState(null,'','/home');document.querySelector(sel).click()},selector);
 const removed=await page.evaluate(()=>!document.querySelector('input.chat-succession-readback') && !document.querySelector('button.chat-succession-source-refresh'));
 const checks={
   fixture_intercepted:intercepted===1,
   source_project_matches:first.project===project && second.project===project,
   source_chat_matches:first.chat===chat && second.chat===chat,
   one_refresh_button:first.count===1 && second.count===1,
   readback_readonly:first.readonly===true,
   no_passive_refresh_without_event:idleAt===first.observedAt,
   on_demand_newer:second.observedAt>first.observedAt,
   no_message_send:first.sendCount===0 && second.sendCount===0,
   chrome_accessibility_button:buttonVisibleInAX,
   unsupported_route_removes_controls:removed,
 };
 console.log(JSON.stringify({test:'L12_HEADLESS_REFRESH',checks,blocked_unmatched_requests:externalBlocked,passed:Object.values(checks).every(Boolean)}));
 if(!Object.values(checks).every(Boolean))process.exitCode=2;
} catch (e) {
 console.log(JSON.stringify({test:'L12_HEADLESS_REFRESH',error:String(e),passed:false}));process.exitCode=3;
} finally {
 if(browser)await browser.close();
 fs.rmSync(profile,{recursive:true,force:true});
}
})();
