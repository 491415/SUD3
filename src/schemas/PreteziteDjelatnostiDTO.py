from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PreteziteDjelatnostiDTO(PovijestPodatkaDTO):
    """
    Model za tablicu pretežitih djelatnosti subjekata.

    JSON - pretezite_djelatnosti (naziv tablice u .json konfiguracijskom fileu)
    """

    nacionalna_klasifikacija_djelatnosti_id: int = Field(..., ge=1, le=999_999_999_999, description="ID djelatnosti prema NKD šifrarniku.")
