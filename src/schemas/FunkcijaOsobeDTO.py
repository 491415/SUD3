from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class FunkcijaOsobeDTO(PovijestPodatkaDTO):
    """
    Model za tablicu funkcija osoba subjekata.

    JSON - funkcije_osoba (naziv tablice u .json konfiguracijskom fileu)
    """

    podruznica_rbr: Optional[int] = Field(None, ge=1, le=9999, description="Redni broj podružnice (ukoliko se funkcija odnosi samo na podružnicu).")
    osoba_rbr: int = Field(..., ge=0, le=999, description="Redni broj osobe u subjektu.")
    funkcija_osobe_rbr: int = Field(..., ge=1, le=99, description="Redni broj funkcije osobe.")
    vrsta_funkcije_id: int = Field(..., ge=1, description="ID vrste funkcije.")
