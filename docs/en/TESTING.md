# Quality checklist and reproducible checks

[English](README.md) · [Español](../es/TESTING.md) · [Bilingual QA](BILINGUAL.md)

Commands run from the repository root with Python dependencies installed:

```powershell
.\.venv\Scripts\python.exe scripts\check_env.py
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe -m pytest tests -q
```

Optional browser QA: Node.js 22.12+, Edge; `cd frontend`, `npm ci`, `npm run qa:ui`. The QA starts/stops a separate local server at port 8134 and intercepts IRSA replies. It does not verify real IRSA download or remote deployment.

## Manual interface checklist

1. Open home and visit all five navigation sections.
2. Select English, then Demo and a test field. Search four synthetic epochs and compare two.
3. Verify A, B and difference appear together after loading. The older before/after slider reference is historical.
4. Open analysis, select a signal, adjust σ and export a labelled CSV.
5. Complete academy lessons and quiz; reload and verify local progress persists.
6. Switch English/Spanish in home, analysis, a lesson dialog and after a quiz answer. Preserve state and meaningful accessible labels.
7. Switch to IRSA and verify previous Demo images are hidden. No request occurs until Search.
8. If Internet is available, separately try a real SIA2 query and compatible epochs. Coverage is not guaranteed.
9. Rehearse mobile/desktop sizes, keyboard navigation, menu, language selector and reduced-motion preference.

## Acceptance criteria

- No JavaScript errors or HTTP 500 responses in Demo.
- Images remain clearly labelled as synthetic or IRSA; no confirmed-planet claim.
- Empty/error IRSA responses do not become simulations.
- IRSA/Gaia use official HTTPS endpoints only.
- Changing language neither initiates IRSA requests nor changes pixels, scientific numbers, IDs, dates or selected epochs.
- A job can finish after a language switch; 100% still requires three loaded images.
- English CSV includes English classifications/notes and an explicit synthetic/real origin.
- Language choice survives reload. Quiz answers and comparison state survive a language switch.
- Automated axe checks pass for examined states; this is not full accessibility certification.

Historical test counts are retained in historical records. The current release adds `tests/test_localization.py` and English paths in `frontend/qa/smoke.cjs`. Scientific validation, physical-device testing and new full IRSA downloads remain separate tasks.
