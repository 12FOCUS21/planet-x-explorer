"""Small single-process public profile. This is not a security certification."""
from __future__ import annotations

import os
import time
from collections import deque
from dataclasses import dataclass
from urllib.parse import urlsplit

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware


@dataclass(frozen=True)
class PublicSettings:
    enabled: bool
    origin: str | None

    @classmethod
    def from_env(cls) -> 'PublicSettings':
        mode=os.getenv('PX_PUBLIC_MODE','0')
        if mode not in ('0','1'):
            raise ValueError('PX_PUBLIC_MODE debe ser 0 o 1')
        if mode=='0':
            return cls(False,None)
        # Render exposes its own exact URL at runtime; a custom domain needs
        # PX_PUBLIC_ORIGIN explicitly. Never accept arbitrary Host headers.
        origin=os.getenv('PX_PUBLIC_ORIGIN') or os.getenv('RENDER_EXTERNAL_URL') or ''
        try:
            parsed=urlsplit(origin)
            valid=(parsed.scheme=='https' and bool(parsed.hostname)
                   and parsed.port in (None,443) and not parsed.username and not parsed.password
                   and parsed.path in ('','/') and not parsed.query and not parsed.fragment
                   and origin==f'https://{parsed.hostname}')
        except ValueError:
            valid=False
        if not valid:
            raise ValueError('PX_PUBLIC_MODE exige PX_PUBLIC_ORIGIN=https://host exacto (o RENDER_EXTERNAL_URL)')
        return cls(True,origin)


CONTENT_POLICY=("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; connect-src 'self'; font-src 'self'; "
                "object-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")


def apply_security(app: FastAPI, settings: PublicSettings) -> None:
    if settings.enabled:
        assert settings.origin is not None
        app.add_middleware(TrustedHostMiddleware,allowed_hosts=[urlsplit(settings.origin).hostname],
                           www_redirect=False)

    # Per-process quota; do not trust X-Forwarded-For (spoofable). On a shared
    # reverse proxy these limits are shared by everyone behind that proxy.
    recent:dict[str,deque[float]]={}

    @app.middleware('http')
    async def secure_response(request: Request, call_next):
        def error(status:int, message:str):
            return JSONResponse({'detail':message},status_code=status)

        path=request.url.path
        if settings.enabled:
            if path in ('/docs','/redoc','/openapi.json'):
                response=error(404,'No encontrado')
            elif request.method=='POST' and path.startswith('/api/') and request.headers.get('origin') not in (None,settings.origin):
                response=error(403,'Origen no permitido')
            elif request.method=='POST' and path=='/api/compare':
                response=error(404,'Usa /api/compare/jobs')
            elif request.method=='POST' and path.startswith('/api/') and await oversized_body(request):
                response=error(413,'Solicitud demasiado grande')
            elif (path=='/api/gaia' or path=='/api/compare/jobs' and request.method=='POST'
                  or path=='/api/observations' and request.query_params.get('mode','demo')=='real'):
                now=time.monotonic()
                if len(recent)>2048:
                    recent.clear()  # Memory bound; this profile is not a distributed WAF.
                ip=request.client.host if request.client else 'unknown'
                calls=recent.setdefault(ip,deque())
                while calls and calls[0]<now-60:
                    calls.popleft()
                if len(calls)>=30:
                    response=error(429,'Límite temporal alcanzado; reintenta más tarde')
                    response.headers['Retry-After']='60'
                else:
                    calls.append(now)
                    response=await call_next(request)
            else:
                response=await call_next(request)
        else:
            response=await call_next(request)

        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='no-referrer'
        response.headers['X-Frame-Options']='DENY'
        response.headers['Permissions-Policy']='camera=(), microphone=(), geolocation=()'
        if path not in ('/docs','/redoc'):
            response.headers['Content-Security-Policy']=CONTENT_POLICY
        if settings.enabled:
            response.headers['Strict-Transport-Security']='max-age=31536000'
            response.headers['Cache-Control']='no-store' if path.startswith('/api/') else response.headers.get('Cache-Control','no-cache')
        return response


async def oversized_body(request: Request) -> bool:
    """Stop consuming a POST after 4 KiB, even without Content-Length."""
    try:
        length=int(request.headers.get('content-length','0'))
    except ValueError:
        return True
    if length>4096 or length<0:
        return True
    chunks=[]
    size=0
    async for chunk in request.stream():
        size+=len(chunk)
        if size>4096:
            return True
        chunks.append(chunk)
    # _CachedRequest (Starlette's HTTP middleware) replays this bounded body
    # to FastAPI's JSON parser; no unbounded request.body() call is made.
    request._body=b''.join(chunks)
    return False
