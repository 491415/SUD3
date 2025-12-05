from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PrijevodSkracenaTvrtkaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu prijevoda skraćenih tvrtki subjekata.

    JSON - prijevodi_skracenih_tvrtki (naziv tablice u .json konfiguracijskom fileu)
    """

    prijevod_skracene_tvrtke_rbr: int = Field(..., ge=1, le=999, description="Redni broj prijevoda.")
    ime: str = Field(..., min_length=1, max_length=512, description="Prijevod skraćene tvrtke.")
    jezik_id: int = Field(..., ge=1, description="ID jezika.")
