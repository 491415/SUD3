from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class ValuteDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu valuta.

    JSON - valute (naziv tablice u .json konfiguracijskom fileu)
    """

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv valute.")
    drzava_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID države.")
