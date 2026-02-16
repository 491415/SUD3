from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrsteFunkcijaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta funkcije.

    JSON - vrste_funkcija (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste funkcije.")
    grupa_vrste_funkcije_id: int = Field(..., ge=1, le=999_999_999_999, description="ID grupe funkcije.")
    ovlast_zastupanja: int = Field(..., ge=0, le=9, description="Oznaka da osoba sa ovom funkcijom ima ovlast zastupanja subjekta.")
