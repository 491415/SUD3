import logging
import random
import time
from datetime import datetime
from pathlib import Path

from environs import env

from src.database.db_connection import OracleDBConn
from src.models.ScriptContext import ScriptContext
from src.models.SudregTables import get_all_models
from src.models.TableManager import TableManager
from src.utils.data.data_utils import process_table, table_in_no_counts
from src.utils.db.db_utils import cleanup_filled_tables, switch_table_suffixes, \
    create_synonyms, truncate_old_data, get_inactive_table_name
from src.utils.error_handler import ScriptExecutionWrapper
from src.utils.web.web_utils import get_snapshot_id, get_table_counts


def download_data(shared_data: ScriptContext) -> None:
    """
    Preuzima sve tablice iz Sudskog registra sa error handlingom.

    1. Dohvati koji sufiks je trenutno aktivan (_A ili _B)
    2. Puni NEAKTIVNI sufiks s novim podacima
    3a. Ako je sve OK -> prebaci neaktivni u aktivan
    3b. Ako je greška -> zaustavi proces i izbriši sve tablice koje su popunjene
    4. Obriši stare podatke iz novog neaktivnog sufiksa

    Args:
        shared_data (ScriptContext): Objekt za dijeljenje podataka s wrapperom.
    """
    db = OracleDBConn(run_file=__file__)
    db.connect()
    shared_data.db = db

    # Inicijalizacija TableManager-a za zapisivanje u A-B tablice
    table_manager = TableManager(db)

    # Dohvat svih tablica
    lista_tablica = get_all_models()
    shared_data.total_tables = len(lista_tablica)

    # Pratimo status svakog downloada
    download_results = {}  # {table_name: (success, error_msg, rows)}

    # Pratimo koje su neaktivne tablice uspješno popunjene (za cleanup u slučaju greške)
    successfully_filled_targets = []  # [(table_name, target_table_name), ...]

    # Dohvaća se najsvježiji snapshot_id
    snapshot_id = get_snapshot_id()

    # Dohvaća se ukupan broj redaka za svaku tablicu i sprema duljinu liste u shared context
    table_counts = get_table_counts()
    shared_data.counts_total = len(table_counts)

    logging.info(f"Početak preuzimanja {len(lista_tablica)} tablica iz SUDREG-a...")
    logging.info("-" * 100)

    for table_name, dto_class in lista_tablica.items():
        logging.info(f"Procesiram tablicu: {table_name}")
        logging.info("-" * 100)

        table_in_no_counts(table_name, table_counts)

        # Dohvat neaktivnog sufixa, trenutno aktivnih tablica i target tablice za punjenje
        inactive_suffix = table_manager.get_inactive_suffix(table_name)
        target_table_name = get_inactive_table_name(table_name, inactive_suffix)
        active_table_name = table_manager.get_active_table_name(table_name, inactive_suffix)

        logging.info(f"Trenutno aktivna tablica: {active_table_name}")
        logging.info("-" * 100)

        # Preuzimanje tablice iz sudskog registra
        successful_download, error_msg, inserted_rows = process_table(db, table_name, dto_class, snapshot_id, target_table_name)

        # Spremanje statistke o preuzimanju pojedine tablice
        download_results[table_name] = (successful_download, error_msg, inserted_rows)

        if successful_download:
            logging.info("-" * 100)
            logging.info(f"✓ Uspješno preuzeto: {inserted_rows} redaka u {target_table_name}")
            logging.info("-" * 100)
            shared_data.successful_tables += 1
            shared_data.total_rows += inserted_rows
            if table_name not in env.list("NO_COUNTS") and inserted_rows == table_counts[table_name]:
                shared_data.counts_tables += 1

            # Bilježimo uspješno popunjenu tablicu za potencijalni cleanup
            successfully_filled_targets.append((table_name, target_table_name))
        else:
            logging.error("-" * 100)
            logging.error(f"✗ Neuspješno preuzimanje za {table_name}")
            logging.error(f"✗ Greška: {error_msg}")
            logging.error("-" * 100)
            shared_data.table_errors.append({
                "table_name": table_name,
                "error_message": error_msg,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            cleanup_filled_tables(db, successfully_filled_targets)

            raise RuntimeError(
                f"Preuzimanje tablice '{table_name}' nije uspjelo: {error_msg}\n"
                f"Proces zaustavljen. Obrisani podaci iz {len(successfully_filled_targets)} prethodno popunjenih tablica."
            )

        # Timeout između tablica da se API ne preoptereti
        if table_name != list(lista_tablica.keys())[-1]:  # Ako nije zadnja tablica
            timeout = random.randint(1, 3)
            logging.info(f"Čekam {timeout} sekunde prije preuzimanja sljedeće tablice...")
            logging.info("-" * 100)
            time.sleep(timeout)

    switched_tables = switch_table_suffixes(table_manager, download_results, shared_data)
    create_synonyms(db, table_manager, switched_tables)
    truncate_old_data(db, table_manager, switched_tables)

    logging.info("-" * 100)
    logging.info("SUD3 - završni izvještaj")
    logging.info("-" * 100)
    logging.info(f"Ukupno tablica: {shared_data.total_tables}/{len(lista_tablica)}")
    logging.info(f"Uspješno: {shared_data.successful_tables}/{len(lista_tablica)}")
    logging.info(f"Ukupno zapisa: {shared_data.total_rows:,}")
    logging.info(f"Točan broj redaka po tablici (Counts): {shared_data.counts_tables}/{shared_data.counts_total}")
    logging.info(f"Vrijeme završetka: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    logging.info("✅ Sve tablice uspješno prebačene na nove verzije!")
    logging.info("✅ Stari podaci obrisani!")
    logging.info("-" * 100)


if __name__ == "__main__":
    """
    Ulazna točka glavne skripte gdje wrapper hvata greške
    koje se dogode prilikom izvršavanja i automatski šalje
    obavijest na mail.
    """
    # Kreiranje klase koja služi za dijeljenje informacija između glavne skripte i
    # wrappera za error handling
    context = ScriptContext()

    # Kreiranje wrappera za error handling
    wrapper = ScriptExecutionWrapper(script_name=Path(__file__).name)

    # Izvršavanje glavne skripte sa error handlingom gdje wrapper upravlja sa
    # konekcijom na bazu, čišćenjem iste i slanjem mailova prilikom završetka/greške
    success = wrapper.execute(
        main_function=lambda: download_data(context),
        context=context
    )

    exit(0 if success else 1)
