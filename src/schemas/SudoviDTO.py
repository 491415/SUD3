from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class SudoviDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu sudova.

    JSON - sudovi (naziv tablice u .json konfiguracijskom fileu)
    """
    # Override polja iz parent klase
    # ge=0 stavljeno jer ima podatak sa ID-em '0'
    id: int = Field(..., ge=0, le=999_999_999_999, description="Primary key ID")
    sifra: int = Field(..., ge=0, le=999_999, description="Šifra države, jezika, grupe, itd...")

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv suda.")
    sifra_zupanije: int = Field(..., ge=1, le=999, description="Šifra županije.")
    naziv_zupanije: str = Field(..., min_length=1, max_length=128, description="Naziv županije.")
    sifra_opcine: int = Field(..., ge=1, le=99_999, description="Šifra općine.")
    naziv_opcine: str = Field(..., min_length=1, max_length=128, description="Naziv općine.")
    sifra_naselja: int = Field(..., ge=1, le=9_999_999_999, description="Šifra naselja.")
    naziv_naselja: str = Field(..., min_length=1, max_length=128, description="Naziv naselja.")
    sud_id_nadlezan: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID nadležnog suda (samo za stalne službe).")
    izdaje_izvatke: int = Field(..., ge=0, le=9, description="Oznaka da li sud izdaje izvatke.")
