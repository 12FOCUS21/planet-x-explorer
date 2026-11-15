"""Consulta opcional y acotada de Gaia DR3 (ESA, no NASA)."""
from __future__ import annotations

async def gaia_catalog(ra: float, dec: float, radius: float, limit: int = 40) -> list[dict]:
    import httpx
    # Parámetros numéricos validados por el API, sin SQL proporcionado por usuarios.
    limit = max(1, min(150, limit))
    radius = min(radius, 0.12)
    query = (
        f'SELECT TOP {limit} source_id,ra,dec,phot_g_mean_mag,pmra,pmdec '
        'FROM gaiadr3.gaia_source WHERE '
        f'1=CONTAINS(POINT(\'ICRS\',ra,dec),CIRCLE(\'ICRS\',{ra:.8f},{dec:.8f},{radius:.8f})) '
        'ORDER BY phot_g_mean_mag ASC'
    )
    url = 'https://gea.esac.esa.int/tap-server/tap/sync'
    async with httpx.AsyncClient(timeout=25.0, follow_redirects=False) as client:
        async with client.stream('GET',url,params={'REQUEST':'doQuery', 'LANG':'ADQL', 'FORMAT':'csv', 'QUERY':query}) as r:
            if r.status_code!=200:
                raise ValueError('Gaia no devolvió un catálogo CSV')
            r.raise_for_status()
            if int(r.headers.get('content-length') or 0)>512*1024:
                raise ValueError('Respuesta Gaia demasiado grande')
            content=bytearray()
            async for chunk in r.aiter_bytes():
                content.extend(chunk)
                if len(content)>512*1024:
                    raise ValueError('Respuesta Gaia demasiado grande')
    import csv, io
    rows=csv.DictReader(io.StringIO(content.decode('utf-8-sig')))
    return [{k: row.get(k, '') for k in ('source_id','ra','dec','phot_g_mean_mag','pmra','pmdec')}
            for _,row in zip(range(limit),rows)]
