"""Bounded IRSA/Gaia responses and FITS validation, all using fake HTTP."""
import asyncio
from io import BytesIO

import httpx
import numpy as np
import pytest
from astropy.io import fits

from backend.app.services import spherex_service as sia
from backend.app.services import gaia_service as gaia

ASYNC_CLIENT=httpx.AsyncClient

def transport(monkeypatch,handler):
    def factory(**kwargs):
        assert not kwargs.get('follow_redirects',True)
        return ASYNC_CLIENT(**{**kwargs,'transport':httpx.MockTransport(handler),'trust_env':False})
    monkeypatch.setattr(httpx,'AsyncClient',factory)


def votable(status='OK'):
    return (f'<VOTABLE version="1.3"><RESOURCE type="results">'
            f'<INFO name="QUERY_STATUS" value="{status}"/>'
            '<TABLE><FIELD name="access_url" datatype="char" arraysize="*"/>'
            '<DATA><TABLEDATA><TR><TD>https://irsa.ipac.caltech.edu/ibe/data/spherex/dr1/x.fits</TD>'
            '</TR></TABLEDATA></DATA></TABLE></RESOURCE></VOTABLE>').encode()


def test_sia_four_collections_and_query_status(monkeypatch):
    assert sia.COLLECTIONS==('spherex_dr1','spherex_qr3','spherex_dr1_deep','spherex_qr3_deep')
    assert len(sia._parse_sia_table(votable())[0])==1
    assert sia._parse_sia_table(votable('OVERFLOW'))[1] is True
    with pytest.raises(ValueError,match='rechazó'):
        sia._parse_sia_table(votable('ERROR'))
    assert not sia.safe_access_url('https://irsa.ipac.caltech.edu:444/ibe/data/spherex/x.fits')
    assert not sia.safe_access_url('https://u:p@irsa.ipac.caltech.edu/ibe/data/spherex/x.fits')
    assert not sia.safe_access_url('https://irsa.ipac.caltech.edu/ibe/data/spherex/x.fits#frag')


def test_sia_does_not_follow_redirect_or_retry_client_error(monkeypatch):
    calls=[]
    def redirect(request):
        calls.append(str(request.url))
        return httpx.Response(302,headers={'Location':'https://evil.example/fits'})
    transport(monkeypatch,redirect)
    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(sia._sia_request({'COLLECTION':'spherex_dr1'}))
    assert len(calls)==1
    def not_found(request):
        calls.append(str(request.url))
        return httpx.Response(404)
    transport(monkeypatch,not_found)
    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(sia._sia_request({}))
    assert len(calls)==2


def test_sia_size_limit_header_and_stream(monkeypatch):
    monkeypatch.setattr(sia,'MAX_SIA_BYTES',64)
    transport(monkeypatch,lambda request:httpx.Response(200,headers={'Content-Length':'65'},content=b'x'*65))
    with pytest.raises(ValueError,match='tamaño'):
        asyncio.run(sia._sia_request({}))
    transport(monkeypatch,lambda request:httpx.Response(200,content=b'x'*65))
    with pytest.raises(ValueError,match='tamaño'):
        asyncio.run(sia._sia_request({}))


def test_fits_requires_bounded_2d_image():
    def encoded(hdus):
        out=BytesIO()
        fits.HDUList(hdus).writeto(out)
        return out.getvalue()
    good=encoded([fits.PrimaryHDU(),fits.ImageHDU(np.ones((24,24),dtype='float32'),name='IMAGE')])
    sia._validate_fits(good)
    too_wide=encoded([fits.PrimaryHDU(),fits.ImageHDU(np.ones((16,2049),dtype='float32'),name='IMAGE')])
    with pytest.raises(ValueError,match='presupuesto'):
        sia._validate_fits(too_wide)
    with pytest.raises(ValueError,match='IMAGE'):
        sia._validate_fits(encoded([fits.PrimaryHDU()]))
    with pytest.raises(ValueError,match='FITS'):
        sia._validate_fits(good[:-1])


def test_gaia_redirect_and_oversized_csv(monkeypatch):
    calls=[]
    def redirect(request):
        calls.append(str(request.url))
        return httpx.Response(302,headers={'Location':'https://evil.example/'})
    transport(monkeypatch,redirect)
    with pytest.raises(ValueError,match='CSV'):
        asyncio.run(gaia.gaia_catalog(10,20,.025))
    assert len(calls)==1
    transport(monkeypatch,lambda request:httpx.Response(200,content=b'x'*(512*1024+1)))
    with pytest.raises(ValueError,match='demasiado grande'):
        asyncio.run(gaia.gaia_catalog(10,20,.025))
