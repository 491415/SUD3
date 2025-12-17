import logging

import oracledb
from datetime import datetime
from typing import Literal, Optional, List, Dict

from src.database.db_connection import OracleDBConn
from src.models.SudregTables import get_model_for_table
from src.utils.db.db_utils import dto_name_to_table_name


class TableManager:
    """
    Manager stanja tablica.

    Pomoćna klasa za određivanje trenutno aktivne tablice sa podacima iz
    Sudskog registra.
    """

    def __init__(self, conn: OracleDBConn) -> None:
        """
        Inicijalizacija managera stanja tablica.

        Args:
            conn (OracleDBConn): Konekcija na bazu podataka.
        """
        self.conn = conn

    def get_active_suffix(self, naziv_tablice_json: str) -> str:
        """
        Dohvaća trenutno aktivan sufiks za danu tablicu.

        Args:
            naziv_tablice_json (str): Naziv tablice bez sufixa (iz .json filea).

        Returns:
            'A' ili 'B' - aktivan sufiks
        """
        db_table_name = dto_name_to_table_name(get_model_for_table(naziv_tablice_json).__name__)

        query = """
        SELECT AKTIVNI_SUFFIX 
        FROM SUD3_AKTIVNA_TABLICA 
        WHERE NAZIV_TABLICE = :naziv_tablice
        """

        result = self.conn.execute_query(query, {"naziv_tablice": db_table_name})

        if result and len(result) > 0:
            return result[0][0]
        else:
            # Ako nema zapisa, inicijaliziramo s 'B' tako da prvi run koristi 'A'
            self._initialize_table_state(db_table_name, "B")
            return "B"

    def get_inactive_suffix(self, naziv_tablice_json: str) -> str:
        """
        Dohvaća trenutno neaktivan sufiks za danu tablicu.

        Args:
            naziv_tablice_json (str): Naziv tablice bez sufixa (iz .json konf filea).

        Returns:
            'A' ili 'B' - neaktivan sufiks
        """
        active = self.get_active_suffix(naziv_tablice_json)

        return "B" if active == "A" else "A"

    def _initialize_table_state(self, naziv_tablice: str, active_suffix: str) -> None:
        """
        Inicijalizira stanje za novu tablicu.

        Args:
            naziv_tablice (str): Naziv tablice bez sufixa.
            active_suffix (str): Sufix tablice ('A' ili 'B').
        """

        insert_sql = """
        INSERT INTO SUD3_AKTIVNA_TABLICA 
        (NAZIV_TABLICE, AKTIVNI_SUFFIX, VRIJEME, STATUS)
        VALUES (:naziv_tablice, :aktivni_sufix, :vrijeme, :status)
        """

        self.conn.execute_query(insert_sql, {
            "naziv_tablice": naziv_tablice,
            "aktivni_sufix": active_suffix,
            "vrijeme": datetime.now(),
            "status": "SUCCESS"
        })

        logging.info(f"Inicijalizirano stanje za {naziv_tablice}: aktivan sufiks = {active_suffix}")

    def switch_active_suffix(
            self,
            inactive_suffix: str,
            naziv_tablice: str
    ) -> str:
        """
        Prebacuje trenutno aktivnu tablicu na drugi sufix (samo ako je success=True).

        A->B ili B->A

        Args:
            inactive_suffix (str): Neaktivan sufix.
            naziv_tablice (str): Naziv tablice bez sufixa.

        Returns:
            Novi aktivan sufiks (ili stari ako nije prebačeno)
        """
        current_active = "A" if inactive_suffix == "B" else "B"

        # Prebacivanje na drugu verziju
        new_active = "B" if current_active == "A" else "A"

        update_sql = """
        UPDATE SUD3_AKTIVNA_TABLICA
        SET AKTIVNI_SUFFIX = :novi_suffix,
            VRIJEME = :vrijeme,
            STATUS = :status
        WHERE NAZIV_TABLICE = :naziv_tablice
        """

        self.conn.execute_query(update_sql, {
            "novi_suffix": new_active,
            "vrijeme": datetime.now(),
            "status": "SUCCESS",
            "naziv_tablice": naziv_tablice
        })

        logging.info(f"Prebačeno {naziv_tablice}: {current_active} -> {new_active}")

        return new_active

    def get_active_table_name(self, naziv_tablice_json: str, inactive_sufix: str) -> str:
        """
        Vraća naziv sa sufixom trenutno aktivne tablice.

        Args:
            naziv_tablice_json (str): Naziv tablice bez sufixa (iz .json filea).
            inactive_sufix (str): Neaktivan sufix.

        Returns:
            Puni naziv aktivne tablice sa sufixom.
        """
        active_suffix = "A" if inactive_sufix == "B" else "B"
        db_table_name = dto_name_to_table_name(get_model_for_table(naziv_tablice_json).__name__)

        return f"{db_table_name}_{active_suffix}"

    def get_inactive_table_name(self, naziv_tablice_json: str, inactive_sufix: str) -> str:
        """
        Vraća naziv sa sufixom trenutno neaktivne tablice.

        Args:
            naziv_tablice_json (str): Naziv tablice bez sufixa.
            inactive_sufix (str): Neaktivan sufix.

        Returns:
            Puni naziv neaktivne tablice sa sufixom.
        """
        db_table_name = dto_name_to_table_name(get_model_for_table(naziv_tablice_json).__name__)

        return f"{db_table_name}_{inactive_sufix}"
