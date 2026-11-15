"""Inicia la API, espera healthcheck y abre el explorador predeterminado."""
import subprocess
import os
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PORT=int(os.getenv('PX_PORT','8000'))
URL=f'http://127.0.0.1:{PORT}/'

def main():
    print('\n  PLANET X EXPLORER / MISSION CONTROL')
    print('  Servidor local: '+URL)
    print('  Para apagarlo: Ctrl + C\n')
    cmd=[sys.executable,'-m','uvicorn','backend.app.main:app','--host','127.0.0.1','--port',str(PORT)]
    # Evitar conflicto al abrir una segunda ventana con la misma aplicación.
    try:
        with urllib.request.urlopen(URL+'api/health',timeout=1.0) as r:
            if b'Planet X Explorer' in r.read():
                print('  La aplicación ya está activa. Abriendo navegador...')
                webbrowser.open(URL)
                return 0
    except Exception:
        pass
    proc=subprocess.Popen(cmd,cwd=ROOT)
    try:
        for _ in range(80):
            if proc.poll() is not None:
                print('El servidor terminó inesperadamente. Comprueba la consola.')
                return 1
            try:
                with urllib.request.urlopen(URL+'api/health',timeout=.6) as r:
                    if r.status==200:
                        print('  ✓ LISTO: navegador abierto en '+URL)
                        webbrowser.open(URL)
                        break
            except Exception:
                time.sleep(.25)
        else:
            print('No se pudo detectar el servidor en el puerto configurado. Revisa si ya está ocupado.')
            return 1
        return proc.wait()
    except KeyboardInterrupt:
        print('\n  Cerrando Planet X Explorer...')
        return 0
    finally:
        if proc.poll() is None:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired: proc.kill()

if __name__=='__main__':raise SystemExit(main())
