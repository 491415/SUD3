from typing import Optional

from pydantic import Field, field_validator

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class EvidencijskaDjelatnostDTO(PovijestPodatkaDTO):
    """
    Model za tablicu evidencijskih djelatnosti subjekata.

    JSON - evidencijske_djelatnosti (naziv tablice u .json konfiguracijskom fileu)
    """

    djelatnost_rbr: int = Field(..., ge=1, le=999, description="Redni broj evidencijske djelatnosti.")
    nacionalna_klasifikacija_djelatnosti_id: Optional[int] = Field(None, ge=1, description="ID djelatnosti prema NKD šifrarniku.")
    djelatnost_tekst: Optional[str] = Field(None, max_length=3400, description="Naziv/opis djelatnosti.")
