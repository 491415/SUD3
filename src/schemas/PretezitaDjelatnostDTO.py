from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PretezitaDjelatnostDTO(PovijestPodatkaDTO):
    """
    Model za tablicu pretežitih djelatnosti subjekata.

    JSON - pretezite_djelatnosti (naziv tablice u .json konfiguracijskom fileu)
    """

    nacionalna_klasifikacija_djelatnosti_id: int = Field(..., ge=1, description="ID djelatnosti prema NKD šifrarniku.")
