"""Pruebas del procesamiento y límites de seguridad."""
import numpy as np
import pytest
from backend.app.services.demo_service import make_demo_pair
from backend.app.analysis.image_difference import difference_image
from backend.app.analysis.motion_detection import detect_candidates
from backend.app.services.spherex_service import safe_access_url


def test_demo_deterministic():
    a,b,_=make_demo_pair(127.6944,-39.17,0,2)
    c,d,_=make_demo_pair(127.6944,-39.17,0,2)
    assert np.array_equal(a,c) and np.array_equal(b,d)

def test_motion_detected():
    a,b,_=make_demo_pair(127.6944,-39.17,0,2)
    diff,stats=difference_image(a,b)
    candidates=detect_candidates(diff,stats['rms_robust'])
    assert candidates and max(c['snr'] for c in candidates)>10
    assert any(c['shift_px'] is not None for c in candidates)

def test_shape_validation():
    with pytest.raises(ValueError,match='igual dimensión'):
        difference_image(np.ones((20,20)),np.ones((30,30)))

def test_safe_irsa_only():
    good='https://irsa.ipac.caltech.edu/ibe/data/spherex/dr1/level2/test.fits'
    assert safe_access_url(good)
    for url in ('http://irsa.ipac.caltech.edu/ibe/data/spherex/foo',
                'https://evil.net/ibe/data/spherex/a',
                'https://irsa.ipac.caltech.edu.evil.net/ibe/data/spherex/a',
                'https://irsa.ipac.caltech.edu/private',
                'file:///etc/passwd'):
        assert not safe_access_url(url)
