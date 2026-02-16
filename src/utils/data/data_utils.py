import logging

import requests
from environs import env
from pydantic import BaseModel

from src.database.db_connection import OracleDBConn
from src.utils.db.db_utils import (
    dto_name_to_table_name,
    generate_insert_query,
    truncate_table,
)
from src.utils.web.web_utils import get_sudreg_api_header


def create_dto_from_data(dto_class: type[BaseModel], data: dict) -> BaseModel:
    """
    Dinamički kreira instancu DTO-a iz dictionary podataka.

    Args:
        dto_class (type[BaseModel]): Pydantic model (npr. PostupakDTO).
        data (dict): Dictionary sa podacima iz API-ja.

    Returns:
        BaseModel: Instanca DTO-a.
    """
    # Pydantic automatski prihvaća dictionary i mapira ga na polja modela.
    return dto_class(**data)


def process_table(conn: OracleDBConn, table_name: str, dto_class: type[BaseModel], snapshot_id: int, target_table=None) -> tuple[bool, str, int]:
    """
    Procesira pojdeinu tablicu i vraća status, eventualni error i broj zapisanih redaka.

    Args:
        conn (OracleDBConn): Konekcija na bazu podataka.
        table_name (str): Tablica koja se procesira.
        dto_class (type[BaseModel]): DTO objekt tablice koja se procesira.
        snapshot_id (int): Najsvježiji snapshot_id.
        target_table (str, optional): Target tablica za punjenje (npr. "SUD_A" ili "SUD_B").
                                      Ako nije specificirana, koristi se bazno ime.

    Returns:
        tuple[bool, str, int]: (success, error_message, inserted_rows)
    """
    db_table_name = dto_name_to_table_name(dto_class.__name__)
    actual_table = target_table if target_table else table_name

    limit = env.int("LIMIT")
    offset = env.int("OFFSET")
    inserted_rows = 0

    url = f"{env('SUDREG_URL')}/{table_name}"

    # Ovdje se dodaje dodatni parametar za određene tablice kako bi se preuzeo stupac
    # "status". Bez dodatnog parametra, ne dohvaćaju se podaci za navedeni stupac.
    if table_name in env.list("HISTORY_TABLICE"):
        url += f"?{env("SUDREG_HISTORY")}"

    # Tablica u koju se zapisuju podaci
    if target_table and target_table != db_table_name:
        logging.info(f"Target tablica: {actual_table}")
        logging.info("-" * 100)

    try:
        while True:
            params = {
                "limit": limit,
                "offset": offset,
                "only_active": "false",
                "expand_relations": "false",
            }
            if snapshot_id is not None:
                params["snapshot_id"] = snapshot_id

            with requests.get(
                    url,
                    headers=get_sudreg_api_header(),
                    params=params,
                    verify=True
            ) as response:

                if response.status_code != 200:
                    error_msg = f"Sudreg API greška {response.status_code} - {response.text}"
                    logging.error(error_msg)
                    raise ValueError(error_msg)

            logging.info(f"Dohvaćam podatke za tablicu {table_name} sa linka: {url}")
            logging.info("-" * 100)

            data = response.json()

            if not data:
                logging.info(f"Paginacija završena. Nema više podataka na offestu {offset}")
                break

            list_dto = [create_dto_from_data(dto_class, line) for line in data]
            params_list = [dto.model_dump(by_alias=True) for dto in list_dto]
            insert_query = generate_insert_query(actual_table, dto_class)

            inserted_rows += conn.execute_many(insert_query, params_list=params_list)

            if len(data) < limit:
                logging.info(f"Zadnji batch je imao {len(data)} podataka (manje od zadanog limita: {limit})")
                break

            offset += limit

        logging.info(f"✓ Tablica {table_name} uspješno procesirana - {inserted_rows} redova")
        return True, "", inserted_rows

    except Exception as e:
        error_msg = f"Greška na offsetu {offset}: {str(e)}"
        logging.error(f"✗ Tablica {table_name} - {error_msg}")

        # Pokušaj truncate tablicu zbog greške
        logging.warning(f"Pokrećem truncate tablice {actual_table} zbog greške...")
        try:
            truncate_table(conn, db_table_name)
            logging.info(f"Truncate tablice {actual_table} uspješan")
        except Exception as truncate_error:
            truncate_msg = f"KRITIČNA GREŠKA: Truncate nije uspio: {truncate_error}"
            logging.error(truncate_msg)
            error_msg += f" | {truncate_msg}"

        return False, error_msg, 0
