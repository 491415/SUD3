from datetime import date
from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PostupakDTO(PovijestPodatkaDTO):
    """
    Model za tablicu postupaka nad subjektima.

    JSON - postupci (naziv tablice u .json konfiguracijskom fileu)
    """

    postupak: int = Field(..., ge=0, le=9, description="Šifra postupka (stečaj, likvidacija, ...)")
    datum_stecaja: Optional[date] = Field(None,
                                          description="Datum donošenja rješenja stečajnog odjela suda o pokretanju stečajnog postupka.")
