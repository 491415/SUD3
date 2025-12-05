from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PravniSljednikDTO(PovijestPodatkaDTO):
    """
    Model za tablicu pravnih sljednika subjekata.

    JSON - pravni_sljednici (naziv tablice u .json konfiguracijskom fileu)
    """

    pravni_sljednik_rbr: int = Field(..., ge=1, le=999, description="Redni broj pravnog sljednika subjekta.")
    mbs_sljednika_u_registru: Optional[int] = Field(None, ge=1, le=999999999, description="Matični broj subjekta.")
    naziv_sljednika_izvan_registra: Optional[str] = Field(None, max_length=1024, description="Ime pravnog sljednika (za subjekte sljednike izvan sudskog registra).")
    oib_sljednika_izvan_registra: Optional[int] = Field(None, ge=0, le=99999999999, description="OIB pravnog sljednika (za subjekta sljednike izvan sudskog registra).")
