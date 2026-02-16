from datetime import date
from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class StatusniPostupciDTO(PovijestPodatkaDTO):
    """
    Model za tablicu statusnih postupaka (pravnih odnosa) subjekata

    JSON - statusni_postupci (naziv tablice u .json konfiguracijskom fileu)
    """

    statusni_postupak_rbr: int = Field(..., ge=0, le=999, description="Redni broj postupka u subjektu.")
    vrsta_statusnog_postupka_id: int = Field(..., ge=1, le=999_999_999_999, description="ID vrste statusnog postupka.")
    sud_id_rjesenja: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID suda rješenja na kojem se statusni postupak temelji.")
    poslovni_broj_rjesenja: Optional[str] = Field(None, max_length=240, description="Poslovni broj rješenja na kojem se statusni postupak temelji.")
    datum_rjesenja: Optional[date] = Field(None, description="Datum rješenja na kojem se statusni postupak temelji.")
    razlog_obustave: Optional[str] = Field(None, max_length=2000, description="Razlog obustave postupka.")
    tekst: Optional[str] = Field(None, description="Tekst statusnog postupka.")
