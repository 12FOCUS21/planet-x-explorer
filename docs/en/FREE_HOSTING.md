# On-demand jury demonstration — USD 0

[English](README.md) · [Español](../es/PUBLICAR_GRATIS.md)

**There is no public application service or deployment URL.** Local or screen-shared demonstrations need only `INICIAR_WINDOWS.bat` and Demo mode; stop with `Ctrl+C`. Remote access requires hosting. Render Free is a possible test option, not persistent hosting or an availability guarantee. Do not select a paid service.

1. Public repository **[12FOCUS21/planet-x-explorer](https://github.com/12FOCUS21/planet-x-explorer)** includes `backend`, `frontend` and `render.yaml`. It excludes `.venv`, `.env` and FITS cache. Publishing source code does not itself authorize application hosting.
2. With team authorization, create a Web Service at https://dashboard.render.com and connect the repository.
3. Choose Python 3 and **Free**, with no paid add-ons.
4. Build: `pip install -r backend/requirements.txt`.
5. Start: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --workers 1 --no-proxy-headers`.
6. Set `PX_PUBLIC_MODE=1`, `PYTHON_VERSION=3.12.8`, `PX_REQUEST_TIMEOUT=60`, `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1` as in `render.yaml`. Render supplies `RENDER_EXTERNAL_URL=https://<service>.onrender.com` at runtime. Without a valid exact HTTPS origin, startup fails. For a custom domain set `PX_PUBLIC_ORIGIN=https://exact-host`, with no trailing slash or wildcard.
7. Use `/api/health` for the health check. Verify the assigned HTTPS URL before sharing it; `127.0.0.1` is not remotely accessible.
8. In a private window select **English → Try guided demo → A/B → Compare → three images → Review differences**. Test IRSA separately; never replace empty real results with a simulation.

Alternatively import `render.yaml` using New → Blueprint and verify `plan: free`. If Free is not offered, do not accept a paid default.

## Free-plan limitations

- Idle instances may sleep; the next request can take a minute or longer. Prepare before the examination.
- Memory sessions and cached files are ephemeral. Search again after restart.
- Monthly limits or high IRSA traffic can interrupt service. There is no continuous-availability guarantee.
- GitHub Pages alone cannot run this Python backend. Use **one worker** because jobs/searches are in memory.
- Public mode restricts Host/origin, request size and expensive requests. `--no-proxy-headers` avoids trusting spoofable forwarded IPs; users behind a proxy may share the 30-expensive-requests/minute quota.
- These controls are not a security audit, large-volume protection or a stable production recommendation. Disable the service afterward if public exposure is not wanted.

Sources originally consulted on 2026-11-15: https://render.com/docs/free, https://render.com/docs/deploy-fastapi, https://render.com/docs/web-services. Free-tier terms can change. Actual deployment and external-access testing remain pending team authorization and a hosting account. No deployment credentials or paid services were configured.
