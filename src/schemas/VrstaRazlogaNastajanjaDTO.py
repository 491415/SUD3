from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaRazlogaNastavljanjaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta razloga nastavljanja subjekta

    JSON - vrste_razloga_nastavljanja (naziv tablice u .json konfiguracijskom fileu)
    """

    tekst: str = Field(..., min_length=1, max_length=100, description="Tekst razloga nastavljanja subjekta.")
