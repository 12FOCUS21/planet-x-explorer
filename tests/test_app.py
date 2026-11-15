"""Pruebas automatizadas de API y distinción de procedencia."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import FRONTEND


class StaticReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources=[]
        self.ids={}
        self.demo_starts=0
        self.real_starts=0

    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if attrs.get('id'):
            self.ids[attrs['id']]=attrs
        self.demo_starts+=int('data-demo-start' in attrs)
        self.real_starts+=int('data-real-start' in attrs)
        if tag in ('img','script') or (tag=='link' and attrs.get('rel') in ('icon','stylesheet')):
            resource=attrs.get('src') or attrs.get('href')
            if resource:
                self.resources.append(resource)
            elif tag=='img':
                assert 'hidden' in attrs or attrs.get('id')=='detectionImage'

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_index_and_health(client):
    assert client.get('/').status_code==200
    assert b'Planet X Explorer' in client.get('/').content
    assert client.get('/api/health').json()['demo_available'] is True


def test_frontend_static_resources_and_progressive_reveal(client):
    """La portada no debe señalar imágenes cargadas ni romper referencias locales."""
    parsed=StaticReferences()
    parsed.feed(client.get('/').text)
    assert parsed.demo_starts>=2 and parsed.real_starts>=2
    assert '/static/css/product-experience.css' in {urlsplit(url).path for url in parsed.resources}
    assert '/static/js/explorer.js' in {urlsplit(url).path for url in parsed.resources}
    assert '/static/js/activity.js' in {urlsplit(url).path for url in parsed.resources}
    for resource in parsed.resources:
        path=urlsplit(resource).path
        assert path.startswith('/static/'),resource
        file=(FRONTEND/path.removeprefix('/static/')).resolve()
        assert file.is_relative_to(Path(FRONTEND).resolve()) and file.is_file(),resource
        assert client.get(resource).status_code==200,resource
    for element in ('searchSummary','scienceFigure','explorerDetails','imageA','imageB','imageDiff',
                    'searchActivity','compareActivity','detectActivity'):
        assert 'hidden' in parsed.ids[element],element
    assert 'hidden' not in parsed.ids['comparisonPlaceholder']
    assert 'disabled' in parsed.ids['runDetectionTop']
    assert 'aria-pressed' in parsed.ids['modeReal'] and parsed.ids['modeReal']['aria-pressed']=='true'

def test_invalid_coordinates(client):
    assert client.get('/api/observations?ra=380').status_code==422
    assert client.get('/api/observations?dec=-95').status_code==422
    assert client.get('/api/observations?mode=invalid').status_code==422

def test_demo_observations_are_explicitly_simulated(client):
    response=client.get('/api/observations?mode=demo')
    assert response.status_code==200
    data=response.json()
    assert len(data['observations'])==4
    assert all(o['simulated'] and 'Simulación' in o['source'] for o in data['observations'])
    assert all('_access_url' not in o for o in data['observations'])

def test_demo_pipeline(client):
    found=client.get('/api/observations').json()
    # The existing detector's motion pairing is validated on epochs 0 and 2.
    first,second=found['observations'][0],found['observations'][2]
    payload={'search_id':found['search_id'],'first_id':first['id'],'second_id':second['id']}
    compare=client.post('/api/compare',json=payload)
    assert compare.status_code==200,compare.text
    data=compare.json()
    assert data['meta']['is_demo'] is True
    assert data['alignment']['overlap_fraction']==1.0
    for kind in ('a','b','difference'):
        image=client.get(data['images'][kind])
        assert image.status_code==200
        assert image.headers['content-type']=='image/png'
        assert image.content.startswith(b'\x89PNG\r\n\x1a\n')
    analysis=client.get('/api/detect/'+data['session_id'])
    assert analysis.status_code==200
    findings=analysis.json()
    assert findings['count']>0
    assert any(item['shift_px'] is not None for item in findings['candidates'])
    assert 'No se puede confirmar Planeta X' in findings['disclaimer']

def test_different_epoch_required(client):
    found=client.get('/api/observations').json()
    oid=found['observations'][0]['id']
    r=client.post('/api/compare',json={'search_id':found['search_id'],'first_id':oid,'second_id':oid})
    assert r.status_code==422

def test_not_found(client):
    assert client.get('/api/image/invalid/a').status_code==404
    assert client.get('/api/detect/invalid').status_code==404

def test_academy_and_sources(client):
    assert len(client.get('/api/academy').json()['questions'])==5
    assert len(client.get('/api/sources').json()['sources'])>=3
