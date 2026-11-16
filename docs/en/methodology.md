# Methodology, assumptions and reproducibility

[English](README.md) · [Español](../es/methodology.md)

## 1. Search

Inputs: RA `0 ≤ RA < 360`, Dec `−90…+90`, cutout radius `0.008–0.3` degrees. IRSA mode queries `spherex_dr1`, `spherex_qr3`, `spherex_dr1_deep`, `spherex_qr3_deep` through SIA2, without an API key or QR2 fallback. A `0.000001°` SIA circle requests images containing the **centre**, independently of the interface radius. That radius sizes the later FITS cutout and does not guarantee full-region coverage.

Each collection is limited to 150 records and 8 MB of response. Warnings identify IRSA `OVERFLOW` or record-limit truncation. Metadata are genuine but may be incomplete. Full timestamps are preserved; only metadata-compatible pairs are offered.

## 2. SPHEREx cutouts

Level 2 FITS files contain multiple extensions. `IMAGE` stores surface brightness in MJy/sr. FLAGS, VARIANCE, ZODI and other extensions are not fully incorporated into detection. Official cutouts avoid transferring entire files (for example, about 70 MB per detector).

## 3. Spatial alignment

A is the reference. B is reprojected to A's celestial WCS with bilinear interpolation. A field with less than 15% valid overlap is rejected. Synthetic images share the same pixel frame and are not reprojected.

## 4. Differences and preliminary signals

Subtract a Gaussian background approximation with sigma 9 pixels for each epoch. Calculate high-frequency `B − A`, then smooth with sigma 0.8 pixels. Estimate robust noise as MAD × 1.4826, without a fixed physical-unit floor. The initial threshold is **5 σ**, adjustable between **2 and 10 σ**. A possible displacement requires mutually nearest positive/negative peaks 5–110 pixels apart and residual amplitudes within a factor of four.

Real pairs also require the same collection and detector, distinct timestamps and at least 80% overlap between declared spectral intervals. Missing verifiable spectral metadata rejects the pair. These filters reduce obvious incompatibility but **do not validate per-pixel LVF equivalence**.

The σ threshold is heuristic, not calibrated statistical significance: pixels are correlated, PSFs vary and noise/filter effects may be non-Gaussian. Peak pairings can be artefacts. The score is not the probability of Planet Nine.

## 5. SPHEREx is not a conventional camera

Its linear variable filter (LVF) changes effective wavelength along the detectors. Two epochs from one detector may have different spectral responses even after WCS alignment. Differences can reflect spectral sampling instead of motion. Scientific analysis would require equivalent-wavelength maps, calibration, VARIANCE/FLAGS and PSF control.

## 6. Current limitations

- No complete LVF correction or calibrated equivalent-wavelength comparison.
- No full instrumental uncertainty propagation or FLAGS masks in results.
- No systematic repeated-detection study or validated candidate photometry.
- No automatic candidate crossmatch with Gaia, MPC, JPL Horizons or WISE.
- No orbital or physical-parameter fitting.
- Only observations returned by the archive at query time are available.

**No list produced by this application is direct evidence of Planet X.**

## 7. Separate synthetic demonstration

`make_demo_pair()` creates a reproducible 440 × 440 field with fixed stars, a variable source, smooth background, noise and an artificial moving object. Coordinates determine the random seed. Metadata use `simulated: true`; the source and interface labels identify the simulation. This teaches the workflow without external Internet dependencies after installation. English presentation does not change the seed, coordinates, pixels or measurements.

## 8. Route toward independently verifiable discoveries

1. Obtain equivalent spectral segments and match resolution/PSF.
2. Propagate masks and uncertainty maps for a physical threshold.
3. Require repeatable signals in at least three distinct epochs.
4. Exclude known objects (MPC, Gaia, WISE), artefacts and variable sources.
5. Fit orbits with residuals and uncertainty estimates.
6. Preserve FITS cutouts, hashes, dates and reproducible scripts, then seek external validation.
