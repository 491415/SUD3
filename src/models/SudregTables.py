from pydantic import BaseModel

from src.schemas.VrstaKapitalaDTO import VrstaKapitalaDTO
from src.schemas.VrstaOblikaVlasnistvaDTO import VrstaOblikaVlasnistvaDTO
from src.schemas.VrstaOvlastiDTO import VrstaOvlastiDTO
from src.schemas.EmailAdresaPodruzniceDTO import EmailAdresaPodruzniceDTO
from src.schemas.FunkcijaClanaSubjektaDTO import FunkcijaClanaSubjektaDTO
from src.schemas.FunkcijaOsobeDTO import FunkcijaOsobeDTO
from src.schemas.GFIDTO import GFIDTO
from src.schemas.GrupaFunkcijaDTO import GrupaFunkcijaDTO
from src.schemas.GrupaVrstaUpisaDTO import GrupaVrstaUpisaDTO
from src.schemas.JezikDTO import JezikDTO
from src.schemas.NacionalnaKlasaDjelDTO import NacionalnaKlasaDjelDTO
from src.schemas.NazivPodruzniceDTO import NazivPodruzniceDTO
from src.schemas.ObjavaPriopcenjaDTO import ObjavaPriopcenjaDTO
from src.schemas.OsobaDTO import OsobaDTO
from src.schemas.OsobaOvlastDTO import OsobaOvlastDTO
from src.schemas.OstaloPodaciDTO import OstaloPodaciDTO
from src.schemas.OstaloTekstDTO import OstaloTekstDTO
from src.schemas.PartnerStatusniPostupakDTO import PartnerStatusniPostupakDTO
from src.schemas.PodruznicaDTO import PodruznicaDTO
from src.schemas.PravniSljednikDTO import PravniSljednikDTO
from src.schemas.PromjeneDTO import PromjeneDTO
from src.schemas.SjedistePodruzniceDTO import SjedistePodruzniceDTO
from src.schemas.SkraceniNazivPodruzniceDTO import SkraceniNazivPodruzniceDTO
from src.schemas.SkupnaOvlastDTO import SkupnaOvlastDTO
from src.schemas.SnapshotsDTO import SnapshotsDTO
from src.schemas.StatusDTO import StatusDTO
from src.schemas.StatusniPostupakDTO import StatusniPostupakDTO
from src.schemas.SubjektDTO import SubjektDTO
from src.schemas.SudDTO import SudDTO
from src.schemas.UpisDTO import UpisDTO
from src.schemas.UpisVrstaUpisaDTO import UpisVrstaUpisaDTO
from src.schemas.ValutaDTO import ValutaDTO
from src.schemas.VrstaClanaSubjektaDTO import VrstaClanaSubjektaDTO
from src.schemas.VrstaFunkcijeDTO import VrstaFunkcijeDTO
from src.schemas.VrstaGFIDokumentaDTO import VrstaGFIDokumentaDTO
from src.schemas.VrstaOsobeDTO import VrstaOsobeDTO
from src.schemas.VrstaPorijeklaKapitalaDTO import VrstaPorijeklaKapitalaDTO
from src.schemas.VrstaPostupkaDTO import VrstaPostupkaDTO
from src.schemas.VrstaPravnogOblikaDTO import VrstaPravnogOblikaDTO
from src.schemas.VrstaPrilogaDTO import VrstaPrilogaDTO
from src.schemas.VrstaRazlogaNastajanjaDTO import VrstaRazlogaNastavljanjaDTO
from src.schemas.VrstaRazlogaPrestankaDTO import VrstaRazlogaPrestankaDTO
from src.schemas.VrstaStPostupkaDTO import VrstaStPostupkaDTO
from src.schemas.VrstaZabiljezbeDTO import VrstaZabiljezbeDTO
from src.schemas.DrzavaDTO import DrzavaDTO
from src.schemas.BrisPravniOblikDTO import BrisPravniOblikDTO
from src.schemas.BrisRegistarDTO import BrisRegistarDTO
from src.schemas.ClanSubjektaDTO import ClanSubjektaDTO
from src.schemas.ClanSubjektaOvlastDTO import ClanSubjektaOvlastDTO
from src.schemas.ClanSubjektaUdioDTO import ClanSubjektaUdioDTO
from src.schemas.ClanSubjektaUlogDTO import ClanSubjektaUlogDTO
from src.schemas.CountsDTO import CountsDTO
from src.schemas.DjelatnostPodruzniceDTO import DjelatnostPodruzniceDTO
from src.schemas.DokumentDTO import DokumentDTO
from src.schemas.EmailAdreseDTO import EmailAdreseDTO
from src.schemas.EvidencijskaDjelatnostDTO import EvidencijskaDjelatnostDTO
from src.schemas.InozemniRegistarDTO import InozemniRegistarDTO
from src.schemas.PostupakDTO import PostupakDTO
from src.schemas.PravniOblikDTO import PravniOblikDTO
from src.schemas.PredmetPoslovanjaDTO import PredmetPoslovanjaDTO
from src.schemas.PretezitaDjelatnostDTO import PretezitaDjelatnostDTO
from src.schemas.PrijevodSkracenaTvrtkaDTO import PrijevodSkracenaTvrtkaDTO
from src.schemas.PrijevodTvrtkaDTO import PrijevodTvrtkaDTO
from src.schemas.RazlogNeaktivnostiDTO import RazlogNeaktivnostiDTO
from src.schemas.SjedisteDTO import SjedisteDTO
from src.schemas.SkracenaTvrtkaDTO import SkracenaTvrtkaDTO
from src.schemas.TemeljniKapitalDTO import TemeljniKapitalDTO
from src.schemas.TvrtkaDTO import TvrtkaDTO
from src.schemas.VrstaUpisaDTO import VrstaUpisaDTO
from src.schemas.ZabijezbaDTO import ZabiljezbaDTO


SUDREG_TABLE_MAPPING = {
    "bris_pravni_oblici": BrisPravniOblikDTO,
    "bris_registri": BrisRegistarDTO,
    "clanovi_subjekata": ClanSubjektaDTO,
    "counts": CountsDTO,
    "djelatnosti_podruznica": DjelatnostPodruzniceDTO,
    "dokumenti": DokumentDTO,
    "drzave": DrzavaDTO,
    "email_adrese": EmailAdreseDTO,
    "email_adrese_podruznica": EmailAdresaPodruzniceDTO,
    "evidencijske_djelatnosti": EvidencijskaDjelatnostDTO,
    "funkcije_clanova_subjekata": FunkcijaClanaSubjektaDTO,
    "funkcije_osoba": FunkcijaOsobeDTO,
    "gfi": GFIDTO,
    "grupe_vrsta_funkcija": GrupaFunkcijaDTO,
    "grupe_vrsta_upisa": GrupaVrstaUpisaDTO,
    "inozemni_registri": InozemniRegistarDTO,
    "jezici": JezikDTO,
    "nacionalna_klasifikacija_djelatnosti": NacionalnaKlasaDjelDTO,
    "nazivi_podruznica": NazivPodruzniceDTO,
    "objave_priopcenja": ObjavaPriopcenjaDTO,
    "osobe": OsobaDTO,
    "ostali_podaci": OstaloPodaciDTO,
    "ostali_tekstovi": OstaloTekstDTO,
    "ovlasti_clanova_subjekata": ClanSubjektaOvlastDTO,
    "ovlasti_osoba": OsobaOvlastDTO,
    "partneri_statusnih_postupaka": PartnerStatusniPostupakDTO,
    "podruznice": PodruznicaDTO,
    "postupci": PostupakDTO,
    "pravni_oblici": PravniOblikDTO,
    "pravni_sljednici": PravniSljednikDTO,
    "predmeti_poslovanja": PredmetPoslovanjaDTO,
    "pretezite_djelatnosti": PretezitaDjelatnostDTO,
    "prijevodi_skracenih_tvrtki": PrijevodSkracenaTvrtkaDTO,
    "prijevodi_tvrtki": PrijevodTvrtkaDTO,
    "promjene": PromjeneDTO,
    "razlozi_neaktivnosti": RazlogNeaktivnostiDTO,
    "sjedista": SjedisteDTO,
    "sjedista_podruznica": SjedistePodruzniceDTO,
    "skracene_tvrtke": SkracenaTvrtkaDTO,
    "skraceni_nazivi_podruznica": SkraceniNazivPodruzniceDTO,
    "skupne_ovlasti": SkupnaOvlastDTO,
    "snapshots": SnapshotsDTO,
    "statusi": StatusDTO,
    "statusni_postupci": StatusniPostupakDTO,
    "subjekti": SubjektDTO,
    "sudovi": SudDTO,
    "temeljni_kapitali": TemeljniKapitalDTO,
    "tvrtke": TvrtkaDTO,
    "udjeli_clanova_subjekata": ClanSubjektaUdioDTO,
    "ulozi_clanova_subjekata": ClanSubjektaUlogDTO,
    "upisi": UpisDTO,
    "upisi_vrste_upisa": UpisVrstaUpisaDTO,
    "valute": ValutaDTO,
    "vrste_clanova_subjekata": VrstaClanaSubjektaDTO,
    "vrste_funkcija": VrstaFunkcijeDTO,
    "vrste_gfi_dokumenata": VrstaGFIDokumentaDTO,
    "vrste_kapitala": VrstaKapitalaDTO,
    "vrste_oblika_vlasnistva": VrstaOblikaVlasnistvaDTO,
    "vrste_osoba": VrstaOsobeDTO,
    "vrste_ovlasti": VrstaOvlastiDTO,
    "vrste_porijekla_kapitala": VrstaPorijeklaKapitalaDTO,
    "vrste_postupaka": VrstaPostupkaDTO,
    "vrste_pravnih_oblika": VrstaPravnogOblikaDTO,
    "vrste_priloga": VrstaPrilogaDTO,
    "vrste_razloga_nastavljanja": VrstaRazlogaNastavljanjaDTO,
    "vrste_razloga_prestanka": VrstaRazlogaPrestankaDTO,
    "vrste_statusnih_postupaka": VrstaStPostupkaDTO,
    "vrste_upisa": VrstaUpisaDTO,
    "vrste_zabiljezbi": VrstaZabiljezbeDTO,
    "zabiljezbe": ZabiljezbaDTO
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
