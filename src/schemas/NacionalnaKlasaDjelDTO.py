from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class NacionalnaKlasaDjelDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu nacionalne klasifikacije djelatnosti.

    JSON - nacionalna_klasifikacija_djelatnosti (naziv tablice u .json konfiguracijskom fileu)
    """

    # Override polja sifra iz parent klase
    sifra: str = Field(..., min_length=1, max_length=10, description="Šifra države, jezika, grupe, itd...")

    puni_naziv: str = Field(..., min_length=1, max_length=512, description="Puni naziv djelatnosti.")
    verzija: str = Field(..., min_length=1, max_length=64, description="Oznaka verzije NKD šifrarnika (NKD 2002, NKD 2007, ...).")
