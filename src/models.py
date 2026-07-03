from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Anime:
    title: str
    rank: int
    url: str
    score: str
    anime_type: str
    episodes: int | None
    start_date: str
    end_date: str
    members: int
