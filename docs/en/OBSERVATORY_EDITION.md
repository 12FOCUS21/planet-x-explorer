# Planet X Explorer — Observatory Edition

[English](README.md) · [Español](../es/OBSERVATORY_EDITION.md)

Historical visual-design notes. The present home page can differ from the slogans quoted here; use the current [video guide](COMPLETE_VIDEO_GUIDE.md) for the demonstration.

## What changed in that revision

- Horizontal desktop navigation and an expandable mobile side menu.
- Cinematic home with exhibition-style typography, conceptual space imagery generated for the interface, and an interactive canvas orbit animation.
- Three large illustration-labelled images with integrated captions.
- Coherent functional views: readable light-background forms, dark image comparison, detector, academy and sources.
- Responsive desktop, laptop and mobile adjustments.

## What did not change in that revision

- No backend files, FastAPI routes, IRSA connection, FITS loading or scientific processing.
- Original HTML IDs and SPA navigation remained compatible with the scripts.

## Design files

- `frontend/css/observatory-premium.css`: new stylesheet loaded last at that revision.
- `frontend/index.html`: updated home structure/text while preserving scientific IDs.
- `frontend/js/orbit3d.js`: ornamental 3D rendering, not scientific modelling.
- `stellar-nursery.jpg`, `infrared-field.jpg`, `deep-field.jpg`: generated concept art, **not NASA images**.

## Historical Windows instructions

1. Extract the ZIP into a new folder; do not merge with the old ZIP.
2. Run `INICIAR_WINDOWS.bat` and open the local URL in Chrome.
3. Use `Ctrl+Shift+R` for a full reload.
4. The historical edition used a blue/violet star field, the slogan “EL UNIVERSO NO ESPERA.” and horizontal desktop menu. Seeing the old side menu and “Otra forma de mirar el cielo” indicated the earlier package. These slogans are not a current-release test.

The cover images are interface artwork, not scientific photos or detections. FITS imagery appears only after data queries/comparisons. Illustrations cannot be scientific evidence.
