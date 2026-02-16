from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class EvidencijskeDjelatnostiDTO(PovijestPodatkaDTO):
    """
    Model za tablicu evidencijskih djelatnosti subjekata.

    JSON - evidencijske_djelatnosti (naziv tablice u .json konfiguracijskom fileu)
    """

    djelatnost_rbr: int = Field(..., ge=1, le=999, description="Redni broj evidencijske djelatnosti.")
    nacionalna_klasifikacija_djelatnosti_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID djelatnosti prema NKD šifrarniku.")
    djelatnost_tekst: Optional[str] = Field(None, max_length=4000, description="Naziv/opis djelatnosti.")
