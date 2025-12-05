from typing import Optional

from pydantic import Field, field_validator

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class ObjavaPriopcenjaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu načina objave priopćenja subjekata.

    JSON - objave_priopcenja (naziv tablice u .json konfiguracijskom fileu)
    """

    tekst: Optional[str] = Field(None, max_length=1000, description="Tekst koji opisuje gdje subjekt objavljuje priopćenja.")
