from decimal import Decimal
from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class TemeljniKapitalDTO(PovijestPodatkaDTO):
    """
    Model za tablicu temeljnih kapitala subjekata.

    JSON - temeljni_kapitali (naziv tablice u .json konfiguracijskom fileu)
    """

    iznos: Decimal = Field(..., ge=0, max_digits=20, decimal_places=2, description="Iznos temeljnog kapitala.")
    valuta_id: int = Field(..., ge=1, description="ID valute.")
    temeljni_kapital_rbr: Optional[int] = Field(None, ge=0, description="Redni broj temeljnog kapitala.")
