/* Enrutamiento SPA, estados y mapa ornamental de estrellas. */
(function(){
  const PX=window.PX;
  function skyStars(){
    const canvas=PX.$('heroStars'),ctx=canvas.getContext('2d');
    const dpr=Math.min(devicePixelRatio||1,2);
    const width=canvas.clientWidth,height=canvas.clientHeight;
    canvas.width=width*dpr;canvas.height=height*dpr;ctx.scale(dpr,dpr);
    let seed=4871;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
    for(let i=0;i<115;i++){
      const x=rand()*width,y=rand()*height,r=rand()*1.2+.25;
      ctx.beginPath();ctx.fillStyle=`rgba(207,238,255,${rand()*.6+.16})`;ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();
    }
    for(let i=0;i<7;i++){
      const x=rand()*width,y=rand()*height;
      ctx.strokeStyle='rgba(152,226,255,.35)';ctx.lineWidth=.8;ctx.beginPath();ctx.moveTo(x-4,y);ctx.lineTo(x+4,y);ctx.moveTo(x,y-4);ctx.lineTo(x,y+4);ctx.stroke();
    }
  }
  function bindNavigation(){
    document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>PX.goto(b.dataset.view)));
    document.querySelectorAll('[data-goto]').forEach(b=>b.addEventListener('click',()=>PX.goto(b.dataset.goto)));
    document.querySelectorAll('[data-demo-start]').forEach(b=>b.addEventListener('click',()=>{
      PX.goto('explorer');PX.explorer.startDemo();
    }));
    document.querySelectorAll('[data-real-start]').forEach(b=>b.addEventListener('click',()=>{
      PX.goto('explorer');PX.explorer.setMode('real');PX.$('searchButton').focus();
    }));
    document.querySelectorAll('[data-nav]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();PX.goto(b.dataset.nav)}));
    PX.$('menuToggle').addEventListener('click',()=>{
      const expanded=PX.$('sidebar').classList.toggle('open');
      PX.$('menuToggle').setAttribute('aria-expanded',String(expanded));
      PX.$('menuToggle').setAttribute('aria-label',expanded?'Cerrar menú':'Abrir menú');
      if(expanded)PX.$('sidebar').querySelector('.nav-item.active')?.focus();
      else PX.$('menuToggle').focus();
    });
    window.addEventListener('hashchange',()=>PX.goto(location.hash.replace('#','')));
    window.addEventListener('keydown',e=>{if(e.key==='Escape'){
      document.querySelector('.modal-backdrop')?.remove();
      if(PX.$('sidebar').classList.contains('open')){
        PX.$('sidebar').classList.remove('open');PX.$('menuToggle').setAttribute('aria-expanded','false');
        PX.$('menuToggle').setAttribute('aria-label','Abrir menú');PX.$('menuToggle').focus();
      }
    }});
  }
  async function init(){
    await PX.i18n.init();
    bindNavigation();skyStars();window.addEventListener('resize',()=>{clearTimeout(PX._resizer);PX._resizer=setTimeout(skyStars,140)});
    try {const health=await PX.get('/api/health');PX.$('apiStatus').textContent=health.status==='ok'?'API DISPONIBLE':'API NO DISPONIBLE';}
    catch(e) {PX.$('apiStatus').textContent='SIN CONEXIÓN';PX.toast(e.message,true);}
    PX.explorer.init();PX.detection.init();PX.academy.init();
    try {
      const sources=await PX.get('/api/sources');
      PX.$('sourcesList').innerHTML=sources.sources.map((s,i)=>`<div class="panel source-card"><span class="source-id">FUENTE ${String(i+1).padStart(2,'0')} · ${i===2?'ESA':'IRSA / NASA'}</span><h3>${PX.escape(s.name)}</h3><p>${PX.escape(s.kind)}</p><a href="${PX.escape(s.url)}" target="_blank" rel="noopener noreferrer">Visitar sitio oficial ↗</a></div>`).join('');
    }catch(e){PX.$('sourcesList').textContent='No se pudieron cargar las fuentes: '+e.message;}
    const route=location.hash.slice(1);PX.goto(route||'overview');
  }
  document.addEventListener('DOMContentLoaded',init);
})();
