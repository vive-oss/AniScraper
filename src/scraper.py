from __future__ import annotations
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from models import Anime

_URL = "https://myanimelist.net/topanime.php"
TIMEOUT_SECONDS = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def extract_number(text: str | None) -> int:
    """Return the first integer in a string, or 0 if none exists."""
    if not text:
        return 0
    match = re.search(r"\d+", text.replace("\xa0", " "))
    return int(match.group()) if match else 0


def parse_type_episodes(text: str) -> tuple[str, int | None]:
    """Parse 'TV (28 eps)' into ('TV', 28)."""
    match = re.match(r"(\w+)\s*\((\d+)\s*eps?\)", text)
    if match:
        return match.group(1), int(match.group(2))
    return text, None


def parse_airtime(text: str) -> tuple[str, str]:
    """Parse 'Sep 2023 - Mar 2024' into ('Sep 2023', 'Mar 2024')."""
    if "-" in text:
        start, _, end = text.partition("-")
        return start.strip(), end.strip() or "N/A"
    return text.strip(), "N/A"


def parse_info(info_tag) -> dict:
    """Break the <div class="information"> block into structured fields."""
    if not info_tag:
        return {"type": "N/A", "episodes": None, "start": "N/A", "end": "N/A", "members": 0}

    raw = info_tag.get_text("\n", strip=True)
    parts = [p.strip() for p in raw.split("\n") if p.strip()]
    anime_type, episodes = parse_type_episodes(parts[0]) if len(parts) > 0 else ("N/A", None)
    start, end = parse_airtime(parts[1]) if len(parts) > 1 else ("N/A", "N/A")
    members = extract_number(parts[2]) if len(parts) > 2 else 0
    return {
        "type": anime_type,
        "episodes": episodes,
        "start": start,
        "end": end,
        "members": members,
    }


def fetch_html(url: str = _URL) -> str:
    """Download a page and return its HTML."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except RequestException as exc:
        raise RuntimeError(f"(!) Failed to fetch {url}, {exc}") from exc
    return response.text


def get_anime_by_rank(rank: int) -> Anime | None:
    """Fetch and parse the single Anime at the given overall rank."""
    page = (rank - 1) // 50 + 1
    offset = (page - 1) * 50
    row_index = (rank - 1) % 50
    page_url = f"{_URL}?limit={offset}"
    html = fetch_html(page_url)
    soup = BeautifulSoup(html, "lxml")
    rows = soup.select("tr.ranking-list")
    if row_index >= len(rows):
        return None
    target_row = rows[row_index]
    return row_to_anime(target_row)


def row_to_anime(row) -> Anime | None:
    """Convert a single <tr class='ranking-list'> element into an Anime object."""
    title_link = row.select_one("h3.anime_ranking_h3 a")
    if title_link is None:
        return None
    href = title_link.get("href")
    anime_url = urljoin(_URL, href if isinstance(href, str) else "")
    rank_tag = row.select_one("td.rank span")
    score_tag = row.select_one("td.score span.text")
    info_tag = row.select_one("div.information")

    info = parse_info(info_tag)

    return Anime(
        rank=extract_number(rank_tag.get_text() if rank_tag else None),
        title=title_link.get_text(" ", strip=True),
        url=anime_url,
        score=score_tag.get_text(strip=True) if score_tag else "N/A",
        anime_type=info["type"],
        episodes=info["episodes"],
        start_date=info["start"],
        end_date=info["end"],
        members=info["members"],
    )
