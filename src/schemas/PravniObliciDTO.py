from pydantic import Field

from src.schemas.base_schemas.PovijestPodatkaDTO import PovijestPodatkaDTO


class PravniObliciDTO(PovijestPodatkaDTO):
    """
    Model za tablicu pravnih oblika subjekata.

    JSON - pravni_oblici (naziv tablice u .json konfiguracijskom fileu)
    """

    vrsta_pravnog_oblika_id: int = Field(..., ge=1, le=999_999_999_999, description="ID vrste pravnog oblika.")
