# Planet X Explorer frente a OrbitLens — revisión 15-11-2026

| Aspecto | Planet X Explorer (esta carpeta) | OrbitLens (repositorio hermano) |
| --- | --- | --- |
| Producto | FastAPI + HTML/CSS/JS, galería, comparador visual, detector exploratorio y academia/quiz; útil para contar el método en una sesión del jurado. | FastAPI + React/Vite, mayor énfasis en análisis reproducible, manifiestos de resultados y estados explícitos. |
| Datos | Demo sintética diferenciada. SIA2 a DR1, QR3 y deep, metadatos de origen, recortes FITS con `IMAGE`, alineación WCS y PNG. Sin QR2. Búsqueda real bajo demanda; SIA y Gaia acotados y sin redirects. | Igual separación demo/IRSA y cuatro colecciones, con manifiestos/hashes y evidencia parcial de campos reales documentada en su `HANDOFF.md`. |
| Ciencia | Cotejo de metadatos, no validación LVF por píxel; no propaga sistemáticamente FLAGS/VARIANCE ni corrige PSF. Picos heurísticos y pares desplazados, no detección confirmada. | Más trazabilidad y controles de cobertura/máscaras; también requiere validación científica independiente. |
| Pruebas | **39 pruebas locales** tras esta revisión, smoke sintético y QA Edge/axe reproducible desde `frontend/` con IRSA simulado, no descargado. Repositorio GitHub privado propio; sin CI ni URL pública de la aplicación. | Commit local `84428` en repo con remoto; su `HANDOFF.md` registra 215 pruebas Python, 34 E2E Edge, axe sin violaciones y CI; consultar el propio repositorio para confirmar el estado remoto vigente. |
| Hosting a 0 USD | Arranque local inmediato; `render.yaml` para ensayo en Render Free con origen HTTPS exacto en runtime y un worker. Disco/sesiones efímeros, sin garantía de disponibilidad. | Varias opciones en `HANDOFF.md`; Render Free también solo para demo, no para conservar evidencia. |

## Cambios puntuales aplicados aquí

- Consulta IRSA solo al pulsar Buscar; sin fallback sintético cuando falla el
  archivo. Se consultan cuatro colecciones, se avisa de `OVERFLOW`/MAXREC y
  se precisa que el radio define el recorte, **no** la búsqueda SIA del centro.
- Salidas SIA/Gaia sin redirecciones y con límite de lectura; FITS 2D acotados;
  mensajes remotos al cliente sin el texto crudo de excepciones.
- Perfil público opcional (activado en `render.yaml`): host/origen HTTPS exactos,
  cuotas por proceso detrás del proxy, cabeceras y cuerpo POST acotado; el modo
  local conserva la ruta heredada del comparador. **No es una certificación.**
- Mejoras de contraste, navegación por teclado y menú móvil; en Edge/axe no
  se encontraron violaciones en las vistas y estados recorridos. La revisión
  automática no reemplaza pruebas de accesibilidad con personas o dispositivos.
- Portada con entradas separadas Demo guiada/IRSA, paso a paso de búsqueda →
  comparación → revisión, resumen de resultados y revelado de imágenes solo
  tras comparar. Control interactivo de umbral y detalle de señales; el QA de
  interfaz vive en `frontend/qa/smoke.cjs` y se ejecuta sin red externa.
- Estados de operación visibles y responsive: hitos de comparación reales,
  barras indeterminadas cuando no hay métricas de avance, cierre al 100 %
  solo tras confirmar respuesta o imágenes y errores sin falsos completados.
  Animación de botones en dispositivos con hover y preferencia de movimiento
  reducido respetada.

## Qué NO se ha verificado aquí

No se ejecutó una **nueva búsqueda y descarga IRSA exitosa** en esta revisión,
ni se ensayó Render, un teléfono físico, una red externa o un navegador del
jurado. La documentación histórica `CORRECCIONES.md` registra trabajo previo
con FITS reales; no atribuye equivalencia espectral ni detección de un objeto.
El código de Planet X tiene su propio repositorio privado autorizado, separado
del de OrbitLens. Esto no equivale a una publicación web o ensayo con usuarios.
El siguiente paso operativo es [ENTREGA_JURADO.md](ENTREGA_JURADO.md).
