"""Previsualización de FITS e identificación PRELIMINAR de diferencias."""
from fastapi import APIRouter,HTTPException,Query
from fastapi.responses import Response
from ..state import SESSIONS
from ..analysis.motion_detection import detect_candidates
from ..analysis.candidate_scoring import prioritize
router=APIRouter(prefix='/api',tags=['detection'])

@router.get('/image/{session_id}/{layer}')
def image(session_id:str,layer:str):
    session=SESSIONS.get(session_id)
    if session is None or layer not in ('a','b','difference'):
        raise HTTPException(404,'Imagen no encontrada o sesión finalizada')
    return Response(session['images'][layer],media_type='image/png',headers={'Cache-Control':'private, max-age=1800'})

@router.get('/detect/{session_id}')
def detect(session_id:str,threshold_sigma:float=Query(5.0,ge=2.0,le=10.0)):
    session=SESSIONS.get(session_id)
    if not session:raise HTTPException(404,'Primero prepara la comparación')
    cache_key=f'{threshold_sigma:.2f}'
    session.setdefault('candidates_by_sigma',{})
    if cache_key not in session['candidates_by_sigma']:
        items=prioritize(detect_candidates(session['diff'],session['stats']['rms_robust'],threshold_sigma=threshold_sigma))
        # Flip y to match the rendered PNG (FITS row 0 is displayed at the bottom).
        for item in items:
            item['y']=round(1-item['y'],5)
            if item['previous_y'] is not None: item['previous_y']=round(1-item['previous_y'],5)
        session['candidates_by_sigma'][cache_key]=items
    candidates=session['candidates_by_sigma'][cache_key]
    return {'session_id':session_id,'mode':'demo' if session['meta']['is_demo'] else 'real',
            'threshold_sigma':threshold_sigma,'count':len(candidates),'candidates':candidates,
            'method':f'deteccion de picos residuales con umbral {threshold_sigma:.2f} sigma',
            'disclaimer':'No se puede confirmar Planeta X con esta detección. Se requiere análisis multibanda, catálogo, validación y ajuste orbital.'}
