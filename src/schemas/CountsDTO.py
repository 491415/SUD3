from typing import TypeVar, Dict, List, Any

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound="CountsDTO")

class CountsDTO(BaseModel):
    """
    Model za tablicu ukupnog broja dostupnih aktivnih i povijesnih redaka za sve metode/tablice.

    JSON - counts (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    table_name: str = Field(..., min_length=1, max_length=128, description="Ime tablice/metode.")
    count_svi: int = Field(..., ge=0, description="Ukupni broj svih redaka.")
    count_aktivni: int = Field(..., ge=0, description="Ukupni broj aktivnih redaka.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste CountsDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista CountsDTO objekata za konverziju.

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
