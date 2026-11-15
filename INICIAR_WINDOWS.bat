@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
cls
echo ============================================================
echo       PLANET X EXPLORER - INICIADOR WINDOWS
echo ============================================================
echo.
if not exist ".venv\Scripts\python.exe" (
 echo [1/3] Creando entorno virtual Python 3.12...
 py -3.12 -m venv .venv
 if errorlevel 1 (
   echo Python 3.12 no encontrado con py. Intentando python...
   python -m venv .venv
   if errorlevel 1 goto failed
 )
)
echo [2/3] Verificando / instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r "backend\requirements.txt"
if errorlevel 1 goto failed
echo [3/3] Iniciando la aplicacion...
".venv\Scripts\python.exe" "scripts\launch.py"
echo.
echo Servidor detenido.
pause
exit /b 0
:failed
echo.
echo ERROR: revisa la version de Python, Internet y el mensaje de arriba.
echo Instala Python 3.12 desde https://www.python.org/downloads/
pause
exit /b 1
