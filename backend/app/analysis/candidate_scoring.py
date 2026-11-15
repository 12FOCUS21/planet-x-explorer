"""Ordenamiento para revisión humana, NO puntuación de posibilidad planetaria."""
def prioritize(items: list[dict]) -> list[dict]:
    return sorted(items,key=lambda x:(x['shift_px'] is not None, x['snr']),reverse=True)
