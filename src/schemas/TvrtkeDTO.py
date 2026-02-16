from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class TvrtkeDTO(PovijestPodatkaDTO):
    """
    Model za tablicu tvrtki (naziva) subjekata.

    JSON - tvrtke (naziv tablice u .json konfiguracijskom fileu)
    """

    ime: str = Field(..., min_length=1, max_length=1024, description="Puna tvrtka/naziv subjekta upisa.")
    naznaka_imena: Optional[str] = Field(None, max_length=512, description="Naznaka tvrtke/naziva.")
