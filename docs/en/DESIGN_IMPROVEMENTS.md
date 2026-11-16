# Design improvements — historical record

[English](README.md) · [Español](../es/MEJORAS_SOLO_DISENO.md)

This records an editorial astronomy-gallery redesign inspired by photo-gallery composition. **Scientific logic was not changed by that design-only revision.** Later functional releases are documented separately.

## Visible changes

- Observatory-style home: clearer typography, compact navigation, dark tones and warm accents.
- Featured gallery retained `homePreview`, updating after a completed comparison.
- Two local astronomical illustrations with no external requests, explicitly labelled as illustration/concept art, never SPHEREx measurements.
- A/B/difference presented as one continuous dark mosaic, retaining captions and script identifiers.
- Comparison, epoch selection, controls, detection, academy, sources and 3D view retained their existing engine.
- Responsive home/gallery/image panels. Home became the initial page; observations remained accessible through menu/buttons.

## Files at that revision

- Modified `frontend/index.html` (home markup/text/theme link) and `frontend/js/main.js` (initial route only).
- Added `frontend/css/editorial-gallery.css`; retained `styles.css`.
- Added `frontend/assets/infrared-art.svg` and `planet-art.svg` as illustrations, not real data or a discovered planet.
- Intentionally unchanged in that revision: all `backend/`, original `api.js`, `explorer.js`, `detection.js`, `academy.js`, `orbit3d.js`, server configuration, tests and Windows launchers.

## Viewing that design

Extract the historical ZIP into a new directory, run `INICIAR_WINDOWS.bat`, open the local URL and Home. In Observations select epochs and Compare to see the image mosaic. Use `Ctrl+F5` if cached styling appears. These instructions describe the historical package; current UI labels may differ.

The design-only revision did not fix archive connectivity or response availability and did not validate scientific analysis.

## Observatory Edition — 15 November 2026

- Horizontal navigation, compact header and new editorial hierarchy.
- Local compressed astronomical art, prominent typography and visible ornamental 3D simulator.
- Three-illustration gallery, separated functional panels, unchanged scientific image IDs/API.
- Clear forms, dark plot backgrounds, readable states and labels.
- New `frontend/css/observatory-premium.css` and three local JPEG assets.
- Concept art remained distinct from actual FITS views, which appear only through the data workflow.
