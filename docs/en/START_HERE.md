# Planet X Explorer — loading repair and first steps

[English](README.md) · [Español](../es/LEEME_PRIMERO.md)

Historical package instructions retained for reproducibility. For the current on-demand demonstration see [jury handoff](JURY_HANDOFF.md); this is not evidence of a public deployment.

1. Close the previous Python server with `Ctrl+C`.
2. Extract the ZIP into a new directory; retain the original as a backup.
3. Run `INICIAR_WINDOWS.bat`. Initial installation needs Internet and Python 3.12.
4. Select **English** in the application header. For IRSA, click **Search observations**, then **Compare** if a compatible pair exists.
5. Incompatible B options are disabled. The comparison reports download/processing status. Cutouts are downloaded automatically; there is no need to download each FITS manually.
6. The home page includes a 3D illustration, not NASA observations.

Wait for status messages if IRSA is slow. Retrying reuses complete cutouts and discards incomplete downloads. If no pair is compatible, change A or the region; the app does not fabricate real data. Demo is a separate, labelled synthetic option.

The package retains FastAPI/HTML. Environments and personal captures are not bundled; the launcher installs dependencies. Code is published in **12FOCUS21/planet-x-explorer**, but the application is not publicly deployed. See [hosting](FREE_HOSTING.md) and [historical corrections](CORRECTIONS.md). The prototype neither confirms Planet X nor guarantees a competition result.
