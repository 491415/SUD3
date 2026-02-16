from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T", bound="SnapshotsDTO")


class SnapshotsDTO(BaseModel):
    """
    Model za tablicu snimki glavne baze sudskog registra.

    JSON - snapshots (naziv tablice u .json konfiguracijskom fileu)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
    )

    id: int = Field(..., ge=1, le=9_999_999_999, description="ID snapshot-a (snimke podataka) (primarni ključ).")
    timestamp: datetime = Field(..., description="Datum i vrijeme izrade snimke.")
    available_until: datetime = Field(..., description="Minimalni datum i vrijeme do kada će snimka sigurno biti dostupna.")
    staleness: int = Field(..., ge=0, le=999, description="Starost snimke (1 - zadnja, 2 - predzadnja, itd.).")
    description: Optional[str] = Field(None, max_length=250, description="Opis.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste SnapshotsDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista SnapshotsDTO objekata za konverziju.

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
