# Mejora de diseño — Planet X Explorer

[Español](README.md) · [English](../en/DESIGN_IMPROVEMENTS.md)

> Registro histórico de diseño; no describe por sí solo la portada vigente.

Versión visual basada en una galería editorial de astronomía, inspirada en la composición de fotografías de Flickr. **La lógica científica no se modificó.**

## Cambios visibles

- Portada de estética observatorio: tipografía más clara, navegación compacta, tonos oscuros y acentos cálidos.
- Galería destacada con una imagen principal que sigue utilizando `homePreview` y cambia automáticamente cuando el usuario termina una comparación.
- Dos ilustraciones astronómicas locales (sin llamadas a servidores externos). Cada una se identifica como **ilustración** o **arte conceptual**, nunca como datos reales de SPHEREx.
- Las tres imágenes **A, B y diferencia** se presentan como un mosaico oscuro continuo. Conservan las leyendas y los identificadores que usan los scripts para mostrar los FITS reales.
- El visor de comparación, selector de épocas, controles, detección, academia, fuentes y vista 3D siguen funcionando con su código original.
- Adaptación de la portada, galería y panel de imágenes a pantallas pequeñas.
- La página inicial ahora es `Inicio`, para que el usuario vea la nueva portada al abrir la aplicación. Se conserva el acceso a `Observaciones` en el menú y en los botones de portada.

## Archivos modificados

- `frontend/index.html`: estructura y textos de presentación de la portada, enlace al tema nuevo.
- `frontend/js/main.js`: cambio de vista inicial, de Explorador a Inicio, únicamente.

## Archivos añadidos

- `frontend/css/editorial-gallery.css`: hoja de estilo adicional. No se borró `styles.css`.
- `frontend/assets/infrared-art.svg`: ilustración local, no datos reales.
- `frontend/assets/planet-art.svg`: arte conceptual local, no un planeta detectado.
- Este documento.

## Archivos intencionalmente no modificados

- Todos los archivos de `backend/`, incluidos los clientes de NASA/IPAC IRSA.
- Los scripts `frontend/js/api.js`, `explorer.js`, `detection.js`, `academy.js` y `orbit3d.js`.
- Configuración del servidor, tests y lanzadores Windows.

## Cómo ver el diseño

1. Extrae el ZIP en una carpeta nueva.
2. Ejecuta `INICIAR_WINDOWS.bat` desde Windows.
3. Abre la dirección local que indique el iniciador y pulsa `Inicio` para ver la galería.
4. En `Observaciones` selecciona épocas y ejecuta `Comparar` para ver el mosaico de imágenes científicas.
5. Si el navegador muestra el diseño antiguo, usa `Ctrl + F5`.

> La mejora es **solo visual**. No soluciona ni modifica posibles fallos de conectividad, tiempos de respuesta o disponibilidad de imágenes de los servidores NASA/IPAC. El diseño tampoco equivale a verificación científica del análisis.

## Rediseño Observatory Edition (15 noviembre 2026)
- Se añadió una navegación horizontal, cabecera compacta y jerarquía editorial nueva.
- Portada con arte astronómico local comprimido, tipografía protagonista y simulador orbital 3D visible (arte visual, no datos reales).
- Galería de tres ilustraciones y paneles de observación diferenciados de la portada, sin cambiar los IDs de imágenes ni las APIs.
- Áreas funcionales con formularios claros, gráficos sobre fondo oscuro, estados y etiquetas legibles.
- CSS nuevo `frontend/css/observatory-premium.css`; 3 imágenes JPG locales en `frontend/assets/`.
- El contenido de arte conceptual no representa imágenes SPHEREx ni observaciones de IRSA; estas siguen apareciendo únicamente al consultar/analizar los datos.
