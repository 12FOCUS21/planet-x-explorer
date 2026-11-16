# Correcciones del 15 de noviembre de 2026

[Español](README.md) · [English](../en/CORRECTIONS.md)

> Registro histórico conservado: las 20 pruebas y el entorno Linux corresponden a esa revisión, no al último QA bilingüe.

## Alcance
Se mantiene FastAPI + HTML/CSS/JavaScript del ZIP recibido. No es una reescritura.

## Causas encontradas y cambios
- La selección inicial usaba los dos primeros registros, aunque no pasaran la
  validación. Ahora el backend calcula pares permitidos; la interfaz propone
  uno y deshabilita opciones B incompatibles.
- Las fechas perdían la hora: dos observaciones de un día quedaban indistinguibles.
  Ahora se preserva el timestamp completo; un mismo instante sigue rechazándose.
- Las descargas eran secuenciales y sin recuperación. Ahora A/B se descargan
  concurrentemente, con hasta tres intentos y un plazo total de 150 segundos.
- Las consultas de DR1 y QR3 también son concurrentes y se reutilizan cinco minutos.
- La petición SIA se centra en la posición solicitada para reducir imágenes que
  solo rozan el campo y no cubren el centro. No se supone que todo el recorte tenga cobertura.
- El centro del recorte indica explícitamente grados, como el tutorial IRSA.
- Las descargas se validan como FITS completos antes de escribirlos atómicamente.
  Se elimina caché corrupta y se migra caché válida de la versión anterior.
- POST /api/compare/jobs devuelve un identificador inmediatamente. El navegador
  consulta el progreso, muestra mensajes de error persistentes y reutiliza trabajos.
  Se mantiene POST /api/compare para clientes anteriores.
- Lectura, reproyección y render se ejecutan fuera del bucle de peticiones.
- La interfaz espera a que los tres PNG carguen antes de presentarlos como listos,
  ignora búsquedas antiguas y limpia resultados cuando cambia la selección.
- A y B utilizan límites de color compartidos; se respeta la proporción del recorte.
- Se conserva la precisión del ruido MAD en vez de redondearlo a cero en datos débiles.
- Ilustración de esfera/orbita 3D ligera, sin librerías remotas; animación pausada
  fuera de pantalla y compatible con preferencia de movimiento reducido.
- render.yaml y PUBLICAR_GRATIS.md preparan alojamiento Python gratuito.

## Pruebas realizadas
- 20 pruebas automáticas aprobadas: API, validación de pares, rechazo de coordenadas,
  generación demo, trabajos asíncronos, reutilización, fallos recuperables,
  FITS incompleto, HTML erróneo, caché antigua y conservación de escala de ruido.
- Se ajustó la prueba de movimiento demo para usar épocas 0/2, el par ya validado
  en test_analysis.py. El detector heurístico no garantiza asociar movimiento en
  todos los pares (incluido 0/1); no se modificó el algoritmo de asociación.
- Navegador: modo Demo → Buscar → Comparar. Los tres PNG visibles midieron 440x440.
  Se comprobó también navegación y esfera 3D en Vista general.
- Ocho FITS incluidos por el usuario pasaron validación de integridad.
- Par real incluido: 06c694ab… y e655153b…, IMAGE de 63x63, detector 1,
  fechas 2025-09-06T04:00:52.347 y 2025-09-13T03:57:54.918.
  Lectura, reproyección y generación de A/B/diferencia correctas; cobertura
  reproyectada 0.989669942, fracción finita común 0.9897. Esto prueba procesamiento,
  no equivalencia espectral ni un objeto en movimiento.

Entorno de pruebas: Linux / Python 3.12. La ejecución Windows no se probó aquí.
Un aviso de deprecación FastAPI/Starlette/httpx no impidió las 20 pruebas.

## Lo que NO pudo comprobarse
- Nueva consulta/descarga completa desde IRSA: agotó el tiempo de espera de este
  entorno. Los reintentos se verificaron con transporte HTTP simulado; no se
  declara disponibilidad de NASA ni una descarga nueva exitosa.
- Página oficial del reto: el enlace devolvió error de acceso/503 desde este
  entorno; no se verificaron todas las bases, duración ni criterios del jurado.
- Publicación pública: no hay cuenta de alojamiento conectada; no se desplegó.
- No hay calibración LVF/ePSF completa ni propagación de VARIANCE y FLAGS.
  La aplicación sigue mostrando candidatos exploratorios, no descubrimientos.

## Reproducción
Desde la raíz: `python -m pytest -q` con backend/requirements.txt instalado.
Las pruebas de red usan respuestas controladas y no consumen datos de IRSA.
Los FITS de caché originales no se redistribuyen en este ZIP ligero.

## Fuentes
- https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/
- https://caltech-ipac.github.io/irsa-tutorials/spherex-intro/
- https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/
- https://www.spaceappschallenge.org/2026/challenges/planet-x-and-spherex/?tab=resources
- https://render.com/docs/free
- https://render.com/docs/deploy-fastapi
