from typing import Any, Dict, List, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound="UpisiVrsteUpisaDTO")


class UpisiVrsteUpisaDTO(BaseModel):
    """
    Model za tablicu vrsta upisa za provedene upise

    JSON - upisi_vrste_upisa (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    upis_id: int = Field(..., ge=1, le=999_999_999_999, description="ID upisa.")
    vrsta_upisa_id: int = Field(..., ge=1, le=999_999_999_999, description="ID vrste upisa.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste UpisiVrsteUpisaDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista UpisiVrsteUpisaDTO objekata za konverziju.

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
