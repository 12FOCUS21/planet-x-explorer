# Guion de prueba para examinadores (sin servicio permanente)

[Español](README.md) · [English](../en/JURY_HANDOFF.md) · [Selector de idioma y QA](BILINGUISMO.md)

Para explicar objetivo, funcionamiento y límites en una grabación, ver
[GUIA_COMPLETA_VIDEO.md](GUIA_COMPLETA_VIDEO.md). Es un guion de preparación;
no significa que el video ya esté grabado.

## Si estás en el mismo equipo o compartes pantalla

1. Una sola vez: Python 3.12, Internet para instalar `backend/requirements.txt`.
2. El día de la prueba: doble clic en `INICIAR_WINDOWS.bat` desde la carpeta del
   proyecto, o `python scripts/launch.py` con el entorno virtual activado. Abre
   `http://127.0.0.1:8000` si el navegador no se abre. No expongas el puerto
   local a Internet. Verifica `/api/health` y que `backend`, `frontend` y `data`
   estén en la misma carpeta de proyecto.
3. Recorrido reproducible sin servicios externos: portada → **Probar demo
   guiada** → comprobar el resumen de cuatro épocas **sintéticas** → seleccionar
   A/B → **Comparar** → verificar A, B y B − A → **Revisar diferencias**.
   Seleccionar una señal para mostrar su posición; si se desea, mover el umbral
   σ para recalcular y visitar la academia. Las tres imágenes no se muestran
   hasta completar la comparación. **Todos los píxeles Demo son sintéticos**;
   los resultados no constituyen evidencia de un planeta.
4. Para probar la otra ruta, pulsar **Explorar datos IRSA** en la portada: solo
   abre el formulario. Con Internet, pulsar **Buscar observaciones** realiza
   la consulta real; **Comparar** solicita recortes FITS si existe un par
   compatible por metadatos. Puede no haber dos épocas comparables o el archivo
   remoto puede no responder. No presentar una prueba Demo como resultado IRSA
   ni sustituir silenciosamente una respuesta vacía por imágenes simuladas.
5. Apagar con `Ctrl+C` en la consola. Las sesiones en memoria expiran al detener.

## Si el jurado necesita abrir una URL desde fuera

Lee [PUBLICAR_GRATIS.md](PUBLICAR_GRATIS.md). Con presupuesto 0 USD se puede
probar Render Free **solo si el equipo autoriza una cuenta de hosting y el
despliegue**. La instancia puede dormir y arrancar lentamente; no almacena
resultados de forma persistente. Publicar con margen, abrir el enlace en una
ventana privada y repetir el recorrido completo antes de enviarlo. Mantener un
plan local por pantalla compartida si falla el proveedor gratuito. No compartir
`localhost` como URL para acceso remoto. Al terminar, desactivar el servicio
si se desea limitar la exposición pública.

## Qué decir y qué no decir

- Planet X / Planeta Nueve sigue siendo hipotético. El umbral 5σ es heurístico.
- La selección real coteja colección, detector, época y bandas por metadatos:
  **no calibra la longitud de onda LVF efectiva por píxel** ni sustituye la
  verificación independiente de artefactos, máscaras, varianzas u órbitas.
- DR1, QR3 y sus colecciones deep se consultan separadamente; sin fallback QR2.
- No se verificó un nuevo recorrido IRSA completo en esta revisión; la evidencia
  histórica de FITS reales está en `docs/CORRECCIONES.md`, no prueba hallazgos.
- No afirmar que hay detección confirmada, despliegue público o certificación de
  seguridad. Presentación y video siguen aplazados.

## Estado reproducible de esta revisión

En Windows/Python 3.12, `.\.venv\Scripts\python.exe -m pytest tests -q`:
**39 pruebas** (API, demo, referencias estáticas/estado inicial, cliente
simulado IRSA/Gaia, límites y perfil público); el smoke Python completó
health, Demo, tres PNG y detector. QA portátil reproducible: con Node.js
≥22.12 y Edge, ejecutar `cd frontend`, `npm ci`, `npm run qa:ui`. Arranca
temporalmente su propio servidor local en el puerto 8134; comprueba la ruta
Demo, tres PNG, carga con hitos confirmados hasta 100 %, error/reintento,
hover, movimiento reducido, revelado progresivo, análisis/umbral, academia,
modo IRSA solo al pulsar Buscar y estados móviles con axe. En búsqueda y
análisis no se inventa un porcentaje mientras espera la red; el 100 % solo
indica una respuesta procesada. Las respuestas IRSA de QA se **simulan en el
navegador**, no demuestran descarga real. Edge 1440×900 y
viewport móvil 390×844 sin errores JS ni violaciones axe en los estados
probados; se revisó también el desbordamiento en anchuras 360–1440 px.
No se probó teléfono físico. Ver
[CONTRASTE_ORBITLENS.md](CONTRASTE_ORBITLENS.md) para pendientes y comparación.

**El código de Planet X Explorer tiene un repositorio GitHub público separado de
OrbitLens, pero la aplicación no tiene URL pública ni despliegue.** Para dar
acceso remoto al jurado, el equipo debe autorizar hosting y una prueba externa.
El repositorio no incluye cachés FITS, `.venv` ni `frontend/node_modules/`.
