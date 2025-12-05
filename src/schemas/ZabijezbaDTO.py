from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class ZabiljezbaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu zabilježbi subjekata.

    JSON - zabiljezbe (naziv tablice u .json konfiguracijskom fileu)
    """

    zabiljezba_rbr: int = Field(..., ge=0, le=999, description="Redni broj zabilježbe.")
    tekst: Optional[str] = Field(None, max_length=4000, description="Tekst zabilježbe.")
    vrsta_zabiljezbe_id: int = Field(..., ge=1, description="ID vrste zabilježbe.")
