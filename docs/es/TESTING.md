# Checklist de calidad

[Español](README.md) · [English](../en/TESTING.md) · [Pruebas bilingües](BILINGUISMO.md)

> Checklist histórico conservado. En la interfaz actual las tres imágenes se muestran juntas; abrir el modo IRSA no consulta el archivo hasta pulsar Buscar.

## Verificación rápida

- `python scripts/smoke_test.py` debe mostrar CORRECTO.
- `python -m pytest tests -q` debe pasar.
- `python scripts/check_env.py` comprueba módulos científicos disponibles.

## Prueba manual de la interfaz

1. Abrir inicio y cambiar entre 5 secciones del menú.
2. En Explorador, seleccionar Campo de prueba, buscar en modo Demo, comparar dos épocas.
3. Mover el deslizador antes/después y abrir el mapa diferencial.
4. Abrir Detector, analizar cambios y exportar CSV.
5. En Academia, completar lecciones y quiz; recargar y verificar que conserva el progreso.
6. Cambiar a NASA / IRSA; comprobar que el estado cambia y que no queda la imagen simulada en el comparador.
7. Si hay conexión, recuperar listados SIA2 e intentar dos épocas de igual detector (puede que no existan).
8. Ensayar resolución de 375 px y 1280 px; comprobar que menú y controles son accesibles.

## Criterios de aceptación

- No aparecen errores JavaScript ni errores 500 en modo demo.
- Las imágenes están correctamente identificadas como simuladas o IRSA.
- No existe mensaje que afirme un descubrimiento planetario.
- La app no ejecuta búsquedas remotas automáticamente sin seleccionar modo real.
- IRSA y Gaia se consultan exclusivamente mediante HTTPS y sus URLs oficiales.
