# Guion de demostración ante los jueces (3 minutos)

## 0:00–0:30 · El problema

«El Planeta Nueve todavía es una hipótesis. Tenemos instrumentos que nos permiten observar el cielo infrarrojo, pero comparar múltiples observaciones requiere herramientas accesibles y científicamente responsables».

## 0:30–1:10 · Mostrar el explorador

Abre `http://127.0.0.1:8000`. En Vista general muestra el concepto. Pasa al explorador, confirma que **MODO DEMO = SIMULACIÓN**. Selecciona dos fechas y desplaza el comparador. Las estrellas permanecen fijas mientras un objeto se desplaza. El mapa diferencial resalta cambios de brillo.

## 1:10–1:45 · Detector

Pulsa «Analizar diferencias». Muestra las posiciones candidatas, su desplazamiento en píxeles y la puntuación en σ. Explica por qué señales variables también aparecen y por qué se descartan falsos positivos. Exporta el CSV. **No digas que el objeto simulado es Planeta Nueve.**

## 1:45–2:15 · NASA real

Cambia a NASA / IRSA y ejecuta una búsqueda en campo de prueba. Presenta los metadatos reales de NASA/IPAC y, si existen dos épocas compatibles y la red responde, muestra sus recortes FITS. Si no hay cobertura o falla el archivo, explica que el modo demo preserva la experiencia de evaluación. Indica claramente que aún es necesario igualar canales de longitud de onda antes de derivar movimiento real.

## 2:15–2:45 · Educación e impacto

Abre Academia espacial, completa una lección y una pregunta. Explica que cualquier estudiante puede aprender qué es una detección preliminar y la importancia de validar la ciencia.

## 2:45–3:00 · Cierre

«No prometemos haber encontrado Planeta Nueve. Entregamos una experiencia open science replicable que conecta datos públicos, análisis y educación, con una ruta clara para mejorar la validación científica».

## Preparación del día

- Ejecuta las pruebas sin red: `python -m pytest tests -q`.
- Ensaya modo demo al menos dos veces.
- Prueba el acceso IRSA con la red real del local; no supongas que funcionará siempre.
- Lleva un archivo CSV exportado y captura de la demo como respaldo.
- Mantén claro qué hallazgos son simulados y cuáles provienen del archivo auténtico.
