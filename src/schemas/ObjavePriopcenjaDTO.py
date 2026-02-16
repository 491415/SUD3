from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class ObjavePriopcenjaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu načina objave priopćenja subjekata.

    JSON - objave_priopcenja (naziv tablice u .json konfiguracijskom fileu)
    """

    tekst: Optional[str] = Field(None, max_length=2000, description="Tekst koji opisuje gdje subjekt objavljuje priopćenja.")
