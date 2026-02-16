from pydantic import BaseModel

from src.schemas.BrisPravniObliciDTO import BrisPravniObliciDTO
from src.schemas.BrisRegistriDTO import BrisRegistriDTO
from src.schemas.ClanoviSubjekataDTO import ClanoviSubjekataDTO
from src.schemas.CountsDTO import CountsDTO
from src.schemas.DjelatnostiPodruznicaDTO import DjelatnostiPodruznicaDTO
from src.schemas.DokumentiDTO import DokumentiDTO
from src.schemas.DrzaveDTO import DrzaveDTO
from src.schemas.EmailAdreseDTO import EmailAdreseDTO
from src.schemas.EmailAdresePodruznicaDTO import EmailAdresePodruznicaDTO
from src.schemas.EvidencijskeDjelatnostiDTO import EvidencijskeDjelatnostiDTO
from src.schemas.FunkcijeClanovaSubjekataDTO import FunkcijeClanovaSubjekataDTO
from src.schemas.FunkcijeOsobaDTO import FunkcijeOsobaDTO
from src.schemas.GFIDTO import GFIDTO
from src.schemas.GrupeVrstaFunkcijaDTO import GrupeVrstaFunkcijaDTO
from src.schemas.GrupeVrstaUpisaDTO import GrupeVrstaUpisaDTO
from src.schemas.InozemniRegistriDTO import InozemniRegistriDTO
from src.schemas.JeziciDTO import JeziciDTO
from src.schemas.NacionalnaKlasifikacijaDjelatnostiDTO import (
    NacionalnaKlasifikacijaDjelatnostiDTO,
)
from src.schemas.NaziviPodruznicaDTO import NaziviPodruznicaDTO
from src.schemas.ObjavePriopcenjaDTO import ObjavePriopcenjaDTO
from src.schemas.OsobeDTO import OsobeDTO
from src.schemas.OstaliPodaciDTO import OstaliPodaciDTO
from src.schemas.OstaliTekstoviDTO import OstaliTekstoviDTO
from src.schemas.OvlastiClanovaSubjekataDTO import OvlastiClanovaSubjekataDTO
from src.schemas.OvlastiOsobaDTO import OvlastiOsobaDTO
from src.schemas.PartneriStatusnihPostupakaDTO import PartneriStatusnihPostupakaDTO
from src.schemas.PodruzniceDTO import PodruzniceDTO
from src.schemas.PostupciDTO import PostupciDTO
from src.schemas.PravniObliciDTO import PravniObliciDTO
from src.schemas.PravniSljedniciDTO import PravniSljedniciDTO
from src.schemas.PredmetiPoslovanjaDTO import PredmetiPoslovanjaDTO
from src.schemas.PreteziteDjelatnostiDTO import PreteziteDjelatnostiDTO
from src.schemas.PrijevodiSkracenihTvrtkiDTO import PrijevodiSkracenihTvrtkiDTO
from src.schemas.PrijevodiTvrtkiDTO import PrijevodiTvrtkiDTO
from src.schemas.PromjeneDTO import PromjeneDTO
from src.schemas.RazloziNeaktivnostiDTO import RazloziNeaktivnostiDTO
from src.schemas.SjedistaDTO import SjedistaDTO
from src.schemas.SjedistaPodruznicaDTO import SjedistaPodruznicaDTO
from src.schemas.SkraceneTvrtkeDTO import SkraceneTvrtkeDTO
from src.schemas.SkraceniNaziviPodruznicaDTO import SkraceniNaziviPodruznicaDTO
from src.schemas.SkupneOvlastiDTO import SkupneOvlastiDTO
from src.schemas.SnapshotsDTO import SnapshotsDTO
from src.schemas.StatusiDTO import StatusiDTO
from src.schemas.StatusniPostupciDTO import StatusniPostupciDTO
from src.schemas.SubjektiDTO import SubjektiDTO
from src.schemas.SudoviDTO import SudoviDTO
from src.schemas.TemeljniKapitaliDTO import TemeljniKapitaliDTO
from src.schemas.TvrtkeDTO import TvrtkeDTO
from src.schemas.UdjeliClanovaSubjekataDTO import UdjeliClanovaSubjekataDTO
from src.schemas.UloziClanovaSubjekataDTO import UloziClanovaSubjekataDTO
from src.schemas.UpisiDTO import UpisiDTO
from src.schemas.UpisiVrsteUpisaDTO import UpisiVrsteUpisaDTO
from src.schemas.ValuteDTO import ValuteDTO
from src.schemas.VrstaRazlogaNastajanjaDTO import VrsteRazlogaNastavljanjaDTO
from src.schemas.VrsteClanovaSubjekataDTO import VrsteClanovaSubjekataDTO
from src.schemas.VrsteFunkcijaDTO import VrsteFunkcijaDTO
from src.schemas.VrsteGFIDokumenataDTO import VrsteGFIDokumenataDTO
from src.schemas.VrsteKapitalaDTO import VrsteKapitalaDTO
from src.schemas.VrsteOblikaVlasnistvaDTO import VrsteOblikaVlasnistvaDTO
from src.schemas.VrsteOsobaDTO import VrsteOsobaDTO
from src.schemas.VrsteOvlastiDTO import VrsteOvlastiDTO
from src.schemas.VrstePorijeklaKapitalaDTO import VrstePorijeklaKapitalaDTO
from src.schemas.VrstePostupakaDTO import VrstePostupakaDTO
from src.schemas.VrstePravnihOblikaDTO import VrstePravnihOblikaDTO
from src.schemas.VrstePrilogaDTO import VrstePrilogaDTO
from src.schemas.VrsteRazlogaPrestankaDTO import VrsteRazlogaPrestankaDTO
from src.schemas.VrsteStatusnihPostupakaDTO import VrsteStatusnihPostupakaDTO
from src.schemas.VrsteUpisaDTO import VrsteUpisaDTO
from src.schemas.VrsteZabiljezbiDTO import VrsteZabiljezbiDTO
from src.schemas.ZabijezbaDTO import ZabiljezbeDTO

SUDREG_TABLE_MAPPING = {
    "bris_pravni_oblici": BrisPravniObliciDTO,
    "bris_registri": BrisRegistriDTO,
    "clanovi_subjekata": ClanoviSubjekataDTO,
    "counts": CountsDTO,
    "djelatnosti_podruznica": DjelatnostiPodruznicaDTO,
    "dokumenti": DokumentiDTO,
    "drzave": DrzaveDTO,
    "email_adrese": EmailAdreseDTO,
    "email_adrese_podruznica": EmailAdresePodruznicaDTO,
    "evidencijske_djelatnosti": EvidencijskeDjelatnostiDTO,
    "funkcije_clanova_subjekata": FunkcijeClanovaSubjekataDTO,
    "funkcije_osoba": FunkcijeOsobaDTO,
    "gfi": GFIDTO,
    "grupe_vrsta_funkcija": GrupeVrstaFunkcijaDTO,
    "grupe_vrsta_upisa": GrupeVrstaUpisaDTO,
    "inozemni_registri": InozemniRegistriDTO,
    "jezici": JeziciDTO,
    "nacionalna_klasifikacija_djelatnosti": NacionalnaKlasifikacijaDjelatnostiDTO,
    "nazivi_podruznica": NaziviPodruznicaDTO,
    "objave_priopcenja": ObjavePriopcenjaDTO,
    "osobe": OsobeDTO,
    "ostali_podaci": OstaliPodaciDTO,
    "ostali_tekstovi": OstaliTekstoviDTO,
    "ovlasti_clanova_subjekata": OvlastiClanovaSubjekataDTO,
    "ovlasti_osoba": OvlastiOsobaDTO,
    "partneri_statusnih_postupaka": PartneriStatusnihPostupakaDTO,
    "podruznice": PodruzniceDTO,
    "postupci": PostupciDTO,
    "pravni_oblici": PravniObliciDTO,
    "pravni_sljednici": PravniSljedniciDTO,
    "predmeti_poslovanja": PredmetiPoslovanjaDTO,
    "pretezite_djelatnosti": PreteziteDjelatnostiDTO,
    "prijevodi_skracenih_tvrtki": PrijevodiSkracenihTvrtkiDTO,
    "prijevodi_tvrtki": PrijevodiTvrtkiDTO,
    "promjene": PromjeneDTO,
    "razlozi_neaktivnosti": RazloziNeaktivnostiDTO,
    "sjedista": SjedistaDTO,
    "sjedista_podruznica": SjedistaPodruznicaDTO,
    "skracene_tvrtke": SkraceneTvrtkeDTO,
    "skraceni_nazivi_podruznica": SkraceniNaziviPodruznicaDTO,
    "skupne_ovlasti": SkupneOvlastiDTO,
    "snapshots": SnapshotsDTO,
    "statusi": StatusiDTO,
    "statusni_postupci": StatusniPostupciDTO,
    "subjekti": SubjektiDTO,
    "sudovi": SudoviDTO,
    "temeljni_kapitali": TemeljniKapitaliDTO,
    "tvrtke": TvrtkeDTO,
    "udjeli_clanova_subjekata": UdjeliClanovaSubjekataDTO,
    "ulozi_clanova_subjekata": UloziClanovaSubjekataDTO,
    "upisi": UpisiDTO,
    "upisi_vrste_upisa": UpisiVrsteUpisaDTO,
    "valute": ValuteDTO,
    "vrste_clanova_subjekata": VrsteClanovaSubjekataDTO,
    "vrste_funkcija": VrsteFunkcijaDTO,
    "vrste_gfi_dokumenata": VrsteGFIDokumenataDTO,
    "vrste_kapitala": VrsteKapitalaDTO,
    "vrste_oblika_vlasnistva": VrsteOblikaVlasnistvaDTO,
    "vrste_osoba": VrsteOsobaDTO,
    "vrste_ovlasti": VrsteOvlastiDTO,
    "vrste_porijekla_kapitala": VrstePorijeklaKapitalaDTO,
    "vrste_postupaka": VrstePostupakaDTO,
    "vrste_pravnih_oblika": VrstePravnihOblikaDTO,
    "vrste_priloga": VrstePrilogaDTO,
    "vrste_razloga_nastavljanja": VrsteRazlogaNastavljanjaDTO,
    "vrste_razloga_prestanka": VrsteRazlogaPrestankaDTO,
    "vrste_statusnih_postupaka": VrsteStatusnihPostupakaDTO,
    "vrste_upisa": VrsteUpisaDTO,
    "vrste_zabiljezbi": VrsteZabiljezbiDTO,
    "zabiljezbe": ZabiljezbeDTO
}


def get_model_for_table(table_name: str) -> type[BaseModel] | None:
    """
    Dohvati Pydantic klasu modela za naziv tablice.

    Args:
        table_name (str): Naziv tablice podataka.

    Returns:
        type[BaseModel] | None: Pydantic klasu modela ili None ako nije pronađeno.
    """
    return SUDREG_TABLE_MAPPING.get(table_name.lower())


def get_all_models() -> dict[str, type[BaseModel]]:
    """
    Dohvat svih Pydantic modela.

    Returns:
        dict[str, type[BaseModel]]: Dictionary sa mapiranim nazivima tablica na klase modela.
    """
    return SUDREG_TABLE_MAPPING.copy()
