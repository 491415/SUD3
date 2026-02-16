import logging
import traceback
from datetime import datetime
from typing import Callable, Optional

from environs import env

from src.models.ScriptContext import ScriptContext
from src.utils.send_mail import send_mail


class ScriptExecutionWrapper:
    """
    Wrapper klasa za run skripte s automatskim obavještavanjem
    ako se dogodi greška.

    Ova klasa djeluje kao sigurnosna mreža oko skripte.
    Ako se dogodi greška tijekom izvršavanja:
        1. Zapisuje detalje o greški
        2. Šalje obavijest e-poštom s greškom i log fileom
        3. Osigurava pravilno zatvaranje konekcije s bazom podataka
    """

    def __init__(
        self,
        script_name: str,
    ) -> None:
        """
        Inicijalizacija ScriptExecutionWrapper klase sa podacima o skripti,
        admin mailu, uspješnosti izvršenja skripte i detaljima o greški.

        Args:
            script_name (str): Naziv skripte koja se pokreće.
        """
        self.script_name = script_name
        self.admin_mail = env("ADMIN_MAIL_ADDRESS")
        self.receivers = env.list("RECEIVERS_MAIL_ADDRESS")
        self.execution_successful = True
        self.error_details = None

    def execute(self, main_function: Callable, context: ScriptContext) -> bool:
        """
        Pokretanje glavne metode unutar skripte sa error handlingom.

        Args:
            main_function (Callable): Metoda u kojoj se nalazi glavni dio koda.
            context (ScriptContext): Kontekst sa dijeljenim podacima između glavne skripte
                                     i error handlera.

        Returns:
            bool: True ako izvršavanje uspije, False ako se dogodi greška.
        """
        log_dir = ""
        log_name = ""
        db_connection = None
        error_occurred = None

        try:
            # Pokretanje glavnog dijela koda za učitavanje podataka sa diska.
            main_function()
            self.execution_successful = True

        except KeyboardInterrupt:
            # Ne šalje se mail ako korisnik prekine izvršavanje skripte.
            logging.warning(
                f"Skripta {self.script_name} prekinuta od strane korisnika!"
            )
            self.execution_successful = False
            self.error_details = "Skripta je ručno prekinuta! (Ctrl+C)"
            error_occurred = "interrupted"

        except Exception as e:
            # Ovdje se hvataju ostale greške.
            self.execution_successful = False
            self.error_details = self._format_error_details(e)
            error_occurred = e

            # Zapisivanje u log greške sa stack traceom
            logging.error(f"GREŠKA u skripti {self.script_name}:")
            logging.error(self.error_details)
            logging.error("-" * 100)

        finally:
            # Dohvat informacija o konekciji na bazu iz contexta ako postoji
            if context and hasattr(context, "db") and context.db:
                db_connection = context.db

            if db_connection:
                if (
                    hasattr(db_connection, "is_connected")
                    and db_connection.is_connected
                ):
                    try:
                        db_connection.close()
                    except Exception as cleanup_error:
                        logging.error(
                            f"Greška pri zatvaranju konekcije na bazu: {cleanup_error}"
                        )

                if hasattr(db_connection, "get_script_execution_time"):
                    try:
                        db_connection.get_script_execution_time()
                    except Exception as time_error:
                        logging.error(
                            f"Nije uspjelo logiranje vremena izvršavanja: {time_error}"
                        )

            if db_connection and hasattr(db_connection, "get_log_file_info"):
                try:
                    log_dir, log_name = db_connection.get_log_file_info()
                except Exception as log_error:
                    logging.error(
                        f"Nije uspjelo dohvaćanje log filea za mail: {log_error}"
                    )

            if error_occurred and error_occurred != "interrupted":
                self._send_error_notification(
                    log_dir=log_dir,
                    log_name=log_name,
                )
            elif self.execution_successful:
                self._send_success_notification(
                    context=context,
                    log_dir=log_dir,
                    log_name=log_name,
                )

        return self.execution_successful

    @staticmethod
    def _format_error_details(exception: Exception) -> str:
        """
        Formatiranje detalja o greški/exceptionu za mail i log.
        Osim error poruke, hvata i full stack trace za što
        precizinije prikazivanje gdje se greška dogodila.
        """
        error_type = type(exception).__name__
        error_message = str(exception)
        stack_trace = traceback.format_exc()

        return f"""
            Vrsta greške: {error_type}
            Error poruka: {error_message}

            Full Stack Trace:
            {stack_trace}
            """

    def _send_error_notification(
        self, log_dir: Optional[str], log_name: Optional[str]
    ) -> None:
        """
        Slanje mail obavijesti o prekidu skripte.
        Kreira se detaljan mail za što brži pronalazak razloga
        zbog kojega je došlo do prekida skripte.

        Args:
            log_dir (Optional[str]): Direktorij u kojemu se nalaze log fileovi.
            log_name (Optional[str]): Naziv log filea.
        """
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        subject = f"❌ {env('APP_NAME')} Skripta Greška: {self.script_name}"

        body = f"""
            {env('APP_NAME')} skripta greška prilikom izvršavanja!
            ========================================

            Skripta: {self.script_name}
            Vrijeme prekida: {timestamp}

            Detalji o greški:
            {self.error_details}

            Slijedeći koraci:
            1. Pogledajte log file u privitku za detalje

            ========================================
            Ovo je automatski generirana poruka iz {env('APP_NAME')} aplikacije.
            """

        try:
            send_mail(
                v_subject=subject,
                v_body=body,
                to_address=self.admin_mail,
                log_dir=log_dir or "",
                log_name=log_name or "",
                send_log_file=True,
            )

            logging.info(f"Poslana obavijest o greški na mail adresu {self.admin_mail}")

        except Exception as email_error:
            logging.error(
                f"Greška prilikom slanja obavijesti o greški na mail: {email_error}"
            )
            import traceback

            logging.error(traceback.format_exc())

    def _send_success_notification(self, context: ScriptContext, log_dir: Optional[str], log_name: Optional[str]) -> None:
        """
        Šalje obavijesti o uspješnom izvršavanju skripte.
        Uključuje statistiku o tablicama i greškama (ako ih ima).

        Args:
            context (ScriptContext): Podaci iz pokrenute skripte za mail.
            log_dir (Optional[str]): Direktorij u kojemu se nalaze log fileovi.
            log_name (Optional[str]): Naziv log filea.
        """
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Provjeri ima li grešaka na pojedinim tablicama
        if hasattr(context, "table_errors") and context.table_errors:
            subject = f"⚠️ {env('APP_NAME')} Izvršena sa Greškama"

            error_list = "\n".join([
                f"  - {error['table_name']}: {error['error_message']}"
                for error in context.table_errors
            ])

            body = f"""
            {env('APP_NAME')} skripta izvršena s greškama na pojedinim tablicama!
            ====================================================================

            Skripta: {self.script_name}
            Vrijeme završetka: {timestamp}

            Statistika:
            - Ukupno tablica: {context.total_tables}
            - Uspješne tablice: {context.successful_tables}
            - Neuspješne tablice: {len(context.table_errors)}
            - Ukupno zapisanih redova: {context.total_rows:,}

            Greške po tablicama:
            {error_list}

            ====================================================================
            Ovo je automatski generirana poruka iz {env('APP_NAME')} aplikacije.
            """
        else:
            subject = f"✅ {env('APP_NAME')} Skripta Uspješno Izvršena"

            body = f"""
                {env('APP_NAME')} skripta uspješno izvršena!
                ===========================================

                Skripta: {self.script_name}
                Vrijeme završetka: {timestamp}

                Statistika:
                - Ukupno tablica: {context.total_tables}
                - Sve tablice uspješno preuzete i zapisane u bazu podataka!
                - Ukupno zapisanih redova: {context.total_rows:,}

                ===========================================
                Ovo je automatski generirana poruka iz {env('APP_NAME')} aplikacije.
                """

        try:
            send_mail(
                v_subject=subject,
                v_body=body,
                to_address=self.receivers,
                log_dir=log_dir or "",
                log_name=log_name or "",
                send_log_file=True,
            )
        except Exception as email_error:
            logging.warning(
                f"Nije uspjelo slanje obavijesti o uspješnom izvršavanju skripte: {email_error}"
            )
