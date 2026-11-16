# Planet X Explorer versus OrbitLens — review of 2026-11-15

[English](README.md) · [Español](../es/CONTRASTE_ORBITLENS.md)

Historical comparison preserved. Counts and sibling-repository claims belong to the cited review; consult the respective repositories for current status.

| Aspect | Planet X Explorer | OrbitLens sibling project |
| --- | --- | --- |
| Product | FastAPI + HTML/CSS/JS, illustrative gallery, visual comparison, exploratory detector and academy/quiz for a jury demonstration. | FastAPI + React/Vite; more emphasis on reproducible analysis, manifests and explicit states. |
| Data | Separate synthetic Demo; SIA2 DR1/QR3/deep, source metadata, FITS IMAGE, WCS and PNGs. No QR2. On-demand search; bounded SIA/Gaia with no redirects. | Same Demo/IRSA separation and four collections; manifests/hashes and partial real-field evidence described in its HANDOFF.md. |
| Science | Metadata checks, not per-pixel LVF validation. Incomplete FLAGS/VARIANCE/PSF handling. Heuristic peaks/pairs, no confirmed discovery. | Greater traceability and coverage/mask checks, but still needs independent scientific validation. |
| Tests at that review | 39 Python checks, synthetic smoke and Edge/axe with mocked IRSA. Public repository; no CI or public application URL. | Local commit `84428`; HANDOFF.md reported 215 Python checks, 34 Edge E2E tests, axe and CI. These sibling claims were not independently reverified here. |
| USD 0 hosting | Immediate local start; render.yaml proposes Render Free, exact runtime HTTPS origin and one worker. Ephemeral disk/session state, no availability guarantee. | Hosting options in HANDOFF.md; Render Free also suitable only for a demo, not durable evidence. |

## Focused changes recorded

- IRSA queried only after Search; no synthetic fallback on archive failure. Four collections, OVERFLOW/MAXREC warnings and clear centre-search versus cutout-radius semantics.
- SIA/Gaia have no redirects and bounded reads; FITS arrays are bounded. Raw remote exception details are not shown to users.
- Optional public profile: exact HTTPS host/origin, per-process quotas behind a proxy, security headers and bounded POST bodies. Legacy comparison remains local. Not a certification.
- Better contrast, keyboard navigation and mobile menu. Edge/axe found no violations in examined states, not a substitute for user/device testing.
- Distinct Demo/IRSA entry points; search → compare → review; images revealed only after comparison; adjustable σ and selected-signal details.
- Confirmed comparison milestones, indeterminate states without metrics, 100% only after confirmation and errors without false completion. Hover feedback respects reduced motion.

## What was not verified

No fresh successful IRSA search/download, Render deployment, physical phone, external network or jury browser was tested in that review. [Corrections](CORRECTIONS.md) records prior supplied-FITS processing, not spectral equivalence or motion discovery. Public source code is not a deployed application or a user study. See [jury handoff](JURY_HANDOFF.md).

The later bilingual release adds Spanish/English application/documentation support without claiming improvements to the scientific detector. See [bilingual release](BILINGUAL.md).
