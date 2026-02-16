from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrsteRazlogaPrestankaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta razloga prestanka subjekta.

    JSON - vrste_razloga_prestanka (naziv tablice u .json konfiguracijskom fileu)
    """

    tekst: str = Field(..., min_length=1, max_length=512, description="Tekst vrste razloga prestanka poslovanja.")
