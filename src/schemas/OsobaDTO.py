from typing import Optional

from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class OsobaDTO(PovijestPodatkaDTO):
    """
    Model za tablicu osoba (zastupnika/ovlaštenika) subjekata.

    JSON - osobe (naziv tablice u .json konfiguracijskom fileu)
    """

    osoba_rbr: int = Field(..., ge=0, le=999, description="Redni broj osobe u subjektu.")
    vrsta_osobe: int = Field(..., ge=1, le=9, description="Vrsta osobe (1 - fizička, 2 - pravna).")
    oib: Optional[int] = Field(None, ge=0, le=99999999999, description="Osobni identifikacijski broj osobe.")
    drzava_id_drzavljanstvo: Optional[int] = Field(None, ge=1, description="ID države državljanstva.")
    titula: Optional[str] = Field(None, max_length=64, description="Titula osobe.")
    ime: Optional[str] = Field(None, max_length=128, description="Ime osobe.")
    prezime: Optional[str] = Field(None, max_length=256, description="Prezime osobe.")
    rodjeno_prezime: Optional[str] = Field(None, max_length=64, description="Rođeno prezime osobe.")
    ime_roditelja: Optional[str] = Field(None, max_length=64, description="Ime roditelja osobe.")
    naziv: Optional[str] = Field(None, max_length=385, description="Naziv osobe (za pravne osobe).")
    drzava_id_osobne_isprave: Optional[int] = Field(None, ge=1, description="ID države osobne isprave.")
    drzava_id: Optional[int] = Field(None, ge=1, description="ID države prebivališta/sjedišta.")
    sifra_zupanije: Optional[int] = Field(None, ge=1, le=999, description="Šifra županije prebivališta/sjedišta.")
    naziv_zupanije: Optional[str] = Field(None, max_length=128, description="Naziv županije prebivališta/sjedišta.")
    sifra_opcine: Optional[int] = Field(None, ge=1, le=99999, description="Šifra općine prebivališta/sjedišta.")
    naziv_opcine: Optional[str] = Field(None, max_length=128, description="Naziv općine prebivališta/sjedišta.")
    sifra_naselja: Optional[int] = Field(None, ge=1, le=9999999999, description="Šifra naselja prebivališta/sjedišta.")
    naziv_naselja: Optional[str] = Field(None, max_length=128, description="Naziv naselja prebivališta/sjedišta.")
    jedinica_drzave: Optional[str] = Field(None, max_length=256, description="Teritorijalna jedinica strane države prebivališta/sjedišta (općina, kanton, pokrajina, ...).")
    naselje_van_sifrarnika: Optional[str] = Field(None, max_length=256, description="Naziv stranog naselja prebivališta/sjedišta.")
    sifra_ulice: Optional[int] = Field(None, ge=1, le=9999999999, description="Šifra ulice prebivališta/sjedišta.")
    ulica: Optional[str] = Field(None, max_length=256, description="Ulica prebivališta/sjedišta.")
    kucni_broj: Optional[int] = Field(None, le=999999, description="Kućni broj prebivališta/sjedišta.")
    kucni_podbroj: Optional[str] = Field(None, max_length=10, description="Kućni podbroj prebivališta/sjedišta.")
    drzava_id_ured: Optional[int] = Field(None, ge=1, description="ID države ureda.")
    sifra_zupanije_ured: Optional[int] = Field(None, ge=1, le=999, description="Šifra županije ureda.")
    naziv_zupanije_ured: Optional[str] = Field(None, max_length=128, description="Naziv županije ureda.")
    sifra_opcine_ured: Optional[int] = Field(None, ge=1, le=99999, description="Šifra općine ureda.")
    naziv_opcine_ured: Optional[str] = Field(None, max_length=128, description="Naziv općine ureda.")
    sifra_naselja_ured: Optional[int] = Field(None, ge=1, le=9999999999, description="Šifra naselja ureda.")
    naziv_naselja_ured: Optional[str] = Field(None, max_length=128, description="Naziv naselja ureda.")
    jedinica_drzave_ured: Optional[str] = Field(None, max_length=256, description="Teritorijalna jedinica strane države ureda (općina, kanton, pokrajina, ...).")
    naselje_van_sifrarnika_ured: Optional[str] = Field(None, max_length=256, description="Naziv stranog naselja ureda.")
    sifra_ulice_ured: Optional[int] = Field(None, ge=1, le=9999999999, description="Šifra ulice ureda.")
    ulica_ured: Optional[str] = Field(None, max_length=256, description="Ulica ureda.")
    kucni_broj_ured: Optional[int] = Field(None, ge=1, le=999999, description="Kućni broj ureda.")
    kucni_podbroj_ured: Optional[str] = Field(None, max_length=10, description="Kućni podbroj ureda.")
