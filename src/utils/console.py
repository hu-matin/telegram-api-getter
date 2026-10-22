from colorama import Fore, Style
from time import sleep
import sys
import os



def typing_effect(text: str, delay: float = 0.03, color: str = Fore.GREEN) -> None:
    for char in text:
        sys.stdout.write(f"{color}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        sleep(delay)
    print()

def clear() -> None:
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def log(message: str, level: str = "info") -> None:
    styles = {
        "info": (Fore.CYAN, "[*]"),
        "success": (Fore.GREEN, "[+]"),
        "error": (Fore.RED, "[!]"),
        "warning": (Fore.YELLOW, "[~]"),
    }

    color, symbol = styles.get(level, (Fore.WHITE, "[*]"))
    print(f"{color}{symbol} {message}{Style.RESET_ALL}")



def banner(banner: str, delay: float = 0.01) -> None:
    typing_effect(banner, delay, Fore.CYAN)



def project_info(author: str, link: str, version: str) -> None:
    author_line = f"- Created by: {author}"
    v_line = f"- Version: {version}"
    so_link = f"- Link: {link}"

    typing_effect(author_line, delay=0.02, color=Fore.BLUE)
    typing_effect(v_line, delay=0.02, color=Fore.BLUE)
    typing_effect(so_link, delay=0.02, color=Fore.BLUE)

    print()
