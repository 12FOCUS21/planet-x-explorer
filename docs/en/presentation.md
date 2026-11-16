# Three-minute presentation for judges

[English](README.md) · [Español](../es/presentation.md)

Adaptation of the historical pitch. Select English first and follow current buttons in the [complete guide](COMPLETE_VIDEO_GUIDE.md). Motion is not guaranteed to be associated for every synthetic pair.

## 0:00–0:30 — the problem

“Planet Nine is still hypothetical. Instruments let us observe the infrared sky, but comparing observations calls for accessible and scientifically responsible tools.”

## 0:30–1:10 — the explorer

Open http://127.0.0.1:8000. Show the concept, then guided Demo. Keep **DEMO = SYNTHETIC** visible. Choose epochs and Compare. Explain fixed stars, the deliberate artificial moving source and the residual map. Do not promise that every heuristic peak pair will be associated.

## 1:10–1:45 — the detector

Review differences, select signals and show pixel separation/σ. Explain variable sources and the need to rule out false positives. Export CSV. **Do not call the simulated source Planet Nine.**

## 1:45–2:15 — real NASA archive route

Choose NASA / IRSA and explicitly Search. Present metadata and, only if a compatible pair and the network permit, the FITS cutouts. If unavailable, explain that the separate labelled Demo preserves the educational evaluation. Effective wavelength channels still need calibration before claiming real motion.

## 2:15–2:45 — education and impact

Open the academy, a lesson and a quiz question. Explain preliminary detections and the need to validate science.

## 2:45–3:00 — closing

“We do not promise to have found Planet Nine. We offer a reproducible open-science learning experience connecting public data, analysis and education, with a clear route to stronger scientific validation.”

## Preparation

- Run `python -m pytest tests -q` without external network requirements.
- Rehearse Demo at least twice and select English before presenting.
- Test IRSA separately on the event network; do not assume availability.
- Keep an exported CSV and labelled synthetic capture as backup.
- Clearly distinguish simulated outputs from archive observations.
