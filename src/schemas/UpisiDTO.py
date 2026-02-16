from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

T = TypeVar("T", bound="UpisiDTO")


class UpisiDTO(BaseModel):
    """
    Model za tablicu provedenih upisa nad subjektima.

    JSON - upisi (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="ignore",
        validate_default=True,
        str_strip_whitespace=True
    )

    id: int = Field(..., ge=1, le=999_999_999_999, description="ID upisa (primarni ključ).")
    mbs: int = Field(..., ge=1, le=999_999_999, description="Matični broj subjekta u sudskom registru.")
    prbu: int = Field(..., ge=1, le=9_999, description="Pravni redni broj upisa.")
    podbroj: Optional[int] = Field(None, ge=1, le=9_999_999_999, description="Pravni redni podbroj upisa.")
    virtualni_upis: int = Field(..., ge=0, le=9, description="Oznaka da je upis virtualan.")
    sud_id: int = Field(..., ge=1, le=999_999_999_999, description="ID suda ili stalne službe koja je provela upis.")
    datum_upisa: datetime = Field(..., description="Datum kada je upis pravomoćno proveden i od kada upisani podaci vrijede.")
    poslovni_broj: str = Field(..., min_length=1, max_length=79, description="Poslovni broj rješenja o upisu.")

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste UpisiDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista UpisiDTO objekata za konverziju.

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
