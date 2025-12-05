from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class OstaloTekstDTO(PovijestPodatkaDTO):
    """
    Model za tablicu ostalih tekstova subjekata.
    
    JSON - ostali_tekstovi (naziv tablice u .json konfiguracijskom fileu)
    """

    tekst_rbr: int = Field(..., ge=1, le=999, description="Redni broj teksta u subjektu.")
    tekst: Optional[str] = Field(None, max_length=4000, description="Tekst.")
