# Corrections of 15 November 2026 — historical record

[English](README.md) · [Español](../es/CORRECCIONES.md)

This is a translation of an earlier Linux-based review. Its **20 tests**, platform statements and package language are historical, not the current Windows/bilingual QA status. The received FastAPI + HTML/CSS/JavaScript engine was retained, not rewritten.

## Causes and changes

- Initial selection used the first two records even if incompatible. The backend now calculates allowed pairs; the interface proposes one and disables incompatible B options.
- Timestamps lost time-of-day. Full timestamps are preserved; identical instants are still rejected.
- Sequential downloads lacked recovery. A/B download concurrently with up to three attempts and a 150-second total deadline.
- DR1/QR3 queries are concurrent and reused for five minutes.
- SIA targets the requested centre to reduce images that merely touch the region. Full cutout coverage is not assumed.
- Cutout centre explicitly uses degrees, as in the official tutorial.
- FITS integrity is checked before atomic cache writes. Corrupt files are discarded and valid older cache migrated.
- POST `/api/compare/jobs` returns a job ID immediately. Polling exposes progress, persistent errors and reuse. Legacy POST `/api/compare` is retained.
- FITS reading, reprojection and rendering run outside the request event loop.
- The UI waits for all three PNGs, ignores obsolete searches and clears results when selection changes.
- A/B use shared colour limits and preserve cutout aspect ratio.
- MAD noise precision is retained instead of rounding weak-data noise to zero.
- Lightweight local 3D orbital art pauses offscreen and respects reduced motion.
- `render.yaml` and hosting instructions prepare an optional free Python service, not a deployment.

## Checks performed in that historical review

- 20 automated checks passed: API/pairs/coordinates, Demo, async jobs/reuse, recovery, incomplete FITS, wrong HTML, older cache and noise-scale preservation.
- Demo motion testing used epochs 0/2, already validated in `test_analysis.py`. The heuristic does not associate motion for every pair, including 0/1; association logic was not changed.
- Browser: Demo → Search → Compare; three visible PNGs at 440 × 440, plus navigation and ornamental sphere.
- Eight user-supplied FITS passed integrity checks.
- Supplied real pair `06c694ab…` / `e655153b…`: IMAGE 63 × 63, detector 1, timestamps `2025-09-06T04:00:52.347` and `2025-09-13T03:57:54.918`. Reading, reprojection and A/B/difference rendering succeeded; reprojected overlap `0.989669942`, common finite fraction `0.9897`. This verifies processing, **not spectral equivalence or a moving object**.

That environment was Linux/Python 3.12; Windows was not tested **in that historical review**. A FastAPI/Starlette/httpx deprecation warning did not prevent passing checks. Later Windows and bilingual testing are recorded separately.

## What could not be verified then

- A fresh full IRSA query/download timed out. Retries were tested with mocked HTTP, not a new successful NASA download.
- The official challenge page returned an access/503 error; complete rules, duration and jury criteria were not verified.
- Public deployment: no connected hosting account, no deployment performed.
- Full LVF/ePSF calibration and FLAGS/VARIANCE propagation remained incomplete; candidates stayed exploratory.

## Reproduction and sources

From the repository root run `python -m pytest -q` with `backend/requirements.txt` installed. Controlled network tests do not consume IRSA data. Original FITS cache is not redistributed.

- https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/
- https://caltech-ipac.github.io/irsa-tutorials/spherex-intro/
- https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/
- https://www.spaceappschallenge.org/2026/challenges/planet-x-and-spherex/?tab=resources
- https://render.com/docs/free
- https://render.com/docs/deploy-fastapi
