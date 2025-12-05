import logging
import re

from pydantic import BaseModel
from environs import env

from src.database.db_connection import OracleDBConn


def generate_insert_query(table_name: str, dto_class: type[BaseModel]) -> str:
    """
    Automatski generira INSERT query na osnovi DTO modela.

    Args:
        table_name (str): Naziv tablice u bazi.
        dto_class (type[BaseModel]): Pydantic model.

    Returns:
        str: Generirani INSERT query.
    """
    fields_with_aliases = []
    placeholders = []

    # Dohvati polja i njihove aliase
    for field_name, field_info in dto_class.model_fields.items():
        # Koristi serialization_alias ako postoji, inače koristi field_name
        column_name = field_info.serialization_alias or field_name
        fields_with_aliases.append(column_name)
        placeholders.append(f":{column_name}")

    columns = ", ".join(fields_with_aliases)
    params = ", ".join(placeholders)

    query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({params})
        """

    return query.strip()


def dto_name_to_table_name(dto_class_name: str, prefix: str = f"{env('APP_NAME')}_") -> str:
    """
    Konverzija DTO naziva klase u naziv tablice iz baze.

    Primjeri:
        ValutaDTO -> SUD3_VALUTA
        TemeljniKapitalDTO -> SUD3_TEMELJNI_KAPITAL
        ClanSubjektaUlogaDTO -> SUD3_CLAN_SUBJEKTA_ULOGA
        GFIDTO -> SUD3_GFI

    Args:
        dto_class_name (str): Ime DTO klase (npr. "ValutaDTO").
        prefix (str): Prefiks za tablicu u bazi (default: "SUD3_").

    Returns:
        str: Ime tablice u bazi.
    """
    special_cases = {
        "GFIDTO": "GFI",
        "VrstaGFIDokumentaDTO": "VRSTA_GFI_DOKUMENTA"
    }

    # Provjeri da li je special case
    if dto_class_name in special_cases:
        return f"{prefix}{special_cases[dto_class_name]}"

    # Ukloni "DTO" suffix ako postoji
    name = dto_class_name.replace("DTO", "")

    # Konverzija CamelCase u SNAKE_CASE (ClanSubjekta -> CLAN_SUBJEKTA)
    # Dodaj underscore prije svakog velikog slova koje dolazi nakon malog.
    snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', name).upper()

    # Dodaj prefiks
    return f"{prefix}{snake_case}"


def truncate_table(conn: OracleDBConn, table_name: str) -> None:
    """
    Truncate tablicu u slučaju greške.

    Args:
        conn (OracleDBConn): Konekcija na bazu podataka.
        table_name (str): Ime tablice za truncate.
    """
    try:
        truncate_query = f"TRUNCATE TABLE {table_name}"
        conn.execute_query(truncate_query)
        logging.info(f"Truncate tablice {table_name} uspješno izvršen.")
    except Exception as e:
        logging.error(f"Greška prilikom truncate-a tablice {table_name}: {e}")
        raise