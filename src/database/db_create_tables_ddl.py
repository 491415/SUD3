import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

from environs import env

from src.logger.Logger import Logger
from src.models import SudregTables


def _parse_column_description(description: str) -> Tuple[str, str]:
    """
    Parsiranje polja 'description' za informacije o vrsti stupca
    (podatka) u bazi i komentaru za stupac unutar tablice.

    Podatak se nalazi:
    table_name -> properties -> column_name -> description

    Primjer:
    "description": "DB type - NUMBER(9) NOT NULL; comment - Matični broj subjekta u sudskom registru"},

    Args:
        description (str): Opis stupa tablice unutar API konfiguracijskog filea.

    Returns:
        Tuple[str, str]: Vrsta stupca(podatka), komentar za stupac

    Raises:
        ValueError: Ako ne postoji 'comment -' u polju 'description'
                    ili ako je format polja 'description' invalid.
    """
    try:
        # Briše prvih 10 znakova
        # "NUMBER(9) NOT NULL; comment - Matični broj subjekta u sudskom registru"}"
        cleaned_desc = description[10:]

        # Split da se dobije vrsta stupca(podatka)
        # "NUMBER(9) NOT NULL;"
        db_type = cleaned_desc.split(";")[0]

        # Izvlačenje komentara koji počinje nakon "comment -"
        if "comment -" not in cleaned_desc:
            error_msg = f"Nije moguće pronaći 'comment -' u polju 'description': {description}"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Split da se dobije komentar
        # 'Matični broj subjekta u sudskom registru"}'
        comment = cleaned_desc.split("comment -")[1].strip()

        return db_type, comment
    except (IndexError, AttributeError) as e:
        error_msg = f"Invalid format polja 'description': {description}"
        logging.error(error_msg)
        raise ValueError(error_msg) from e


def _generate_table_ddl(table_name: str, table_details: Dict[str, Any]) -> Tuple[str, str]:
    """
    Generiranje DDL-a za pojedinu tablicu.

    Dohvaća se polje 'properties' unutar API konfiguracijskog filea i izvlače se detalji
    o izgledu tablice.

    Args:
        table_name (str): Naziv tablice.
        table_details (str): Detaljna shema tablice iz API konfiguracijskog filea.

    Returns:
        Tuple[str, str]: DDL za tablicu, DDL za kometare.

    Raises:
        ValueError: Ako stupac u tablici nema polje 'properties' i ako je došlo do
                    greške prilikom parsiranja stupca u tablici.
    """
    if "properties" not in table_details:
        error_msg = f"Tablica {table_name} nema polje 'properties'."
        logging.error(error_msg)
        raise ValueError(error_msg)

    table_ddl_lines = [f"CREATE TABLE {table_name} ("]
    comment_ddl_lines = []

    properties = table_details["properties"]

    for i, (col_name, col_prop) in enumerate(properties.items()):
        if "description" not in col_prop:
            error_msg = f"Stupac {col_name} u tablici {table_name} nema polje 'description'."
            logging.error(error_msg)
            raise ValueError(error_msg)

        try:
            col_dbtype, col_comment = _parse_column_description(col_prop["description"])
        except ValueError as e:
            error_msg = f"Greška prilikom parsiranja stupca {col_name} u tablici {table_name}: {e}"
            logging.error(error_msg)
            raise ValueError(error_msg) from e

        # Dodavanje definicije stupca (zadnji stupac nema ',')
        is_last_column = i == len(properties) - 1
        comma = "" if is_last_column else ","
        table_ddl_lines.append(f' {col_name} {col_dbtype}{comma}')

        # Dodavanje sql naredbe za kreiranje komentara na stupcu u listu
        comment_ddl_lines.append(f"COMMENT ON COLUMN {table_name}.{col_name} IS '{col_comment}';")

    table_ddl_lines.append(");\n")

    table_ddl = "\n".join(table_ddl_lines)
    comment_ddl = "\n".join(comment_ddl_lines)

    return table_ddl, comment_ddl


def generate_ddl(api_definition_file: Path) -> str:
    """
    Generiranje Oracle DDL skripte za kreiranje tablica dostupnih preko
    SUDREG API-a. Također, dodaje naredbu za dodavanje komentara na kraju
    upita za svaki stupac unutar pojedine tablice.

    Args:
        api_definition_file (Path): Path do SUDREG API konfiguracijskog filea.

    Returns:
        str: DDL skripta za kreiranje tablica.

    Raises:
        FileNotFoundError: Ako API konfiguracijski file nije pronađen.
        json.JSONDecodeError: Ako je invalid JSON u API konfiguracijskom fileu.
        ValueError: Ako API konfiguracijski file nema potrebnu strukturu (components.schemas)
    """
    if not api_definition_file.exists():
        error_msg = f"API konfiguracijski file nije pronađen: {api_definition_file}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        with open(api_definition_file, "r", encoding="utf-8") as api_def_file:
            data = json.load(api_def_file)
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON u API konfiguracijskom fileu: {e}"
        logging.error(error_msg)
        raise json.JSONDecodeError(error_msg, e.doc, e.pos) from e

    # Validiranje strukture JSON filea
    # Polje 'components' sadrži polje 'schemas' koje u sebi ima podatke o pojedinoj tablici
    if "components" not in data or "schemas" not in data["components"]:
        error_msg = "API konfiguracijski file nema potrebnu strukturu (components.schemas)"
        logging.error(error_msg)
        raise ValueError(error_msg)

    schemas = data["components"]["schemas"]
    table_names = SudregTables.SUDREG_TABLE_MAPPING.keys()

    all_table_ddl = []
    all_comment_ddl = []

    for table_name, table_details in schemas.items():
        if table_name in table_names:
            try:
                table_ddl, comment_ddl = _generate_table_ddl(table_name, table_details)
                all_table_ddl.append(table_ddl)
                all_comment_ddl.append(comment_ddl)
            except ValueError as e:
                logging.warning(f"Warning: Preskačem tablicu {table_name}: {e}")
                continue

    # Spajanje svih DDL naredbi
    combined_ddl = "\n\n".join(all_table_ddl)
    if all_comment_ddl:
        combined_ddl += "\n\n" + "\n".join(all_comment_ddl)

    return combined_ddl


def save_ddl_to_file(ddl_content: str, output_path: Path) -> None:
    """
    Spremanje DDL skripte na disk.

    Args:
        ddl_content (str): DDL naredbe.
        output_path (Path): Path gdje se sprema DDL skripta

    Raises:
        IOError: Ako se DDL skripta ne može zapisati na proslijeđenu lokaciju.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as output_ddl_file:
            output_ddl_file.write(ddl_content)

        logging.info(f"DDL skripta spremljena na lokaciju: {output_path}")

    except IOError as e:
        error_msg = f"Greška prilikom zapisivanja DDL skripte na lokaciju {output_path}: {e}"
        logging.error(error_msg)
        raise IOError(error_msg) from e


if __name__ == "__main__":
    log = Logger(datetime.now().strftime(env("DATE_FORMAT")), __file__)
    save_ddl_to_file(generate_ddl(Path("../json/sudreg_api_v3.json")), env("DDL_FILE"))
