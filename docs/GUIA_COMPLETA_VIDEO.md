# Planet X Explorer — proyecto completo y guion para video

> **Documento de preparación, no video grabado ni resultado científico.**
> Duración sugerida: 4–5 minutos. Recorrido principal: **Demo sintética**, reproducible sin Internet tras instalar las dependencias. El código está en un repositorio GitHub **público**; no hay aplicación desplegada ni URL pública **de la aplicación**.

## 1. La idea en una frase

**Planet X Explorer es una aplicación educativa para elegir una zona del cielo, comparar observaciones infrarrojas de dos épocas, examinar sus diferencias y aprender por qué una señal todavía no demuestra la existencia de un planeta.**

El Planeta Nueve o Planeta X sigue siendo una **hipótesis**. El objetivo no es anunciar su descubrimiento, sino hacer comprensible y comprobable una parte del proceso de búsqueda: **región → épocas → comparación → señales para revisión**.

## 2. ¿Para quién y qué problema resuelve?

Para estudiantes, público curioso y examinadores que quieran entender cómo se exploran cambios en imágenes astronómicas. Una diferencia entre dos imágenes puede deberse a movimiento, variabilidad, ruido o al instrumento. En vez de presentarla como un hallazgo automático, la aplicación deja ver las dos imágenes originales, el mapa residual, la procedencia de cada dato y los límites del análisis.

| Área | Qué puede hacer la persona usuaria |
| --- | --- |
| **Inicio** | Elegir claramente entre **Probar demo guiada** y **Explorar datos IRSA**. La galería de portada es ilustrativa, no una observación. |
| **Explorador** | Introducir ascensión recta (RA), declinación (Dec) y radio de recorte o usar un campo sugerido; buscar épocas y seleccionar un par A/B. |
| **Comparador** | Ver A, B y el residual **B − A** en una escala visual compartida después de completar la comparación. |
| **Análisis** | Revisar picos preliminares en el mapa, variar el umbral entre **2 y 10 σ** (5 σ inicial) y exportar un CSV etiquetado con su origen. |
| **Academia** | Completar tres lecciones y un cuestionario de cinco preguntas; el progreso educativo queda en el navegador. |
| **Fuentes** | Consultar procedencia, metodología y limitaciones; Gaia DR3 es una consulta auxiliar opcional, **no confirma candidatos**. |

La interfaz es responsive, permite navegación por teclado y respeta la preferencia de movimiento reducido. Las cargas muestran estados: **el 100 % de la comparación solo aparece cuando las tres imágenes están listas**. Su porcentaje representa hitos confirmados, **no tiempo restante**. Búsqueda y análisis permanecen indeterminados mientras esperan respuesta, en lugar de inventar un porcentaje.

## 3. Dos rutas que no deben confundirse

### Ruta A — Demo guiada (la recomendada para grabar)

1. Al pulsar **Probar demo guiada**, el servidor genera **cuatro épocas sintéticas** de un campo de 440 × 440 píxeles. Hay estrellas fijas, una fuente variable, ruido y una fuente artificial que cambia de posición. Las escenas son reproducibles para las mismas coordenadas.
2. Elige A y B; la aplicación prepara y muestra los tres PNG: A, B y B − A. Las etiquetas indican **SIMULACIÓN**. Ni las fechas ilustrativas ni el objeto artificial son observaciones de NASA.
3. Pulsa **Revisar diferencias**; selecciona una señal, explica su posición y prueba otro umbral. **Una señal con σ alto no equivale a una probabilidad de planeta**.
4. Puedes mostrar el CSV y la academia. La Demo funciona sin consultar IRSA; **sí necesita que el servidor local esté encendido**.

### Ruta B — Archivo NASA/IPAC IRSA (opcional, requiere Internet)

1. **Explorar datos IRSA** solo abre el formulario: **no contacta IRSA** al abrir la página ni al elegir este modo. La consulta empieza al pulsar **Buscar observaciones**.
2. El backend consulta por SIA2 cuatro colecciones de SPHEREx: `spherex_dr1`, `spherex_qr3`, `spherex_dr1_deep` y `spherex_qr3_deep`. **No hay fallback QR2**. Busca imágenes que contienen el **centro** indicado; el radio del formulario determina el tamaño del recorte posterior, no amplía la búsqueda a todo el círculo.
3. Se ofrecen pares por **metadatos**: misma colección y detector, fechas distintas y al menos 80 % de solapamiento de rangos espectrales declarados. Esto **no verifica equivalencia LVF por píxel**.
4. Si se elige un par y se pulsa **Comparar**, el servidor solicita recortes FITS de IRSA, lee la extensión `IMAGE`, alinea B con A mediante coordenadas WCS y genera las vistas A/B/diferencia. Esta ruta depende de cobertura, respuesta del archivo y red; puede no devolver un par compatible.
5. Si IRSA no devuelve datos o falla, **se muestra el estado de error o vacío**. No se sustituyen imágenes reales faltantes por una simulación.

**Importante para el video:** si no has ejecutado y comprobado una búsqueda y descarga IRSA durante esa grabación, muestra únicamente el formulario y explica que existe la ruta real **bajo demanda**. No narrar «estas son imágenes NASA» encima de capturas de la Demo. Esta revisión no verificó una nueva descarga IRSA completa; `docs/CORRECCIONES.md` registra procesamiento histórico de FITS aportados anteriormente, no una detección.

## 4. ¿Cómo funciona por dentro? (explicación sin jerga excesiva)

```text
Navegador (HTML/CSS/JavaScript)
  → API FastAPI en Python
  → Demo sintética  O  consulta bajo demanda a NASA/IPAC IRSA
  → selección de dos épocas compatibles por metadatos
  → FITS reales o dos escenas simuladas
  → alineación WCS en datos reales + resta de fondo
  → mapa B − A + picos preliminares
  → tres PNG, controles de revisión y CSV
```

- **Frontend (`frontend/`):** interfaz sin compilación obligatoria; distingue el origen Demo/IRSA, guía los tres pasos, oculta imágenes hasta terminar y muestra hitos de carga, errores y posibilidad de reintentar.
- **Backend (`backend/app/`):** FastAPI valida coordenadas y pares, consulta el archivo desde el servidor (el navegador no necesita llamar directamente a IRSA), procesa imágenes y devuelve resultados de sesión. Búsquedas y comparaciones se mantienen temporalmente en memoria; `data/cache/` guarda recortes locales y **no se sube a Git**.
- **Comparación (`backend/app/analysis/`):** en datos reales se reproyecta B sobre A con WCS. Se retira un fondo suavizado por imagen y se calcula el residual **B − A**. El ruido se estima de forma robusta mediante MAD; el detector busca picos positivos y posibles pares positivo/negativo compatibles con desplazamiento aparente. La Demo comparte píxeles y no necesita reproyección WCS.
- **Resultados:** las posiciones, la puntuación en σ y los desplazamientos en píxeles son **pistas para revisión humana**, no órbitas ni descubrimientos. El análisis puede recalcularse al cambiar el umbral; el CSV conserva la etiqueta SIMULACIÓN o IRSA.
- **Gaia DR3:** consulta opcional de estrellas de ESA para contexto, no clasificación automática de las señales.

**Límites que conviene explicar:** SPHEREx usa un filtro variable lineal (LVF); dos épocas del mismo detector pueden medir distintas longitudes de onda efectivas en un píxel. Aquí no se aplican completamente máscaras `FLAGS`, incertidumbres `VARIANCE`, corrección PSF ni descarte sistemático de objetos conocidos. No se calcula órbita ni se confirma Planeta X. Una coincidencia de metadatos **no es validación científica independiente**.

## 5. Guion de grabación: voz + acción en pantalla

La columna «voz» está escrita para leerla o adaptarla. Las duraciones son aproximadas; espera a que termine cada operación **sin acelerar o editar la carga para fingir un resultado**.

| Tiempo | Pantalla y acción | Voz sugerida |
| --- | --- | --- |
| **0:00–0:30** | Portada, título y dos rutas visibles. | «¿Cómo buscamos cambios en el cielo sin confundir una señal con un descubrimiento? Planet X Explorer convierte esa pregunta en un recorrido interactivo. El Planeta Nueve es todavía una hipótesis: esta herramienta no afirma haberlo encontrado.» |
| **0:30–1:00** | Señala **Probar demo guiada** y **Explorar datos IRSA**. Pulsa Demo. | «Ofrecemos dos caminos separados. La Demo crea imágenes sintéticas reproducibles y funciona sin Internet; la otra ruta puede consultar observaciones SPHEREx de NASA/IPAC IRSA, únicamente cuando alguien pulsa Buscar. Para esta demostración usaré la simulación, claramente etiquetada.» |
| **1:00–1:40** | Muestra las cuatro épocas, el selector A/B y el estado de carga. Pulsa **Comparar**. | «Elegimos una región y dos épocas. La interfaz valida el par y nos muestra el avance por etapas verificadas. El porcentaje no es una promesa de tiempo: llega a cien solo cuando las tres imágenes están listas. Antes de comparar, no se presentan imágenes como si ya se hubieran cargado.» |
| **1:40–2:20** | Enfoca A, B y B − A; recorre las etiquetas **SIMULACIÓN**. | «Aquí vemos el campo de referencia, la segunda época y su diferencia. Un punto que cambia puede ser movimiento aparente, una fuente variable, ruido o un efecto instrumental. Las imágenes de esta escena son totalmente artificiales; no representan una detección de NASA.» |
| **2:20–3:00** | Pulsa **Revisar diferencias**, selecciona una señal y mueve el umbral. | «El análisis destaca picos residuales para inspeccionarlos y permite ajustar la sensibilidad. Al cambiar el umbral recalcula los resultados. La puntuación en sigma es una medida heurística de contraste; por sí sola no identifica un planeta. El CSV conserva la procedencia de los datos.» |
| **3:00–3:30** | Muestra una lección, el cuestionario y la sección de fuentes. | «También enseñamos por qué hacen falta más épocas, controles y catálogos. La academia y la página de fuentes convierten el resultado visual en una oportunidad de aprender ciencia, no en una afirmación extraordinaria.» |
| **3:30–4:10** | Vuelve al inicio. Abre **Explorar datos IRSA** pero **no pulses Buscar** si no vas a verificar una respuesta real. | «Para datos reales, el servidor puede consultar DR1, QR3 y sus colecciones profundas, y solicitar recortes FITS al comparar. Que dos imágenes pasen filtros de metadatos no asegura igual longitud de onda efectiva en cada píxel. Sin una descarga verificada no mostraré la Demo como si fuera IRSA.» |
| **4:10–4:40** | Cierre en **Fuentes y método** o portada. | «Nuestra aportación es una experiencia clara, reproducible y honesta para explorar señales preliminares. El siguiente paso científico requiere calibración instrumental, más épocas y validación independiente. Primero entender el cambio; después comprobar qué significa.» |

### Si una consulta IRSA falla durante la grabación

Di: «La disponibilidad del archivo externo puede variar. Esta consulta no produjo un par verificable; el sistema no reemplaza esa ausencia con datos ficticios. Continuaremos con la Demo, que está identificada como sintética». **No pegues imágenes de la Demo sobre una narración que las llame observaciones reales.**

## 6. Preparación práctica antes de grabar

1. Desde la carpeta del proyecto, inicia `INICIAR_WINDOWS.bat` con Python 3.12 y las dependencias ya instaladas; abre `http://127.0.0.1:8000` en el **mismo equipo**. La primera instalación sí requiere Internet. `localhost` no es un enlace para el jurado remoto.
2. Mantén la ventana del servidor abierta. Cierra pestañas o notificaciones personales; graba una ventana de navegador a una anchura cómoda. Haz una prueba corta del micrófono y del texto en pantalla.
3. Ensaya el recorrido **Demo → A/B → Comparar → Revisar diferencias → Academia/Fuentes**. Espera a que A, B y B − A se carguen antes de decir «resultado listo». Las cifras de señales pueden variar según épocas, coordenadas y umbral: evita fijar un número en la locución.
4. Deja visible el distintivo **DEMO · SINTÉTICA** y menciona explícitamente que la ilustración 3D de la portada no es una observación. Si muestras IRSA, deja visible su estado independiente y prueba la conexión **en ese momento**.
5. Termina el servidor con `Ctrl+C`. El presupuesto previsto es **0 USD** y uso **bajo demanda**. El repositorio público de GitHub aloja código, **no la aplicación funcionando**; Render Free es solo una opción futura si el equipo autoriza hosting y confirma el enlace.

## 7. Evidencia y frases seguras para preguntas del jurado

- **Comprobado localmente:** 39 pruebas Python, smoke sintético de tres PNG y análisis; QA automatizado en Edge/axe sobre estados de Demo, carga, error, móvil, teclado y movimiento reducido, sin violaciones axe en los estados examinados. Estas pruebas **no certifican accesibilidad total ni seguridad**.
- **No comprobado en esta revisión:** un nuevo recorrido completo de búsqueda + descarga IRSA, rendimiento con público remoto, despliegue web, validación LVF por píxel ni detección científica independiente.
- **Frase correcta:** «La aplicación permite investigar cambios preliminares con una Demo sintética y una vía separada de consulta IRSA bajo demanda».
- **Evitar:** «Encontramos Planeta X», «estos píxeles de la Demo son NASA», «el 5σ demuestra un planeta», «ya está publicada la web» o «el sistema está certificado».

## 8. Archivos para ampliar cada tema

- [README.md](../README.md): instalación, funcionamiento y pruebas.
- [ENTREGA_JURADO.md](ENTREGA_JURADO.md): operación local y acceso remoto pendiente.
- [methodology.md](methodology.md): parámetros y limitaciones científicas.
- [CONTRASTE_ORBITLENS.md](CONTRASTE_ORBITLENS.md): comparación y diferencias con el repositorio hermano.
- [CORRECCIONES.md](CORRECCIONES.md): historial de pruebas con FITS previos y pendientes.
- [PUBLICAR_GRATIS.md](../PUBLICAR_GRATIS.md): posible alojamiento gratuito **no realizado**.

**Créditos:** SPHEREx y NASA/IPAC IRSA para la ruta de archivo; ESA Gaia DR3 para consulta auxiliar. Planet X Explorer es un proyecto educativo independiente, sin aval oficial de NASA o ESA.
