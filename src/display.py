from __future__ import annotations
import os
import platform
from colorama import Fore, Style, init

from models import Anime

init(autoreset=True)

def clear_screen() -> None:
    """
    Clear the terminal screen,
    works on Windows and UNIX-like
    systems.
    """
    os.system("cls" if platform.system() == "Windows" else "clear")

def print_anime_list(animes: list[Anime]) -> None:
    """
    Print a list of Anime to the terminal
    """
    if not animes:
        print(f"{Fore.RED}(!) WARNING: no anime parsed{Style.RESET_ALL}")
        return

    for anime in animes:
        episodes_str = anime.episodes if anime.episodes is not None else "?"
        print(f"{Fore.CYAN}{anime.rank}. {Style.BRIGHT}{anime.title}{Style.RESET_ALL}"
              f"  (Score: {anime.score}{Style.RESET_ALL})")
        print(f"    {Fore.RED}URL:{Style.RESET_ALL} {Fore.GREEN}{anime.url}{Style.RESET_ALL}")
        print(f"    {Fore.MAGENTA}Type:{Style.RESET_ALL} {anime.anime_type} "
              f"{episodes_str} eps")
        print(f"    {Fore.MAGENTA}Aired:{Style.RESET_ALL} {anime.start_date} - {anime.end_date}")
        print(f"    {Fore.MAGENTA}Members:{Style.RESET_ALL} {anime.members:,}")
        print()

def print_single_anime(anime: Anime) -> None:
    """
    Print one Anime using the same formatting as the list view.
    """
    print_anime_list([anime])
