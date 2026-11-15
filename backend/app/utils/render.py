"""Crea previews PNG solo a partir de arreglos científicos, no de material de archivo falso."""
from io import BytesIO
import numpy as np
from PIL import Image

def render_png(arr:np.ndarray, variant:str='indigo', limits=None) -> bytes:
    a=np.asarray(arr,dtype=np.float64)
    finite=np.isfinite(a)
    if finite.sum()<10:
        raise ValueError('Imagen sin valores finitos')
    lo,hi=limits if limits is not None else np.nanpercentile(a[finite],[5,99.6])
    if hi<=lo: hi=lo+1
    v=np.clip((np.nan_to_num(a,nan=lo)-lo)/(hi-lo),0,1)
    v=np.arcsinh(v*6)/np.arcsinh(6)
    if variant=='difference':
        # Diverging residual map: blue for negative, white near zero, red for positive.
        scale=np.nanpercentile(np.abs(a[finite]),99.4)
        z=np.clip(np.nan_to_num(a)/max(scale,1e-12),-1,1)
        pos=np.maximum(0,z);neg=np.maximum(0,-z);mag=np.abs(z)
        out=np.stack([248-216*neg+7*pos,249-167*mag,250-12*neg-220*pos],axis=-1)
    else:
        # Purple sky background with warm orange-yellow sources, like the reference plot.
        out=np.stack([12+90*v+153*v**4,4+27*v+170*v**4,28+125*v-120*v**4],axis=-1)
    out=np.clip(out,0,255).astype(np.uint8)
    out[~finite]=np.array([5,11,25],dtype=np.uint8)
    out=np.flipud(out)  # FITS origin bottom-left; canvas images top-left.
    buf=BytesIO(); Image.fromarray(out,'RGB').save(buf,format='PNG',optimize=True)
    return buf.getvalue()
