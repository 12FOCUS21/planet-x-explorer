/* Visible operation states. No invented timer-based completion percentage. */
(function(){
  const PX=window.PX;
  function card(id){return PX.$(id);}
  function reset(id){
    const el=card(id);el.hidden=true;el.dataset.state='idle';el.dataset.percent='0';
    el.querySelector('.activity-track').removeAttribute('aria-valuenow');
    el.querySelector('.activity-track').removeAttribute('aria-valuetext');
  }
  function set(id,{state='loading',title,detail,percent=null,step,kicker}){
    const el=card(id);el.hidden=false;el.dataset.state=state;
    if(title!==undefined&&el.querySelector('.activity-title').textContent!==title)el.querySelector('.activity-title').textContent=title;
    if(detail!==undefined)el.querySelector('.activity-detail').textContent=detail;
    if(step!==undefined)el.querySelector('.activity-step').textContent=step;
    if(kicker!==undefined)el.querySelector('.activity-kicker').textContent=kicker;
    const meter=el.querySelector('.activity-track'),fill=el.querySelector('.activity-fill');
    if(percent===null){
      meter.removeAttribute('aria-valuenow');meter.setAttribute('aria-valuetext',state==='error'?'No completado':'En curso, sin porcentaje medible');
      el.querySelector('.activity-value').textContent=state==='error'?'NO COMPLETADO':'EN CURSO';
      fill.style.width='0%';el.dataset.percent='0';
    }else{
      const value=Math.max(0,Math.min(100,Math.round(percent)));
      meter.setAttribute('aria-valuenow',String(value));meter.removeAttribute('aria-valuetext');
      fill.style.width=value+'%';el.querySelector('.activity-value').textContent=value+'%';el.dataset.percent=String(value);
    }
  }
  function advance(id,options){
    const previous=Number(card(id).dataset.percent||0);
    set(id,{...options,percent:Math.max(previous,options.percent)});
  }
  PX.activity={reset,set,advance};
})();
