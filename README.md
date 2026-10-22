# ihgetter

A simple Python script to extract Telegram API ID and API Hash from my.telegram.org.

## What it does

Automates the process of logging into my.telegram.org and retrieving your API credentials. If no application exists, it attempts to create one automatically.

## Installation

```bash
git clone https://github.com/hu-matin/telegram-api-getter.git
cd ihgetter
uv sync
```

## Usage

You should just run it.
```python
python ihgetter.py
```

## Limitations

- Telegram may block automated app creation for new or flagged accounts
- If automatic creation fails, you'll need to create the app manually at my.telegram.org/apps
- This tool does not bypass Telegram's rate limits or security measures
