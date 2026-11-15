"""Búsqueda simple de pares residuales +/-; un indicador, no una órbita medida."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import maximum_filter


def detect_candidates(diff: np.ndarray, rms: float, max_candidates: int=12, threshold_sigma: float=5.0) -> list[dict]:
    a=np.nan_to_num(diff,nan=0,posinf=0,neginf=0)
    # Guard borders; suppress broad non-point features.
    noise=max(float(rms),float(np.finfo(np.float32).eps*np.nanmax(np.abs(a))))
    threshold=float(threshold_sigma)*noise
    positive=(a==maximum_filter(a,size=11))&(a>threshold)
    negative=(-a==maximum_filter(-a,size=11))&(-a>threshold)
    positive[:8,:]=False;positive[-8:,:]=False;positive[:,:8]=False;positive[:,-8:]=False
    negative[:8,:]=False;negative[-8:,:]=False;negative[:,:8]=False;negative[:,-8:]=False
    py,px=np.where(positive);ny,nx=np.where(negative)
    peak_sorted=np.argsort(a[py,px])[::-1]
    candidates=[]
    h,w=a.shape
    # A displacement is plausible only when the two peaks are mutual nearest
    # neighbours and have broadly similar residual amplitudes.
    if len(px) and len(nx):
        distances=np.hypot(px[:,None]-nx[None,:],py[:,None]-ny[None,:])
        nearest_negative=np.argmin(distances,axis=1)
        nearest_positive=np.argmin(distances,axis=0)
    else:
        distances=np.empty((len(px),0));nearest_negative=np.array([],dtype=int);nearest_positive=np.array([],dtype=int)
    for j in peak_sorted:
        if len(candidates)>=max_candidates: break
        x,y=int(px[j]),int(py[j]); snr=round(float(a[y,x]/noise),1)
        prev_x=prev_y=shift=None
        if len(nx):
            match=int(nearest_negative[j]);dist=float(distances[j,match])
            negative_amp=abs(float(a[ny[match],nx[match]]))
            amplitude_ratio=float(a[y,x])/max(negative_amp,np.finfo(float).tiny)
            if (5<=dist<=110 and nearest_positive[match]==j and .25<=amplitude_ratio<=4):
                prev_x=float(nx[match]/w);prev_y=float(ny[match]/h)
                shift=round(dist,1)
        # No real known-object crossmatching or orbital fit at this stage.
        cls='Movimiento aparente (preliminar)' if shift is not None else 'Variabilidad / cambio'
        candidates.append({'id':f'PX-{len(candidates)+1:03d}', 'x':round(x/w,5), 'y':round(y/h,5),
           'previous_x':prev_x,'previous_y':prev_y, 'shift_px':shift,'snr':snr,'classification':cls,
           'note': 'Señal provisional; requiere validar longitud de onda, artefactos y fuentes conocidas.'})
    return candidates
