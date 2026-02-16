from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class OvlastiOsobaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu ovlasti osoba subjekata.

    JSON - ovlasti_osoba (naziv tablice u .json konfiguracijskom fileu)
    """

    osoba_rbr: int = Field(..., ge=0, le=999, description="Redni broj osobe u subjektu.")
    funkcija_osobe_rbr: int = Field(..., ge=1, le=99, description="Redni broj funkcije osobe.")
    ovlast_osobe_rbr: int = Field(..., ge=0, le=99, description="Redni broj ovlasti osobe.")
    ovlast_tekst: Optional[str] = Field(None, max_length=2000, description="Opis ovlasti.")
    vrsta_ovlasti_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID vrste ovlasti.")
