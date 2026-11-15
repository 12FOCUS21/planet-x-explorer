/* Búsqueda, comparación visual y session de FITS/demostración. */
(function(){
  const PX=window.PX;
  let revision=0, searching=false, comparing=false;
  const message=text=>{PX.$('compareStatus').textContent=text;};
  function progress(){
    const {search,compare,detection}=PX.state;
    const hasObservations=search?.count>0;
    const step=detection?4:compare?3:hasObservations?2:1;
    document.querySelectorAll('.journey-step').forEach(el=>{
      const number=Number(el.dataset.step);
      el.classList.toggle('is-current',number===step);
      el.classList.toggle('is-done',number<step);
      if(number===step)el.setAttribute('aria-current','step');else el.removeAttribute('aria-current');
    });
    PX.$('journeyStatus').textContent=step===4?'Recorrido completado · Revisa cada señal; ninguna confirma un planeta.':
      step===3?'Paso 3 de 3 · Compara el mapa B − A y analiza las señales.':
      step===2?(search.suggested_pair?'Paso 2 de 3 · Elige dos épocas y pulsa Comparar.':'Paso 2 de 3 · No hay un par por metadatos; prueba otras coordenadas.'):
      'Paso 1 de 3 · Elige una fuente y busca un campo.';
    PX.$('runDetectionTop').disabled=!compare;
    const panel=PX.$('searchSummary');panel.hidden=!search;
    if(!search)return;
    PX.$('summaryCount').textContent=String(search.count);
    PX.$('summaryType').textContent=search.mode==='demo'?'ÉPOCAS SIMULADAS':'REGISTROS IRSA';
    PX.$('summaryTitle').textContent=compare?'Comparación preparada':search.count?'Búsqueda completada':'Sin imágenes para este centro';
    const pairs=Object.values(search.compatible_pairs||{}).reduce((total,ids)=>total+ids.length,0);
    PX.$('summaryDescription').textContent=compare?
      `${compare.meta.is_demo?'Simulación didáctica':'Recortes FITS de IRSA'}: imágenes A, B y residual listos. Los cambios aún necesitan revisión.`:
      search.count?`${pairs} pares ordenados A→B pasan los filtros de metadatos. ${search.mode==='demo'?'Todo el contenido es sintético.':'La respuesta LVF por píxel no está validada.'} ${search.warnings.join(' ')}`:
      'No se generarán imágenes ficticias como sustituto. Prueba otras coordenadas.';
    PX.$('summaryNext').disabled=!(compare||search.suggested_pair);
    PX.$('summaryNext').innerHTML=compare?'Ir al análisis <span aria-hidden="true">↗</span>':
      search.suggested_pair?'Elegir épocas <span aria-hidden="true">↗</span>':'Sin par disponible';
  }
  function clearComparison(){
    PX.state.compare=null;PX.state.detection=null;
    PX.activity.reset('compareActivity');PX.detection.invalidate();
    PX.$('comparisonPlaceholder').removeAttribute('data-working');
    PX.$('placeholderTitle').textContent='Compara dos épocas para revelar las imágenes.';
    PX.$('comparisonPlaceholder').hidden=false;PX.$('scienceFigure').hidden=true;PX.$('explorerDetails').hidden=true;
    for(const id of ['imageA','imageB','imageDiff']){PX.$(id).hidden=true;PX.$(id).removeAttribute('src');}
    for(const id of ['sourceEmptyA','sourceEmptyB','emptyStage'])PX.$(id).style.display='flex';
    for(const id of ['sourceDateA','sourceDateB','compareDateA','compareDateB','fieldDetector','fieldOverlap','fieldPixels','sourceDetectorA','sourceDetectorB','sourceBandA','sourceBandB'])PX.$(id).textContent='—';
    PX.$('homePreview').src='/static/assets/sky-preview.svg';
    PX.$('homeImageBadge').textContent='VISTA ILUSTRATIVA';PX.$('homeImageBadge').classList.remove('real');
    PX.$('homeSkyLabel').textContent='VISTA ARTÍSTICA · SIN DATOS CIENTÍFICOS';
    PX.$('fieldSource').textContent='Aún sin comparar';
    PX.$('runDetectionTop').disabled=true;
    PX.$('candidateOverlay').innerHTML='';PX.detection.render();progress();
  }
  function updatePair(){
    const data=PX.state.search;if(!data)return;
    const allowed=data.compatible_pairs?.[PX.$('obsA').value]||[];
    for(const option of PX.$('obsB').options)option.disabled=!allowed.includes(option.value);
    if(!allowed.includes(PX.$('obsB').value))PX.$('obsB').value=allowed[allowed.length-1]||'';
    PX.$('compareBtn').disabled=!allowed.length||comparing;
    if(!allowed.length)message('No hay otro registro compatible con A. Elige otra observación, región o consulta más tarde. No se generarán datos ficticios.');
    else message('Par compatible por metadatos. La equivalencia espectral por píxel aún requiere revisión.');
    progress();
  }
  async function waitForJob(jobId,token){
    const until=Date.now()+240000;let failures=0;
    while(Date.now()<until){
      if(token!==revision)throw new Error('La selección cambió. Vuelve a comparar.');
      let job;
      try{job=await PX.get('/api/compare/jobs/'+encodeURIComponent(jobId));failures=0;}
      catch(e){if(++failures>=3)throw e;
        PX.activity.advance('compareActivity',{percent:20,title:'Reintentando conexión con el trabajo',detail:`Intento ${failures} de 3. El trabajo de comparación puede seguir activo.`,step:'Conexión en revisión'});
        await new Promise(r=>setTimeout(r,1500));continue;}
      message(job.message);
      if(job.status==='error')throw new Error(job.message);
      if(job.status==='done'){
        PX.activity.advance('compareActivity',{percent:80,title:'Imágenes generadas',detail:'El servidor terminó; comprobando que las tres imágenes se puedan abrir.',step:'4 de 5 hitos'});
        return job.result;
      }
      const stage=job.message.includes('Generando imágenes')?
        {percent:60,title:'Construyendo la vista diferencial',step:'3 de 5 hitos'}:
        job.message.includes('Leyendo FITS')?
        {percent:40,title:'Alineando observaciones FITS',step:'2 de 5 hitos'}:
        {percent:20,title:job.message.includes('Descargando')?'Obteniendo recortes A y B':'Preparando el par seleccionado',step:'1 de 5 hitos'};
      PX.activity.advance('compareActivity',{...stage,detail:job.message});
      await new Promise(r=>setTimeout(r,900));
    }
    throw new Error('Se agotó la espera. Puedes reintentar: se reutilizará el trabajo o la caché disponible.');
  }
  async function preloadImages(images,onLoaded){
    let loaded=0;
    await Promise.all(Object.values(images).map(url=>new Promise((resolve,reject)=>{
      const img=new Image();const timer=setTimeout(()=>reject(new Error('No se pudo cargar una imagen. Reintenta la comparación.')),30000);
      img.onload=()=>{clearTimeout(timer);onLoaded?.(++loaded);resolve();};
      img.onerror=()=>{clearTimeout(timer);reject(new Error('La imagen expiró o el servidor se reinició. Busca y compara otra vez.'));};
      img.src=url;
    })));
  }
  function showObservationMessage(message){
    for(const id of ['obsA','obsB'])PX.$(id).innerHTML=`<option value="" selected disabled>${PX.escape(message)}</option>`;
    PX.$('compareBtn').disabled=true;
  }
  function fieldChanged(){
    if(!PX.state.search&&!PX.state.compare&&!searching)return;
    revision++;searching=false;PX.state.search=null;
    PX.busy(PX.$('searchButton'),false);clearComparison();
    PX.activity.reset('searchActivity');
    showObservationMessage('Campo modificado: vuelve a pulsar Buscar observaciones.');
    message('Las observaciones anteriores pertenecían al campo previo. Busca otra vez.');
    PX.$('searchInfo').textContent='Coordenadas modificadas. Pulsa Buscar para actualizar las observaciones; los resultados anteriores se han ocultado.';
    PX.$('globalModeTag').textContent=PX.state.mode==='demo'?'DEMO · SINTÉTICA':'IRSA · sin consultar';
    PX.$('homeSkyCoord').textContent='Explora el cielo en el explorador';
    PX.$('homeSkySource').textContent='Ilustración de bienvenida; las imágenes aparecen al comparar dos épocas.';
  }
  function selectOptions(){
    const {search}=PX.state;if(!search)return;
    const items=search.observations;
    if(!items.length){showObservationMessage('No hay imágenes que cubran el centro. Prueba otras coordenadas.');return;}
    for(const id of ['obsA','obsB']){
      PX.$(id).innerHTML=items.map((obs,i)=>`<option value="${PX.escape(obs.id)}">${PX.escape(obs.label)} — ${PX.escape(obs.date)}</option>`).join('');
    }
    if(search.suggested_pair){PX.$('obsA').value=search.suggested_pair[0];PX.$('obsB').value=search.suggested_pair[1];}
    updatePair();
  }
  function modeSwitch(mode){
    revision++;searching=false;PX.busy(PX.$('searchButton'),false);clearComparison();message('Busca observaciones para empezar.');
    PX.activity.reset('searchActivity');
    PX.state.mode=mode;PX.state.search=null;PX.state.compare=null;PX.state.detection=null;
    PX.$('homePreview').src='/static/assets/sky-preview.svg';
    PX.$('homeImageBadge').textContent='VISTA ILUSTRATIVA';
    PX.$('homeImageBadge').classList.remove('real');
    PX.$('sourceDateA').textContent='Sin cargar';PX.$('sourceDateB').textContent='Sin cargar';
    PX.$('sourceDetectorA').textContent='—';PX.$('sourceDetectorB').textContent='—';
    PX.$('sourceBandA').textContent='—';PX.$('sourceBandB').textContent='—';
    PX.$('compareDateA').textContent='—';PX.$('compareDateB').textContent='—';
    PX.$('fieldDetector').textContent='—';PX.$('fieldOverlap').textContent='—';PX.$('fieldPixels').textContent='—';
    PX.$('homeSkyLabel').textContent='VISTA ARTÍSTICA · SIN DATOS CIENTÍFICOS';
    PX.$('homeSkyCoord').textContent='Explora el cielo en el explorador';
    PX.$('homeSkySource').textContent='Ilustración de bienvenida; las imágenes reales aparecen al comparar dos épocas.';
    for(const id of ['imageA','imageB','imageDiff']){PX.$(id).hidden=true;PX.$(id).removeAttribute('src');}
    PX.$('sourceEmptyA').style.display='flex';PX.$('sourceEmptyB').style.display='flex';PX.$('emptyStage').style.display='flex';PX.$('candidateOverlay').innerHTML='';PX.detection.render();
    PX.$('modeDemo').classList.toggle('active',mode==='demo');
    PX.$('modeReal').classList.toggle('active',mode==='real');
    PX.$('modeReal').classList.toggle('real',mode==='real');
    PX.$('modeDemo').setAttribute('aria-pressed',String(mode==='demo'));
    PX.$('modeReal').setAttribute('aria-pressed',String(mode==='real'));
    PX.$('globalModeTag').textContent=mode==='demo'?'DEMO · SINTÉTICA':'IRSA · sin consultar';
    PX.$('globalModeTag').classList.toggle('real',mode==='real');
    PX.$('searchInfo').textContent=mode==='demo'?'● Modo demo: todos los píxeles son simulados, no observados.':'● NASA / IRSA: consulta remota de imágenes reales; requiere Internet y puede tardar.';
    PX.$('modeExplainer').textContent=mode==='demo'?'Cuatro épocas generadas localmente y etiquetadas como simulación. Ideal para recorrer la aplicación sin Internet.':
      'IRSA consulta observaciones reales al pulsar Buscar. Requiere Internet; no se reemplazarán resultados vacíos por imágenes simuladas.';
    PX.$('placeholderDetail').textContent=mode==='demo'?'Primero busca las cuatro épocas sintéticas y elige dos para ver A, B y el mapa B − A. No son datos de NASA.':
      'Primero busca metadatos IRSA. Los recortes FITS solo se solicitan cuando eliges dos épocas y pulsas Comparar.';
    PX.$('imageBadge').textContent='SIN IMÁGENES';
    PX.$('imageBadge').classList.remove('real');
    showObservationMessage('Pulsa Buscar observaciones para cargar épocas.');
    PX.$('presets').querySelectorAll('.preset').forEach(b=>b.classList.remove('active'));
    PX.$('presets').firstChild?.classList.add('active');
    progress();
  }
  async function search(autoCompare=false){
    if(searching||comparing)return;searching=true;const token=++revision;clearComparison();
    const mode=PX.state.mode;
    const btn=PX.$('searchButton');PX.busy(btn,true,'Buscando...');
    PX.activity.set('searchActivity',{state:'loading',percent:null,
      kicker:mode==='demo'?'BÚSQUEDA · DEMO SINTÉTICA':'BÚSQUEDA · NASA / IRSA',
      title:mode==='demo'?'Preparando épocas simuladas':'Consultando metadatos IRSA',
      detail:mode==='demo'?'Generando datos didácticos locales; no se consulta IRSA.':'Buscando imágenes que cubran el centro indicado. La duración depende del archivo remoto.',
      step:'Esperando respuesta'});
    PX.state.search=null;progress();
    showObservationMessage(PX.state.mode==='real'?'Consultando NASA / IRSA...':'Cargando épocas de demostración...');
    PX.$('searchInfo').textContent=PX.state.mode==='real'?'Consultando el archivo NASA / IRSA. Puede tardar unos segundos.':'Preparando observaciones sintéticas de demostración.';
    const params=new URLSearchParams({mode:PX.state.mode,ra:PX.$('ra').value,dec:PX.$('dec').value,radius:PX.$('radius').value});
    try{
      const data=await PX.get('/api/observations?'+params);
      if(token!==revision)return;PX.state.search=data;selectOptions();progress();
      PX.activity.set('searchActivity',{state:'done',percent:100,
        title:data.count?'Búsqueda completada':'Búsqueda completada sin resultados',
        detail:`${data.count} ${data.mode==='demo'?'épocas sintéticas':'registros IRSA'} encontrados. ${data.count?'Selecciona un par para continuar.':'Prueba otras coordenadas; no se crearán imágenes ficticias.'}`,
        step:'Respuesta recibida'});
      PX.$('globalModeTag').textContent=data.mode==='demo'?'DEMO · SINTÉTICA':'IRSA · CONSULTADO';
      PX.$('searchInfo').textContent=`${data.count} observaciones ${data.mode==='demo'?'SIMULADAS':'REALES'} disponibles. ${data.note} ${data.warnings.join(' ')}`;
      if(data.count===0)PX.toast(data.mode==='real'?'IRSA no encontró imágenes que cubran el centro. Prueba otras coordenadas.':'No hay observaciones simuladas.',true);
      if(autoCompare && data.count>=2)await compare(true);
    }catch(e){if(token===revision){showObservationMessage('Sin épocas: revisa el mensaje de búsqueda.');PX.toast(e.message,true);PX.$('searchInfo').textContent=e.message;
      PX.activity.set('searchActivity',{state:'error',percent:null,title:'No se completó la búsqueda',detail:e.message,step:'Corrige el problema y pulsa Buscar de nuevo'});progress();}}
    finally{if(token===revision){searching=false;PX.busy(btn,false);}}
  }
  async function compare(quiet=false){
    if(comparing||searching)return;
    const data=PX.state.search;
    if(!data){PX.toast('Primero busca observaciones.',true);return;}
    const first_id=PX.$('obsA').value,second_id=PX.$('obsB').value;
    if(first_id===second_id){PX.toast('Elige dos épocas diferentes.',true);return;}
    if(!(data.compatible_pairs?.[first_id]||[]).includes(second_id)){updatePair();return;}
    comparing=true;const token=revision;clearComparison();
    PX.$('comparisonPlaceholder').dataset.working='true';
    PX.$('placeholderTitle').textContent='Preparando las tres imágenes…';
    PX.$('placeholderDetail').textContent='A, B y B − A aparecerán juntos cuando terminen el procesamiento y la carga de imágenes.';
    PX.activity.set('compareActivity',{state:'loading',percent:0,
      kicker:data.mode==='demo'?'COMPARACIÓN · SIMULACIÓN':'COMPARACIÓN · FITS DE IRSA',
      title:'Solicitando la comparación',detail:'Verificando el par A/B y preparando el trabajo en el servidor.',step:'0 de 5 hitos'});
    const locked=['obsA','obsB','searchButton','modeReal','modeDemo','ra','dec','radius'];
    locked.forEach(id=>PX.$(id).disabled=true);
    PX.$('presets').querySelectorAll('.preset').forEach(button=>button.disabled=true);
    const btn=PX.$('compareBtn');PX.busy(btn,true,'Procesando FITS...');message('Solicitando comparación…');
    try{
      const job=await PX.post('/api/compare/jobs',{search_id:data.search_id,first_id,second_id});
      if(token!==revision)return;
      PX.activity.advance('compareActivity',{percent:20,title:'Par aceptado',detail:'Trabajo iniciado; preparando datos de ambas épocas.',step:'1 de 5 hitos'});
      const cmp=await waitForJob(job.job_id,token);
      message('Cargando las tres imágenes…');await preloadImages(cmp.images,loaded=>{
        if(token===revision&&PX.$('compareActivity').dataset.state==='loading')
          PX.activity.advance('compareActivity',{percent:80,title:'Comprobando imágenes A, B y diferencia',detail:`${loaded} de 3 imágenes cargadas y verificadas.`,step:'4 de 5 hitos'});
      });
      if(token!==revision)return;
      PX.state.compare=cmp;PX.state.detection=null;
      PX.$('comparisonPlaceholder').hidden=true;PX.$('scienceFigure').hidden=false;PX.$('explorerDetails').hidden=false;
      document.querySelectorAll('.plot-data').forEach(el=>el.style.aspectRatio=cmp.width+'/'+cmp.height);
      message('Comparación lista. '+cmp.notes.join(' '));
      PX.$('imageA').src=cmp.images.a;PX.$('imageB').src=cmp.images.b;
      PX.$('imageDiff').src=cmp.images.difference;
      PX.$('homePreview').src=cmp.images.b;
      PX.$('homeImageBadge').textContent=cmp.meta.is_demo?'SIMULACIÓN':'NASA / IRSA · FITS';
      PX.$('homeImageBadge').classList.toggle('real',!cmp.meta.is_demo);
      PX.$('homeSkyCoord').textContent=`RA ${Number(PX.$('ra').value).toFixed(5)}° / Dec ${Number(PX.$('dec').value).toFixed(5)}°`;
      PX.$('homeSkyLabel').textContent=cmp.meta.is_demo?'ESCENA SINTÉTICA · DEMO':'RECORTE REAL SPHEREx · IRSA';
      PX.$('homeSkySource').textContent=cmp.meta.is_demo?'Escena generada localmente; no son datos NASA.':'Recorte FITS SPHEREx servido por NASA/IPAC IRSA.';
      for(const id of ['imageA','imageB'])PX.$(id).hidden=false;
      PX.$('sourceEmptyA').style.display='none';PX.$('sourceEmptyB').style.display='none';
      PX.$('sourceDateA').textContent=cmp.first.date;PX.$('sourceDateB').textContent=cmp.second.date;
      PX.$('sourceDetectorA').textContent=cmp.first.detector;PX.$('sourceDetectorB').textContent=cmp.second.detector;
      PX.$('sourceBandA').textContent=cmp.first.band;PX.$('sourceBandB').textContent=cmp.second.band;
      PX.$('compareDateA').textContent=cmp.first.date;PX.$('compareDateB').textContent=cmp.second.date;
      PX.$('imageDiff').hidden=false;PX.$('emptyStage').style.display='none';
      PX.$('fieldSource').textContent=cmp.meta.is_demo?'Simulación (no NASA)':'NASA / IPAC IRSA';
      PX.$('fieldDetector').textContent=cmp.first.detector+' / '+cmp.second.detector;
      PX.$('fieldOverlap').textContent=Math.round(cmp.alignment.overlap_fraction*100)+'%';
      PX.$('fieldPixels').textContent=Math.round(cmp.statistics.valid_fraction*100)+'%';
      PX.$('imageBadge').textContent=cmp.meta.is_demo?'SIMULACIÓN':'FITS · IRSA';
      PX.$('imageBadge').classList.toggle('real',!cmp.meta.is_demo);
      PX.$('candidateOverlay').innerHTML='';
      PX.detection.render();
      progress();
      PX.activity.set('compareActivity',{state:'done',percent:100,title:'Tres imágenes listas',
        detail:cmp.meta.is_demo?'Simulación A, B y B − A disponibles; no son observaciones NASA.':'Recortes A, B y B − A disponibles. Revisa los límites LVF y los artefactos.',step:'5 de 5 hitos'});
    }catch(e){if(token===revision){message(e.message);PX.toast(e.message,true);
      PX.activity.set('compareActivity',{state:'error',percent:null,title:'No se completó la comparación',detail:e.message,step:'Reintenta con este par u otra región'});progress();}}
    finally{comparing=false;PX.$('comparisonPlaceholder').removeAttribute('data-working');locked.forEach(id=>PX.$(id).disabled=false);
      if(!PX.state.compare){
        PX.$('placeholderTitle').textContent='Compara dos épocas para revelar las imágenes.';
        PX.$('placeholderDetail').textContent=PX.state.mode==='demo'?'Elige dos épocas sintéticas y vuelve a pulsar Comparar. No son datos NASA.':
          'Elige dos registros IRSA compatibles y vuelve a pulsar Comparar para solicitar los recortes FITS.';
      }
      PX.$('presets').querySelectorAll('.preset').forEach(button=>button.disabled=false);
      PX.busy(btn,false);PX.$('compareBtn').disabled=PX.state.search!==data||!(data.compatible_pairs?.[PX.$('obsA').value]||[]).length;}
  }
  function fieldButton(preset,i){
    const b=document.createElement('button');b.className='preset'+(i===0?' active':'');b.textContent=preset.name;b.type='button';
    b.title=preset.subtitle;b.addEventListener('click',()=>{
      if(comparing)return;
      PX.$('ra').value=preset.ra;PX.$('dec').value=preset.dec;PX.$('radius').value=preset.radius;
      PX.$('presets').querySelectorAll('.preset').forEach(x=>x.classList.remove('active'));b.classList.add('active');
      fieldChanged();
    });return b;
  }
  async function init(){
    showObservationMessage('Pulsa Buscar observaciones para cargar épocas.');progress();
    PX.$('searchForm').addEventListener('submit',e=>{e.preventDefault();search();});
    for(const id of ['ra','dec','radius'])PX.$(id).addEventListener('input',()=>{
      PX.$('presets').querySelectorAll('.preset').forEach(b=>b.classList.remove('active'));
      fieldChanged();
    });
    PX.$('modeDemo').addEventListener('click',()=>modeSwitch('demo'));
    PX.$('modeReal').addEventListener('click',()=>modeSwitch('real'));
    PX.$('compareBtn').addEventListener('click',()=>compare());
    PX.$('summaryNext').addEventListener('click',()=>{
      if(PX.state.compare){PX.goto('detection');PX.detection.detect();}
      else if(PX.state.search?.suggested_pair){PX.$('comparisonStep').scrollIntoView({behavior:'smooth',block:'start'});PX.$('obsA').focus({preventScroll:true});}
    });
    PX.$('obsA').addEventListener('change',()=>{clearComparison();updatePair();});
    PX.$('obsB').addEventListener('change',()=>{clearComparison();updatePair();});
    PX.$('thresholdRange').addEventListener('input',e=>PX.$('thresholdValue').textContent=Number(e.target.value).toFixed(2)+' \u03c3');
    PX.$('runDetectionTop').addEventListener('click',async()=>{PX.goto('detection');await PX.detection.detect();});
    PX.$('gaiaBtn').addEventListener('click',async()=>{
      const btn=PX.$('gaiaBtn');PX.busy(btn,true,'Consultando ESA...');
      try{const ra=Number(PX.$('ra').value),dec=Number(PX.$('dec').value),radius=Math.min(.025,Number(PX.$('radius').value));
        const result=await PX.get('/api/gaia?'+new URLSearchParams({ra,dec,radius}));
        PX.$('gaiaInfo').textContent=`${result.count} estrellas Gaia DR3 obtenidas en un radio de ${radius}°. Referencia ESA: NO es una clasificación de candidatos.`;
        PX.toast(`${result.count} fuentes Gaia DR3 consultadas.`);
      }catch(e){PX.$('gaiaInfo').textContent='Gaia no disponible: '+e.message;PX.toast(e.message,true);}finally{PX.busy(btn,false);}
    });
    // Never contact IRSA merely because the page loaded. Search is user initiated.
    try{const data=await PX.get('/api/presets');PX.state.presets=data.presets;data.presets.forEach((p,i)=>PX.$('presets').appendChild(fieldButton(p,i)));}
    catch(e){PX.toast('No se pudo preparar el explorador: '+e.message,true);}
  }
  PX.explorer={init,compare,search,progress,setMode:modeSwitch,
    async startDemo(){modeSwitch('demo');await search();}};
})();
