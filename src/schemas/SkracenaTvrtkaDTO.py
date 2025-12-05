from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class SkracenaTvrtkaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu skraćenih tvrtki subjekata.

    JSON - skracene_tvrtke (naziv tablice u .json konfiguracijskom fileu)
    """

    ime: str = Field(..., min_length=1, max_length=512, description="Naziv skraćene tvrtke.")
