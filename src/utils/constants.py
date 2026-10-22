from fake_useragent import UserAgent

ua = UserAgent()

BASE_URL = "https://my.telegram.org"

HEADERS = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://my.telegram.org',
    'Referer': 'https://my.telegram.org/auth',
}

BANNER = """
_______       ______  __             _____
___    |      ___  / / /___  __________  /_____________
__  /| |      __  /_/ /_  / / /_  __ \\  __/  _ \\_  ___/
_  ___ |      _  __  / / /_/ /_  / / / /_ /  __/  /
/_/  |_|      /_/ /_/  \\__,_/ /_/ /_/\\__/ \\___//_/

"""
