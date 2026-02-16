from typing import Any, Dict, List, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound="VrstePostupakaDTO")


class VrstePostupakaDTO(BaseModel):
    """
    Model za tablicu vrsta postupaka.

    JSON - vrste_postupaka (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    postupak: int = Field(..., ge=0, le=9, description="Šifra vrste postupka (ujedno i primarni ključ).")
    znacenje: str = Field(..., min_length=1, max_length=256, description="Naziv vrste postupka.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste VrstePostupakaDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista VrstePostupakaDTO objekata za konverziju.

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
