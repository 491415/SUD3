from datetime import date
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# Osigurava da type hintovi rade kako treba sa nasljeđivanjem klase.
T = TypeVar("T", bound="ReferencaPodatkaDTO")


class ReferencaPodatkaDTO(BaseModel):
    """
    Base model za podatke koji imaju reference tablica.

    Ova polja se pojavljuju u nekoliko tablica pa je napravljena zasebna klasa
    da se ne ponavljaju u DTO modelima pojedinih tablica.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    id: int = Field(..., ge=1, le=999_999_999_999, description="Primary key ID")
    sifra: int = Field(..., ge=1, le=999_999, description="Šifra države, jezika, grupe, itd...")
    vrijedi_od: Optional[date] = Field(None, description="Podatak vrijedi od.")
    vrijedi_do: Optional[date] = Field(None, description="Podatak vrijedi do.")
    status: Optional[int] = Field(None, ge=0, le=9, description="Status podatka (0, 1, 5, 8, 9)).")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls,dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste PovijestPodatkaDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista PovijestPodatkaDTO objekata za konverziju.

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
