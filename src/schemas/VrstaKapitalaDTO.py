from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaKapitalaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta kapitala.

    JSON - vrste_kapitala (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste kapitala")
