# Aplicación y documentación en Español / English

[Español](README.md) · [English](../en/BILINGUAL.md) · [Índice general](../README.md)

## Cambio de idioma

El selector **Español / English** de la cabecera está disponible en escritorio y móvil. Español es el idioma inicial si no hay preferencia. Se guarda en `localStorage` bajo `px-language`; si el almacenamiento está bloqueado, el cambio sigue funcionando en la página actual. No se utiliza traducción en línea, API de pago ni servicio permanente.

Se traducen navegación, portada, formularios, estados, etiquetas accesibles, resultados, academia, cuestionario, mensajes conocidos del servidor y descripciones del CSV. Los nombres institucionales, identificadores técnicos, coordenadas, fechas y valores científicos no cambian. Las capturas históricas incluidas en documentos traducidos pueden conservar rótulos españoles, con advertencia explícita.

Cambiar idioma no consulta IRSA, modifica coordenadas, borra observaciones, reinicia comparaciones o respuestas del cuestionario. La preferencia persiste al recargar. La selección de idioma de la aplicación no modifica archivos Word/PDF ya descargados: usa la versión correspondiente en `docs/es/` o `docs/en/`.

## Implementación y pruebas

- Catálogo local: `frontend/locales/en.json`; motor de presentación: `frontend/js/i18n.js`.
- La traducción conserva textos de origen y actualiza texto/atributos, sin sustituir HTML, IDs, valores de entrada ni manejadores.
- API: `?lang=en` o `Accept-Language: en` para JSON inglés; español predeterminado. Cabeceras `Content-Language` y `Vary`. Los datos de sesión no se modifican y los PNG no se traducen.
- El navegador solicita JSON español canónico para no alterar la lógica de trabajos; localiza la presentación y las descripciones del CSV. Los nombres de columnas científicas siguen estables.
- Python: `python -m pytest tests -q` desde la raíz, con dependencias instaladas. Suite ampliada de 44 pruebas; los registros históricos conservan sus cifras originales.
- UI: `cd frontend`, `npm ci`, `npm run qa:ui`. Recorre ambos idiomas, cambio durante trabajos, CSV, lección abierta, respuestas del quiz, persistencia, errores IRSA simulados, escritorio/móvil y axe.

Estas comprobaciones no prueban una nueva descarga real IRSA, un teléfono físico, certificación integral de accesibilidad o despliegue público. La operación sigue siendo local y bajo demanda, con presupuesto previsto de hosting de 0 USD.

## Organización

La documentación española está en `docs/es/` y la inglesa en `docs/en/`. El README raíz permite elegir idioma y `docs/README.md` organiza todos los temas. Las rutas Markdown anteriores conservan pequeños índices de compatibilidad para enlaces ya compartidos. Se preserva el historial de Git y los límites científicos del proyecto.
