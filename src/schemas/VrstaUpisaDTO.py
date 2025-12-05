from pydantic import Field

from src.schemas.base_schemas.ReferencaPodatkaDTO import ReferencaPodatkaDTO


class VrstaUpisaDTO(ReferencaPodatkaDTO):
    """
    Model za tablicu vrsta upisa.

    JSON - vrste_upisa (naziv tablice u .json konfiguracijskom fileu)
    """
    # Override polja iz parent klase
    # ge=0 stavljeno jer ima podatak sa ID-em '0'
    sifra: int = Field(..., ge=0, le=999999, description="Šifra države, jezika, grupe, itd...")

    naziv: str = Field(..., min_length=1, max_length=128, description="Naziv vrste upisa.")
    grupa_vrste_upisa_id: int = Field(..., ge=1, description="ID grupe vrste upisa.")

