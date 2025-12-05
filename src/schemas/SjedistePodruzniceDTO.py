from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class SjedistePodruzniceDTO(PovijestPodatkaDTO):
    """
    Model za tablicu sjedišta i adresa podružnica subjekata.

    JSON - sjedista_podruznica (naziv tablice u .json konfiguracijskom fileu)
    """

    podruznica_rbr: int = Field(..., ge=1, le=9999, description="Redni broj podružnice u subjektu.")
    sifra_zupanije: Optional[int] = Field(None, ge=0, le=999, description="Šifra županije.")
    naziv_zupanije: str = Field(..., min_length=1, max_length=128, description="Naziv županije.")
    sifra_opcine: Optional[int] = Field(None, ge=0, le=99999, description="Šifra općine.")
    naziv_opcine: str = Field(..., min_length=1, max_length=128, description="Naziv općine.")
    sifra_naselja: Optional[int] = Field(None, ge=0, le=9999999999, description="Šifra naselja.")
    naziv_naselja: str = Field(..., min_length=1, max_length=128, description="Naziv naselja.")
    sifra_ulice: Optional[int] = Field(None, ge=1, le=9999999999, description="Šifra ulice.")
    ulica: Optional[str] = Field(None, max_length=512, description="Ulica.")
    kucni_broj: Optional[int] = Field(None, le=999999, description="Kućni broj.")
    kucni_podbroj: Optional[str] = Field(None, max_length=10, description="Kućni podbroj.")
