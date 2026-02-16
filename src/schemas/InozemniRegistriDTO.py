from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class InozemniRegistriDTO(PovijestPodatkaDTO):
    """
    Model za tablicu podataka o inozemnim registrima subjekata (za inozemne podružnice).

    JSON - inozemni_registri (naziv tablice u .json konfiguracijskom fileu)
    """

    drzava_id: int = Field(..., ge=1, le=999_999_999_999, description="ID države.")
    naziv_registra: Optional[str] = Field(None, max_length=128, description="Naziv matičnog registra subjekta.")
    registarsko_tijelo: Optional[str] = Field(None, max_length=128, description="Naziv tijela koje vodi matični registar subjekta.")
    broj_iz_registra: Optional[str] = Field(None, max_length=128, description="Broj subjekta u matičnom registru.")
    pravni_oblik: Optional[str] = Field(None, max_length=200, description="Slobodni unos pravnog oblika za inozemne osnivače izvan EU.")
    bris_registar_identifikator: Optional[str] = Field(None, max_length=15, description="Šifra BRIS registra.")
    euid: Optional[str] = Field(None, max_length=54, description="EU jedinstveni registarski broj subjekta - EU unique identifier.", alias="eu_id")
    bris_pravni_oblik_kod: Optional[str] = Field(None, max_length=9, description="Šifra BRIS pravnog oblika.")
