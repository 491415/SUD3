from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaOblikaVlasnistvaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta oblika vlasništva.

    JSON - vrste_oblika_vlasnistva (naziv tablice u .json konfiguracijskom fileu)
    """

    tekst: str = Field(..., min_length=1, max_length=60, description="Naziv/opis vrste oblika vlasništva.")
