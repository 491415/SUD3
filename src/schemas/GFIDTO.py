from datetime import date
from typing import Dict, List, Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T", bound="GFIDTO")

class GFIDTO(BaseModel):
    """
    Model za tablicu predanih godišnjih financijskih izvješća subjekata.

    JSON - gfi (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    mbs: int = Field(..., ge=1, le=999999999, description="Matični broj subjekta u sudskom registru.")
    gfi_rbr: int = Field(..., ge=1, le=9999999999, description="Redni broj izvješća u subjektu.")
    vrsta_dokumenta: int = Field(..., ge=0, le=9, description="Vrsta dokumenta.")
    oznaka_konsolidacije: int = Field(..., ge=0, le=9, description="Označava da li je u pitanju konsolidirano izvješće.")
    godina_izvjestaja: int = Field(..., ge=1900, le=2100, description="Godina za koju je izvješće predano.")
    datum_dostave: date = Field(..., description="Datum dostave izvještaja.")
    datum_od: date = Field(..., description="Datum početka izvještajnog perioda GFI.")
    datum_do: date = Field(..., description="Datum završetka izvještajnog perioda GFI.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste GFIDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista GFIDTO objekata za konverziju.

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
