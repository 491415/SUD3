from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PravniOblikDTO(PovijestPodatkaDTO):
    """
    Model za tablicu pravnih oblika subjekata.

    JSON - pravni_oblici (naziv tablice u .json konfiguracijskom fileu)
    """

    vrsta_pravnog_oblika_id: int = Field(..., ge=1, description="ID vrste pravnog oblika.")
