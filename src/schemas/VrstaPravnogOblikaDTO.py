from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaPravnogOblikaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta pravnih oblika.

    JSON - vrste_pravnih_oblika (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste pravnog oblika.")
    kratica: str = Field(..., min_length=1, max_length=15, description="Kratica vrste pravnog oblika.")
