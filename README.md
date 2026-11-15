> Actualización 15-11-2026: empieza por [LEEME_PRIMERO.md](LEEME_PRIMERO.md). Publicación: [PUBLICAR_GRATIS.md](PUBLICAR_GRATIS.md).

> Uso previsto: **prueba bajo demanda para el jurado**, sin servicio permanente. Guion y preparación: [docs/ENTREGA_JURADO.md](docs/ENTREGA_JURADO.md). Contraste con OrbitLens: [docs/CONTRASTE_ORBITLENS.md](docs/CONTRASTE_ORBITLENS.md). El código se conserva en un [repositorio público](https://github.com/12FOCUS21/planet-x-explorer); **no existe una URL pública de la aplicación**.

# Planet X Explorer

**Para preparar un video:** [guía completa y guion escena por escena](docs/GUIA_COMPLETA_VIDEO.md).

**Memoria profesional del proyecto:** [Word editable](docs/Planet_X_Explorer_Informe_Profesional_Mejorado.docx) · [PDF](docs/Planet_X_Explorer_Informe_Profesional_Mejorado.pdf). Incluye equipo, objetivos, metodología, resultados y declaración de uso de IA.

**Plataforma web educativa para explorar y comparar observaciones infrarrojas de SPHEREx (NASA/IPAC IRSA), con modo demostración sin Internet.**

> ⚠️ El Planeta Nueve / Planeta X es una hipótesis, no un descubrimiento confirmado. Esta aplicación no puede confirmar un planeta. La demo es completamente SINTÉTICA; el modo IRSA es la única vía de observaciones SPHEREx auténticas.

## Inicio rápido: Windows 10/11

1. Abre esta carpeta (`backend`, `frontend` y `INICIAR_WINDOWS.bat` deben estar juntos); no hace falta que se llame `C:\hacket`.
2. Necesitas Python 3.12 (con `py -3.12 --version` comprobable) e Internet **solo para instalar dependencias**.
3. Doble clic en **`INICIAR_WINDOWS.bat`**. Se crea `.venv` si no existe, se comprueban las librerías y se abre el navegador.
4. Si el navegador no se abre solo, visita **http://127.0.0.1:8000**. Para la prueba sin Internet, pulsa **Probar demo guiada** en la portada: carga cuatro épocas **sintéticas**. Elige las épocas A y B, pulsa **Comparar** y luego **Revisar diferencias**. Ajusta el umbral del análisis si quieres recalcular las señales.
5. Para cerrar, vuelve a la terminal del servidor y pulsa `Ctrl+C`.

### Desde la terminal de VS Code (PowerShell)

```powershell
cd C:\ruta\Planet_X_Explorer
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe scripts\launch.py
```

> Si ya tienes `.venv` del proyecto anterior, puedes usarla. La instalación de pip no debería borrar tus archivos. **Haz una copia de la carpeta anterior** antes de mezclar el ZIP con archivos existentes.

### Linux/macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
.venv/bin/python scripts/launch.py
```

## Dos recorridos separados

- **Demo guiada:** un clic en la portada selecciona y busca cuatro épocas sintéticas. No consulta IRSA. Después selecciona A y B, pulsa **Comparar**, examina las tres imágenes y abre **Revisar diferencias**. Las imágenes se revelan **solo después de comparar** y llevan la etiqueta SIMULACIÓN; las señales son preliminares.
- **NASA / IRSA:** pulsa **Explorar datos IRSA** para abrir el formulario, **sin consultar todavía**. Introduce coordenadas o un campo sugerido y pulsa **Buscar observaciones** para iniciar la consulta. Una búsqueda sin resultados no se sustituye por datos Demo.

El indicador de progreso separa búsqueda → comparación → revisión. Las operaciones muestran estados animados y resultados: la comparación avanza por **hitos confirmados** del servidor y llega al 100 % cuando sus tres imágenes han cargado. Búsqueda y análisis no proporcionan progreso medible: muestran «en curso» hasta recibir una respuesta y solo entonces 100 %, o un error con opción de reintentar. **Ningún porcentaje estima el tiempo restante.** La vista de análisis permite seleccionar una señal para ver su posición, cambiar el umbral σ y exportar un CSV de resultados preliminares. La academia ofrece lecciones y cuestionario; no sustituye una validación científica.

## Consultar imágenes reales de SPHEREx

El Explorador tiene NASA / IRSA seleccionado por defecto, **pero no consulta IRSA hasta pulsar Buscar**. Para buscar un campo:

1. Ingresa RA y Dec del centro del cielo, o pulsa uno de los campos preestablecidos. El radio ajusta el tamaño del recorte FITS; la búsqueda SIA solicita imágenes que cubren el **centro**, no toda la región circular.
2. Pulsa **Buscar observaciones** y espera la respuesta del archivo IRSA.
3. Selecciona dos observaciones de fechas distintas y pulsa **Comparar** para descargar y visualizar sus recortes FITS reales.
4. Si IRSA no devuelve observaciones, prueba otras coordenadas. Aumentar el radio **no amplía esta búsqueda**. El modo Demo sigue disponible como opción separada.

La seleccion del campo se hace mediante coordenadas numericas y presets; el proyecto aun no incluye un mapa celeste interactivo. La busqueda y descarga real requieren Internet.

## Qué contiene

| Módulo | Funcionalidad |
|---|---|
| Vista general | Dos entradas inequívocas (Demo / IRSA), método, galería ilustrativa y navegación |
| Explorador | Región RA/Dec, campos preestablecidos, búsqueda simulada o SIA2 IRSA, selección de observaciones |
| Comparador | Rejilla temporal antes/después, recortes FITS, alineación por WCS, vista diferencial |
| Detector | Diferencia robusta, picos positivos/negativos, pares de desplazamiento, CSV de candidatos |
| Academia | Tres lecciones científicas, cinco preguntas, progreso local |
| Fuentes | Procedencia, metodología y limitaciones explícitas |
| Gaia DR3 | Consulta auxiliar de estrellas del campo al archivo ESA; no es clasificación automática |

**Modo demo:** funciona sin Internet después de instalar las dependencias. Genera imágenes sintéticas deterministas (4 épocas). No debe presentarse como evidencia NASA. Sirve para mostrar el recorrido completo y calibrar el pitch.

**Modo NASA/IRSA:** requiere Internet y respuesta de los servicios remotos. Consulta `spherex_dr1`, `spherex_qr3`, `spherex_dr1_deep` y `spherex_qr3_deep` vía SIA2 (sin QR2), descarga recortes FITS del servidor oficial, extrae la extensión `IMAGE` (MJy/sr), alinea WCS y produce vistas. La lista puede ser incompleta si IRSA la trunca o se alcanza MAXREC=150 por colección; se avisa en pantalla. Dos imágenes del mismo detector **no necesariamente usan la misma longitud de onda efectiva por píxel**: la comparación es orientativa. La selección puede fallar si no existen épocas distintas compatibles por metadatos para ese centro.

## Verificar sistema

```powershell
.\.venv\Scripts\python.exe scripts\check_env.py
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe -m pytest tests -q
```

### QA opcional de interfaz (sin consultas IRSA externas)

Requiere Node.js **22.12 o superior** y Edge instalado en Windows. Con las dependencias Python de arriba ya instaladas, desde la raíz del proyecto:

```powershell
cd frontend
npm ci
npm run qa:ui
```

El script arranca y detiene **su propio servidor local** en `127.0.0.1:8134` (no usa el servidor de la demostración en el puerto 8000), prueba la Demo, tres PNG, estados de carga y 100 %, error/reintento, umbral, hover, movimiento reducido, academia, menú móvil y accesibilidad automatizada con axe. Simula localmente una respuesta IRSA vacía y un fallo para comprobar que **solo se solicita tras pulsar Buscar** y que nunca aparece un fallback sintético; **no verifica conectividad ni descarga real de IRSA**. Si el puerto está ocupado, utiliza `PX_QA_PORT` para elegir otro; `PX_QA_PYTHON` selecciona un Python alternativo. Para otro sistema, instala Chromium con `npx playwright install chromium` después de `npm ci`; `PX_QA_BROWSER_CHANNEL` permite elegir un canal disponible. Instalar herramientas de QA requiere Internet una vez; ejecutar la Demo y el QA no.

Las comprobaciones axe cubren los estados automatizados, no garantizan por sí solas accesibilidad universal. El QA no forma parte de la ejecución normal de FastAPI: `frontend/` sigue sin compilación y `frontend/node_modules/` se ignora.

La documentación FastAPI local está en http://127.0.0.1:8000/docs; se oculta al activar el perfil público.

## Conexiones científicas

- SPHEREx Data Access, NASA/IPAC IRSA: https://irsa.ipac.caltech.edu/spherex-archive-documentation/spherex-data-access/
- Introducción a imágenes FITS: https://caltech-ipac.github.io/irsa-tutorials/spherex-intro/
- Cutouts: https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/
- Gaia DR3: https://gea.esac.esa.int/archive/

## Qué falta para una validación científica seria

El comparador no modela completamente las diferencias del filtro LVF de SPHEREx; no aplica sistemáticamente máscaras `FLAGS` ni ajuste de PSF; no modela incertidumbre de `VARIANCE` por píxel; no calcula órbitas ni cruza automáticamente todos los catálogos de objetos del Sistema Solar. Por tanto, los "candidatos" son **señales preliminares**. No podemos garantizar que las observaciones IRSA de una región concreta produzcan dos épocas comparables, ni que la red responda en el evento. Ver `docs/methodology.md`.

## Estructura

```
backend/app/api/         Rutas HTTP
backend/app/services/    SPHEREx, Gaia, WISE, demo
backend/app/analysis/    alineación, restas y detección
backend/app/models/      esquemas Pydantic
backend/app/utils/       FITS y generación de PNG
frontend/                HTML, CSS, JavaScript sin build step
data/cache/              caché de recortes FITS (local, ignorada por git)
scripts/                 inicio, autoprueba, verificación
tests/                   pruebas automatizadas
docs/                    arquitectura, metodología, fuentes, pitch
```

## Privacidad, licencia y créditos

No requiere cuenta de usuario ni claves API. El progreso de la academia se almacena en el `localStorage` del navegador. En perfil público, el servidor mantiene temporalmente la dirección de conexión en memoria para limitar consultas; el proveedor de hosting puede registrar accesos según su propia política. El ZIP contiene código original y ningún archivo de datos NASA predescargado. Usa las fuentes astronómicas sujetas a sus condiciones de atribución; consulta la documentación oficial para publicar resultados. Proyecto educativo independiente: **no existe afiliación ni aval oficial de NASA**.

Código disponible para uso y modificación educativa bajo licencia MIT (`LICENSE`).
