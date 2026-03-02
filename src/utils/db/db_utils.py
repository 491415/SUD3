import logging
import re
from datetime import datetime

from environs import env
from pydantic import BaseModel

from src.database.db_connection import OracleDBConn
from src.models.ScriptContext import ScriptContext
from src.models.SudregTables import get_model_for_table

from typing import TYPE_CHECKING
# Ovo mora ovako jer ako se samo importa dolazi do greške:
#
if TYPE_CHECKING:
    from src.models.TableManager import TableManager


def get_inactive_table_name(naziv_tablice_json: str, inactive_sufix: str) -> str:
    """
    Vraća naziv sa sufixom trenutno neaktivne tablice.

    Args:
        naziv_tablice_json (str): Naziv tablice bez sufixa.
        inactive_sufix (str): Neaktivan sufix.

    Returns:
        str: Puni naziv neaktivne tablice sa sufixom.
    """
    db_table_name = dto_name_to_table_name(get_model_for_table(naziv_tablice_json).__name__)

    return f"{db_table_name}_{inactive_sufix}"


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
        "VrsteGFIDokumenataDTO": "VRSTE_GFI_DOKUMENATA"
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


def create_public_synonym(conn: OracleDBConn, synonym_name: str, table_name: str) -> None:
    """
    Kreiranje public synonyma za tablicu.

    Args:
        conn (OracleDBConn): Konekcija na bazu podataka.
        synonym_name (str): Naziv synonyma za tablicu.
        table_name (str): Naziv tablice.
    """
    query = f"CREATE OR REPLACE PUBLIC SYNONYM {synonym_name} for {table_name}"

    try:
        conn.execute_query(query)
        logging.info(f"Public synonym {synonym_name} za tablicu {table_name} uspješno kreiran.")
    except Exception as e:
        logging.error(f"Došlo je do greške prilikom kreiranja public synonyma za tablicu {table_name}: {e}")
        raise


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


def cleanup_filled_tables(db: OracleDBConn, successfully_filled_targets: list) -> None:
    """
    Briše podatke iz svih uspješno popunjenih neaktivnih tablica.
    Poziva se kada dođe do greške pri preuzimanju neke tablice.

    Args:
        db (OracleDBConn): Konekcija na bazu podataka.
        successfully_filled_targets (list): Lista tuplova (table_name, target_table_name)
                                            koji su uspješno popunjeni prije greške.
    """
    logging.error("-" * 100)
    logging.error("❌ Preuzimanje prekinuto! Čistim podatke iz uspješno popunjenih tablica...")
    logging.error("-" * 100)

    if not successfully_filled_targets:
        logging.info("Nema tablica za čišćenje.")
        return

    for _, filled_target_table in successfully_filled_targets:
        try:
            logging.warning(f"⚠ Truncate tablice: {filled_target_table}")
            truncate_table(db, filled_target_table)
            logging.warning(f"✓ Obrisani podaci iz: {filled_target_table}")
        except Exception as cleanup_err:
            logging.error(f"✗ Greška pri brisanju podataka iz {filled_target_table}: {cleanup_err}")


def switch_table_suffixes(
    table_manager: "TableManager",
    download_results: dict,
    shared_data: ScriptContext
) -> list[str]:
    """
    Za svaku uspješno preuzetu tablicu prebacuje aktivni sufiks s _A na _B ili obrnuto.

    Args:
        table_manager (TableManager): Upravlja A-B sufiksima tablica.
        download_results (dict): Dictionary {table_name: (success, error_msg, rows)}.
        shared_data (ScriptContext): Objekt za dijeljenje podataka - za bilježenje grešaka.

    Returns:
        list[str]: Lista naziva tablica kojima je uspješno promijenjen sufiks.
    """
    logging.info("-" * 100)
    logging.info("Prebacivanje tablica na nove verzije...")
    logging.info("-" * 100)

    switched_tables = []

    for table_name in download_results.keys():
        try:
            inactive_suffix = table_manager.get_inactive_suffix(table_name)
            old_active = table_manager.get_active_table_name(table_name, inactive_suffix)

            new_active_suffix = table_manager.switch_active_suffix(
                inactive_suffix=inactive_suffix,
                naziv_tablice=old_active[:-2]
            )
            new_active_table = f"{old_active[:-2]}_{new_active_suffix}"

            switched_tables.append(table_name)

            logging.info(f"✓ {table_name}: {old_active} -> {new_active_table}")

        except Exception as e:
            logging.error(f"✗ Greška pri prebacivanju {table_name}: {e}")
            shared_data.table_errors.append({
                "table_name": table_name,
                "error_message": f"Greška pri prebacivanju: {str(e)}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

    logging.info(f"✓ Prebačeno {len(switched_tables)} tablica na nove verzije!")

    return switched_tables


def create_synonyms(db: OracleDBConn, table_manager: "TableManager", switched_tables: list) -> None:
    """
    Kreira public synonyme za sve tablice kojima je promijenjen aktivni sufiks.

    Args:
        db (OracleDBConn): Konekcija na bazu podataka.
        table_manager (TableManager): Upravlja A-B sufiksima tablica.
        switched_tables (list): Lista naziva tablica kojima je uspješno promijenjen sufiks.
    """
    logging.info("-" * 100)
    logging.info("Kreiranje public synonyma...")
    logging.info("-" * 100)

    for table_name in switched_tables:
        inactive_suffix = table_manager.get_inactive_suffix(table_name)
        active_table = table_manager.get_active_table_name(table_name, inactive_suffix)
        create_public_synonym(db, active_table[:-2], active_table)

    logging.info(f"✓ Svi synonymi uspješno kreirani ({len(switched_tables)} ukupno)!")


def truncate_old_data(db: OracleDBConn, table_manager: "TableManager", switched_tables: list) -> None:
    """
    Briše stare podatke iz neaktivnih tablica nakon što su nove aktivirane.

    Args:
        db (OracleDBConn): Konekcija na bazu podataka.
        table_manager (TableManager): Upravlja A-B sufiksima tablica.
        switched_tables (list): Lista naziva tablica kojima je uspješno promijenjen sufiks.
    """
    logging.info("-" * 100)
    logging.info("Brisanje starih podataka...")
    logging.info("-" * 100)

    for table_name in switched_tables:
        inactive_suffix = table_manager.get_inactive_suffix(table_name)
        inactive_table = get_inactive_table_name(table_name, inactive_suffix)
        logging.info(f"Truncate tablice: {inactive_table}")
        truncate_table(db, inactive_table)

    logging.info("✅ Stari podaci obrisani!")