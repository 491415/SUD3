from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

T = TypeVar("T", bound="DokumentiDTO")


class DokumentiDTO(BaseModel):
    """
    Model za tablicu dokumenata digitalne zbirke isprava subjekata (sa URL-ovima putem kojih se mogu preuzeti).

    JSON - dokumenti (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    id: int = Field(..., ge=1, le=999_999_999_999, description="ID dokumenta digitalne zbirke isprava (primarni ključ).")
    dokument_rbr: int = Field(..., ge=0, le=9_999, description="Redni broj dokumenta u digitalnoj zbirci isprava.")
    dokument_podbroj: Optional[int] = Field(None, le=9_999, description="Redni podbroj dokumenta u digitalnoj zbirci isprava.")
    sud_id: int = Field(..., ge=1, le=999_999_999_999, description="ID suda.")
    upisnik: str = Field(..., min_length=1, max_length=64, description="Vrsta upisnika (Tt / R3).")
    godina: int = Field(..., ge=0, le=99, description="Godina upisnika.")
    broj_spisa: int = Field(..., ge=1, le=99_999, description="Broj spisa u upisniku i godini.")
    broj_pismena: Optional[int] = Field(None, ge=0, le=99_999, description="Broj pismena u spisu.")
    poslovni_broj: str = Field(..., min_length=1, max_length=79, description="Poslovni broj samog pismena/dokumenta ili pismena na koje je dokument vezan.")
    mbs: Optional[int] = Field(None, ge=1, le=999_999_999, description="Matični broj subjekta u sudskom registru kojem dokument pripada.")
    opis: Optional[str] = Field(None, max_length=256, description="Naziv ili opis dokumenta.")
    datum: datetime = Field(..., description="Datum na dokumentu sa vremenom.")
    vrsta_priloga_id: int = Field(..., ge=1, le=999_999_999_999, description="ID vrste priloga/dokumenta.")
    jezik_id: Optional[int] = Field(None, ge=0, le=999_999_999_999, description="ID jezika dokumenta.")
    izvorni_dokument_id: Optional[int] = Field(None, ge=0, le=999_999_999_999, description="ID izvornog dokumenta (predstavlja izvornik prevedenog dokumenata).")
    ekstenzija: str = Field(..., min_length=1, max_length=16, description="Ekstenzija odnosno format originalne datoteke.")
    velicina: Optional[int] = Field(None, ge=0, le=999_999_999_999, description="Veličina datoteke (u byte-ima).")
    url: str = Field(..., min_length=1, max_length=337, description="Poveznica sa koje se dokument može preuzeti u digitalnom obliku (permalink).")
    broj_zadnje_izmjene: int = Field(..., ge=0, le=9_999_999_999_999_999_999,
                                     description="Redni broj zadnje izmjene retka (povećava se kod svake izmjene dokumenta, koristi se za brzu detekciju izmjene dokumenta bez analiziranja sadržaja).")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste DokumentiDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista DokumentiDTO objekata za konverziju.

        Returns:
            List[Dict[str, Any]]: Lista dictionarya objekata koji predstavljaju serijalizirane DTO objekte.
        """
        if not dto_list:
            return []

        return [dto.model_dump() for dto in dto_list]

    def __str__(self) -> str:
        """
        String reprezentacija objekta za logging i debugging.

        Returns:
            str: Potpuna reprezentacija objekta sa svim poljima..
        """
        return f"{self.__class__.__name__} ({self.model_dump()})"
