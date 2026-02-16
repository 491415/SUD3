from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class SkraceniNaziviPodruznicaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu skraćenih naziva podružnica subjekata.

    JSON - skraceni_nazivi_podruznica (naziv tablice u .json konfiguracijskom fileu)
    """""

    podruznica_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj podružnice u subjektu.")
    ime: str = Field(..., min_length=1, max_length=512, description="Naziv skraćene podružnice.")
