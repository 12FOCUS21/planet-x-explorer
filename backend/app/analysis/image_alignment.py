"""Reproyección al mismo sistema de coordenadas antes de restar imágenes."""
import numpy as np

def align_to_reference(reference: np.ndarray, reference_header, moving: np.ndarray, moving_header) -> tuple[np.ndarray, dict]:
    from astropy.wcs import WCS
    from reproject import reproject_interp
    ref_wcs = WCS(reference_header).celestial
    mov_wcs = WCS(moving_header).celestial
    if not ref_wcs.has_celestial or not mov_wcs.has_celestial:
        raise ValueError('FITS sin WCS celestial: no es seguro comparar estas observaciones')
    data,footprint = reproject_interp((moving, mov_wcs),ref_wcs,shape_out=reference.shape,order='bilinear')
    valid = np.isfinite(data)&(footprint>0)
    if valid.mean()<.15:
        raise ValueError('Las dos observaciones no tienen suficiente cielo en común (>15%)')
    data = np.where(valid,data,np.nan).astype(np.float32)
    return data,{'registered':True, 'overlap_fraction':float(valid.mean()),'method':'Reproyección WCS (interpolación bilineal)'}
