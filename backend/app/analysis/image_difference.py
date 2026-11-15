"""Diferencia tras suprimir el fondo grande; no inferir probabilidad de Planeta X."""
import numpy as np
from scipy.ndimage import gaussian_filter

def difference_image(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray,dict]:
    if a.shape!=b.shape or a.ndim!=2:
        raise ValueError('La comparación requiere dos imágenes 2D de igual dimensión')
    a,b=np.asarray(a,dtype=np.float32),np.asarray(b,dtype=np.float32)
    valid=np.isfinite(a)&np.isfinite(b)
    if valid.sum()<200:
        raise ValueError('Muy pocos píxeles válidos compartidos')
    # Subtract per-image robust sky background. Missing pixels are zero-filled only for smoothing.
    def highpass(arr):
        fill=float(np.median(arr[valid]))
        z=np.where(valid,arr,fill)
        return z - gaussian_filter(z,9)
    ah,bh=highpass(a),highpass(b)
    diff=gaussian_filter(bh-ah,.8).astype(np.float32)
    diff[~valid]=np.nan
    robust=float(1.4826*np.median(np.abs(diff[valid]-np.median(diff[valid]))))
    # Keep the noise estimate tied to the image scale instead of imposing a
    # fixed physical floor that changes sensitivity across datasets.
    scale=float(np.nanmax(np.abs(diff[valid])))
    robust=max(robust,float(np.finfo(np.float32).eps*scale))
    return diff,{'rms_robust':robust,'valid_fraction':round(float(valid.mean()),4),
                 'method':'Restas después de eliminar el fondo (Gauss σ=9 px)'}
