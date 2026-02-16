from decimal import Decimal
from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class UloziClanovaSubjekataDTO(PovijestPodatkaDTO):
    """
    Model za tablicu uloga članova subjekata.

    JSON - ulozi_clanova_subjekata (naziv tablice u .json konfiguracijskom fileu)
    """

    clan_subjekta_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj člana subjekta.")
    ulog_rbr: int = Field(..., ge=1, le=99, description="Redni broj uloga.")
    valuta_id: int = Field(..., ge=1, le=999_999_999_999, description="ID valute.")
    vrsta_kapitala_id: int = Field(..., ge=1, le=999_999_999_999, description="ID vrste kapitala.")
    iznos_uloga: Optional[Decimal] = Field(None, ge=0, max_digits=20, decimal_places=2, description="Iznos uloga.")
