"""Autoprueba sin Internet del flujo completo."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend.app.main import app

def run():
    with TestClient(app) as c:
        assert c.get('/api/health').status_code==200
        region=c.get('/api/observations',params={'mode':'demo','ra':127.69444,'dec':-39.1776}).json()
        assert region['count']==4
        a,b=region['observations'][:2]
        r=c.post('/api/compare',json={'search_id':region['search_id'],'first_id':a['id'],'second_id':b['id']})
        assert r.status_code==200,r.text
        compare=r.json()
        assert compare['meta']['is_demo'] is True
        for layer in ('a','b','difference'):
            img=c.get(compare['images'][layer]);assert img.status_code==200 and img.content[:8]==b'\x89PNG\r\n\x1a\n'
        detected=c.get('/api/detect/'+compare['session_id']).json()
        assert detected['count']>=1
        print('CORRECTO: health, 4 épocas, comparación, 3 PNG y detección de',detected['count'],'candidatos preliminares.')

if __name__=='__main__':run()
