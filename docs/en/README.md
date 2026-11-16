# Planet X Explorer — English documentation

[English](README.md) · [Español](../es/README.md) · [All documents](../README.md)

**Educational web application for exploring and comparing infrared SPHEREx observations from NASA/IPAC IRSA, with a synthetic offline demonstration.**

Start with the [project report](PROJECT_REPORT.md), [jury handoff](JURY_HANDOFF.md) and [complete video guide](COMPLETE_VIDEO_GUIDE.md). Download the [professional Word report](Planet_X_Explorer_Professional_Report.docx) or its [PDF](Planet_X_Explorer_Professional_Report.pdf).

> Planet Nine / Planet X is hypothetical. This application cannot confirm a planet. Demo images are entirely synthetic. The repository is public; **the application is not publicly deployed**.

## Quick start — Windows 10/11

1. Keep `backend`, `frontend`, `data` and `INICIAR_WINDOWS.bat` in the project directory.
2. Install Python 3.12. Internet is required for the initial dependency installation.
3. Double-click `INICIAR_WINDOWS.bat`; it creates `.venv` if necessary, checks dependencies and opens a browser.
4. Open **http://127.0.0.1:8000** if it does not open automatically. Select **English** in the header.
5. Choose **Try guided demo**, select A and B, click **Compare**, then **Review differences**. Optionally change the analysis threshold.
6. Stop the server with `Ctrl+C`.

Commands below run from the **repository root**, not this documentation directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe scripts\launch.py
```

Back up an existing project folder before merging an old ZIP. The pip installation should not delete personal files.

### Linux/macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
.venv/bin/python scripts/launch.py
```

## Two separate workflows

- **Guided demo:** loads four deterministic synthetic epochs without querying IRSA. Select A/B and compare before the images are revealed. Every scene is labelled as a simulation; detected signals are preliminary.
- **NASA / IRSA:** **Explore IRSA data** opens the form without contacting IRSA. Enter numeric coordinates or select a preset, then click **Search observations**. Empty responses are not replaced by Demo data.

The comparison percentage represents confirmed milestones, not estimated time remaining. It reaches 100% only after all three images load. Search and analysis remain indeterminate until a response is processed. Errors do not show a false completed state. The analysis supports signal selection, a **2–10 σ** threshold (initially 5 σ), and CSV export. The academy provides lessons and a quiz, not scientific validation.

The language selector is available on desktop and mobile. Its preference is saved locally. Switching language preserves coordinates, comparison sessions and quiz answers. See [bilingual behaviour](BILINGUAL.md).

## Querying real SPHEREx images

1. Select NASA / IRSA. No search occurs until **Search observations** is pressed.
2. Enter RA/Dec. The radius controls FITS cutout size; SIA searches for images covering the **centre**, not the entire circle.
3. Choose two metadata-compatible epochs and click **Compare** to request their FITS cutouts.
4. If no observations are returned, try other coordinates. Increasing the radius does **not** widen this search.

There is no interactive sky map yet. Real searches and downloads require Internet. Collections: `spherex_dr1`, `spherex_qr3`, `spherex_dr1_deep`, `spherex_qr3_deep`; **no QR2 fallback**. Responses may be incomplete at MAXREC=150 or IRSA truncation; warnings are displayed. `IMAGE` contains brightness in MJy/sr. Sharing a detector does not guarantee equal effective wavelength per pixel; comparisons remain exploratory.

## Modules

| Module | Function |
| --- | --- |
| Home | Separate Demo/IRSA entry points, method and illustrative gallery |
| Explorer | RA/Dec region, presets, epoch search and selection |
| Comparison | FITS cutouts, WCS alignment and A/B/difference views |
| Detector | Robust residuals, positive/negative peaks, apparent displacement and CSV |
| Academy | Three lessons, five questions and local progress |
| Sources | Provenance, methodology and explicit limitations |
| Gaia DR3 | Optional ESA stellar query; no automatic candidate classification |

## Verification

```powershell
.\.venv\Scripts\python.exe scripts\check_env.py
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe -m pytest tests -q
```

Optional UI QA requires Node.js **22.12+** and Edge on Windows:

```powershell
cd frontend
npm ci
npm run qa:ui
```

The QA starts/stops its own server at `127.0.0.1:8134`. It checks Demo, three PNGs, progress, error/retry, thresholds, hover, reduced motion, academy, mobile, language persistence, language switching during a job and CSV translation. IRSA empty/error responses are **intercepted locally**: this does not prove real archive connectivity or download. `PX_QA_PORT` changes the port; `PX_QA_PYTHON` selects a Python executable. On other systems install Chromium with `npx playwright install chromium`; `PX_QA_BROWSER_CHANNEL` selects an available channel. Installing QA tools requires Internet once; running this controlled QA does not require IRSA.

Axe checks only the automated states and is not an accessibility certification. Node dependencies are not required for normal FastAPI execution. Local API docs: http://127.0.0.1:8000/docs (disabled in public mode). API clients can request English with `?lang=en` or `Accept-Language: en`; Spanish is the default. Codes, IDs, numbers and data sources remain unchanged.

## Scientific limitations

No full per-pixel LVF equivalence, systematic FLAGS/VARIANCE propagation, PSF matching, validated photometry, automatic crossmatch against every Solar System catalogue, or orbital fitting. A **5 σ heuristic score is not a planet probability**. Coverage, compatible epochs and remote availability cannot be guaranteed. Read the [methodology](methodology.md) and [scientific sources](nasa_sources.md).

## Structure and privacy

`backend/app/api/`: endpoints; `services/`: archives and Demo; `analysis/`: alignment/differences/detection; `utils/`: FITS and PNG; `frontend/`: HTML/CSS/JS and local translation catalogue; `tests/`: automated checks; `docs/es/` and `docs/en/`: language-separated documents. FITS cache at `data/cache/`, `.venv` and `frontend/node_modules/` are excluded from Git.

No account or API key is required. The academy and language preference use browser localStorage. Public mode temporarily keeps connection addresses in memory for rate limiting; a hosting provider may log accesses under its own policy. This is an independent project without NASA/ESA endorsement. Code is available under the [MIT license](../../LICENSE).
