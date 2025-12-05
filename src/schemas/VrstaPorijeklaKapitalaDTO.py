from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaPorijeklaKapitalaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta porijekla kapitala.

    JSON - vrste_porijekla_kapitala (naziv tablice u .json konfiguracijskom fileu)
    """

    tekst: str = Field(..., min_length=1, max_length=60, description="Naziv/opis vrste porijekla kapitala.")
