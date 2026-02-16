from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class SjedistaPodruznicaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu sjedišta i adresa podružnica subjekata.

    JSON - sjedista_podruznica (naziv tablice u .json konfiguracijskom fileu)
    """

    podruznica_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj podružnice u subjektu.")
    sifra_zupanije: int = Field(..., ge=0, le=999, description="Šifra županije.")
    naziv_zupanije: str = Field(..., min_length=1, max_length=128, description="Naziv županije.")
    sifra_opcine: int = Field(..., ge=0, le=99_999, description="Šifra općine.")
    naziv_opcine: str = Field(..., min_length=1, max_length=128, description="Naziv općine.")
    sifra_naselja: int = Field(..., ge=0, le=9_999_999_999, description="Šifra naselja.")
    naziv_naselja: str = Field(..., min_length=1, max_length=128, description="Naziv naselja.")
    sifra_ulice: Optional[int] = Field(None, ge=1, le=9_999_999_999, description="Šifra ulice.")
    ulica: Optional[str] = Field(None, max_length=512, description="Ulica.")
    kucni_broj: Optional[int] = Field(None, le=999_999, description="Kućni broj.")
    kucni_podbroj: Optional[str] = Field(None, max_length=10, description="Kućni podbroj.")
