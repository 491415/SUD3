from datetime import datetime
from typing import TypeVar, Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict, field_validator

T = TypeVar("T", bound="UpisDTO")

class UpisDTO(BaseModel):
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
        str_strip_whitespace=True,
    )

    id: Optional[int] = Field(None, ge=1, description="ID upisa (primarni ključ).", alias="upis_id")
    mbs: int = Field(..., ge=1, le=999999999, description="Matični broj subjekta u sudskom registru.")
    prbu: int = Field(..., ge=1, le=9999, description="Pravni redni broj upisa.")
    podbroj: Optional[str] = Field(None, max_length=20, description="Pravni redni podbroj upisa.")
    virtualni_upis: int = Field(..., ge=0, le=9, description="Oznaka da je upis virtualan.")
    sud_id: int = Field(..., ge=1, description="ID suda ili stalne službe koja je provela upis.")
    datum_upisa: datetime = Field(..., description="Datum kada je upis pravomoćno proveden i od kada upisani podaci vrijede.")
    poslovni_broj: str = Field(..., min_length=1, max_length=79, description="Poslovni broj rješenja o upisu.")

    @field_validator("podbroj", mode="before")
    @classmethod
    def validate_podbroj(cls, value: Any) -> str:
        """
        Validacija polja "podbroj" jer zna doći integer pa
        da se pretvori u string da ne dolazi do pucanja
        na bazi.

        Args:
            value (Any): podbroj

        Returns:
            str: Vraća string neovisno o dolaznom podatku.
        """
        if isinstance(value, int):
            return str(value)

        return value

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste UpisDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista UpisDTO objekata za konverziju.

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
