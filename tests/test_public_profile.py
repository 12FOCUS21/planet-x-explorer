"""Public profile regression checks; no external network or deployment required."""
import os
import subprocess
import sys
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from backend.app.security import PublicSettings, apply_security


@pytest.mark.parametrize('origin', [
    '', 'http://px.example', 'https://px.example/path',
    'https://px.example:444', 'https://user@px.example',
    'https://px.example/?token=secret', 'https://px.example.evil/extra',
])
def test_public_mode_fails_closed(monkeypatch, origin):
    monkeypatch.setenv('PX_PUBLIC_MODE','1')
    monkeypatch.setenv('PX_PUBLIC_ORIGIN',origin)
    monkeypatch.delenv('RENDER_EXTERNAL_URL',raising=False)
    with pytest.raises(ValueError,match='PX_PUBLIC_ORIGIN'):
        PublicSettings.from_env()


def test_render_origin_only_when_present(monkeypatch):
    monkeypatch.setenv('PX_PUBLIC_MODE','1')
    monkeypatch.delenv('PX_PUBLIC_ORIGIN',raising=False)
    monkeypatch.setenv('RENDER_EXTERNAL_URL','https://planet-x.onrender.com')
    assert PublicSettings.from_env()==PublicSettings(True,'https://planet-x.onrender.com')
    monkeypatch.setenv('PX_PUBLIC_ORIGIN','https://custom.example')
    assert PublicSettings.from_env().origin=='https://custom.example'


def public_app():
    app=FastAPI()
    apply_security(app,PublicSettings(True,'https://px.example'))

    @app.get('/api/gaia')
    def gaia(): return {'ok':True}

    @app.get('/api/observations')
    def observations(): return {'ok':True}

    @app.post('/api/compare/jobs')
    async def job(request:Request): return {'body':await request.json()}

    return app


def test_public_host_origin_headers_and_body_limits():
    with TestClient(public_app(),base_url='https://px.example') as c:
        ok=c.post('/api/compare/jobs',json={'hello':'world'},headers={'Origin':'https://px.example'})
        assert ok.status_code==200 and ok.json()['body']=={'hello':'world'}
        assert ok.headers['content-security-policy'].startswith("default-src 'self'")
        assert ok.headers['strict-transport-security']=='max-age=31536000'
        assert ok.headers['cache-control']=='no-store'
        assert c.post('/api/compare/jobs',json={},headers={'Origin':'https://evil.example'}).status_code==403
        assert c.post('/api/compare',json={}).status_code==404
        assert c.get('/docs').status_code==404
        assert c.post('/api/compare/jobs',content='x'*4097).status_code==413
        streamed=c.post('/api/compare/jobs',content=iter([b'a'*2048,b'b'*3072]))
        assert streamed.status_code==413
    with TestClient(public_app(),base_url='https://other.example') as c:
        assert c.get('/api/gaia').status_code==400


def test_public_quota_for_remote_queries_only():
    with TestClient(public_app(),base_url='https://px.example') as c:
        assert c.get('/api/observations?mode=demo').status_code==200
        assert all(c.get('/api/gaia').status_code==200 for _ in range(30))
        limited=c.get('/api/observations?mode=real')
        assert limited.status_code==429 and limited.headers['retry-after']=='60'
        assert c.get('/api/observations?mode=demo').status_code==200


def test_real_app_starts_with_render_origin_and_hides_docs():
    env=os.environ.copy()
    env.pop('PX_PUBLIC_ORIGIN',None)
    env.update(PX_PUBLIC_MODE='1',RENDER_EXTERNAL_URL='https://px.onrender.com')
    code="""from backend.app.main import app
from fastapi.testclient import TestClient
with TestClient(app,base_url='https://px.onrender.com') as c:
    assert c.get('/api/health').status_code==200
    assert c.get('/docs').status_code==404
    assert c.get('/static/css/accessibility.css').status_code==200
    assert c.get('/api/health').headers['strict-transport-security']
    found=c.get('/api/observations?mode=demo').json()
    first,second=found['suggested_pair']
    job=c.post('/api/compare/jobs',json=dict(search_id=found['search_id'],first_id=first,second_id=second),headers={'Origin':'https://px.onrender.com'})
    assert job.status_code==202,job.text
    print('public startup and demo job OK')
"""
    result=subprocess.run([sys.executable,'-c',code],env=env,text=True,capture_output=True,timeout=30)
    assert result.returncode==0,result.stderr
    assert 'public startup and demo job OK' in result.stdout
