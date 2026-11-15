/* Utilidades de red y acceso a API. Sin tokens ni credenciales en frontend. */
window.PX = {
  state: { mode:'real', search:null, compare:null, detection:null, layer:'blend', presets:[], busy:false },
  async get(url) { return this.request(url); },
  async post(url,payload) { return this.request(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); },
  async request(url,options={}) {
    const controller=new AbortController();
    const timer=setTimeout(()=>controller.abort(),140000);
    let response,data;
    try {
      response=await fetch(url,{...options,signal:controller.signal});
      data=await response.json();
    } catch(e) {
      throw new Error(e.name==='AbortError'?'La consulta tardó demasiado. Reintenta; los recortes completos quedan en caché.':'No se pudo comunicar con el servidor. Comprueba la conexión; si es local, revisa Python.');
    } finally { clearTimeout(timer); }
    if(!response.ok){
      const detail=typeof data.detail==='string'?data.detail:Array.isArray(data.detail)?data.detail.map(x=>x.msg).join('; '):'Error de servidor ('+response.status+').';
      throw new Error(detail);
    }
    return data;
  },
  $(id){return document.getElementById(id)},
  escape(value){return String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));},
  toast(message,isError=false){const el=this.$('toast');el.textContent=message;el.className='toast visible'+(isError?' error':'');clearTimeout(this._toastTimer);this._toastTimer=setTimeout(()=>el.classList.remove('visible'),6500);},
  busy(button,yes,label){if(!button)return;button.disabled=yes;button.classList.toggle('busy',yes);if(!button.dataset.original)button.dataset.original=button.innerHTML;button.innerHTML=yes?(label||'Procesando...'):button.dataset.original;},
  goto(view){
    if(!['overview','explorer','detection','academy','sources'].includes(view))view='overview';
    document.querySelectorAll('.view').forEach(el=>el.classList.toggle('active',el.id==='view-'+view));
    document.querySelectorAll('.nav-item').forEach(el=>{
      const active=el.dataset.view===view;el.classList.toggle('active',active);
      if(active)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current');
    });
    this.$('breadcrumb').textContent=({overview:'Vista general',explorer:'Explorador espacial',detection:'Detector de cambios',academy:'Academia espacial',sources:'Datos y metodología'})[view];
    if(this.$('sidebar').classList.contains('open')){
      this.$('sidebar').classList.remove('open');
      this.$('menuToggle').focus();
    }
    this.$('menuToggle').setAttribute('aria-expanded','false');
    this.$('menuToggle').setAttribute('aria-label','Abrir menú');
    history.replaceState(null,'','#'+view);
    window.scrollTo({top:0,behavior:'smooth'});
    if(view==='detection')this.detection.render();
  }
};
