# Spanish / English application and documentation

[English](README.md) · [Español](../es/BILINGUISMO.md)

## Using the selector

Use **Español / English** in the header, on desktop or mobile. Spanish is the default when no preference exists. `px-language` in localStorage remembers the selection. If browser storage is blocked, switching still works for the current page. No online translation service, paid API or permanent server is required.

The selector updates navigation, home, forms, progress, accessibility labels, source descriptions, observations, analysis, lessons, quiz feedback, known server messages and exported CSV descriptions. Institutional names, collection identifiers, numbers, timestamps and coordinates remain unchanged. Source screenshots in translated documents can retain original Spanish labels; this is explicitly disclosed.

Switching does not query IRSA, reset coordinates/observations, restart a comparison job, erase analysis or reset a quiz answer. Lesson previews rerender in the chosen language; an open dialog translates without losing its close/focus behaviour.

## Implementation

- `frontend/locales/en.json`: local Spanish-to-English catalogue including parameterized messages.
- `frontend/js/i18n.js`: reversible text/attribute presentation translation, preserved source strings, dynamic-content observation and bounded cache. It never replaces element HTML, changes IDs, event handlers or input values.
- `frontend/js/main.js`: initializes language resources before the application workflow.
- `backend/app/localization.py`: optional localized JSON responses using `?lang=en` or `Accept-Language: en`; Spanish is the default. `Content-Language` and `Vary: Accept-Language` describe responses. Numbers and session objects remain intact. PNG responses are not translated.
- The browser deliberately requests canonical Spanish JSON for internal workflow matching, then localizes only presentation. CSV descriptions use the active language while scientific columns keep stable machine names.

## Verification

Run `python -m pytest tests -q` and `npm run qa:ui` from `frontend/` after installation. The Python suite covers English lessons/questions/sources, explicit language override, IDs/pair compatibility, error translation and session immutability. UI QA covers Spanish plus English home, search, three PNGs, analysis, CSV, switching during a job, lesson dialog, quiz feedback/answer preservation, reload persistence, opt-in IRSA failures, desktop/mobile overflow and axe.

These are controlled local checks, not a new successful IRSA download, physical-device study, comprehensive accessibility certification or public deployment. Historical reports keep their original 20/39-test counts; the bilingual suite currently contains 44 Python checks.

## Documentation structure

- `docs/es/`: Spanish documents and original report.
- `docs/en/`: English documentation, report in Markdown/Word/PDF, scripts and historical translations.
- Root README: English-first language entry point.
- `docs/README.md`: bilingual topic index.
- Old Markdown paths: compatibility links to both languages, avoiding deletion of the historical trail.

Documentation language and application language are independent. Changing the live selector does not translate a downloaded Word/PDF; use the corresponding language file. The application still runs locally on demand, with USD 0 intended hosting and no verified public deployment.
