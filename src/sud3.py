import logging
import random
import time
from datetime import datetime
from pathlib import Path

from src.database.db_connection import OracleDBConn
from src.models.ScriptContext import ScriptContext
from src.models.SudregTables import get_all_models
from src.models.TableManager import TableManager
from src.utils.data.data_utils import process_table
from src.utils.db.db_utils import truncate_table
from src.utils.error_handler import ScriptExecutionWrapper


def download_data(shared_data: ScriptContext) -> None:
    """
    Preuzima sve tablice iz Sudskog registra sa error handlingom.

    1. Dohvati koji sufiks je trenutno aktivan (_A ili _B)
    2. Puni NEAKTIVNI sufiks s novim podacima
    3. Ako je sve OK -> prebaci neaktivni u aktivan
    4. Obriši stare podatke iz novog neaktivnog sufiksa

    Args:
        shared_data (ScriptContext): Objekt za dijeljenje podataka s wrapperom.
    """
    db = OracleDBConn(run_file=__file__)
    db.connect()
    shared_data.db = db

    # Inicijalizacija TableManager-a za blue-green deployment
    table_manager = TableManager(db)

    # Dohvat svih tablica
    lista_tablica = get_all_models()
    shared_data.total_tables = len(lista_tablica)

    # Pratimo status svakog downloada
    download_results = {}  # {table_name: (success, error_msg, rows)}

    # Spremaju se tablice koje su promijenile sufixe
    switched_tables = []

    logging.info(f"Početak preuzimanja {len(lista_tablica)} tablica iz SUDREG-a...")
    logging.info("-" * 100)

    for table_name, dto_class in lista_tablica.items():
        logging.info(f"Procesiram tablicu: {table_name}")
        logging.info("-" * 100)

        # Dohvat neaktivnog sufixa, trenutno aktivnih tablica i target tablice za punjenje
        inactive_suffix = table_manager.get_inactive_suffix(table_name)
        target_table_name = table_manager.get_inactive_table_name(table_name, inactive_suffix)
        active_table_name = table_manager.get_active_table_name(table_name, inactive_suffix)

        logging.info(f"Trenutno aktivna tablica: {active_table_name}")
        logging.info("-" * 100)

        # Preuzimanje tablice iz sudskog registra
        successful_download, error_msg, inserted_rows = process_table(db, table_name, dto_class, target_table_name)

        # Spremanje statistke o preuzimanju pojedine tablice
        download_results[table_name] = (successful_download, error_msg, inserted_rows)

        if successful_download:
            logging.info("-" * 100)
            logging.info(f"✓ Uspješno preuzeto: {inserted_rows} redaka u {target_table_name}")
            logging.info("-" * 100)
            shared_data.successful_tables += 1
            shared_data.total_rows += inserted_rows
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

        # Timeout između tablica da se API ne preoptereti
        if table_name != list(lista_tablica.keys())[-1]:  # Ako nije zadnja tablica
            timeout = random.randint(1, 3)
            logging.info(f"Čekam {timeout} sekunde prije preuzimanja sljedeće tablice...")
            logging.info("-" * 100)
            time.sleep(timeout)

    logging.info("-" * 100)
    logging.info("FAZA 3: PREBACIVANJE NA NOVE VERZIJE")
    logging.info("-" * 100)

    # Prvo prvojeravamo da li su se tablice uspješno preuzete i zapisane u bazu
    all_successful = all(success for success, _, _ in download_results.values())

    if not all_successful:
        logging.error("-" * 100)
        logging.error("❌ PREBACIVANJE OTKAZANO - NISU SVE TABLICE USPJEŠNO DOWNLODANE!")
        logging.error("-" * 100)
        logging.error("Tablice s greškama:")
        for table_name, (success, error_msg, _) in download_results.items():
            if not success:
                logging.error(f" ✗ {table_name}: {error_msg}")

        logging.warning("⚠ STARE AKTIVNE TABLICE OSTAJU NEPROMIJENJENE")
        logging.warning("⚠ Novi podaci su u neaktivnim tablicama - neće biti korišteni")

        raise

    # Za svaku tablicu zapisuje novi aktivno sufix
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
            # Ovo se ne bi trebalo desiti, ali ako se desi, spremi za mail
            shared_data.table_errors.append({
                "table_name": table_name,
                "error_message": f"Greška pri prebacivanju: {str(e)}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

    logging.info(f"✓ Prebačeno {len(switched_tables)} tablica na nove verzije!")

    logging.info("-" * 100)
    logging.info("FAZA 4: BRISANJE STARIH PODATAKA")
    logging.info("-" * 100)

    for table_name in switched_tables:
        inactive_suffix = table_manager.get_inactive_suffix(table_name)
        inactive_table = table_manager.get_inactive_table_name(table_name, inactive_suffix)
        logging.info(f"Truncate tablice: {inactive_table}")

        truncate_table(db, inactive_table)

    logging.info("-" * 100)
    logging.info("SUD3 - ZAVRŠNI IZVJEŠTAJ")
    logging.info("-" * 100)
    logging.info(f"Ukupno tablica: {shared_data.total_tables}/{len(lista_tablica)}")
    logging.info(f"Uspješno: {shared_data.successful_tables}/{len(lista_tablica)}")
    logging.info(f"Ukupno zapisa: {shared_data.total_rows:,}")
    logging.info(f"Vrijeme završetka: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    logging.info("✅ SVE TABLICE USPJEŠNO PREBAČENE NA NOVE VERZIJE!")
    logging.info("✅ STARI PODACI OBRISANI!")
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
