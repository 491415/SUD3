from typing import Dict, List, Any, TypeVar

from pydantic import ConfigDict, Field, BaseModel

T = TypeVar("T", bound="PodruznicaDTO")

class PodruznicaDTO(BaseModel):
    """
    Model za tablicu podružnica subjekata.

    JSON - podruznice (naziv tablice u .json konfiguracijskom fileu)
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
    podruznica_rbr: int = Field(..., ge=1, le=9999, description="Redni broj podružnice u subjektu.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste PodruznicaDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista PodruznicaDTO objekata za konverziju.

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
