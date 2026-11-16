"""Planet X Explorer: API local y aplicación web, con separación inequívoca demo/IRSA."""
from __future__ import annotations
import sys
from pathlib import Path
# Permite ejecutar desde la carpeta del proyecto sin instalar el paquete.
from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import FileResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from .config import FRONTEND
from .api import routes_explorer,routes_observations,routes_detection,routes_education
from .services.catalog_service import SOURCES
from .services.gaia_service import gaia_catalog
from .security import PublicSettings,apply_security
from .localization import LanguageMiddleware

public=PublicSettings.from_env()
app=FastAPI(title='Planet X Explorer',description='Exploración SPHEREx, detección preliminar y academia científica',version='1.0.0',
            docs_url=None if public.enabled else '/docs',redoc_url=None if public.enabled else '/redoc',
            openapi_url=None if public.enabled else '/openapi.json')
apply_security(app,public)
app.add_middleware(LanguageMiddleware)
for router in (routes_explorer.router,routes_observations.router,routes_detection.router,routes_education.router):
    app.include_router(router)
app.mount('/static',StaticFiles(directory=str(FRONTEND)),name='static')

@app.get('/',include_in_schema=False)
def index():return FileResponse(FRONTEND/'index.html')

@app.get('/api/health')
def health():return {'status':'ok','version':'1.0.0','demo_available':True,
                   'real_source':'NASA/IPAC IRSA SIA2','app':'Planet X Explorer'}

@app.get('/api/sources')
def sources():return {'sources':SOURCES,
 'notice':'La demostración genera datos sintéticos. El modo IRSA usa imágenes SPHEREx reales.'}

@app.get('/api/gaia')
async def gaia(ra:float=Query(ge=0,lt=360),dec:float=Query(ge=-90,le=90),radius:float=Query(.025,ge=.001,le=.12)):
    try:
        stars=await gaia_catalog(ra,dec,radius)
        return {'source':'ESA Gaia DR3','count':len(stars),'stars':stars,'disclaimer':'Una coincidencia posicional por sí sola no clasifica un objeto.'}
    except Exception as exc:
        raise HTTPException(503,detail='Gaia no disponible; intenta de nuevo más tarde.') from exc
