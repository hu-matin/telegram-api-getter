import tomllib
from pathlib import Path

from typing import Any

def metadata() -> dict[str, Any]:
    root = Path(__file__).parent.parent.parent
    path = root / "pyproject.toml"

    with open(path, "rb") as f:
        data = tomllib.load(f)

    project_data = data.get("project", {})

    authors = project_data.get("authors", [{}])
    author_name = authors[0].get("name", "Unknown") if authors else "Unknown"

    return {
        "name": project_data.get("name", "ihgetter"),
        "version": project_data.get("version", ""),
        "description": project_data.get("description", "Telegram API Extractor"),
        "author": author_name,

        "channel": "https://t.me/ahunter0",
    }

def get_version() -> str:
    return metadata()["version"]

def get_author() -> str:
    return metadata()["author"]
