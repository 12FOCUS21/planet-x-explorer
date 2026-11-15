"""Descubrimiento de regiones y observaciones reales/simuladas."""
from __future__ import annotations
import secrets
from ..analysis.validation import validate_pair
from fastapi import APIRouter,HTTPException,Query
from ..models.observation import Region
from ..services import demo_service,spherex_service
from ..state import SEARCHES

router=APIRouter(prefix='/api',tags=['explorer'])

@router.get('/presets')
def presets():
    return {'presets':demo_service.PRESETS}

@router.get('/observations')
async def observations(mode:str='demo',ra:float=Query(127.69444,ge=0,lt=360),
                       dec:float=Query(-39.1776,ge=-90,le=90),
                       radius:float=Query(.08,ge=.008,le=.3)):
    if mode not in ('demo','real'): raise HTTPException(status_code=422,detail='Modo no válido')
    r=Region(ra=ra,dec=dec,radius=radius)
    if mode=='demo':
        items=demo_service.observations(r.ra,r.dec);warnings=[]
    else:
        items,warnings=await spherex_service.search(r.ra,r.dec,r.radius)
        if not items and warnings:
            detail='IRSA no esta disponible: '+'; '.join(warnings)+'. Comprueba la conexion a Internet y vuelve a buscar.'
            raise HTTPException(status_code=503,detail=detail)
    key=secrets.token_urlsafe(11)
    SEARCHES[key]={'mode':mode,'ra':r.ra,'dec':r.dec,'radius':r.radius,
                  'observations':{o['id']:o for o in items}}
    while len(SEARCHES)>30: SEARCHES.pop(next(iter(SEARCHES)))
    clean=[{k:v for k,v in o.items() if not k.startswith('_')} for o in items]
    pairs = {}
    for a in items:
        pairs[a['id']] = []
        for b in items:
            try: validate_pair(a,b)
            except ValueError: continue
            pairs[a['id']].append(b['id'])
    suggested = next(([a,bs[-1]] for a,bs in pairs.items() if bs), None)
    return {'search_id':key,'mode':mode,'count':len(clean), 'observations':clean,
             'compatible_pairs':pairs,'suggested_pair':suggested,'warnings':warnings,'note':'Datos SIMULADOS, no NASA.' if mode=='demo'
                else 'Metadatos reales IRSA; los pares cumplen filtros de metadatos, no equivalencia LVF por píxel.'}
