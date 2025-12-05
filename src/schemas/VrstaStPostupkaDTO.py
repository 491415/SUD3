from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaStPostupkaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta statusnih postupaka.

    JSON - vrste_statusnih_postupaka (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste statusnog postupka.")
    redoslijed: int = Field(..., ge=1, le=999, description="Redoslijed koji se koristi kod ispisa na izvacima i sl.")
