"""Detección: puntuación de significancia heurística, no probabilidad planetaria."""
from pydantic import BaseModel

class Candidate(BaseModel):
    id: str
    x: float
    y: float
    previous_x: float | None = None
    previous_y: float | None = None
    shift_px: float | None = None
    snr: float
    classification: str
    note: str
