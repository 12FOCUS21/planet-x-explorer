# Planet X Explorer

**Explore, compare, understand.** An educational SPHEREx image-comparison application with a reproducible synthetic demo and a separate, on-demand NASA/IPAC IRSA workflow.

## Choose your language / Elige tu idioma

| English — for the jury | Español |
| --- | --- |
| [Complete documentation](docs/en/README.md) | [Documentación completa](docs/es/README.md) |
| [Project report](docs/en/PROJECT_REPORT.md) · [Word](docs/en/Planet_X_Explorer_Professional_Report.docx) · [PDF](docs/en/Planet_X_Explorer_Professional_Report.pdf) | [Memoria Word](docs/es/Planet_X_Explorer_Informe_Profesional_Mejorado.docx) · [PDF](docs/es/Planet_X_Explorer_Informe_Profesional_Mejorado.pdf) |
| [Jury demonstration](docs/en/JURY_HANDOFF.md) | [Demostración para el jurado](docs/es/ENTREGA_JURADO.md) |
| [Complete video script](docs/en/COMPLETE_VIDEO_GUIDE.md) | [Guion completo de video](docs/es/GUIA_COMPLETA_VIDEO.md) |
| [Language switch and tests](docs/en/BILINGUAL.md) | [Selector de idioma y pruebas](docs/es/BILINGUISMO.md) |

**In the application:** use the **Español / English** selector in the header. The preference is stored in your browser. Changing language does not start an IRSA search, reset a comparison or reset your quiz answers. The academic content, states, errors and exported CSV descriptions support both languages.

## Run locally

Install Python 3.12, then double-click `INICIAR_WINDOWS.bat`, or run from the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe scripts\launch.py
```

Open **http://127.0.0.1:8000**, select **English**, then **Try guided demo → choose A/B → Compare → Review differences**. The first installation requires Internet; the synthetic demo does not require external services afterward. Stop the server with `Ctrl+C`.

## Scientific and operational status

- Planet Nine / Planet X remains hypothetical. This application **does not confirm a planet**.
- Demo pixels are **synthetic**, not NASA measurements. An empty IRSA response never becomes an unlabelled simulation.
- IRSA uses DR1, QR3 and their deep collections; **no QR2 fallback**. Per-pixel LVF equivalence, FLAGS/VARIANCE and PSF handling are not fully validated.
- Repository: **[12FOCUS21/planet-x-explorer](https://github.com/12FOCUS21/planet-x-explorer)**. Public source code is **not a public application deployment**.
- The intended hosting budget is **USD 0**, with on-demand use and no permanent service. Video recording and a new end-to-end IRSA download remain pending.
- AI assistance: OpenCode with **Sol 6.1, Astra and DeepSeek**, as declared by the team. The team remains responsible for review and claims.

See the [documentation index](docs/README.md), [scientific methodology](docs/en/methodology.md), [testing guide](docs/en/TESTING.md) and [MIT license](LICENSE).
