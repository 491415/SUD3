from datetime import datetime
from typing import Dict, List, Any, TypeVar

from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T", bound="PromjeneDTO")

class PromjeneDTO(BaseModel):
    """
    Model za tablicu zadnjih promjena nad subjektima

    JSON - promjene (naziv tablice u .json konfiguracijskom fileu)
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
    id: int = Field(..., ge=1, description="ID promjene (primarni ključ).")
    vrijeme: datetime = Field(..., description="Datum i vrijeme promjene.")
    scn: int = Field(..., ge=0, description="Sistemski broj promjene - System change number (monotono rastuća sekvenca, koristi se za detekciju promjena).")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste PromjeneDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista PromjeneDTO objekata za konverziju.

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
