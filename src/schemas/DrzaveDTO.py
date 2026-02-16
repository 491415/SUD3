from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class DrzaveDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu država.

    JSON - drzave (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv države.")
    oznaka_2: str = Field(..., min_length=2, max_length=2, description="ISO dvoslovna oznaka države.")
    oznaka_3: str = Field(..., min_length=3, max_length=3, description="ISO troslovna oznaka države.")
