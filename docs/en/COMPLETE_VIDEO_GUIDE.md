# Planet X Explorer — complete project overview and video guide

[English](README.md) · [Español](../es/GUIA_COMPLETA_VIDEO.md)

> Preparation material, not a recorded video or scientific result. Suggested duration: 4–5 minutes. Use the reproducible **synthetic Demo** after dependencies are installed. Code is public; there is no public application deployment. Select **English** in the application header before recording.

## 1. The idea in one sentence

**An educational application for choosing a sky region, comparing two infrared epochs, examining changes and learning why a signal is not proof of a planet.**

Planet Nine / Planet X remains a hypothesis. The objective is not to announce its discovery, but to explain a transparent workflow: **region → epochs → comparison → signals → review**.

## 2. Audience and problem

Students, interested non-specialists and evaluators need to understand that a difference may reflect motion, variability, noise or the instrument. The application keeps originals, residuals, source labels and limitations visible instead of calling every change a discovery.

| Area | What the user can do |
| --- | --- |
| Home | Choose **Try guided demo** or **Explore IRSA data**. Cover art is illustrative, not an observation. |
| Explorer | Enter RA, Dec and cutout radius or select a preset; search epochs and select A/B. |
| Comparison | View A, B and B − A on a shared visual scale, only after completion. |
| Analysis | Inspect preliminary peaks, select a position, vary 2–10 σ (5 σ initially), export labelled CSV. |
| Academy | Read three lessons and answer five questions; progress stays in the browser. |
| Sources | Review provenance and limits; optional Gaia DR3 context does not confirm candidates. |

The responsive interface supports keyboard use and reduced motion. Comparison percentages reflect **confirmed milestones**, not remaining time; 100% means all three images loaded. Search and analysis remain indeterminate until a processed response. The header language choice persists and does not change measurements or restart jobs.

## 3. Two workflows that must not be confused

### A. Guided synthetic Demo — recommended for recording

1. **Try guided demo** generates four reproducible 440 × 440 scenes with fixed stars, a variable source, noise and a deliberately moving artificial source.
2. Select A/B, click **Compare**, then view three PNGs labelled **SIMULATION**. Neither the illustrative dates nor the artificial object are NASA measurements.
3. Open **Review differences**, select a signal and change the threshold. A large σ score is not a planet probability.
4. Optionally show CSV and academy. No IRSA connection is required, but the local server must remain running.

### B. NASA/IPAC IRSA archive — optional, Internet required

1. **Explore IRSA data** only opens the form. The query starts after **Search observations**, not on page load or language change.
2. SIA2 searches `spherex_dr1`, `spherex_qr3`, `spherex_dr1_deep`, `spherex_qr3_deep`, with **no QR2 fallback**. Images must contain the centre; the interface radius sizes the later cutout, not the search circle.
3. Metadata filters require matching collection/detector, distinct times and at least 80% declared spectral-range overlap. This does **not** establish per-pixel LVF equivalence.
4. **Compare** requests FITS cutouts, reads `IMAGE`, reprojects B onto A using WCS, and produces views. Coverage and archive/network availability can prevent success.
5. Empty results and failures stay explicit. Missing real data are never silently replaced by synthetic scenes.

If a real search/download has not been executed and verified for the recording, show only the form and describe the on-demand feature. Do not call Demo pixels NASA data. The preceding review did not verify a fresh complete IRSA download; [historical corrections](CORRECTIONS.md) document prior processing of supplied FITS, not a detection.

## 4. How it works

```text
Browser: HTML / CSS / JavaScript, with local Spanish / English presentation
  → Python FastAPI API
  → synthetic generator OR on-demand NASA/IPAC IRSA
  → two metadata-compatible epochs
  → real FITS or simulated arrays
  → WCS alignment for real data + background removal
  → B − A residual + preliminary peaks
  → three PNGs, review controls and CSV
```

- **Frontend:** no required build step. Separates data sources, guides the workflow, hides unfinished images and displays confirmed progress and errors.
- **Backend:** validates inputs/pairs, queries archives and processes arrays. Searches/sessions are temporary memory objects. FITS cutouts may be cached locally; they are excluded from Git.
- **Comparison:** B is reprojected to A for real data; background is removed, residuals calculated and robust noise estimated by MAD. Peak pairs suggest possible displacement, not an orbit. Demo arrays already share a pixel frame.
- **Results:** coordinates, heuristic σ scores and pixel separations are human-review clues. Recalculation and CSV preserve provenance.
- **Gaia DR3:** optional ESA stellar context, not automatic signal classification.

**Scientific limitations:** LVF can produce different effective wavelengths at a pixel across epochs. FLAGS masks, VARIANCE uncertainty propagation, PSF correction and systematic known-object rejection are incomplete. No orbit or confirmed Planet X detection is produced. Matching metadata is not independent scientific validation.

## 5. Recording script — screen and narration

Times are approximate. Wait for real completion; do not edit loading to fabricate a result.

| Time | Screen/action | Suggested narration |
| --- | --- | --- |
| 0:00–0:30 | Home, title and two routes. | “How can we search for changes in the sky without confusing a signal with a discovery? Planet X Explorer turns that question into an interactive workflow. Planet Nine is still hypothetical; this tool does not claim to have found it.” |
| 0:30–1:00 | Point to both routes; choose guided Demo. | “We provide two separate paths. Demo creates reproducible synthetic images and works offline after installation. The other path can query NASA/IPAC IRSA SPHEREx observations, only after Search is pressed. Here I will use the clearly labelled simulation.” |
| 1:00–1:40 | Four epochs, A/B selectors, then Compare. | “We choose a region and two epochs. The interface validates the pair and reports confirmed stages. The percentage is not a time promise: it reaches one hundred only when all three images are ready. Images are not presented as loaded before the comparison.” |
| 1:40–2:20 | A, B and residual; keep SIMULATION visible. | “This is the reference field, the second epoch and their difference. A change can be apparent motion, variability, noise or an instrumental effect. These scenes are artificial; they are not a NASA detection.” |
| 2:20–3:00 | Review differences, select a signal, change σ. | “The analysis highlights residual peaks for inspection and lets us adjust sensitivity. Changing the threshold recalculates results. Sigma is a heuristic contrast score, not a planet identification. The CSV retains data provenance.” |
| 3:00–3:30 | Lesson, quiz and sources. | “We also explain why more epochs, checks and catalogues are necessary. The academy and source page make the visual result an opportunity to learn science, rather than an extraordinary claim.” |
| 3:30–4:10 | Open IRSA form; do not search unless verifying real data. | “For real data, the server can query DR1, QR3 and their deep collections and request FITS cutouts. Passing metadata filters does not ensure the same effective wavelength at every pixel. I will not present Demo as IRSA without a verified download.” |
| 4:10–4:40 | Close on sources or home. | “Our contribution is a clear, reproducible and honest way to explore preliminary signals. The next scientific step requires instrumental calibration, more epochs and independent validation. First understand the change; then verify what it means.” |

### If IRSA fails during recording

Say: “The external archive's availability can vary. This query did not produce a verifiable pair. The application does not replace that absence with fictional observations. We will continue with the clearly identified synthetic Demo.” Do not overlay Demo images while describing them as real observations.

## 6. Recording preparation

1. Start `INICIAR_WINDOWS.bat` with Python 3.12 and installed dependencies; open http://127.0.0.1:8000 **on the same computer**. Installation requires Internet once; localhost is not a remote-jury link.
2. Keep the server console open. Select English. Close personal notifications; test microphone and text readability.
3. Rehearse **Demo → A/B → Compare → Review differences → Academy/Sources**. Wait for A, B and B − A before saying “ready.” Counts depend on coordinates, epochs and threshold; do not hard-code a discovery count in narration.
4. Keep the synthetic badge visible and describe the 3D art as illustration. If showing IRSA, verify a separate real request at that time.
5. Stop with `Ctrl+C`. Hosting budget: USD 0, on-demand operation. GitHub hosts source code, not the running app. Render Free is only a future option with authorization and external verification.

## 7. Evidence and safe jury answers

- The earlier reviewed release passed 39 Python tests and synthetic smoke plus Edge/axe states. The bilingual release adds localization tests and Spanish/English UI coverage; see [testing](TESTING.md). Automated checks are not comprehensive accessibility/security certification.
- Still unverified: a new complete IRSA download, remote-user performance, deployment, per-pixel LVF calibration and independent scientific detection.
- Safe: “The application supports preliminary change exploration through a synthetic Demo and a separate on-demand IRSA route.”
- Avoid: “We found Planet X,” “Demo pixels are NASA,” “5σ proves a planet,” “the app is already deployed” or “the system is certified.”

## 8. Further reading

[Installation](README.md) · [Jury handoff](JURY_HANDOFF.md) · [Methodology](methodology.md) · [OrbitLens comparison](ORBITLENS_COMPARISON.md) · [Historical corrections](CORRECTIONS.md) · [Hosting, not performed](FREE_HOSTING.md).

Credits: SPHEREx/NASA/IPAC IRSA for the archive route and ESA Gaia DR3 for optional context. This independent educational project has no official NASA or ESA endorsement. AI assistance used OpenCode with Sol 6.1, Astra and DeepSeek as declared by the team; scientific responsibility remains with the team.
