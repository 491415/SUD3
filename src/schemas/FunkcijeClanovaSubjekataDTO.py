from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class FunkcijeClanovaSubjekataDTO(PovijestPodatkaDTO):
    """
    Model za tablicu funkcija članova subjekata.

    JSON - funkcije_clanova_subjekata (naziv tablice u .json konfiguracijskom fileu)
    """

    clan_subjekta_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj člana subjekta.")
    funkcija_clana_subjekta_rbr: int = Field(..., ge=1, le=99, description="Redni broj funkcije člana subjekta.")
    vrsta_funkcije_id: int = Field(..., ge=1, le=999_999_999_999, description="ID vrste funkcije.")
