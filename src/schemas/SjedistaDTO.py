from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class SjedistaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu sjedišta i adresa subjekata.

    JSON - sjedista (naziv tablice u .json konfiguracijskom fileu)
    """

    drzava_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID države (za domaća sjedišta je NULL).")
    sifra_zupanije: Optional[int] = Field(None, ge=0, le=999, description="Šifra županije.")
    naziv_zupanije: Optional[str] = Field(None, max_length=128, description="Naziv županije.")
    sifra_opcine: Optional[int] = Field(None, ge=0, le=99_999, description="Šifra općine.")
    naziv_opcine: Optional[str] = Field(None, max_length=128, description="Naziv općine.")
    sifra_naselja: Optional[int] = Field(None, ge=0, le=9_999_999_999, description="Šifra naselja.")
    naziv_naselja: Optional[str] = Field(None, max_length=128, description="Naziv naselja.")
    naselje_van_sifrarnika: Optional[str] = Field(None, max_length=128, description="Naziv stranog naselja.")
    sifra_ulice: Optional[int] = Field(None, ge=1, le=9_999_999_999, description="Šifra ulice.")
    ulica: Optional[str] = Field(None, max_length=512, description="Naziv ulice.")
    kucni_broj: Optional[int] = Field(None, le=999_999, description="Kućni broj.")
    kucni_podbroj: Optional[str] = Field(None, max_length=10, description="Kućni podbroj.")
    postanski_broj: Optional[int] = Field(None, ge=10000, le=99_999, description="Poštanski broj.")
