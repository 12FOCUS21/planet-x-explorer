# Jury demonstration — no permanent service

[English](README.md) · [Español](../es/ENTREGA_JURADO.md) · [Bilingual release](BILINGUAL.md)

Use the [complete video guide](COMPLETE_VIDEO_GUIDE.md) to explain objectives, functionality and scientific limits. A script is not a recorded video.

## On the same computer or through screen sharing

1. Install Python 3.12 and `backend/requirements.txt` once; installation requires Internet.
2. Run `INICIAR_WINDOWS.bat`, or `python scripts/launch.py` in the configured environment. Open http://127.0.0.1:8000 and select **English**. Do not expose the local port directly to the Internet. Check `/api/health` and keep `backend`, `frontend`, `data` together.
3. Follow **Try guided demo → four synthetic epochs → select A/B → Compare → verify A, B and B − A → Review differences**. Select a signal, optionally adjust σ, then visit the academy. Images remain hidden until comparison completes. **All Demo pixels are artificial**, not evidence of a planet.
4. To show the other workflow, return home and choose **Explore IRSA data**. Opening this form performs no external query. **Search observations** starts a real search; **Compare** requests FITS cutouts if a metadata-compatible pair exists. Coverage or network availability may prevent a successful comparison. Do not present Demo as IRSA or silently replace an empty response.
5. Stop with `Ctrl+C`. Memory sessions disappear when the server stops.

The language selector is available on desktop/mobile and persists after reload. Switching language does not restart jobs or reset quiz answers. Screenshots embedded in the report may retain Spanish labels; the live interface now supports English.

## If judges need their own external URL

Read [free hosting](FREE_HOSTING.md). With a USD 0 budget, Render Free is only an optional test after team authorization. It may sleep and does not persist results. Verify the exact URL in a private browser and rehearse before sharing. Keep local screen sharing as a fallback. Never share `localhost` as a remote URL. Disable the service afterward if appropriate. **No public deployment has been verified.**

## Claims to make — and avoid

- Planet X / Planet Nine remains hypothetical; 5 σ is a heuristic threshold, not a discovery probability.
- Real pair selection checks collection, detector, timestamp and declared spectral ranges, **not per-pixel effective LVF wavelength calibration**.
- DR1, QR3 and their deep collections are queried separately; no QR2 fallback.
- A fresh complete IRSA search/download was not verified in the preceding review. [Historical corrections](CORRECTIONS.md) record earlier processing of user-provided FITS, not a discovery.
- Do not claim a confirmed planet, public deployment, security certification or completed video.

## Reproducible checks

From the repository root on Windows: `.\.venv\Scripts\python.exe -m pytest tests -q`; `python scripts/smoke_test.py` exercises synthetic health/search/comparison/three PNGs/detection. UI QA: Node.js 22.12+, Edge, then `cd frontend`, `npm ci`, `npm run qa:ui`.

The UI test runs its own local server on port 8134 and checks Spanish/English, switching while a job is active, translated CSV, lessons and quiz, persistence, opt-in IRSA behaviour, mobile and axe. IRSA responses in this QA are **locally simulated**; no real download is proven. Automated accessibility checks cover tested states, not every device or user. See [current bilingual testing scope](BILINGUAL.md). Earlier handoff records reported 39 Python checks; the expanded suite adds localization coverage.

The public repository is separate from OrbitLens and excludes FITS caches, `.venv` and `frontend/node_modules/`. Public code is not a running public web application.
