# Planet X Explorer — Observatory Edition

[Español](README.md) · [English](../en/OBSERVATORY_EDITION.md)

> Registro histórico de diseño; la portada actual puede diferir de las frases citadas.

## Qué cambió

- Arquitectura visual rediseñada: navegación principal horizontal en PC, menú lateral desplegable en móvil.
- Portada cinematográfica con tipografía de exposición, fotografía espacial **conceptual** generada para esta interfaz y animación orbital interactiva en canvas.
- Galería de tres imágenes grandes, con textos integrados, etiquetada como ilustración.
- Vistas funcionales rediseñadas: formularios legibles en fondo claro, comparador de imágenes sobre fondo oscuro, detector, academia y fuentes con la misma guía visual.
- Ajustes de diseño adaptable para escritorio, portátil y móvil.

## Qué NO cambió

- Ningún archivo de `backend/`.
- Las rutas de FastAPI, conexión IRSA, carga de FITS ni el procesamiento científico.
- Los identificadores de HTML que usan los scripts originales y la navegación SPA.

## Archivos de diseño

- `frontend/css/observatory-premium.css` (nuevo, cargado al final)
- `frontend/index.html` (estructura y textos de portada actualizados; la estructura científica conserva ID)
- `frontend/js/orbit3d.js` (render visual 3D, no scientific)
- `frontend/assets/stellar-nursery.jpg`, `infrared-field.jpg`, `deep-field.jpg` (arte conceptual generado, **no imágenes NASA**)

## Cómo ver la versión nueva en Windows

1. Extrae este ZIP **en una carpeta nueva** (no mezcles con el ZIP viejo).
2. Ejecuta `INICIAR_WINDOWS.bat`.
3. Abre la URL local indicada por el iniciador en Chrome.
4. Si ya tenías una pestaña abierta, presiona `Ctrl + Shift + R` para hacer una recarga completa.
5. La nueva portada tiene fondo de estrellas azul-violeta, el título `EL UNIVERSO NO ESPERA.` y menú horizontal en PC; si aún ves el menú lateral y el título `Otra forma de mirar el cielo`, sigues ejecutando la versión antigua.

## Nota sobre las imágenes

Las imágenes de la portada son ilustraciones artísticas de interfaz, no fotografías científicas ni detecciones reales. La aplicación muestra las imágenes FITS correspondientes a su flujo NASA/IRSA solamente al realizar las consultas y comparaciones. Las ilustraciones no pueden utilizarse como evidencia científica.
