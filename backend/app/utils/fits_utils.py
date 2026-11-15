"""Herramientas FITS: lectura de la extensión IMAGE y metadatos."""
from io import BytesIO
import numpy as np


def extract_science_image(content: bytes) -> tuple[np.ndarray, object, dict]:
    from astropy.io import fits
    with fits.open(BytesIO(content), memmap=False, lazy_load_hdus=False) as hdul:
        if 'IMAGE' in hdul:
            hdu = hdul['IMAGE']
        else:
            hdu = next((item for item in hdul if getattr(item, 'data', None) is not None and getattr(item.data, 'ndim', 0) == 2), None)
        if hdu is None or hdu.data is None:
            raise ValueError('El FITS recibido no contiene imagen 2D')
        img = np.asarray(hdu.data, dtype=np.float32).copy()
        head = hdu.header.copy()
        info = {'shape': list(img.shape), 'unit': head.get('BUNIT', 'MJy/sr'), 'extension': head.get('EXTNAME', 'IMAGE')}
    if min(img.shape) < 16:
        raise ValueError('La imagen FITS es demasiado pequeña para analizar')
    return img, head, info
