from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound="BrisPravniObliciDTO")


class BrisPravniObliciDTO(BaseModel):
    """
    Model za tablicu BRIS pravnih oblika.

    JSON - bris_pravni_oblici (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    bris_kod: str = Field(..., min_length=1, max_length=9, description="Šifra BRIS pravnog oblika (ujedno i primarni ključ).")
    kratica: Optional[str] = Field(None, max_length=130, description="Skraćeni naziv BRIS pravnog oblika.")
    naziv: str = Field(..., min_length=1, max_length=1024, description="Naziv BRIS pravnog oblika.")
    drzava_id: int = Field(..., ge=1, le=999_999_999_999, description="ID države kojoj pravni oblik pripada.")
    vrsta_pravnog_oblika_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID vrste odgovarajućeg pravnog oblika u RH.")
    status: int = Field(..., ge=0, le=9, description="Status podatka (vidi odjeljak Standardni mehanizam povijesnosti u uputama za razvojne inženjere).")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste BrisPravniObliciDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista BrisPravniObliciDTO objekata za konverziju.

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
