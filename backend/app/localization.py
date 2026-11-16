"""Translate JSON presentation strings without mutating sessions or scientific values."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from urllib.parse import parse_qs

from .config import FRONTEND

CATALOG=json.loads((FRONTEND/'locales'/'en.json').read_text(encoding='utf-8'))


def compile_template(source: str, target: str):
    names=[]
    parts=[]
    for part in re.split(r'(\{\w+\})',source):
        if re.fullmatch(r'\{\w+\}',part):
            name=part[1:-1];names.append(name)
            parts.append(r'([\d.+-]+)' if name in {
                'count','number','total','threshold','radius','size','x','y','distance'
            } else r'(.+?)')
        else:
            parts.append(re.escape(part))
    return re.compile('^'+''.join(parts)+'$'),target,names


TEMPLATES=[compile_template(s,t) for s,t in CATALOG.items() if '{' in s]
PHRASES=re.compile(r'(?<![^\W\d_])(?:'+'|'.join(
    re.escape(s) for s in sorted(CATALOG,key=len,reverse=True) if '{' not in s
)+r')(?![^\W\d_])')


@lru_cache(maxsize=3000)
def translate(text: str) -> str:
    if text in CATALOG:
        return CATALOG[text]
    for pattern,target,names in TEMPLATES:
        match=pattern.fullmatch(text)
        if match:
            captures={name:translate(value) for name,value in zip(names,match.groups())}
            return re.sub(r'\{(\w+)\}',lambda m:captures[m[1]],target)
    return PHRASES.sub(lambda m:CATALOG[m[0]],text)


def localized(value):
    if isinstance(value,str):return translate(value)
    if isinstance(value,list):return [localized(item) for item in value]
    if isinstance(value,dict):return {key:localized(item) for key,item in value.items()}
    return value


class LanguageMiddleware:
    """Opt-in English via ?lang=en or Accept-Language; Spanish remains the default."""
    def __init__(self,app):self.app=app

    async def __call__(self,scope,receive,send):
        if scope['type']!='http' or not scope.get('path','').startswith('/api/'):
            return await self.app(scope,receive,send)
        headers=dict(scope.get('headers',[]))
        query=parse_qs(scope.get('query_string',b'').decode('ascii',errors='ignore'))
        requested=query.get('lang',[None])[0]
        if requested not in ('en','es'):
            requested=headers.get(b'accept-language',b'es').decode('ascii',errors='ignore').split(',')[0].split(';')[0].split('-')[0].lower()
        language='en' if requested=='en' else 'es'
        start=None;chunks=[]

        async def localized_send(message):
            nonlocal start
            if message['type']=='http.response.start':
                content_type=dict(message.get('headers',[])).get(b'content-type',b'')
                if b'application/json' in content_type:
                    start=message
                    return
            if message['type']=='http.response.body' and start is not None:
                chunks.append(message.get('body',b''))
                if message.get('more_body',False):return
                body=b''.join(chunks)
                if language=='en':
                    body=json.dumps(localized(json.loads(body)),ensure_ascii=False,separators=(',',':')).encode('utf-8')
                output_headers=[(k,v) for k,v in start.get('headers',[]) if k.lower() not in (b'content-length',b'content-language',b'vary')]
                vary=dict(start.get('headers',[])).get(b'vary',b'')
                output_headers.extend([(b'content-length',str(len(body)).encode()),(b'content-language',language.encode()),(b'vary',vary+b', Accept-Language' if vary else b'Accept-Language')])
                await send({**start,'headers':output_headers})
                await send({**message,'body':body})
                return
            await send(message)

        await self.app(scope,receive,localized_send)
