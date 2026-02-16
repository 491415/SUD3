from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class NaziviPodruznicaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu naziva podružnica subjekata.

    JSON - nazivi_podruznica (naziv tablice u .json konfiguracijskom fileu)
    """

    podruznica_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj podružnice u subjektu.")
    ime: str = Field(..., min_length=1, max_length=1024, description="Puni naziv podružnice.")
    naznaka_imena: Optional[str] = Field(None, max_length=128, description="Naznaka imena podružnice.")
    postupak: int = Field(..., ge=0, le=9, description="Šifra postupak (stečaj, likvidacija, ...).")
    glavna_podruznica: int = Field(..., ge=0, le=9, description="Da li je ovo glavna podružnica inozemnog subjekta.")
