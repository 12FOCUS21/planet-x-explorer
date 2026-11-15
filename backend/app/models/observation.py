"""Esquema de cada observación presentada por la interfaz."""
from pydantic import BaseModel, Field

class Region(BaseModel):
    ra: float = Field(ge=0, lt=360)
    dec: float = Field(ge=-90, le=90)
    radius: float = Field(default=0.08, ge=0.008, le=0.3)

class Observation(BaseModel):
    id: str
    label: str
    date: str
    detector: str
    band: str
    source: str
    collection: str
    simulated: bool
