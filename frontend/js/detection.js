/* Resultados del análisis local; marcas visuales y revisión humana. */
(function(){
  const PX=window.PX;
  let requestVersion=0;
  async function detect(quiet=false){
    const cmp=PX.state.compare;
    if(!cmp){PX.goto('explorer');PX.$('searchButton').focus();return;}
    const version=++requestVersion;
    const threshold=Number(PX.$('thresholdRange')?.value||5);
    PX.state.detection=null;
    PX.activity.set('detectActivity',{state:'loading',percent:null,
      title:quiet?'Recalculando señales':'Analizando el mapa diferencial',
      detail:`Aplicando el umbral ${threshold.toFixed(2)} σ al residual B − A. El tiempo depende del tamaño de la imagen.`,
      step:'Esperando resultado'});
    render();
    const btn=PX.$('detectBtn');PX.busy(btn,true,'Buscando señales...');
    try{
      const result=await PX.get('/api/detect/'+encodeURIComponent(cmp.session_id)+'?threshold_sigma='+threshold);
      if(version!==requestVersion||PX.state.compare?.session_id!==cmp.session_id)return;
      PX.busy(btn,false);PX.state.detection=result;render();
      PX.activity.set('detectActivity',{state:'done',percent:100,
        title:quiet?'Análisis actualizado':'Análisis completado',
        detail:`${result.count} señales preliminares con el umbral ${threshold.toFixed(2)} σ. Revísalas individualmente; ninguna confirma un planeta.`,
        step:'Resultado calculado'});
      if(!quiet)PX.$('candidateInsight').textContent=`${result.count} señales preliminares sobre el umbral. Selecciona una para verla en el mapa. No son descubrimientos confirmados.`;
    }catch(e){if(version===requestVersion){PX.toast('Análisis no disponible: '+e.message,true);
      PX.activity.set('detectActivity',{state:'error',percent:null,title:'No se completó el análisis',detail:e.message,step:'Reintenta el análisis'});render();}}
    finally{if(version===requestVersion&&btn.classList.contains('busy')){
      PX.busy(btn,false);btn.textContent=PX.state.compare?'Ejecutar análisis ↗':'Ir al explorador ↗';}}
  }
  function invalidate(){
    requestVersion++;PX.activity.reset('detectActivity');PX.busy(PX.$('detectBtn'),false);
  }
  function render(){
    const cmp=PX.state.compare,det=PX.state.detection;
    if(cmp)PX.$('detectionImage').src=cmp.images.difference;else PX.$('detectionImage').removeAttribute('src');
    PX.$('detectionEmpty').style.display=cmp?'none':'flex';
    PX.$('candidateCount').textContent=det?String(det.count).padStart(2,'0'):'00';
    PX.$('detectBtn').textContent=cmp?(det?'Recalcular análisis ↗':'Ejecutar análisis ↗'):'Ir al explorador ↗';
    PX.$('thresholdRange').disabled=!cmp;
    PX.$('candidateInsight').textContent=det?.candidates.length?'Selecciona una señal para ver su ubicación en el mapa. No identifica un objeto.':
      'Selecciona un resultado para revisar su posición en el mapa. No identifica un objeto.';
    PX.$('detectionMarkers').innerHTML='';PX.$('candidateOverlay').innerHTML='';PX.$('exportBtn').disabled=!det||!det.candidates.length;
    PX.explorer.progress();
    if(!det&&PX.$('detectActivity').dataset.state==='loading'){
      PX.$('candidateList').innerHTML='<div class="candidate-pending"><div class="candidate-skeleton" aria-hidden="true"><i></i><i></i><i></i></div><strong>Revisando señales…</strong><p>Los resultados aparecerán al terminar el cálculo. No son detecciones confirmadas.</p></div>';
      return;
    }
    if(!det){PX.$('candidateList').innerHTML=`<div class="candidate-empty"><span>⌕</span><strong>Aún no hay resultados</strong><p>${cmp?'Ejecuta el análisis sobre las épocas seleccionadas.':'Primero busca y compara dos épocas en el explorador.'}</p><button class="btn btn-outline" id="goDetect">${cmp?'Analizar ahora':'Ir al explorador'} ↗</button></div>`;
      PX.$('goDetect').addEventListener('click',()=>detect());return;}
    if(!det.candidates.length){PX.$('candidateList').innerHTML='<div class="candidate-empty"><strong>Sin picos sobre el umbral</strong><p>Este resultado no significa que no existan objetos móviles.</p></div>';return;}
     PX.$('candidateList').innerHTML=det.candidates.map((c,i)=>`<div class="candidate-item" data-candidate="${i}" tabindex="0" role="button" aria-pressed="false"><div class="candidate-rank">${String(i+1).padStart(2,'0')}</div><div class="candidate-item-body"><div class="candidate-top"><strong>${PX.escape(c.id)}</strong><span class="snr">${c.snr}σ</span></div><p>${PX.escape(c.classification)}</p><small>DESPLAZAMIENTO: ${c.shift_px===null?'No asociado':c.shift_px+' px'} · X ${Math.round(c.x*100)}% / Y ${Math.round(c.y*100)}%</small></div></div>`).join('');
    det.candidates.forEach((c,i)=>{
      const dot=document.createElement('div');dot.className='detection-marker';dot.style.left=c.x*100+'%';dot.style.top=c.y*100+'%';dot.innerHTML='<b>'+PX.escape(c.id)+'</b>';dot.dataset.candidate=i;PX.$('detectionMarkers').appendChild(dot);
      const overlay=document.createElement('div');overlay.className='candidate-dot';overlay.style.left=c.x*100+'%';overlay.style.top=c.y*100+'%';overlay.title=c.id+' · '+c.classification;PX.$('candidateOverlay').appendChild(overlay);
    });
    PX.$('candidateList').querySelectorAll('[data-candidate]').forEach(el=>{
      el.addEventListener('click',()=>highlight(Number(el.dataset.candidate)));
      el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();highlight(Number(el.dataset.candidate));}});
    });
  }
  function highlight(index){
    PX.$('candidateList').querySelectorAll('.candidate-item').forEach((el,i)=>{
      el.classList.toggle('active',i===index);el.setAttribute('aria-pressed',String(i===index));
    });
    PX.$('detectionMarkers').querySelectorAll('.detection-marker').forEach((el,i)=>el.style.borderColor=i===index?'#c0ff7b':'#ffbb77');
    const item=PX.state.detection?.candidates[index];
    if(item)PX.$('candidateInsight').textContent=`${item.id}: ${item.classification}. Posición relativa X ${Math.round(item.x*100)}%, Y ${Math.round(item.y*100)}%. ${item.shift_px===null?'Sin desplazamiento asociado.':'Separación aparente: '+item.shift_px+' píxeles.'} Requiere revisión; no es un descubrimiento.`;
  }
  function exportCsv(){
    const d=PX.state.detection,c=PX.state.compare;if(!d||!c||!d.candidates.length)return;
    const columns=['id','classification','snr','x','y','previous_x','previous_y','shift_px','note'];
    const quote=x=>'"'+String(x??'').replace(/"/g,'""')+'"';
    const disclaimer='# Planet X Explorer — señales preliminares, NO descubrimientos confirmados';
    const table=[disclaimer,'# Origen: '+(c.meta.is_demo?'SIMULACIÓN SINTÉTICA':'NASA / IPAC IRSA (FITS reales)'),'# Fechas: '+c.first.date+' / '+c.second.date,columns.join(','),...d.candidates.map(row=>columns.map(key=>quote(row[key])).join(','))].join('\r\n');
    const blob=new Blob(['\uFEFF'+table],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob);
    const a=document.createElement('a');a.href=url;a.download='planetx_candidatos_'+(c.meta.is_demo?'DEMO':'IRSA')+'.csv';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);
  }
  function init(){PX.$('detectBtn').addEventListener('click',()=>detect());PX.$('exportBtn').addEventListener('click',exportCsv);
    PX.$('thresholdRange').addEventListener('change',()=>{if(PX.state.compare)detect(true);});}
  PX.detection={init,detect,render,invalidate};
})();
