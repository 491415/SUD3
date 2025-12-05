from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class JezikDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu jezika.

    JSON - jezici (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv jezika.")
