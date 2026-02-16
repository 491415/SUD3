from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class ClanoviSubjekataDTO(PovijestPodatkaDTO):
    """
    Model za tablicu članova (osnivača) subjekata.

    JSON - clanovi_subjekata (naziv tablice u .json konfiguracijskom fileu)
    """

    clan_subjekta_rbr: int = Field(..., ge=1, le=9_999, description="Redni broj člana subjekta.")
    vrsta_clana_subjekta_id: int = Field(..., ge=1, le=999_999_999_999, description="ID vrste člana subjekta.")
    oib: Optional[int] = Field(None, ge=0, le=99_999_999_999, description="Osobni identifikacijski broj člana subjekta (za fizičke i pravne osobe).")
    euid: Optional[str] = Field(None, max_length=54, description="EU jedinstveni registarski broj subjekta.")
    drzava_id_drzavljanstvo: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID države državljanstva.")
    titula: Optional[str] = Field(None, max_length=64, description="Titula člana subjekta (za fizičke osobe).")
    ime: Optional[str] = Field(None, max_length=128, description="Ime člana subjekta (za fizičke osobe).")
    prezime: Optional[str] = Field(None, max_length=256, description="Prezime člana subjekta (za fizičke osobe).")
    drzava_id_osobne_isprave: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID države osobne isprave.")
    drzava_id_registra: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID države matičnog registra (za pravne osobe).")
    naziv_registra: Optional[str] = Field(None, max_length=1024,
                                          description="Naziv matičnog registra (za pravne osobe).")
    broj_iz_registra: Optional[str] = Field(None, max_length=256,
                                            description="Broj iz matičnog registra (za pravne osobe).")
    naziv_tijela: Optional[str] = Field(None, max_length=128,
                                        description="Naziv tijela matičnog registra (za pravne osobe).")
    mbs_u_registru: Optional[int] = Field(None, ge=0, le=999_999_999,
                                          description="Matični broj subjekta (u ulozi člana subjekta) u sudskom registru.")
    rul: Optional[int] = Field(None, ge=0, le=999_999,
                               description="Broj registarskog uloška (za domaće pravne osobe iz starog trgovačkog registra).")
    rul1: Optional[int] = Field(None, ge=0, le=9,
                                description="Predbroj registarskog uloška (za domaće pravne osobe iz starog trgovačkog registra).")
    naziv_clana_subjekta: Optional[str] = Field(None, max_length=1024,
                                                description="Naziv člana subjekta (za pravne osobe).")

    # Polja adrese
    drzava_id: Optional[int] = Field(None, ge=1, le=999_999_999_999, description="ID države prebivališta/sjedišta.")
    sifra_zupanije: Optional[int] = Field(None, ge=1, le=999, description="Šifra županije prebivališta/sjedišta.")
    naziv_zupanije: Optional[str] = Field(None, max_length=128, description="Naziv županije prebivališta/sjedišta.")
    sifra_opcine: Optional[int] = Field(None, ge=1, le=99_999, description="Šifra općine prebivališta/sjedišta.")
    naziv_opcine: Optional[str] = Field(None, max_length=128, description="Naziv općine prebivališta/sjedišta.")
    sifra_naselja: Optional[int] = Field(None, ge=1, le=9_999_999_999, description="Šifra naselja prebivališta/sjedišta.")
    naziv_naselja: Optional[str] = Field(None, max_length=128, description="Naziv naselja prebivališta/sjedišta.")
    jedinica_drzave: Optional[str] = Field(None, max_length=256,
                                           description="Teritorijalna jedinica strane države prebivališta/sjedišta (općina, kanton, pokrajina, ...).")
    naselje_van_sifrarnika: Optional[str] = Field(None, max_length=256,
                                                  description="Naziv stranog naselja prebivališta/sjedišta.")
    sifra_ulice: Optional[int] = Field(None, ge=1, le=9_999_999_999, description="Šifra ulice prebivališta/sjedišta.")
    ulica: Optional[str] = Field(None, max_length=256, description="Ulica prebivališta/sjedišta.")
    kucni_broj: Optional[int] = Field(None, le=999_999, description="Kućni broj prebivališta/sjedišta.")
    kucni_podbroj: Optional[str] = Field(None, max_length=10, description="Kućni podbroj prebivališta/sjedišta.")
