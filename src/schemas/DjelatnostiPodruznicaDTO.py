from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class DjelatnostiPodruznicaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu djelatnosti podružnica.

    JSON - djelatnosti_podruznica (naziv tablice u .json konfiguracijskom fileu)
    """

    podruznica_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj podružnice u subjektu.")
    djelatnost_rbr: int = Field(..., ge=1, le=999, description="Redni broj djelatnosti unutar podružnice.")
    nacionalna_klasifikacija_djelatnosti_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID djelatnosti prema NKD šifrarniku." ,
                                                                   alias="nac_klas_djelatnosti_id", serialization_alias="nac_klas_djelatnosti_id")
    djelatnost_tekst: Optional[str] = Field(None, max_length=4000, description="Naziv djelatnosti.")
