from decimal import Decimal
from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class UdjeliClanovaSubjekataDTO(PovijestPodatkaDTO):
    """
    Model za tablicu (osnivačkih) udjela članova subjekata.

    JSON - udjeli_clanova_subjekata (naziv tablice u .json konfiguracijskom fileu)
    """

    clan_subjekta_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj člana subjekta.")
    udjel_rbr: int = Field(..., ge=0, le=9_999, description="Redni broj udjela.")
    prbu_podbroj_od: Optional[int] = Field(None, ge=1, le=9_999_999_999, description="Pravni redni podbroj upisa (samo za virtualne upise).")
    prbu_podbroj_do: Optional[int] = Field(None, ge=1, le=9_999_999_999, description="Pravni redni podbroj upisa (samo za virtualne upise).")
    nominalni_iznos: Decimal = Field(..., ge=0, max_digits=20, decimal_places=2, description="Nominalni iznos udjela.")
    broj_udjela: int = Field(..., ge=0, le=999_999_999_999_999, description="Broj udjela člana subjekta.")
    divizor: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="Divizor.")
    identifikator_udjela: Optional[str] = Field(None, max_length=2000, description="Identifikator udjela (opis ili redni broj unutar cijelog subjekta).")
    napomena_udjela: Optional[str] = Field(None, max_length=2000, description="Napomena.")
    valuta_id: int = Field(..., ge=1, le=999_999_999_999, description="ID valute.")
