from enum import Enum


class SudregTables(Enum):
    """
    Popis 72 Sudreg API tablice, od kojih se 2 ne preuzimaju.
    """
    TABLES = {
        "included": [
            "bris_pravni_oblici",
            "bris_registri",
            "clanovi_subjekata",
            "counts",
            "djelatnosti_podruznica",
            "dokumenti",
            "drzave",
            "email_adrese",
            "email_adrese_podruznica",
            "evidencijske_djelatnosti",
            "funkcije_clanova_subjekata",
            "funkcije_osoba",
            "gfi",
            "grupe_vrsta_funkcija",
            "grupe_vrsta_upisa",
            "inozemni_registri",
            "jezici",
            "nacionalna_klasifikacija_djelatnosti",
            "nazivi_podruznica",
            "objave_priopcenja",
            "osobe",
            "ostali_podaci",
            "ostali_tekstovi",
            "ovlasti_clanova_subjekata",
            "ovlasti_osoba",
            "partneri_statusnih_postupaka",
            "podruznice",
            "postupci",
            "pravni_oblici",
            "pravni_sljednici",
            "predmeti_poslovanja",
            "pretezite_djelatnosti",
            "prijevodi_skracenih_tvrtki",
            "prijevodi_tvrtki",
            "promjene",
            "razlozi_neaktivnosti",
            "sjedista",
            "sjedista_podruznica",
            "skracene_tvrtke",
            "skraceni_nazivi_podruznica",
            "skupne_ovlasti",
            "snapshots",
            "statusi",
            "statusni_postupci",
            "subjekti",
            "sudovi",
            "temeljni_kapitali",
            "tvrtke",
            "udjeli_clanova_subjekata",
            "ulozi_clanova_subjekata",
            "upisi",
            "upisi_vrste_upisa",
            "valute",
            "vrste_clanova_subjekata",
            "vrste_funkcija",
            "vrste_gfi_dokumenata",
            "vrste_kapitala",
            "vrste_oblika_vlasnistva",
            "vrste_osoba",
            "vrste_ovlasti",
            "vrste_porijekla_kapitala",
            "vrste_postupaka",
            "vrste_pravnih_oblika",
            "vrste_priloga",
            "vrste_razloga_nastavljanja",
            "vrste_razloga_prestanka",
            "vrste_statusnih_postupaka",
            "vrste_upisa",
            "vrste_zabiljezbi",
            "zabiljezbe",
        ],
        "excluded": [
            "detalji_subjekta",
            "subjekti_osobe",
        ]}

    def __init__(self, value) -> None:
        """
        Inicijalizacija Enum klase sa podacima o tablicama koje se
        preuzimaju/ne prezimaju iz Sudskog registra.
        """

        self.included = value["included"]
        self.excluded = value["excluded"]

    def __str__(self) -> str:
        """
        Enum ime kao string.
        """
        return self.name

    def __repr__(self) -> str:
        """
        Detaljan prikaz za debugging.
        """
        return (
            f"Tablice za preuzimanje ({len(self.value['included'])}): {self.value['included']} \n"
            f"Tablice bez preuzimanja ({len(self.value['excluded'])}): {self.value['excluded']}"
        )
