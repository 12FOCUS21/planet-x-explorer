# Provenance and scientific links

[English](README.md) · [Español](../es/nasa_sources.md)

Real SPHEREx data are retrieved only from official public NASA/IPAC IRSA servers. Demo pixels are generated in software and deliberately include a moving artificial source and a variable source; they do not represent a known celestial body.

## Main NASA/IPAC archive

- SPHEREx archive: https://irsa.ipac.caltech.edu/Missions/spherex.html
- Access, SIA2 collections and cutouts: https://irsa.ipac.caltech.edu/spherex-archive-documentation/spherex-data-access/
- Image tutorial: https://caltech-ipac.github.io/irsa-tutorials/spherex-intro/
- Cutout tutorial: https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/
- Data products: https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-products/
- Recommended DOI for DR1 images: https://doi.org/10.26131/IRSA678
- DR1 all-sky cube DOI (**not used here**): https://doi.org/10.26131/IRSA679

Current collections are `spherex_dr1`, `spherex_qr3` and their `_deep` variants (public Level 2 spectral images). Queries use `https://irsa.ipac.caltech.edu/SIA` and `POS=CIRCLE ra dec radius`. Cutouts use official `center` and `size` parameters on SIA2 `access_url` values. No credentials or API keys are required. The original Spanish record's shorter DR1/QR3 list is historical; there is no QR2 fallback.

IRSA may limit, delay or change availability; indexing may lag ingestion. Previously downloaded observations are not distributed in the repository. Real mode needs Internet and may return zero matches.

## Auxiliary source — ESA Gaia DR3

- https://gea.esac.esa.int/archive/
- https://docs.astropy.org/projects/astroquery/en/stable/gaia/gaia.html

Gaia belongs to ESA, not NASA. The app optionally queries up to 40 bright stars in a small region. These results do not confirm candidates; automatic matching needs additional work.

## WISE — NASA/IPAC

https://irsa.ipac.caltech.edu/Missions/wise.html

WISE provides historical context and methodological inspiration. The initial engine does not use real WISE pixels in its comparisons; no PNG should be attributed to WISE.

## Suggested attribution

> This independent educational project accesses public SPHEREx products through NASA/IPAC IRSA and optionally queries ESA Gaia DR3. It is not developed or endorsed by NASA or ESA.
