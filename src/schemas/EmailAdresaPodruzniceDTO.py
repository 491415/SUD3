from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class EmailAdresaPodruzniceDTO(PovijestPodatkaDTO):
    """
    Model za tablicu e-mail adresa podružnica.

    JSON - email_adrese_podruznica (naziv tablice u .json konfiguracijskom fileu)
    """

    podruznica_rbr: int = Field(..., ge=1, le=9999, description="Redni broj podružnice u subjektu.")
    email_adresa_rbr: int = Field(..., ge=1, le=999, description="Redni broj adrese u podružnici.")
    adresa: str = Field(..., min_length=3, max_length=256, description="E-mail adresa.")
