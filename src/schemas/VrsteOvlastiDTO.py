from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrsteOvlastiDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu ovlasti.

    JSON - vrste_ovlasti (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste ovlasti.")
