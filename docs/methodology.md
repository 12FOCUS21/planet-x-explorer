# Metodología, supuestos y reproducibilidad

## 1. Búsqueda

La interfaz recibe ascensión recta RA (0 <= RA < 360), declinación Dec (-90 a +90) y radio angular 0.008–0.3 grados. En modo IRSA, el backend busca `spherex_dr1`, `spherex_qr3`, `spherex_dr1_deep` y `spherex_qr3_deep` por SIA2, **sin QR2**, y sin pedir API key. Solicita imágenes que **contengan el centro** con un círculo SIA de 0.000001°, independientemente del radio de la interfaz. Este último dimensiona el recorte FITS y no asegura la cobertura completa del área. Cada colección está limitada a 150 registros y 8 MB de respuesta; se avisa si IRSA declara `OVERFLOW` o se llega al límite de registros. La lista contiene metadatos reales, pero puede estar incompleta. Se ofrecen pares que cumplen la validación de metadatos y se conserva la hora completa de observación. El usuario elige dos épocas.

## 2. Recortes de SPHEREx

Las imágenes Level 2 son archivos FITS con varias extensiones; la principal se llama `IMAGE` y guarda brillo superficial en MJy/sr. Existen FLAGS, VARIANCE, ZODI y otras extensiones, pero la versión actual no las incorpora totalmente a la detección. Se solicita un recorte oficial en vez de transferir cada archivo completo (p. ej., ~70 MB por detector).

## 3. Alineación espacial

La referencia es la imagen A. La imagen B se reproyecta a las coordenadas WCS celestes de A con interpolación bilineal. Se rechaza un campo cuyo solapamiento válido sea inferior al 15%. En modo demo, ambas imágenes comparten píxeles; no se reproyectan.

## 4. Diferencia e indicios

Para cada época, se resta una aproximación gaussiana del fondo de sigma 9 píxeles. El mapa residual es una sustracción de alta frecuencia `B - A`, suavizado sigma 0.8 px. Se estima el ruido mediante desviación absoluta mediana (MAD) x 1.4826, sin imponer un piso fijo en unidades físicas. Se buscan máximos por encima de 5 veces ese ruido. Un desplazamiento solo se propone si el pico positivo y el negativo son vecinos mutuos, están a 5–110 píxeles y sus amplitudes residuales difieren como máximo por un factor de cuatro.

En datos reales también se exige misma colección, detector, instante de observación distinto y al menos 80% de solapamiento entre los intervalos espectrales declarados por IRSA. Si faltan esos metadatos, se rechaza el par. Este control reduce comparaciones evidentemente incompatibles, pero no garantiza equivalencia de respuesta LVF por píxel.

Este **5σ es un umbral heurístico**, no una significancia estadística debidamente calibrada: existen correlaciones entre píxeles, PSF variable, filtros y ruido no gaussiano. Los emparejamientos de picos también pueden ser artefactos. La puntuación no representa la probabilidad de Planeta Nueve.

## 5. Importante: SPHEREx no es una cámara convencional

El filtro variable lineal (LVF) genera longitudes de onda efectivas distintas a lo largo de los detectores. Dos imágenes del mismo detector, observadas en fechas diferentes, pueden no tener una respuesta espectral equivalente incluso tras alineación WCS. Las diferencias observadas podrían reflejar el muestreo espectral y no un movimiento real. Un análisis científico completo debería generar mapas a longitud de onda equivalente, incorporar calibración, VARIANCE y FLAGS y controlar la PSF.

## 6. Limitaciones actuales

- No hay corrección completa de efectos LVF ni comparación calibrada de longitud de onda.
- No hay propagación instrumental de incertidumbre mediante VARIANCE ni máscaras FLAGS en los resultados.
- No hay prueba sistemática de detecciones repetidas, no hay fotometría de candidatos validada.
- No hay crossmatch automático de candidatos con Gaia, MPC, JPL Horizons o WISE.
- No se ajustan órbitas o parámetros físicos.
- Solo se exponen regiones y observaciones que el archivo IPAC retorna en ese momento.

**Por ello ninguna lista de esta aplicación es evidencia directa de Planeta X.**

## 7. Demo diferenciada

`make_demo_pair()` crea un campo reproducible de 440 x 440 con estrellas fijas, una fuente variable, fondo suave, ruido y un objeto sintético móvil. Utiliza semilla determinista a partir de las coordenadas. Cada imagen se marca `simulated:true` y fuente `Simulación didáctica`, y sus fotos PNG incluyen una etiqueta de simulación en la interfaz. La intención es enseñar el método y demostrar que el flujo de trabajo no depende de Internet.

## 8. Ruta para extenderlo a descubrimientos verificables

1. Obtener mosaicos SPHEREx del mismo segmento espectral e igualar resolución/PSF.
2. Propagar máscaras y mapas de incertidumbre para un umbral físico.
3. Localizar señales repetibles en al menos 3 observaciones con fechas distintas.
4. Excluir objetos catalogados (MPC, Gaia, WISE), artefactos y fuentes variables.
5. Hacer ajuste orbital con residuos y estimación de incertidumbres.
6. Guardar recortes FITS, hashes, fechas y scripts reproducibles y pedir validación externa.
