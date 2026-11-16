# Procedencia y enlaces científicos

[Español](README.md) · [English](../en/nasa_sources.md)

> Aclaración vigente: también se consultan `spherex_dr1_deep` y `spherex_qr3_deep`. La referencia a DR1/QR3 más abajo se conserva como parte de la documentación original.

Los datos **reales** de SPHEREx solo se recuperan de los servidores públicos NASA/IPAC IRSA mediante los protocolos oficiales. Las imágenes del modo demo se generan por software y contienen deliberadamente un objeto que se mueve, además de una fuente variable; no corresponden a ningún cuerpo celeste conocido.

## Archivo principal NASA/IPAC

- IRSA SPHEREx archive: https://irsa.ipac.caltech.edu/Missions/spherex.html
- SPHEREx Data Access (SIA2, colecciones, cutouts): https://irsa.ipac.caltech.edu/spherex-archive-documentation/spherex-data-access/
- Tutorial oficial de imágenes SPHEREx: https://caltech-ipac.github.io/irsa-tutorials/spherex-intro/
- Tutorial oficial de recortes SPHEREx: https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/
- Especificación de productos SPHEREx: https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-products/
- DOI recomendado para imágenes SPHEREx DR1: https://doi.org/10.26131/IRSA678
- DOI recomendado para el cubo DR1 de todo el cielo (no usado aquí): https://doi.org/10.26131/IRSA679

### Colecciones consultadas

`spherex_dr1`, `spherex_qr3` (imágenes Level 2 públicas). La app solicita listados con `https://irsa.ipac.caltech.edu/SIA` y `POS=CIRCLE ra dec radius`. Los recortes se solicitan con los parámetros oficiales `center` y `size`, sobre las URL `access_url` aportadas por SIA2. No usa credenciales ni claves.

**Advertencia**: IRSA puede limitar, retrasar o cambiar el servicio; las nuevas imágenes pueden tardar en indexarse. No se incluyen observaciones previamente bajadas dentro de este ZIP. La ruta en modo real necesita conexión y puede devolver 0 coincidencias.

## Fuente auxiliar: Gaia DR3 (ESA)

- https://gea.esac.esa.int/archive/
- https://docs.astropy.org/projects/astroquery/en/stable/gaia/gaia.html

Su archivo es de la Agencia Espacial Europea, no NASA. La app permite consultar hasta 40 estrellas brillantes en una pequeña región, sin utilizar ese resultado para confirmar candidatos. Las coincidencias automáticas requieren trabajo adicional.

## WISE (NASA/IPAC)

- https://irsa.ipac.caltech.edu/Missions/wise.html

WISE aparece como contexto histórico e inspiración metodológica; el motor de la primera versión no incorpora píxeles reales WISE a las comparaciones. No se atribuye ningún PNG a WISE.

## Atribución sugerida

> Este proyecto usa acceso a productos públicos SPHEREx del archivo NASA/IPAC IRSA y consultas auxiliares a Gaia DR3 de ESA. No está respaldado ni desarrollado por NASA o ESA.
