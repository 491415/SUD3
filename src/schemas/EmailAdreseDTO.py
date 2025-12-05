from pydantic import field_validator, Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class EmailAdreseDTO(PovijestPodatkaDTO):
    """
    Model za tablicu e-mail adresa subjekata.

    JSON - email_adrese (naziv tablice u .json konfiguracijskom fileu)
    """

    email_adresa_rbr: int = Field(..., ge=1, le=999, description="Redni broj adrese u subjektu.")
    adresa: str = Field(..., min_length=1, max_length=256, description="E-mail adresa.")
