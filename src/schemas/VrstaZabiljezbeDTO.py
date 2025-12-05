from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaZabiljezbeDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta zabilježbi.

    JSON - vrste_zabiljezbi (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste zabilježbe.")
