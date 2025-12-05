from typing import Optional, Dict, List, Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# Osigurava da type hintovi rade kako treba sa nasljeđivanjem klase.
T = TypeVar("T", bound="PovijestPodatkaDTO")

class PovijestPodatkaDTO(BaseModel):
    """
    Base model za podatke koji imaju povijesno praćenje.

    Ova polja se pojavljuju u većini tablica pa je napravljena zasebna klasa
    da se ne ponavljaju u DTO modelima pojedinih tablica.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        strict=False,
        extra="forbid",
        validate_default=True,
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    mbs: int = Field(..., ge=1, le=999999999, description="Matični broj subjekta u sudskom registru. (MBS)")
    status: int = Field(..., ge=0, le=9,
                        description="Status podatka (0, 1, 5, 8, 9)), pogledati upute za razvojne inženjere.")
    prbu_od: int = Field(..., ge=1, description="Pravni redni broj upisa kojim je podatak upisan.")
    prbu_do: Optional[int] = Field(None, ge=1,
                                   description="Pravni redni broj upisa kojim je podatak brisan/prestao vrijediti.")
    upis_id_od: int = Field(..., ge=1, description="ID upisa kojim je podatak upisan.")
    upis_id_do: Optional[int] = Field(None, ge=1, description="ID upisa kojim je podatak brisan/prestao vrijediti.")

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls,dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste PovijestPodatkaDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista PovijestPodatkaDTO objekata za konverziju.

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
