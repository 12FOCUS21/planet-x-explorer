"""Language is a presentation choice, never a change to the scientific state."""
import json
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.localization import CATALOG,localized,translate

client=TestClient(app)


def test_academy_and_sources_in_english():
    response=client.get('/api/academy?lang=en')
    assert response.headers['content-language']=='en'
    assert 'Accept-Language' in response.headers['vary']
    assert response.json()['lessons'][0]['title']=='What is Planet Nine?'
    assert response.json()['questions'][0]['correct']==1
    assert response.json()['questions'][0]['answers'][1]=='No, it remains a hypothesis'
    assert client.get('/api/sources',headers={'Accept-Language':'en-US,en;q=0.8'}).json()['sources'][0]['kind']=='SPHEREx scientific archive'


def test_default_spanish_and_explicit_override():
    assert client.get('/api/academy').json()['lessons'][0]['title']=='¿Qué es el Planeta Nueve?'
    assert client.get('/api/academy?lang=es',headers={'Accept-Language':'en'}).headers['content-language']=='es'
    assert client.get('/api/academy?lang=unsupported').headers['content-language']=='es'


def test_language_does_not_change_observation_ids_or_pairing():
    es=client.get('/api/observations?mode=demo&lang=es').json()
    en=client.get('/api/observations?mode=demo&lang=en').json()
    assert es['compatible_pairs']==en['compatible_pairs']
    assert es['suggested_pair']==en['suggested_pair']
    assert en['observations'][0]['id']=='demo-0'
    assert en['observations'][0]['label']=='Simulation · Epoch 1'
    assert en['observations'][0]['date']==es['observations'][0]['date']
    assert en['note']=='SIMULATED data, not NASA.'


def test_error_translation_and_no_shared_state_mutation():
    response=client.get('/api/detect/missing?lang=en')
    assert response.status_code==404
    assert response.json()['detail']=='Prepare the comparison first'
    assert client.get('/api/detect/missing?lang=es').json()['detail']=='Primero prepara la comparación'
    data={'id':'PX-001','x':0.25,'simulated':True,'classification':'Variabilidad / cambio'}
    translated=localized(data)
    assert translated=={**data,'classification':'Variability / change'}
    assert data['classification']=='Variabilidad / cambio'
    assert translate('Descargando A: 2.1 MB de 3.7 MB')=='Downloading A: 2.1 MB of 3.7 MB'


def test_catalog_is_available_and_has_unique_sources():
    response=client.get('/static/locales/en.json')
    assert response.status_code==200
    pairs=json.loads(response.text,object_pairs_hook=list)
    assert len(pairs)==len(CATALOG)
    assert all(source and target for source,target in pairs)
    assert client.get('/static/js/i18n.js').status_code==200
