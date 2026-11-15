# Opcion desde la terminal PowerShell abierta en C:\hacket
Set-Location $PSScriptRoot
if (-not (Test-Path '.venv\Scripts\python.exe')) {
  py -3.12 -m venv .venv
  if ($LASTEXITCODE -ne 0) { throw 'Se requiere Python 3.12. Instálalo desde python.org.' }
}
& '.\.venv\Scripts\python.exe' -m pip install -r 'backend\requirements.txt'
if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación de dependencias.' }
& '.\.venv\Scripts\python.exe' 'scripts\launch.py'
