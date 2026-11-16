# Planet X Explorer — reparación de carga

[Español](README.md) · [English](../en/START_HERE.md)

Para pruebas del jurado bajo demanda, ver [ENTREGA_JURADO.md](ENTREGA_JURADO.md). Esta guía conserva las instrucciones históricas del paquete; no demuestra un despliegue público.

1. Cierra la ventana de Python de la versión anterior con Ctrl+C.
2. Extrae este ZIP en una carpeta nueva. Conserva la versión original como respaldo.
3. Abre INICIAR_WINDOWS.bat. La primera instalación requiere Internet y Python 3.12.
4. En NASA / IRSA pulsa Buscar observaciones y luego Comparar.
5. Ahora las opciones B incompatibles aparecen deshabilitadas y la comparación
   muestra progreso de descarga y procesamiento. Los recortes se descargan
   automáticamente: no tienes que descargar FITS uno a uno.
6. Para ver el elemento 3D, abre Vista general. Es una ilustración, no datos NASA.

Si NASA/IRSA tarda, espera el mensaje de estado. Ante un corte puedes reintentar:
se reutilizan los recortes completos y se descartan las descargas incompletas.
Si no hay pares compatibles no se generan imágenes falsas; cambia la época A
u otra región. El modo Demo usa datos sintéticos y lo indica claramente.

Este paquete conserva tu aplicación FastAPI/HTML. No incluye .venv ni tus capturas
personales. Las dependencias se instalan con el iniciador. Para publicación,
lee PUBLICAR_GRATIS.md. No se ha publicado en Internet desde esta conversación.

Consulta docs/CORRECCIONES.md para los cambios y pruebas. La solución sigue siendo
exploratoria: no confirma Planeta X ni garantiza un puesto en la competición.
