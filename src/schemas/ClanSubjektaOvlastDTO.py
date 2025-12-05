from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class ClanSubjektaOvlastDTO(PovijestPodatkaDTO):
    """
    Model za tablicu ovlasti članova subjekata.

    JSON - ovlasti_clanova_subjekata (naziv tablice u .json konfiguracijskom fileu)
    """

    clan_subjekta_rbr: int = Field(..., ge=1, le=9999, description="Redni broj člana subjekta.")
    funkcija_clana_subjekta_rbr: int = Field(..., ge=1, le=99, description="Redni broj funkcije člana subjekta.")
    ovlast_clana_subjekta_rbr: int = Field(..., ge=1, le=99, description="Redni broj ovlasti člana subjekta.")
    ovlast_tekst: str = Field(..., min_length=1, max_length=2000, description="Opis ovlasti.")
