/* Optional, self-contained Edge/axe QA. Real-mode search is intercepted locally. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const net=require('node:net');
const path=require('node:path');
const {spawn}=require('node:child_process');
const {chromium}=require('@playwright/test');
const {AxeBuilder}=require('@axe-core/playwright');

const root=path.resolve(__dirname,'../..');
const python=process.env.PX_QA_PYTHON || path.join(root,'.venv',process.platform==='win32'?'Scripts/python.exe':'bin/python');
const port=Number(process.env.PX_QA_PORT||8134);
const base=`http://127.0.0.1:${port}`;
const tags=['wcag2a','wcag2aa','wcag21a','wcag21aa','wc22aa'];
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function shot(page,name){
  if(!process.env.PX_QA_SHOTS)return;
  const directory=path.resolve(process.env.PX_QA_SHOTS);
  fs.mkdirSync(directory,{recursive:true});
  await page.screenshot({path:path.join(directory,`${name}.png`),fullPage:true});
}
const isRealSearch=request=>new URL(request.url()).pathname==='/api/observations' &&
  new URL(request.url()).searchParams.get('mode')==='real';

async function portAvailable(){
  await new Promise((resolve,reject)=>{
    const socket=net.connect({host:'127.0.0.1',port});
    socket.once('connect',()=>{socket.destroy();reject(new Error(`Puerto ${port} ocupado. Usa PX_QA_PORT para elegir otro.`));});
    socket.once('error',e=>{socket.destroy();e.code==='ECONNREFUSED'?resolve():reject(e);});
  });
}

async function accessible(page,view){
  await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));
  await delay(550); // exclude transition opacity from contrast analysis
  const result=await new AxeBuilder({page}).withTags(tags).analyze();
  assert.deepEqual(result.violations.map(v=>v.id),[],`${view}: ${result.violations.map(v=>v.id).join(', ')}`);
}
async function ready(server){
  for(let n=0;n<80;n++){
    if(server.exitCode!==null)throw new Error(`Servidor terminó al arrancar (${server.exitCode})`);
    try {if((await fetch(`${base}/api/health`)).ok)return;}catch{}
    await delay(250);
  }
  throw new Error('Servidor local no disponible en '+base);
}
async function main(){
  assert.ok(fs.existsSync(python),`Falta Python con dependencias: ${python}`);
  assert.ok(Number.isInteger(port)&&port>1024&&port<65536,'PX_QA_PORT inválido');
  await portAvailable();
  const server=spawn(python,['-m','uvicorn','backend.app.main:app','--host','127.0.0.1','--port',String(port),'--no-proxy-headers','--log-level','warning'],
    {cwd:root,env:{...process.env,PX_PUBLIC_MODE:'0'},stdio:['ignore','pipe','pipe']});
  let stderr='';server.stderr.on('data',chunk=>{stderr=(stderr+chunk).slice(-3000);});
  let browser;
  try{
    await ready(server);
    const channel=process.env.PX_QA_BROWSER_CHANNEL || (process.platform==='win32'?'msedge':undefined);
    browser=await chromium.launch(channel?{channel}:{});
    const context=await browser.newContext({viewport:{width:1440,height:900}});
    const page=await context.newPage();
    const failures=[],realRequests=[];
    page.on('pageerror',e=>failures.push(e.message));
    page.on('console',m=>{if(m.type()==='error')failures.push(m.text());});
    context.on('request',r=>{if(isRealSearch(r))realRequests.push(r.url());});
    await page.goto(base,{waitUntil:'domcontentloaded'});
    assert.equal(realRequests.length,0,'La portada consultó IRSA');
    assert.equal(await page.locator('#searchActivity').isHidden(),true);
    await accessible(page,'Portada');
    await page.locator('.hero-actions [data-demo-start]').hover();
    await delay(300);
    assert.notEqual(await page.locator('.hero-actions [data-demo-start]').evaluate(el=>getComputedStyle(el).transform),'none','El botón principal debe reaccionar al hover');
    await page.route('**/api/observations?mode=demo*',async route=>{await delay(600);await route.continue();});
    await page.locator('[data-demo-start]').first().click();
    assert.equal(await page.locator('#searchActivity').getAttribute('data-state'),'loading');
    assert.equal(await page.locator('#searchActivity .activity-track').getAttribute('aria-valuenow'),null);
    await shot(page,'01-demo-loading-desktop');
    await page.waitForFunction(()=>document.querySelector('#summaryCount')?.textContent==='4');
    await page.waitForFunction(()=>document.querySelector('#searchActivity')?.dataset.state==='done');
    assert.equal(await page.locator('#searchActivity .activity-track').getAttribute('aria-valuenow'),'100');
    await page.unroute('**/api/observations?mode=demo*');
    await shot(page,'02-demo-ready-desktop');
    assert.equal(realRequests.length,0,'La Demo consultó IRSA');
    assert.equal(await page.locator('#scienceFigure').isHidden(),true);
    await accessible(page,'Demo: búsqueda guiada');
    await page.route('**/api/compare/jobs/*',async route=>{await delay(600);await route.continue();});
    await page.locator('#compareBtn').click();
    assert.equal(await page.locator('#compareActivity').getAttribute('data-state'),'loading');
    assert.ok(Number(await page.locator('#compareActivity .activity-track').getAttribute('aria-valuenow'))<100);
    assert.equal(await page.locator('#scienceFigure').isHidden(),true);
    await shot(page,'03-comparison-loading-desktop');
    await page.waitForFunction(()=>['imageA','imageB','imageDiff'].every(id=>{
      const image=document.getElementById(id);
      return !image.hidden&&image.complete&&image.naturalWidth>0;
    }),null,{timeout:60000});
    assert.equal(await page.locator('#scienceFigure').isVisible(),true);
    assert.equal(await page.locator('#compareActivity .activity-track').getAttribute('aria-valuenow'),'100');
    await page.unroute('**/api/compare/jobs/*');
    await shot(page,'04-comparison-ready-desktop');
    await accessible(page,'Demo: comparación');
    await page.route('**/api/detect/*',async route=>{await delay(600);await route.continue();});
    await page.locator('#runDetectionTop').click();
    assert.equal(await page.locator('#detectActivity').getAttribute('data-state'),'loading');
    assert.equal(await page.locator('#detectActivity .activity-track').getAttribute('aria-valuenow'),null);
    assert.equal(await page.locator('#candidateList #goDetect').count(),0,'No ofrecer otro análisis mientras se procesa');
    assert.equal(await page.locator('.candidate-pending').isVisible(),true);
    await shot(page,'05-analysis-loading-desktop');
    await page.waitForFunction(()=>Number(document.querySelector('#candidateCount').textContent)>0);
    await page.waitForFunction(()=>document.querySelector('#detectActivity')?.dataset.state==='done');
    assert.equal(await page.locator('#detectActivity .activity-track').getAttribute('aria-valuenow'),'100');
    await page.unroute('**/api/detect/*');
    await page.locator('.candidate-item').first().click();
    assert.match(await page.locator('#candidateInsight').innerText(),/no es un descubrimiento/i);
    const updated=page.waitForResponse(r=>r.url().includes('threshold_sigma=6')&&r.ok());
    await page.locator('#thresholdRange').evaluate(el=>{
      el.value='6';el.dispatchEvent(new Event('input',{bubbles:true}));
      el.dispatchEvent(new Event('change',{bubbles:true}));
    });
    await updated;
    await page.waitForFunction(()=>document.querySelector('#detectActivity .activity-track')?.getAttribute('aria-valuenow')==='100');
    await shot(page,'06-analysis-ready-desktop');
    await accessible(page,'Demo: análisis y umbral');
    for(const width of [360,768,1024,1440]){
      await page.setViewportSize({width,height:900});
      const size=await page.evaluate(()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]);
      assert.ok(size[0]<=size[1],`Desbordamiento en análisis a ${width}px: ${size}`);
    }
    await page.locator('[data-view="academy"]').click();
    await page.locator('[data-lesson="0"]').click();
    await page.keyboard.press('Escape');
    assert.equal(await page.getByRole('dialog').count(),0);
    assert.equal(await page.evaluate(()=>document.activeElement?.dataset.lesson),'0');
    await page.locator('#quizStart').click();
    await accessible(page,'Academia y cuestionario');
    await page.locator('[data-view="sources"]').click();
    await accessible(page,'Fuentes');
    await page.locator('[data-view="explorer"]').click();
    await page.locator('#radius').fill('0.09');
    assert.equal(await page.locator('#scienceFigure').isHidden(),true,'Campo modificado: ocultar imágenes anteriores');
    assert.equal(await page.locator('#searchSummary').isHidden(),true,'Campo modificado: ocultar búsqueda anterior');
    assert.equal(await page.locator('#compareBtn').isDisabled(),true,'Campo modificado: volver a buscar');
    assert.deepEqual(failures,[],'Errores JavaScript/recursos en escritorio');

    const realPage=await context.newPage();
    let failNext=false;
    realPage.on('pageerror',e=>failures.push('IRSA simulado: '+e.message));
    realPage.on('console',m=>{
      if(m.type()==='error'&&!(failNext&&m.text().includes('503 (Service Unavailable)')))
        failures.push('IRSA simulado: '+m.text());
    });
    await realPage.route('**/api/observations?*',async route=>{
      assert.ok(isRealSearch(route.request()),'Solo se debe buscar en modo IRSA');
      await delay(600);
      if(failNext)return route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({detail:'IRSA no disponible para esta prueba.'})});
      return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({
        mode:'real',count:0,observations:[],compatible_pairs:{},suggested_pair:null,
        note:'Sin cobertura para el centro indicado.',warnings:[]
      })});
    });
    await realPage.goto(base,{waitUntil:'domcontentloaded'});
    assert.equal(realRequests.length,0,'La segunda pestaña consultó IRSA al cargar');
    await realPage.locator('[data-real-start]').first().click();
    assert.equal(await realPage.locator('#modeReal').getAttribute('aria-pressed'),'true');
    assert.equal(realRequests.length,0,'IRSA debe esperar el clic explícito en Buscar');
    await realPage.locator('#searchButton').click();
    assert.equal(await realPage.locator('#searchActivity').getAttribute('data-state'),'loading');
    await realPage.emulateMedia({reducedMotion:'reduce'});
    assert.equal(await realPage.locator('#searchActivity .activity-orbit i').evaluate(el=>getComputedStyle(el).animationName),'none','Respetar movimiento reducido');
    await realPage.waitForFunction(()=>document.querySelector('#summaryTitle')?.textContent==='Sin imágenes para este centro');
    await realPage.waitForFunction(()=>document.querySelector('#searchActivity')?.dataset.state==='done');
    assert.equal(await realPage.locator('#searchActivity .activity-track').getAttribute('aria-valuenow'),'100');
    assert.equal(realRequests.length,1,'Buscar debe solicitar una sola vez los metadatos IRSA');
    assert.equal(await realPage.locator('#scienceFigure').isHidden(),true,'La respuesta IRSA vacía no debe generar imágenes demo');
    assert.equal(await realPage.locator('#summaryNext').isDisabled(),true);
    await accessible(realPage,'IRSA: respuesta vacía simulada');
    failNext=true;
    await realPage.locator('#searchButton').click();
    await realPage.waitForFunction(()=>document.querySelector('#searchActivity')?.dataset.state==='error');
    assert.equal(await realPage.locator('#searchActivity .activity-track').getAttribute('aria-valuenow'),null,'Un error no debe mostrar 100 %');
    assert.equal(await realPage.locator('#searchSummary').isHidden(),true);
    assert.equal(await realPage.locator('#searchButton').isEnabled(),true);
    assert.equal(realRequests.length,2);
    await accessible(realPage,'IRSA: error simulado y reintento');
    assert.deepEqual(failures,[],'Errores JavaScript en IRSA simulado');

    const mobileContext=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
    const mobile=await mobileContext.newPage();
    mobile.on('pageerror',e=>failures.push('móvil: '+e.message));
    await mobile.goto(base,{waitUntil:'domcontentloaded'});
    await accessible(mobile,'Móvil: portada');
    await mobile.locator('#menuToggle').click();
    assert.equal(await mobile.locator('#menuToggle').getAttribute('aria-expanded'),'true');
    await mobile.keyboard.press('Escape');
    assert.equal(await mobile.locator('#menuToggle').getAttribute('aria-expanded'),'false');
    await mobile.route('**/api/observations?mode=demo*',async route=>{await delay(600);await route.continue();});
    await mobile.locator('[data-demo-start]').first().click();
    assert.equal(await mobile.locator('#searchActivity').getAttribute('data-state'),'loading');
    const loadingSize=await mobile.evaluate(()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]);
    assert.ok(loadingSize[0]<=loadingSize[1],`Desbordamiento móvil durante carga ${loadingSize}`);
    await shot(mobile,'07-demo-loading-mobile');
    await mobile.waitForFunction(()=>document.querySelector('#summaryCount')?.textContent==='4');
    await shot(mobile,'08-demo-ready-mobile');
    await accessible(mobile,'Móvil: búsqueda guiada');
    const size=await mobile.evaluate(()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]);
    assert.ok(size[0]<=size[1],`Desbordamiento móvil ${size}`);
    assert.deepEqual(failures,[],'Errores JavaScript en móvil');
    console.log('QA UI: demo guiada, comparación, 3 PNG, umbral, academia, IRSA opt-in, móvil y axe: OK.');
  }finally{
    await browser?.close();
    server.kill();
    if(stderr&&server.exitCode!==null&&server.exitCode!==0)console.error(stderr);
  }
}
main().catch(error=>{console.error(error);process.exitCode=1;});
