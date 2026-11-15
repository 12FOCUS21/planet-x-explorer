"""Cielo sintético REPRODUCIBLE. Nunca etiquetar como mediciones NASA."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import gaussian_filter

SIZE = 440
DEMO_DATES = ['2025-05-19','2025-07-03','2025-08-18','2025-10-06']
PRESETS = [
    {'name':'Campo de prueba', 'subtitle':'Escenario de entrenamiento', 'ra':127.69444, 'dec':-39.17760, 'radius':0.08, 'tag':'Recomendado'},
    {'name':'Orión', 'subtitle':'Región de formación estelar', 'ra':83.82, 'dec':-5.39, 'radius':0.08, 'tag':'Nebulosa'},
    {'name':'Andrómeda', 'subtitle':'Galaxia M31', 'ra':10.6847, 'dec':41.269, 'radius':0.08, 'tag':'Galaxia'},
    {'name':'Centro galáctico', 'subtitle':'Centro de la Vía Láctea', 'ra':266.4168, 'dec':-29.0078, 'radius':0.08, 'tag':'Campo denso'},
]

def observations(ra: float, dec: float) -> list[dict]:
    return [
        {'id':f'demo-{i}', 'label':f'Simulación · Época {i + 1}', 'date':d,
         'detector':'D2 (ficticio)', 'band':'Simulada · IR', 'source':'Simulación didáctica',
         'collection':'DEMO', 'simulated': True}
        for i,d in enumerate(DEMO_DATES)
    ]


def make_demo_pair(ra: float, dec: float, index_a: int, index_b: int) -> tuple[np.ndarray,np.ndarray,dict]:
    rng = np.random.default_rng(42 + (int(ra * 100) % 500) + (int((dec+90)*10) % 500))
    size = SIZE
    stars_x = rng.uniform(12,size-12,155)
    stars_y = rng.uniform(12,size-12,155)
    bright = np.clip(rng.lognormal(2.0,.9,155),2,160)
    # A single sky scene; only the moving source depends on epoch.
    yy, xx = np.mgrid[:size,:size]
    cloud = (4.2 * np.exp(-((xx-size*.67)**2+(yy-size*.26)**2)/(2*(size*.23)**2)) +
             1.9*np.sin(xx/110)*np.cos(yy/88))
    def epoch(i):
        p = np.zeros((size,size),dtype=np.float32)
        for x,y,v in zip(stars_x,stars_y,bright):
            p[int(round(y)),int(round(x))]+=float(v)
        sources = gaussian_filter(p,1.45)*25
        # Object visibly moves, but less than a small fraction of the field per epoch.
        x = size*(.39 + i*.047)
        y = size*(.59 - i*.026)
        blob = 70*np.exp(-((xx-x)**2+(yy-y)**2)/(2*1.85**2))
        # Synthetic variable source, to teach that changes are not always motion.
        variable = (8 + i*3.5)*np.exp(-((xx-size*.77)**2+(yy-size*.71)**2)/(2*2.2**2))
        noise = np.random.default_rng(8800 + i + (int(ra) % 200)).normal(0,1.05,(size,size))
        return np.asarray(8+cloud+sources+blob+variable+noise, dtype=np.float32)
    a,b=epoch(index_a),epoch(index_b)
    return a,b,{'dataset':'SIMULACIÓN','instrument':'Generador determinista interno', 'unit':'unidades arbitrarias', 'is_demo':True,
        'description':'Escena sintética con un objeto desplazado, estrellas fijas y una fuente variable. No son imágenes SPHEREx.'}
