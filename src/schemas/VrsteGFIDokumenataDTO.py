from typing import Any, Dict, List, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound="VrsteGFIDokumenataDTO")


class VrsteGFIDokumenataDTO(BaseModel):
    """
    Model za tablicu vrsta GFI dokumenata.

    JSON - vrste_gfi_dokumenata (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    vrsta: int = Field(..., ge=0, le=9, description="Šifra vrste GFI dokumenta (ujedno i primarni ključ).")
    znacenje: str = Field(..., min_length=1, max_length=256, description="Naziv vrste GFI dokumenta.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste VrsteGFIDokumenataDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista VrsteGFIDokumenataDTO objekata za konverziju.

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
