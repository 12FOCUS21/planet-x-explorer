"""Comparación real con reproyección WCS o comparación sintética etiquetada."""
from __future__ import annotations
import secrets
import asyncio
import time
from starlette.concurrency import run_in_threadpool
import numpy as np
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from ..state import SEARCHES,SESSIONS
from ..analysis.image_alignment import align_to_reference
from ..analysis.image_difference import difference_image
from ..analysis.validation import validate_pair
from ..services.demo_service import make_demo_pair
from ..services.spherex_service import download_cutout
from ..utils.fits_utils import extract_science_image
from ..utils.render import render_png

router=APIRouter(prefix='/api',tags=['observations'])

class CompareRequest(BaseModel):
    search_id:str
    first_id:str
    second_id:str

async def compare(payload:CompareRequest, progress=None):
    search=SEARCHES.get(payload.search_id)
    if not search: raise HTTPException(404,'La búsqueda expiró. Consulta nuevamente la región.')
    obs=search['observations']
    if payload.first_id not in obs or payload.second_id not in obs:
        raise HTTPException(404,'Observación no encontrada en esta búsqueda')
    aa,bb=obs[payload.first_id],obs[payload.second_id]
    try: validate_pair(aa,bb)
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
    demo=search['mode']=='demo'
    notes=[]
    try:
        if demo:
            ia=int(aa['id'].split('-')[-1]);ib=int(bb['id'].split('-')[-1])
            a,b,meta=make_demo_pair(search['ra'],search['dec'],ia,ib)
            align={'registered':True,'overlap_fraction':1.,'method':'Escena idéntica simulada'}
        else:
            if progress: progress('Descargando dos recortes de IRSA…')
            def transferred(name):
                return lambda done,total: progress(f'Descargando {name}: {done/1048576:.1f} MB' + (f' de {total/1048576:.1f} MB' if total else '')) if progress else None
            (payload_a,srca),(payload_b,srcb)=await asyncio.gather(
                download_cutout(aa,search['ra'],search['dec'],search['radius'],transferred('A')),
                download_cutout(bb,search['ra'],search['dec'],search['radius'],transferred('B')))
            if progress: progress('Leyendo FITS y alineando coordenadas…')
            a,header_a,details_a=await run_in_threadpool(extract_science_image,payload_a)
            raw_b,header_b,details_b=await run_in_threadpool(extract_science_image,payload_b)
            b,align=await run_in_threadpool(align_to_reference,a,header_a,raw_b,header_b)
            meta={'dataset':'SPHEREx DR1 / QR3 / deep', 'instrument':'NASA SPHEREx / IPAC IRSA',
                  'unit':details_a['unit'],'is_demo':False, 'description':'Recortes FITS reales. Validar filtros LVF, flags y varianzas antes de análisis científico.'}
            notes.append('Las diferencias pueden ser causadas por filtros LVF, PSF, calibración o ruido: no prueban movimiento.')
            notes.append(f'FITS A: {srca}; FITS B: {srcb}.')
        if progress: progress('Generando imágenes A, B y diferencia…')
        diff,stats=await run_in_threadpool(difference_image,a,b)
        sid=secrets.token_urlsafe(12)
        shared=np.concatenate((a[np.isfinite(a)],b[np.isfinite(b)]))
        limits=np.percentile(shared,[5,99.6])
        imgs={'a':await run_in_threadpool(render_png,a,'indigo',limits),'b':await run_in_threadpool(render_png,b,'indigo',limits),'difference':await run_in_threadpool(render_png,diff,'difference')}
        SESSIONS[sid]={'a':a,'b':b,'diff':diff,'stats':stats,'meta':meta,'images':imgs,
           'alignment':align,'region':{k:search[k] for k in ('ra','dec','radius')},
           'first':{k:v for k,v in aa.items() if not k.startswith('_')},
           'second':{k:v for k,v in bb.items() if not k.startswith('_')},'notes':notes}
        while len(SESSIONS)>8: SESSIONS.pop(next(iter(SESSIONS)))
        return {'session_id':sid,'first':SESSIONS[sid]['first'], 'second':SESSIONS[sid]['second'],
          'images':{s:f'/api/image/{sid}/{s}' for s in imgs}, 'mode':'demo' if demo else 'real',
          'width':int(a.shape[1]),'height':int(a.shape[0]),'alignment':align,
          'statistics':stats,'meta':meta,'notes':notes}
    except HTTPException: raise
    except TimeoutError as exc:
        raise HTTPException(504,'IRSA agotó el tiempo de espera de 150 segundos. Reintenta; los recortes completos se conservan.') from exc
    except Exception as exc:
        # httpx may include an upstream URL or proxy details in its exception.
        raise HTTPException(502,detail='No se pudo preparar la comparación; revisa el par y reintenta.') from exc


JOBS = {}
TASKS = set()

@router.post('/compare')
async def compare_legacy(payload:CompareRequest):
    return await compare(payload)

async def run_job(job_id,payload):
    job=JOBS[job_id]
    try:
        job['status']='running'
        result=await compare(payload,lambda message:job.update(message=message))
        job.update(status='done',message='Comparación lista',result=result)
    except HTTPException as exc:
        job.update(status='error',message=str(exc.detail),error_code=exc.status_code)
    except Exception as exc:
        job.update(status='error',message=f'No se pudo completar: {type(exc).__name__}. Reintenta la comparación.',error_code=502)

@router.post('/compare/jobs',status_code=202)
async def start_comparison(payload:CompareRequest):
    key=(payload.search_id,payload.first_id,payload.second_id)
    for jid,job in list(JOBS.items()):
        if job['status'] in ('done','error') and time.monotonic()-job['created']>1800:
            JOBS.pop(jid,None)
            continue
        if job['key']==key and job['status']!='error':
            if job['status']!='done' or job['result']['session_id'] in SESSIONS:
                return {'job_id':jid}
    search=SEARCHES.get(payload.search_id)
    if not search: raise HTTPException(404,'La búsqueda expiró. Busca de nuevo.')
    try:
        validate_pair(search['observations'][payload.first_id],search['observations'][payload.second_id])
    except KeyError: raise HTTPException(404,'La observación no pertenece a esta búsqueda.')
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
    if sum(j['status'] in ('queued','running') for j in JOBS.values())>=2:
        raise HTTPException(429,'Hay dos comparaciones en curso. Espera a que finalicen.')
    jid=secrets.token_urlsafe(16)
    JOBS[jid]={'status':'queued','message':'Preparando descarga…','created':time.monotonic(),'key':key}
    while len(JOBS)>40:
        removable=next((k for k,v in JOBS.items() if v['status'] in ('done','error')),None)
        if removable is None: break
        JOBS.pop(removable)
    task=asyncio.create_task(run_job(jid,payload));TASKS.add(task);task.add_done_callback(TASKS.discard)
    return {'job_id':jid}

@router.get('/compare/jobs/{job_id}')
async def comparison_status(job_id:str):
    job=JOBS.get(job_id)
    if job is None: raise HTTPException(404,'El servidor se reinició o el trabajo expiró. Busca y compara de nuevo.')
    return {k:v for k,v in job.items() if k not in ('key','created')}
