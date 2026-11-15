"""Diagnóstico sencillo, sin conexiones de red."""
import importlib
import platform
from pathlib import Path
mods=['fastapi','uvicorn','numpy','scipy','PIL','astropy','reproject','astroquery','pyvo','httpx','pytest']
print('Planet X Explorer — revisión de entorno')
print('Python:',platform.python_version(),'| SO:',platform.system())
failed=[]
for x in mods:
    try:
        obj=importlib.import_module(x)
        print(' OK',x,getattr(obj,'__version__',''))
    except Exception as ex:
        failed.append(x)
        print(' FALTA',x,str(ex))
print('Resultado:', 'APTO' if not failed else 'INSTALA '+', '.join(failed))
raise SystemExit(1 if failed else 0)
