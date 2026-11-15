"""Búsqueda real en NASA/IPAC IRSA vía IVOA SIA2 y extracción de cutouts FITS.

La búsqueda no implica que las observaciones sean comparables científicamente:
SPHEREx usa filtros LVF con longitud de onda variable a lo largo de sus detectores.
"""
from __future__ import annotations
import asyncio
import time
import os
import tempfile
from collections import OrderedDict
import hashlib
from io import BytesIO
from pathlib import Path
from urllib.parse import urlsplit
import re
import xml.etree.ElementTree as ET
import httpx
from ..config import CACHE, MAX_DOWNLOAD, REQUEST_TIMEOUT

SIA_URL='https://irsa.ipac.caltech.edu/SIA'
COLLECTIONS=('spherex_dr1','spherex_qr3','spherex_dr1_deep','spherex_qr3_deep')
MAX_SIA_BYTES=8*1024*1024

def safe_access_url(url: str) -> bool:
    try:
        parsed=urlsplit(url)
        return (parsed.scheme=='https' and parsed.hostname=='irsa.ipac.caltech.edu'
                and parsed.port in (None,443) and not parsed.username and not parsed.password
                and not parsed.fragment and not any(ord(char)<33 for char in url)
                and parsed.path.startswith('/ibe/data/spherex/'))
    except ValueError:
        return False


def _cell(row,key,default=''):
    try:
        cell=row[key]
        if getattr(cell,'mask',False) is True or str(cell)=='--': return default
        return str(cell).strip()
    except (KeyError,IndexError,TypeError,ValueError): return default


def _date_mjd(value):
    try:
        from astropy.time import Time
        return Time(float(value),format='mjd').isot
    except Exception:
        return 'Fecha no indicada'


def _is_votable(response: httpx.Response) -> bool:
    return b'<VOTABLE' in response.content[:8192].upper()


def _parse_sia_table(content: bytes):
    root=ET.fromstring(content)
    overflow=False
    for info in root.iter():
        if info.tag.rsplit('}',1)[-1].upper()=='INFO' and info.attrib.get('name','').upper()=='QUERY_STATUS':
            if info.attrib.get('value','').upper()=='ERROR':
                raise ValueError('IRSA rechazó la consulta SIA')
            if info.attrib.get('value','').upper()=='OVERFLOW':
                overflow=True
    from astropy.io.votable import parse_single_table
    return parse_single_table(BytesIO(content)).to_table(use_names_over_ids=True),overflow


async def _sia_request(params: dict) -> httpx.Response:
    """Read a bounded VOTable without following redirects to other destinations."""
    async with httpx.AsyncClient(timeout=httpx.Timeout(REQUEST_TIMEOUT, connect=15), follow_redirects=False) as client:
        for attempt in range(2):
            try:
                async with client.stream('GET',SIA_URL,params=params) as stream:
                    stream.raise_for_status()
                    length=int(stream.headers.get('content-length') or 0)
                    if length>MAX_SIA_BYTES:
                        raise ValueError('La tabla SIA excede el límite de tamaño')
                    chunks=[];size=0
                    async for chunk in stream.aiter_bytes():
                        size+=len(chunk)
                        if size>MAX_SIA_BYTES:
                            raise ValueError('La tabla SIA excede el límite de tamaño')
                        chunks.append(chunk)
                    response=httpx.Response(stream.status_code,headers=stream.headers,
                                            content=b''.join(chunks),request=stream.request)
                response.raise_for_status()
                if not _is_votable(response):
                    raise ValueError('IRSA respondió sin VOTable. Reintenta la búsqueda.')
                return response
            except httpx.HTTPStatusError as exc:
                if attempt or exc.response.status_code not in (429,500,502,503,504): raise
                await asyncio.sleep(1)
            except httpx.RequestError:
                if attempt: raise
                await asyncio.sleep(1)


_SEARCH_CACHE = OrderedDict()

async def search(ra:float, dec:float, radius:float) -> tuple[list[dict],list[str]]:
    key = (round(ra, 7), round(dec, 7))
    cached = _SEARCH_CACHE.get(key)
    if cached and time.monotonic() - cached[0] < 300:
        return cached[1], cached[2]

    async def collection(coll):
        output = []
        # Request images containing the centre, not every image touching a large circle.
        params = {'COLLECTION':coll, 'POS':f'CIRCLE {ra:.7f} {dec:.7f} 0.000001',
                  'MAXREC':'150', 'RESPONSEFORMAT':'VOTABLE'}
        try:
            response = await _sia_request(params)
            table,overflow = await asyncio.to_thread(_parse_sia_table, response.content)
            for i,row in enumerate(table):
                raw = _cell(row, 'access_url')
                if not safe_access_url(raw): continue
                filename = Path(urlsplit(raw).path).name
                match = re.search(r'D([1-6])_', filename, re.I)
                detector = 'D'+match.group(1) if match else 'Desconocido'
                lo,hi = _cell(row,'em_min'),_cell(row,'em_max')
                try: em_min,em_max = float(lo),float(hi)
                except (TypeError,ValueError): em_min=em_max=None
                oid = hashlib.sha256(raw.encode()).hexdigest()[:18]
                output.append({'id':oid, 'label':f'{coll.upper()} · {detector} · {i+1:02}',
                    'date':_date_mjd(_cell(row,'t_min')), 'detector':detector,
                    'band':f'{lo}–{hi} m', 'source':'NASA / IPAC IRSA',
                    'collection':coll.upper(), 'simulated':False, '_access_url':raw,
                    '_filename':filename, '_em_min':em_min, '_em_max':em_max})
            return output, ([f'{coll}: tabla SIA truncada o al límite de 150 registros; la lista puede ser incompleta']
                            if overflow or len(table)>=150 else [])
        except Exception as exc:
            # Never return an upstream URL, exception body or proxy credentials to a client.
            return [], [f'{coll}: consulta temporalmente no disponible ({type(exc).__name__})']

    results = await asyncio.gather(*(collection(coll) for coll in COLLECTIONS))
    by_id = {o['id']:o for items,_ in results for o in items}
    items = sorted(by_id.values(), key=lambda d:(d['collection'],d['detector'],d['date'],d['id']))
    warnings = [w for _,messages in results for w in messages]
    if items:
        _SEARCH_CACHE[key] = (time.monotonic(), items, warnings)
        while len(_SEARCH_CACHE)>20: _SEARCH_CACHE.popitem(last=False)
    return items,warnings


def _validate_fits(content):
    """Reject truncated/HTML files before committing them to the cache."""
    if len(content)>MAX_DOWNLOAD or len(content)<2880 or len(content)%2880 or not content.startswith(b'SIMPLE'):
        raise ValueError('FITS incompleto o respuesta no FITS de IRSA.')
    from astropy.io import fits
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('error', category=Warning)
        with fits.open(BytesIO(content), memmap=False, lazy_load_hdus=False) as hdul:
            if len(hdul)>16:
                raise ValueError('FITS con demasiadas extensiones')
            hdul.verify('exception')
            if 'IMAGE' not in hdul:
                raise ValueError('El FITS no contiene IMAGE.')
            header=hdul['IMAGE'].header
            width,height=header.get('NAXIS1'),header.get('NAXIS2')
            if (header.get('NAXIS')!=2 or not isinstance(width,int) or not isinstance(height,int)
                    or min(width,height)<16 or max(width,height)>2048 or width*height>2_000_000):
                raise ValueError('IMAGE supera el presupuesto de píxeles o no es 2D')
            if hdul['IMAGE'].data.ndim != 2:
                raise ValueError('IMAGE debe ser bidimensional.')


def cutout_request(obs, ra, dec, radius):
    url = obs.get('_access_url','')
    if not safe_access_url(url): raise ValueError('URL IRSA no permitida')
    size = min(.15,max(.035,radius*1.35))
    # Explicit decimal degrees, matching IRSA's cutout tutorial.
    params = {'center':f'{ra:.7f},{dec:.7f}d', 'size':f'{size:.5f}'}
    cache_key = hashlib.sha256(f'{url}?center={params["center"]}&size={params["size"]}'.encode()).hexdigest()
    return url,params,CACHE/f'{cache_key}.fits'


async def download_cutout(obs:dict,ra:float,dec:float,radius:float,progress=None)->tuple[bytes,str]:
    url,params,path = cutout_request(obs,ra,dec,radius)
    # Reuse verified files produced by the previous version (without the d suffix).
    old_params=dict(params,center=params['center'].removesuffix('d'))
    old_key=hashlib.sha256(f'{url}?center={old_params["center"]}&size={old_params["size"]}'.encode()).hexdigest()
    old_path=CACHE/f'{old_key}.fits'
    if not path.exists() and old_path.exists():
        try:
            old_content=await asyncio.to_thread(old_path.read_bytes)
            await asyncio.to_thread(_validate_fits,old_content)
            os.replace(old_path,path)
        except Exception: old_path.unlink(missing_ok=True)
    if path.is_file():
        content = await asyncio.to_thread(path.read_bytes)
        try:
            await asyncio.to_thread(_validate_fits,content)
            if progress: progress(len(content),len(content))
            return content,'caché verificada'
        except Exception:
            path.unlink(missing_ok=True)

    async def transfer():
        for attempt in range(3):
            content=bytearray()
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(60,connect=15),follow_redirects=False) as client:
                    async with client.stream('GET',url,params=params) as response:
                        response.raise_for_status()
                        total=int(response.headers.get('content-length') or 0)
                        if total>MAX_DOWNLOAD: raise ValueError('Recorte demasiado grande; reduce el radio.')
                        async for chunk in response.aiter_bytes():
                            content.extend(chunk)
                            if len(content)>MAX_DOWNLOAD: raise ValueError('Recorte demasiado grande; reduce el radio.')
                            if progress: progress(len(content),total)
                data=bytes(content)
                await asyncio.to_thread(_validate_fits,data)
                # Atomic commit: interrupted downloads never become a cache hit.
                fd,tmp=tempfile.mkstemp(dir=CACHE,suffix='.part')
                try:
                    with os.fdopen(fd,'wb') as f: f.write(data)
                    os.replace(tmp,path)
                finally:
                    if os.path.exists(tmp): os.unlink(tmp)
                # Bound disk use for small free hosting instances.
                cached=sorted(CACHE.glob('*.fits'),key=lambda p:p.stat().st_mtime)
                size=sum(p.stat().st_size for p in cached)
                for old in cached:
                    if size<=256*1024*1024: break
                    if old!=path:
                        size-=old.stat().st_size;old.unlink(missing_ok=True)
                return data,'IRSA'
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code not in (429,500,502,503,504) or attempt==2: raise
            except (httpx.RequestError,ValueError):
                if attempt==2: raise
            await asyncio.sleep(attempt+1)
    async with asyncio.timeout(150):
        return await transfer()
