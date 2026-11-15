"""Regression tests: pair selection, async jobs, retries and cache integrity."""
import asyncio
import hashlib
import time
from io import BytesIO
from pathlib import Path
import httpx
import numpy as np
import pytest
from astropy.io import fits
from fastapi import HTTPException
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services import spherex_service as svc
from backend.app.api import routes_observations as routes
from backend.app.analysis.validation import validate_pair
from backend.app.state import SESSIONS


def fits_bytes():
    b=BytesIO()
    fits.HDUList([fits.PrimaryHDU(),fits.ImageHDU(np.ones((24,24),dtype='float32'),name='IMAGE')]).writeto(b)
    return b.getvalue()


def observation(oid='a', date='2025-05-01T01:00:00'):
    return {'id':oid,'date':date,'collection':'SPHEREX_DR1','detector':'D1',
            'simulated':False,'_em_min':1e-6,'_em_max':1.2e-6,
            '_access_url':'https://irsa.ipac.caltech.edu/ibe/data/spherex/dr1/level2/test.fits'}


def test_distinct_times_same_day():
    validate_pair(observation(),observation('b','2025-05-01T02:00:00'))
    assert 'T' in svc._date_mjd('60800.1234')


def test_suggested_pairs_match_server_validation(monkeypatch):
    obs=[observation(),observation('bad','2025-05-02T00:00:00'),observation('good','2025-05-03T00:00:00')]
    obs[1]['detector']='D2'
    async def search(*args):return obs,[]
    monkeypatch.setattr(svc,'search',search)
    with TestClient(app) as client:
        data=client.get('/api/observations?mode=real').json()
        assert data['compatible_pairs']['a']==['good']
        assert data['compatible_pairs']['bad']==[]
        assert data['suggested_pair']==['a','good']


def test_real_failure_never_falls_back_to_demo(monkeypatch):
    async def unavailable(*args):return [],['spherex_dr1: consulta temporalmente no disponible']
    monkeypatch.setattr(svc,'search',unavailable)
    with TestClient(app) as client:
        response=client.get('/api/observations?mode=real')
        assert response.status_code==503
        assert 'observations' not in response.json()


def test_real_job_hides_upstream_exception_text(monkeypatch):
    routes.JOBS.clear()
    async def found(*args):return [observation(),observation('b','2025-05-02T00:00:00')],[]
    async def broken(*args,**kwargs):raise ValueError('https://private.example/?token=secret')
    monkeypatch.setattr(svc,'search',found)
    monkeypatch.setattr(routes,'download_cutout',broken)
    with TestClient(app) as client:
        result=client.get('/api/observations?mode=real').json()
        a,b=result['suggested_pair']
        started=client.post('/api/compare/jobs',json={
            'search_id':result['search_id'],'first_id':a,'second_id':b})
        job=wait_job(client,started.json()['job_id'])
        assert job['status']=='error' and job['error_code']==502
        assert 'private.example' not in job['message'] and 'secret' not in job['message']


def install_transport(monkeypatch,handler):
    client=httpx.AsyncClient
    def factory(**kwargs):
        kwargs.update(transport=httpx.MockTransport(handler),trust_env=False)
        return client(**kwargs)
    monkeypatch.setattr(svc.httpx,'AsyncClient',factory)


def test_corrupt_cache_is_replaced_and_reused(tmp_path,monkeypatch):
    monkeypatch.setattr(svc,'CACHE',tmp_path)
    obs=observation();url,params,path=svc.cutout_request(obs,1,2,.08)
    path.write_bytes(b'SIMPLE  '+b'x'*100)
    calls=[]
    def response(request):
        calls.append(request)
        assert request.url.params['center'].endswith('d')
        return httpx.Response(200,content=fits_bytes())
    install_transport(monkeypatch,response)
    async def run():
        a,source=await svc.download_cutout(obs,1,2,.08)
        b,cached=await svc.download_cutout(obs,1,2,.08)
        assert a==b==path.read_bytes()
        assert source=='IRSA' and 'caché' in cached
    asyncio.run(run())
    assert len(calls)==1
    assert not list(tmp_path.glob('*.part'))


def test_retries_after_connection_break(tmp_path,monkeypatch):
    monkeypatch.setattr(svc,'CACHE',tmp_path)
    class Broken(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield b'SIMPLE  '
            raise httpx.ReadError('interrupted')
    calls=[]
    def response(req):
        calls.append(req)
        return httpx.Response(200,stream=Broken()) if len(calls)==1 else httpx.Response(200,content=fits_bytes())
    install_transport(monkeypatch,response)
    data,_=asyncio.run(svc.download_cutout(observation(),1,2,.08))
    assert data==fits_bytes() and len(calls)==2


def test_html_never_enters_cache(tmp_path,monkeypatch):
    monkeypatch.setattr(svc,'CACHE',tmp_path)
    install_transport(monkeypatch,lambda req:httpx.Response(200,content=b'<html>upstream error</html>'))
    with pytest.raises(ValueError,match='FITS'):
        asyncio.run(svc.download_cutout(observation(),1,2,.08))
    assert not list(tmp_path.glob('*.fits'))


def test_legacy_verified_cache_reused(tmp_path,monkeypatch):
    monkeypatch.setattr(svc,'CACHE',tmp_path)
    obs=observation();url,params,path=svc.cutout_request(obs,1,2,.08)
    key=hashlib.sha256(f'{url}?center={params["center"][:-1]}&size={params["size"]}'.encode()).hexdigest()
    (tmp_path/f'{key}.fits').write_bytes(fits_bytes())
    install_transport(monkeypatch,lambda req:pytest.fail('Unexpected network request'))
    data,source=asyncio.run(svc.download_cutout(obs,1,2,.08))
    assert 'caché' in source and path.exists()


def wait_job(client,jid):
    for _ in range(100):
        job=client.get('/api/compare/jobs/'+jid).json()
        if job['status'] in ('done','error'):return job
        time.sleep(.02)
    pytest.fail('Job did not finish')


def test_job_completes_and_duplicate_reuses_result():
    routes.JOBS.clear()
    with TestClient(app) as c:
        found=c.get('/api/observations?mode=demo').json()
        a,b=found['suggested_pair']
        payload=dict(search_id=found['search_id'],first_id=a,second_id=b)
        started=c.post('/api/compare/jobs',json=payload)
        assert started.status_code==202
        jid=started.json()['job_id'];job=wait_job(c,jid)
        assert job['status']=='done',job
        assert c.post('/api/compare/jobs',json=payload).json()['job_id']==jid
        assert all(c.get(url).status_code==200 for url in job['result']['images'].values())
        assert c.get('/api/health').status_code==200


def test_job_failure_is_terminal_and_retry_creates_new_job(monkeypatch):
    routes.JOBS.clear()
    async def fail(*args):raise HTTPException(504,'IRSA timeout')
    monkeypatch.setattr(routes,'compare',fail)
    with TestClient(app) as c:
        f=c.get('/api/observations?mode=demo').json();a,b=f['suggested_pair']
        payload=dict(search_id=f['search_id'],first_id=a,second_id=b)
        jid=c.post('/api/compare/jobs',json=payload).json()['job_id']
        job=wait_job(c,jid)
        assert job['status']=='error' and job['error_code']==504
        assert c.post('/api/compare/jobs',json=payload).json()['job_id']!=jid


def test_noise_scale_does_not_round_to_zero():
    from backend.app.analysis.image_difference import difference_image
    rng=np.random.default_rng(7)
    a=rng.normal(size=(32,32)).astype('float32')*1e-8
    _,s=difference_image(a,a*2)
    assert 0<s['rms_robust']<1e-6
