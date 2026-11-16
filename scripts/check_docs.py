"""Offline validation of local documentation links and report packages."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def main():
    documents=[ROOT/'README.md',ROOT/'LEEME_PRIMERO.md',ROOT/'PUBLICAR_GRATIS.md',*sorted((ROOT/'docs').rglob('*.md'))]
    errors=[];checked=0
    for document in documents:
        text=document.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)',text):
            parsed=urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            checked+=1
            path=(document.parent/unquote(parsed.path)).resolve()
            if not path.exists():errors.append(f'{document.relative_to(ROOT)} -> {target}')
    for lang,name in [('es','Planet_X_Explorer_Informe_Profesional_Mejorado'),('en','Planet_X_Explorer_Professional_Report')]:
        for suffix in ['.docx','.pdf']:
            path=ROOT/'docs'/lang/(name+suffix)
            if not path.is_file():errors.append(f'Missing {path.relative_to(ROOT)}')
            elif suffix=='.docx':
                with zipfile.ZipFile(path) as archive:
                    if archive.testzip():errors.append(f'Corrupt Word archive: {path.name}')
            elif not path.read_bytes().startswith(b'%PDF-'):errors.append(f'Invalid PDF: {path.name}')
    es_deps=(ROOT/'docs/es/DEPENDENCIAS_PROBADAS_LINUX.txt').read_text(encoding='utf-8').splitlines()
    en_deps=(ROOT/'docs/en/TESTED_LINUX_DEPENDENCIES.txt').read_text(encoding='utf-8').splitlines()
    records=lambda lines:[line for line in lines if line and not line.startswith('#')]
    if records(es_deps)!=records(en_deps):errors.append('Historical dependency versions differ between languages')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'Documentation OK: {len(documents)} Markdown documents, {checked} local links, ES/EN Word/PDF and matching historical dependency records.')


if __name__=='__main__':main()
