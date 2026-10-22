from urllib.parse import urljoin
import random
import string
import requests
from bs4 import BeautifulSoup

from src.utils.constants import BASE_URL, HEADERS



def create_app(session: requests.Session, soup: BeautifulSoup) -> bool:

    hash_input = soup.find('input', {'name': 'hash'})
    if not hash_input or not hash_input.get('value'):
        return False

    csrf_hash = hash_input['value']
    rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    app_title = f"MyTelegramApp_{rand_suffix}"
    app_name = f"app{rand_suffix}"

    payload = {
        'hash': csrf_hash,
        'app_title': app_title,
        'app_shortname': app_name,
        'app_url': 'https://telegram.org',
        'app_platform': 'desktop',
        'app_desc': 'Personal Telegram MTProto Developer Client',
    }

    headers = dict(HEADERS)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Referer'] = urljoin(BASE_URL, "/apps")

    try:
        resp = session.post(urljoin(BASE_URL, "/apps/create"), data=payload, headers=headers, timeout=15)

        if resp.status_code == 200:

            if 'ERROR' in resp.text:
                return False

            return True

        else:
            return False

    except Exception as e:

        return False
