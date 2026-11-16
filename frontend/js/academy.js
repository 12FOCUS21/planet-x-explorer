/* Academia: lecciones correctas y cuestionario con retroalimentación y progreso local. */
(function(){
 const PX=window.PX;
 let lessons=[],questions=[],current=0,score=0,selected=null,answered=false;
 let completed=[];
 try{completed=JSON.parse(localStorage.getItem('px-learned')||'[]');if(!Array.isArray(completed))completed=[];}catch(e){completed=[];}
 function progress(){PX.$('progressNum').textContent=completed.length+'/'+lessons.length;PX.$('progressFill').style.width=(lessons.length?(completed.length/lessons.length*100):0)+'%';}
 function renderLessons(){
   PX.$('lessons').innerHTML=lessons.map((l,i)=>`<div class="lesson-card ${completed.includes(l.id)?'completed':''}"><div class="lesson-card-top"><span>LECCIÓN ${PX.escape(l.id)}</span><span>${PX.escape(l.length)}</span></div><div class="lesson-card-icon">${['◎','✺','⌁'][i%3]}</div><h3>${PX.escape(l.title)}</h3><p>${PX.escape(l.tag)} · ${PX.escape(PX.t(l.text).slice(0,105))}...</p><button data-lesson="${i}">${completed.includes(l.id)?'Revisar lección':'Comenzar lección'} →</button></div>`).join('');
   PX.$('lessons').querySelectorAll('[data-lesson]').forEach(b=>b.addEventListener('click',()=>openLesson(Number(b.dataset.lesson))));progress();
 }
  function openLesson(i){
    const l=lessons[i];if(!l)return;
    const trigger=document.activeElement;
    const modal=document.createElement('div');modal.className='modal-backdrop';modal.innerHTML=`<div class="lesson-modal" role="dialog" aria-modal="true" aria-labelledby="lessonTitle"><button class="modal-close" aria-label="Cerrar lección">×</button><span class="panel-overline">LECCIÓN ${PX.escape(l.id)} / ${PX.escape(l.tag)}</span><h2 id="lessonTitle">${PX.escape(l.title)}</h2><p>${PX.escape(l.text)}</p><div class="lesson-fact">✦ &nbsp; ${PX.escape(l.fact)}</div><button class="btn btn-primary" id="finishLesson">Marcar como completada ✓</button></div>`;
    const close=()=>{modal.remove();if(trigger?.isConnected)trigger.focus();};
    document.body.appendChild(modal);modal.querySelector('.modal-close').addEventListener('click',close);
    modal.addEventListener('click',e=>{if(e.target===modal)close();});
    modal.addEventListener('keydown',e=>{
      if(e.key==='Escape'){e.preventDefault();e.stopPropagation();close();}
      if(e.key==='Tab'){
        const first=modal.querySelector('.modal-close'),last=modal.querySelector('#finishLesson');
        if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
        else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
      }
    });
    modal.querySelector('#finishLesson').addEventListener('click',()=>{
      if(!completed.includes(l.id))completed.push(l.id);
      try{localStorage.setItem('px-learned',JSON.stringify(completed));}catch(e){}
      modal.remove();renderLessons();PX.$('lessons').querySelector(`[data-lesson="${i}"]`)?.focus();
      PX.toast('Lección completada. ¡Sigue explorando!');
   });modal.querySelector('.modal-close').focus();
 }
 function questionScreen(){
   const q=questions[current];if(!q)return;
   PX.$('quizBadge').textContent=`${current+1} / ${questions.length}`;
   PX.$('quizRoot').innerHTML=`<div class="quiz-progress">PREGUNTA ${current+1} DE ${questions.length}</div><h3 style="font-size:17px;line-height:1.5;margin:12px 0 0">${PX.escape(q.question)}</h3><div class="quiz-options">${q.answers.map((a,i)=>`<button class="quiz-option" data-choice="${i}">${String.fromCharCode(65+i)}. ${PX.escape(a)}</button>`).join('')}</div><div id="feedback"></div><button id="quizNext" class="btn btn-primary" disabled>${current===questions.length-1?'Finalizar evaluación':'Siguiente →'}</button>`;
   selected=null;answered=false;
   PX.$('quizRoot').querySelectorAll('[data-choice]').forEach(b=>b.addEventListener('click',()=>{
     if(answered)return;answered=true;selected=Number(b.dataset.choice);if(selected===q.correct)score++;
     PX.$('quizRoot').querySelectorAll('[data-choice]').forEach((option,i)=>{
       option.disabled=true;option.classList.toggle('selected',i===selected);option.style.borderColor=i===q.correct?'#baff7b':i===selected?'#ff9f8f':'';
     });
     PX.$('feedback').innerHTML=`<div class="quiz-feedback">${selected===q.correct?'✓ Respuesta correcta.':'→ Revisemos la respuesta.'} ${PX.escape(q.explanation)}</div>`;
     PX.$('quizNext').disabled=false;
   }));
   PX.$('quizNext').addEventListener('click',()=>{current++;if(current>=questions.length)finishQuiz();else questionScreen();});
 }
 function finishQuiz(){
   PX.$('quizBadge').textContent='MISIÓN FINALIZADA';
   const perfect=score>=4;
   PX.$('quizRoot').innerHTML=`<div style="font-size:42px;color:var(--mint)">${perfect?'✳':'◎'}</div><h3>${perfect?'¡Insignia de investigador desbloqueada!':'Misión de práctica completada'}</h3><p>Respuestas correctas: <strong style="color:var(--mint)">${score}/${questions.length}</strong>. ${perfect?'Ya conoces las bases para analizar señales sin sacar conclusiones precipitadas.':'Repasa las lecciones y vuelve a intentarlo. El método es tan importante como la respuesta.'}</p><button class="btn btn-primary" id="quizAgain">Repetir misión ↗</button>`;
   PX.$('quizAgain').addEventListener('click',startQuiz);
 }
 function startQuiz(){if(!questions.length){PX.toast('No hay preguntas disponibles.',true);return;}current=0;score=0;questionScreen();}
 async function init(){
   document.addEventListener('px:languagechange',()=>{if(lessons.length)renderLessons();});
   PX.$('quizStart').addEventListener('click',startQuiz);
   try{const data=await PX.get('/api/academy');lessons=data.lessons;questions=data.questions;renderLessons();}
   catch(e){PX.$('lessons').textContent='No se pudieron cargar lecciones: '+e.message;}
 }
 PX.academy={init};
})();
