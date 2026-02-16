from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PrijevodiTvrtkiDTO(PovijestPodatkaDTO):
    """
    Model za tablicu prijevoda tvrtki subjekata.

    JSON - prijevodi_tvrtki (naziv tablice u .json konfiguracijskom fileu)
    """

    prijevod_tvrtke_rbr: int = Field(..., ge=1, le=999, description="Redni broj prijevoda.")
    ime: str = Field(..., min_length=1, max_length=1024, description="Prijevod tvrtke.")
    jezik_id: int = Field(..., ge=1, le=999_999_999_999, description="ID jezika.")
