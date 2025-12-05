from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaClanaSubjektaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta članova subjekata.

    JSON - vrste_clanova_subjekata (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste člana subjekta.")
