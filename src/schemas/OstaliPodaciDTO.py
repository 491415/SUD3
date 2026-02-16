from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class OstaliPodaciDTO(PovijestPodatkaDTO):
    """
    Model za tablicu ostalih podataka o subjektima.

    JSON - ostali_podaci (naziv tablice u .json konfiguracijskom fileu)
    """

    vrsta_porijekla_kapitala_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID vrste porijekla kapitala.")
    vrsta_oblika_vlasnistva_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID vrste oblika vlasništva.")
    sud_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID suda.")
    vrsta_razloga_prestanka_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID vrste razloga prestanka.")
    vrsta_razloga_nastavljanja_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID razloga nastavljanja.")
    rul: Optional[int] = Field(None, ge=0, le=999_999, description="Broj registarskog uloška (u starom trgovačkom registru).")
    rul1: Optional[int] = Field(None, ge=0, le=9, description="Predbroj registarskog uloška (u starom trgovačkom registru).")
