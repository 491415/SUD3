import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict

import requests
from environs import env
from requests import Response

from src.logger.Logger import Logger
from src.utils.send_mail import send_warning_notification


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
        logging.warning(f"Postoji nova verzija SUDREG API konfiguracijskog filea.")
        # Spremanje nove verzije SUDREG API konfiguracijskog filea na mjesto staroga
        with open(env("SUDREG_API_DEF_PATH"), "w", encoding="utf8") as f:
            f.write(online_API_definition)
        logging.info(
            f"Ažurirana verzija SUDREG API konfiguracijskog filea."
        )
        # Slanje maila upozorenja da je došlo do promjene SUDREG API konfiguracijskog filea
        send_warning_notification()


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
                proxies={'http': os.environ['HTTP_PROXY']},
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
    sudreg_access_token = {}

    if len(sudreg_access_token) == 0:
        sudreg_access_token = _get_oauth_token()

    if "expiration_time" in sudreg_access_token:
        if datetime.now() > datetime.fromisoformat(sudreg_access_token["expiration_time"]):
            logging.info("OAuth2 token je istekao. Dohvaćam novi token...")
            sudreg_access_token = _get_oauth_token()
    else:
        error_msg = "Polje 'expiration_time' ne postoji u access token dictionaryu."
        logging.error(error_msg)
        raise ValueError(error_msg)

    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sudreg_access_token['access_token']}",
    }


if __name__ == "__main__":
    log = Logger(datetime.now().strftime(env("DATE_FORMAT")), __file__)
    check_api_definition()
