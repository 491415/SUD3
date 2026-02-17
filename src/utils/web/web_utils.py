import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict

import requests
from environs import env
from requests import Response

from src.utils.send_mail import send_warning_notification

# Varijabla na razini modula za 0auth2 token
_sudreg_access_token = {}
# Flag da se API definicija provjeri samo jednom po pokretanju
_api_definition_checked = False


def _check_api_availability(response: Response) -> bool:
    """
    Provjera da li je SUDREG API dostupan.

    Returns:
        bool: True ako je API dostupan ili False ako je nedostupan nakon maksimalnog broja pokušaja.
    """
    retries = 120

    for attempt in range(retries):
        try:
            logging.info(
                f"Provjera dostupnosti SUDREG API-a {response.url}: {attempt + 1}/{retries}..."
            )

            if response.status_code == 200:
                logging.info(f"SUDREG API {response.url} je dostupan.")
                logging.info("-" * 100)
                return True
            elif response.status_code == 503:
                logging.info(
                    f"SUDREG API {env('SUDREG_URL')} je privremeno nedostupan."
                )
                time.sleep(5)
                continue
            else:
                logging.warning(
                    f"SUDREG API {env('SUDREG_URL')} je nedostupan: {response.status_code}."
                )
                logging.info("-" * 100)

        except requests.exceptions.Timeout:
            logging.warning(f"Timeout: {attempt + 1}...")
        except requests.exceptions.ConnectionError:
            logging.warning(f"Greška u konekciji: {attempt + 1}...")
        except requests.exceptions.RequestException as e:
            logging.error(f"Greška u zahtjevu: {e}...")

        if attempt < retries - 1:
            wait_time = 2**attempt
            logging.info(
                f"Čekam {wait_time} sekundi prije ponovnog pokušaja spajanja..."
            )
            time.sleep(wait_time)

    logging.error("SUDREG API nije dostupan nakon maksimalnog broja pokušaja!")
    logging.error(
        f"Za prijavu greške, kontaktirajte sudski.registar@pravosudje.hr sa X-Log-Id ({response.headers['X-Log-Id']}).")

    return False


def _report_connection_error(exception: str) -> None:
    """
    Logira greške prilikom spajanja na SUDREG API.
    Primarno za bypass-a HNB proxy-a, ali i sve ostale greške koje se mogu
    javiti.

    Args:
        exception (str): Tekst expcetion koji se javio prilikom pokušaja spajanja na
                         SUDREG API.

    Raises:
        OSError: Ako nije moguće pristupiti SUDREG API-u zbog proxy-a.
        RuntimeError: Ako iz bilo kojeg drugog razloga nije moguće pristupiti SUDREG API-u.
    """
    if "Tunnel connection failed: 407 Proxy Authentication Required" in exception:
        error_msg = "Nije moguće pristupiti Sudreg API-u. Prijavite se ili onemogućite HNB Proxy!"
        logging.error(error_msg)
        raise OSError(error_msg)
    else:
        error_msg = f"Nije moguće pristupiti SUDREG API-u: {exception}"
        logging.error({error_msg})
        raise RuntimeError(error_msg)


def check_api_definition() -> None:
    """
    Provjera jesu li lokalni i web SUDREG API konfiguracijski file jednaki.
    Ako postoje razlike, kreira se novi SUDREG API konfiguracijski file na mjestu staroga.
    """
    # Provjera i preuzimanje najnovije verzije SUDREG API konfiguracijskog filea
    global _api_definition_checked

    # Provjeri samo jednom po pokretanju programa
    if _api_definition_checked:
        return

    logging.info("Provjeravam SUDREG API definiciju...")

    try:
        with requests.get(env("SUDREG_API_DEF_URL"), verify=True, timeout=60) as r:
            _check_api_availability(r)
    except OSError as e:
        _report_connection_error(str(e))

    # Čitanje lokalne verzije SUDREG API konfiguracije
    with open(env("SUDREG_API_DEF_PATH"), "r", encoding="utf8") as file:
        # Formatiranje lokalne verzije SUDREG API konfiguracije
        local_API_definition = json.dumps(json.load(file), indent=2, ensure_ascii=False)

    # Formatiranje online verzije SUDREG API konfiguracije
    online_API_definition = json.dumps(r.json(), indent=2, ensure_ascii=False)

    # Usporedba lokalne i preuzete verzije SUDREG API konfiguracije
    if local_API_definition == online_API_definition:
        logging.info("Lokalni SUDREG API konfiguracijski file je up to date.")
    else:
        logging.warning("Postoji nova verzija SUDREG API konfiguracijskog filea.")
        # Spremanje nove verzije SUDREG API konfiguracijskog filea na mjesto staroga
        with open(env("SUDREG_API_DEF_PATH"), "w", encoding="utf8") as f:
            f.write(online_API_definition)
        logging.info(
            "Ažurirana verzija SUDREG API konfiguracijskog filea."
        )
        # Slanje maila upozorenja da je došlo do promjene SUDREG API konfiguracijskog filea
        send_warning_notification()

    _api_definition_checked = True


def _get_oauth_token() -> Dict:
    """
    Dohvaća i vraća 0Auth2 pristupni token sa SUDREG API-a.
    Računa i sprema vrijeme trajanja tokena u token dict.

    Returns:
        Dict: Dictionary lista podataka vezanih za access token.
              npr. 'access-token': '', 'token_type': '',
                   'expires_in': '' ...
    """
    try:
        with requests.post(
                env("SUDREG_TOKEN_URL"),
                data={"grant_type": "client_credentials"},
                auth=(env("SUDREG_CLIENT_ID"), env("SUDREG_CLIENT_SECRET"),),
                verify=True,
                timeout=60
        ) as response:
            _check_api_availability(response)
    except OSError as exception:
        _report_connection_error(str(exception))

    access_token = response.json()
    access_token["expires_in_min"] = int(access_token["expires_in"] / 60)
    access_token["expiration_time"] = (datetime.now() + timedelta(seconds=access_token["expires_in"])).isoformat()

    logging.info(f"OAuth2 token uspješno dohvaćen. Token traje {access_token['expires_in_min']} minuta do {access_token['expiration_time']}")

    return access_token


def get_sudreg_api_header() -> Dict:
    """
    Vraća POST request header potreban za SUDREG API.
    Dohvaća/ažurira ako OAuth2 token ne postoji/je istekao.

    Returns:
        Dict: Dictionary sa poljima potrebnim za autorizaciju
              na SUDREG API.

    Raises:
        ValueError: Ako polje 'expiration_time' ne postoji u access tokenu.
    """
    global _sudreg_access_token

    # Provjeri API definiciju prvi put kad se pozove ova funkcija
    check_api_definition()

    # Provjera postoji li token i je li još uvijek valjan
    if len(_sudreg_access_token) > 0 and "expiration_time" in _sudreg_access_token:
        # Dodajemo 5 minuta buffer prije isteka tokena za sigurnost
        expiration_with_buffer = datetime.fromisoformat(_sudreg_access_token["expiration_time"]) - timedelta(minutes=5)

        if datetime.now() < expiration_with_buffer:
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_sudreg_access_token['access_token']}",
            }
        else:
            logging.info("OAuth2 token je istekao ili je blizu isteka. Dohvaćam novi token...")

    # Dohvaćanje novog tokena ako ne postoji ili je istekao
    _sudreg_access_token = _get_oauth_token()

    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_sudreg_access_token['access_token']}",
    }


def get_snapshot_id() -> int | None:
    """
    Dohvaća najsvježiji snapshots_id.

    Returns:
         int | None: Najnoviji (najveći) snapshots_id ili None
    """
    url = env("SUDREG_SNAPSHOTS_URL")
    logging.info("Dohvaćam najsvježiji snapshot_id...")

    try:
        with requests.get(
                url,
                headers=get_sudreg_api_header(),
                params={
                    "limit": 10000,
                    "offset": 0,
                    "only_active": "false",
                    "expand_relations": "false",
                },
                verify=True
        ) as response:

            snapshot_id = 0
            for item in response.json():
                if item["id"] > snapshot_id:
                    snapshot_id = item["id"]

            logging.info(f"Dohvaćen snapshot_id {snapshot_id}")

            return snapshot_id
    except Exception as e:
        logging.warning(f"Došlo je do greške prilikom dohvata snapshots_id: {e}")
        logging.warning("Dohvat podataka će koristiti defaultni snapshots_id.")
        return None


def get_table_counts() -> Dict[str, int] | None:
    """
    Dohvaća broj redaka za svaku tablicu.

    Returns:
        Dict[str, int] | None: {"naziv_tablice": broj_redaka} ili None.
    """
    url = env("SUDREG_COUNTS_URL")

    try:
        with requests.get(
                url,
                headers=get_sudreg_api_header(),
                params={
                    "limit": 10000,
                    "offset": 0,
                    "only_active": "false",
                    "expand_relations": "false",
                },
                verify=True
        ) as response:
            table_rows = {}
            for item in response.json():
                item["table_name"] = item["table_name"][4:]
                table_rows[item["table_name"].lower()] = item["count_svi"]

            return table_rows
    except Exception as e:
        logging.warning(f"Došlo je do greške prilikom dohvata counts za tablice: {e}")
        logging.warning("Dohvat podataka se nastavlja bez provjere broja dohvaćenih redaka.")
        return None


def reset_sudreg_token() -> None:
    """
    Briše trenutni OAuth2 token iz memorije.
    Za testiranje ili forsiranje dohvaćanja novog tokena.
    """
    global _sudreg_access_token
    _sudreg_access_token = {}
    logging.info("OAuth2 token je resetiran.")
