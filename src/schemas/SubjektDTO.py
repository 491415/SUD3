import math
from datetime import date
from typing import TypeVar, Optional, Dict, List, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

T = TypeVar("T", bound="SubjektDTO")

class SubjektDTO(BaseModel):
    """
    Model za tablicu osnovnih podataka o subjektima.

    JSON - subjekti (naziv tablice u .json konfiguracijskom fileu)
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
    status: int = Field(..., ge=0, le=9, description="Status subjekta (1 - Aktivan, 0 - Neaktivni/Brisan).")
    sud_id_nadlezan: int = Field(..., ge=1, description="ID nadležnog suda.")
    sud_id_sluzba: int = Field(..., ge=1, description="ID stalne službe ili nadležnog suda ako nema stalne službe.")
    postupak: int = Field(..., ge=0, le=9, description="Postupak u kojem se subjekt nalazi (stečaj, likvidacija, ...).")
    oib: Optional[int] = Field(None, ge=0, le=99999999999, description="Osobni identifikacijski broj subjekta.")
    mb: Optional[int] = Field(None, ge=0, le=99999999, description="Matični broj poslovnog subjekta (dodjeljuje DZS).")
    ino_podruznica: int = Field(..., ge=0, le=9, description="Oznaka da li je subjekt podružnica inozemnog osnivača (denormalizirano iz vrste pravnog oblika).")
    stecajna_masa: int = Field(..., ge=0, le=9, description="Oznaka da je je subjekt stečajna masa (denormalizirano iz vrste pravnog oblika).")
    likvidacijska_masa: int = Field(..., ge=0, le=9, description="Oznaka da li je subjekt likvidacijska masa (denormalizirano iz vrste pravnog oblika).")
    mbs_brisanog_subjekta: Optional[int] = Field(None, ge=1, le=999999999, description="Brisani subjekt iza kojeg ovaj subjekt nastaje (samo za stečaju i likvidacijsku masu).")
    glavna_djelatnost: Optional[int] = Field(None, ge=0, le=99999, description="Šifra glavne djelatnosti prema NKD šifrarniku.")
    glavna_podruznica_rbr: Optional[int] = Field(None, ge=1, le=9999, description="Redni broj trenutno glavne podružnice inozemnog osnivača.")
    datum_osnivanja: Optional[date] = Field(None, description="Datum osnivanja subjekta.")
    datum_brisanja: Optional[date] = Field(None, description="Datum brisanja subjekta.")
    sud_id_brisanja: Optional[int] = Field(None, ge=1, description="ID suda koji je brisao subjekt iz registra.")
    tvrtka_kod_brisanja: Optional[str] = Field(None, max_length=1024, description="Puna tvrtka/naziv subjekta upisa u trenutku brisanja (denormalizirano iz tvrtke).")
    poslovni_broj_brisanja: Optional[str] = Field(None, max_length=17, description="Poslovni broj rješenja kojim je subjekt brisan iz registra.")
    razlog_neaktivnosti: Optional[int] = Field(None, ge=0, le=99, description="Razlog neaktivnosti (određen dedukcijom iz raspoloživih podataka).")

    @field_validator("mbs_brisanog_subjekta", mode='before')
    @classmethod
    def validate_mbs_brisanog_subjekta(cls, value: Optional[int]) -> Optional[int]:
        """
        Validacija polja 'mbs_brisanog_subjekta' s obzirom da
        dolaze razni podaci, svi koju su manji od '1' dobivaju vrijednost
        '0'.

        Args:
            value (Optional[int]): mbs_brisanog_subjekta

        Returns:
            int: Ako je broj manji od 1, vraća None.
        """
        if value is None or math.isnan(value) or value < 1:
            return None

        return value

    def to_dict(self) -> Dict:
        return self.model_dump()

    @classmethod
    def as_dict(cls, dto_list: List[T]) -> List[Dict[str, Any]]:
        """
        Konverzija liste SubjektDTO u listu dictonarya koristeći Pydantic model_dump
        za serijalizaciju svakog objekta.

        Args:
            dto_list (List[T]): Lista SubjektDTO objekata za konverziju.

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
