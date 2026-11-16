# Prueba del jurado bajo demanda (0 USD)

[Español](README.md) · [English](../en/FREE_HOSTING.md)

**Aún no hay servicio ni URL pública de la aplicación Planet X Explorer.** Para una demostración
presencial o por pantalla compartida basta con `INICIAR_WINDOWS.bat` y el modo
Demo; apágalo con Ctrl+C. Para que un examinador remoto abra un enlace propio,
se necesita hosting. Render Free es una **opción de prueba**, no alojamiento
persistente ni garantía de disponibilidad. No elijas un servicio de pago.

1. El [repositorio GitHub público](https://github.com/12FOCUS21/planet-x-explorer)
   contiene `backend`, `frontend` y `render.yaml` en la raíz. No incluye `.venv`,
   `.env`, `data/cache`, archivos personales ni el ZIP. **Crear el repositorio
   no autoriza por sí solo publicar la aplicación como servicio.**
2. En https://dashboard.render.com crea un Web Service y conecta ese repositorio.
3. Selecciona Python 3 y el plan **Free**, sin complementos de pago.
4. Build Command: `pip install -r backend/requirements.txt`
5. Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 1 --no-proxy-headers`
6. Define `PX_PUBLIC_MODE=1`, `PYTHON_VERSION=3.12.8`, `PX_REQUEST_TIMEOUT=60`,
   `OPENBLAS_NUM_THREADS=1` y `OMP_NUM_THREADS=1` (ya están en `render.yaml`).
   Render provee `RENDER_EXTERNAL_URL=https://<servicio>.onrender.com` **en
   ejecución**. Sin URL HTTPS exacta válida, el proceso no inicia. Para un
   dominio personalizado, define `PX_PUBLIC_ORIGIN=https://dominio-exacto`;
   no añadas una barra final. No uses comodines.
7. Usa `/api/health` como health check. Despliega y verifica la URL `onrender.com`
   asignada antes de compartirla. La URL local `127.0.0.1` no es accesible por
   examinadores remotos.
8. Abre la URL desde una ventana privada y prueba **Probar demo guiada →
   seleccionar A/B → Comparar → tres imágenes → Revisar diferencias**. Si
   deseas mostrar IRSA, haz una búsqueda real aparte y confirma que el
   servicio remoto responde; **no
   sustituyas resultados vacíos por simulación**.

También puedes importar render.yaml con New → Blueprint. Revisa que se conserve
`plan: free`. Si el servicio no ofrece Free, no elijas un plan de pago por defecto.

## Límites del plan gratuito

Render puede suspender instancias sin tráfico; el siguiente acceso puede tardar
un minuto o más. Inicia y comprueba el enlace con margen antes del examen.
Las sesiones y archivos en caché se pierden al
reiniciar. Vuelve a buscar las observaciones después de un reinicio. Hay límites
mensuales y el tráfico elevado hacia IRSA puede causar suspensión del servicio.
Es una opción para demostrar el proyecto, sin garantía de disponibilidad continua.
El motor requiere Python; GitHub Pages solo no ejecuta este backend.
Mantén un solo worker: las búsquedas y trabajos están en memoria.
El perfil público restringe el Host, los POST de otro origen, cuerpos de petición
y algunas consultas costosas. Detrás del proxy, `--no-proxy-headers` evita
confiar en cabeceras de IP manipulables; varios visitantes pueden compartir una
misma cuota de 30 consultas costosas por minuto. No equivale a una auditoría de
seguridad ni a protección frente a grandes volúmenes de tráfico. No emplear
para producción estable. Tras la sesión, desactiva o retira el servicio si no
quieres dejar el enlace disponible.

Fuentes consultadas el 15-11-2026:
- https://render.com/docs/free
- https://render.com/docs/deploy-fastapi
- https://render.com/docs/web-services

La publicación efectiva y la prueba de acceso público siguen pendientes de
autorización del equipo y una cuenta de hosting. No se configuraron
credenciales de despliegue ni servicios de pago.
