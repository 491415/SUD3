from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class SkupneOvlastiDTO(PovijestPodatkaDTO):
    """
    Model za tablicu skupnih ovlasti subjekata.

    JSON - skupne_ovlasti (naziv tablice u .json konfiguracijskom fileu)
    """

    skupna_ovlast_rbr: int = Field(..., ge=1, le=999, description="Redni broj skupne ovlasti u subjektu.")
    grupa_vrste_funkcije_id: int = Field(..., ge=1, le=999_999_999_999, description="ID grupe.")
    ovlast_tekst: str = Field(..., min_length=1, max_length=2000,
                              description="Tekst skupnih ovlasti/ograničenja kod subjekta upisa.")
