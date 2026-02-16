from typing import Any, Dict, List, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound="GrupeVrstaFunkcijaDTO")


class GrupeVrstaFunkcijaDTO(BaseModel):
    """
    Model za tablicu grupa vrsta funkcija.

    JSON - grupe_vrsta_funkcija (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    id: int = Field(..., ge=1, le=999_999_999_999, description="ID grupe (primarni ključ).")
    sifra: int = Field(..., ge=1, le=999, description="Šifra grupe.")
    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv grupe.")
    uprava: int = Field(..., ge=0, le=9, description="Da li se grupa odnosi na zastupnike/ovlaštenike.")
    clanovi_subjekta: int = Field(..., ge=0, le=9, description="Da li se grupa odnosi na članove subjekata/osnivače.")
    pismena: int = Field(..., ge=0, le=9, description="Da li se grupa odnosi na osobe ovlaštene za zaprimanje pismena i obavijesti.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste GrupeVrstaFunkcijaDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista GrupeVrstaFunkcijaDTO objekata za konverziju.

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
