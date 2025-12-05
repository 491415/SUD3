from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PartnerStatusniPostupakDTO(PovijestPodatkaDTO):
    """
    Model za tablicu partnera u statusnim postupcima subjekata.
    
    JSON - partneri_statusnih_postupaka (naziv tablice u .json konfiguracijskom fileu)
    """

    statusni_postupak_rbr: int = Field(..., ge=1, le=999, description="Redni broj statusnog postupka.")
    partner_rbr: int = Field(..., ge=1, le=999, description="Redni broj partnera statusnog postupka.")
    naziv: str = Field(..., min_length=1, max_length=1024, description="Naziv partnera.")
    sifra_zupanije: Optional[int] = Field(None, ge=1, le=999, description="Šifra županije.")
    naziv_zupanije: Optional[str] = Field(None, max_length=128, description="Naziv županije.")
    sifra_opcine: Optional[int] = Field(None, ge=1, le=99999, description="Šifra općine.")
    naziv_opcine: Optional[str] = Field(None, max_length=128, description="Naziv općine.")
    sifra_naselja: Optional[int] = Field(None, ge=1, le=9999999999, description="Šifra naselja.")
    naziv_naselja: Optional[str] = Field(None, max_length=128, description="Naziv naselja.")
    ulica: Optional[str] = Field(None, max_length=35, description="Ulica.")
    kucni_broj: Optional[int] = Field(None, ge=1, le=999999, description="Kućni broj.")
    kucni_podbroj: Optional[str] = Field(None, max_length=10, description="Kućni podbroj.")
