from typing import Any

from bs4 import BeautifulSoup, Tag
import re


def _extract_value(parent: Tag, pattern: str) -> str | None:
    if not (el := parent.find(['span', 'input', 'strong', 'code'])):

        return None

    value = str(el.get_text(strip=True) or el.get('value', ''))
    if matched := re.search(pattern, value):
        return matched.group(0)

    return None


def _extract_text(parent: Tag, tags: list[str]) -> str | None:
    if el := parent.find(tags):
        return el.get_text(strip=True)

    return None


def _extract_from_selectable(soup: BeautifulSoup, api_id: str | None, api_hash: str | None):
    def is_selectable(tag: Tag) -> bool:
        return tag.name in ['span', 'input'] and (
            'this.select()' in tag.get('onclick', '')
            or 'uneditable-input' in tag.get('class', [])
            or 'form-control' in tag.get('class', [])
        )

    for item in soup.find_all(is_selectable):
        value = str(item.get_text(strip=True) or item.get('value', ''))

        if not api_id and re.fullmatch(r'\d{5,12}', value):
            api_id = value

        elif not api_hash and re.fullmatch(r'[0-9a-fA-F]{32}', value):
            api_hash = value

    return api_id, api_hash


def _regex_fallback(html: str, pattern: str) -> str | None:
    if matched := re.search(pattern, html, re.I | re.S):
        return matched.group(1)
    return None


def extract_data(html: str, soup: BeautifulSoup) -> dict[str, Any]:

    api_id = api_hash = public_key = prod_config = None

    for element in soup.find_all(['label', 'span', 'strong', 'td', 'th']):
        if api_id and api_hash and public_key and prod_config:
            break

        text = element.get_text(strip=True).lower()
        parent = element.find_parent(['div', 'tr', 'fieldset']) or element

        match text:
            case t if not api_id and 'api_id' in t:
                api_id = _extract_value(parent, r'\b\d{5,12}\b')

            case t if not api_hash and 'api_hash' in t:
                api_hash = _extract_value(parent, r'\b[0-9a-fA-F]{32}\b')

            case t if not public_key and 'public key' in t:
                public_key = _extract_text(parent, ['code', 'pre', 'span'])

            case t if not prod_config and 'production configuration' in t:
                prod_config = _extract_text(parent, ['strong', 'code', 'span'])

    if not api_id or not api_hash:
        api_id, api_hash = _extract_from_selectable(soup, api_id, api_hash)


    api_id = api_id or _regex_fallback(html, r'api_id.*?(\b\d{5,12}\b)')
    api_hash = api_hash or _regex_fallback(html, r'api_hash.*?(\b[0-9a-fA-F]{32}\b)')

    if not public_key:
        if m := re.search(
            r'Public\s*keys?:.*?(-----BEGIN[^-]+-----.*?-----END[^-]+-----|<code[^>]*>(.*?)</code>)',
            html, re.I | re.S
        ):
            public_key = re.sub(r'<[^>]+>', '', (m.group(1) or m.group(2)).strip())

    if not prod_config:
        if m := re.search(
            r'Production\s*configuration:.*?<strong[^>]*>(.*?)</strong>',
            html, re.I | re.S
        ):
            prod_config = m.group(1).strip()

    return {
        "api_id": api_id,
        "api_hash": api_hash,
        "key": public_key,
        "pc": prod_config,
    }
