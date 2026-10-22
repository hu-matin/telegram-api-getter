import re
from urllib.parse import urljoin
import requests
from time import sleep
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

from src.crawler import extract_data
from src.tg_app import create_app
from src.utils.console import banner, clear, log, project_info
from src.utils.metadata import metadata
from src.utils.constants import BANNER, BASE_URL, HEADERS

init(autoreset=True)

def main() -> None:
    clear()

    banner(BANNER, delay=0.005)

    metas = metadata()
    project_info(
        author=metas["author"],
        link=metas["channel"],
        version=metas["version"]
    )

    phone_input = input(f"\n{Fore.GREEN}Enter your number with country code (e.g., +989123456789): {Fore.YELLOW}").strip()

    phone_number = re.sub(r'[\s\-()]', '', phone_input)
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number

    if not re.match(r'^\+\d{7,15}$', phone_number):
        log("Invalid phone number format. Please use international format.", "error")
        return

    with requests.Session() as session:
        session.headers.update(HEADERS)

        log("Requesting confirmation code from Telegram...", "info")
        try:
            send_resp = session.post(
                urljoin(BASE_URL, 'auth/send_password'),
                data={'phone': phone_number},
                headers={'X-Requested-With': 'XMLHttpRequest'},
                timeout=15
            )
        except requests.RequestException as e:
            log(f"Network error while connecting to Telegram: {e}", "error")
            return

        if 'Sorry, too many tries' in send_resp.text:
            log("Account temporarily rate-limited. Please wait a few hours and try again.", "error")
            return

        try:
            send_data = send_resp.json()
            random_hash = send_data.get('random_hash')
            if not random_hash:
                log("Failed to retrieve random hash from Telegram response.", "error")
                return
        except Exception:
            log("Failed to parse Telegram response (invalid JSON).", "error")
            return

        log("Confirmation code sent to your Telegram app!", "success")

        code = input(f"{Fore.GREEN}Enter the code sent to your Telegram account: {Fore.YELLOW}").strip()
        if not code:
            log("Confirmation code cannot be empty.", "error")
            return

        log("Logging in to my.telegram.org...", "info")
        try:
            login_resp = session.post(
                urljoin(BASE_URL, '/auth/login'),
                data={'phone': phone_number, 'random_hash': random_hash, 'password': code, 'remember': '1'},
                headers={'X-Requested-With': 'XMLHttpRequest'},
                timeout=15
            )
        except requests.RequestException as e:
            log(f"Network error during login: {e}", "error")
            return

        if login_resp.status_code != 200 or login_resp.text.strip().lower() != 'true':
            err_msg = login_resp.text.strip() or f"HTTP {login_resp.status_code}"
            log(f"Login failed: {err_msg}", "error")
            return

        log("Login successful!", "success")

        log("Fetching API configuration page...", "info")
        try:
            apps_page = session.get(
                urljoin(BASE_URL, '/apps'),
                headers={'Referer': BASE_URL},
                timeout=15
            )
        except requests.RequestException as e:
            log(f"Network error while fetching apps page: {e}", "error")
            return

        if '/auth' in apps_page.url or 'my_login_form' in apps_page.text:
            log("Session expired or redirected to login. Please try again.", "error")
            return

        soup = BeautifulSoup(apps_page.text, 'html.parser')

        if soup.find('form', action=re.compile(r'/apps/create')):
            log("No existing app found. Attempting to create one automatically...", "warning")
            if not create_app(session, soup):
                log("Failed to create Telegram application automatically.", "error")
                return

            apps_page = session.get(urljoin(BASE_URL, '/apps'), timeout=15)
            soup = BeautifulSoup(apps_page.text, 'html.parser')

        data = extract_data(apps_page.text, soup)
        api_id = data["api_id"]
        api_hash = data["api_hash"]
        key = data["key"]
        pc = data["pc"]

        if not api_id or not api_hash:
            log("Failed to extract API credentials. Page layout may have changed.", "error")
            return

        sleep(1)
        print(f"\n{Fore.CYAN}APIs successfully received:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}+{Style.RESET_ALL} Api ID   : {Fore.YELLOW}{api_id}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}+{Style.RESET_ALL} Api HASH : {Fore.YELLOW}{api_hash}{Style.RESET_ALL}")

        if key:
            print(f"  {Fore.GREEN}~{Style.RESET_ALL} Public Key        : {Fore.YELLOW}{key}{Style.RESET_ALL}")
        if pc:
            print(f"  {Fore.GREEN}~{Style.RESET_ALL} Production Config : {Fore.YELLOW}{pc}{Style.RESET_ALL}")

        log("Done! You can now use your Telegram API credentials.", "success")
