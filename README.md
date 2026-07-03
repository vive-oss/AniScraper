<img width="1250" height="200" alt="image" src="https://github.com/user-attachments/assets/6ab7e836-c5a1-482d-87ff-55ecae105779" />

# AniScraper

A simple web scraper for MyAnimeList, built to help me figure out what anime to watch next.

AniScraper pulls data from MyAnimeList's Top Anime list and randomly picks one for you to watch - no more endless scrolling trying to decide.

## Features

- Scrapes MyAnimeList's Top Anime rankings (you choose the range at runtime, e.g. top 300, top 10000, up to ~30,150)
- Extracts key info for each anime: rank, title, URL, score, type, episode count, air dates, and member count
- Randomly selects a single title from within your chosen range
- Only fetches the one page it actually needs - not the entire list - so it's fast and light on requests
- Re-roll as many times as you want in one session; type `q` to quit
- Color-coded terminal output

## Project structure

```
src/
├── main.py      # entry point - runs the input loop and ties everything together
├── scraper.py   # fetches pages from MyAnimeList and parses anime data out of the HTML
├── display.py   # terminal output, colors, and screen clearing
└── models.py    # the Anime data structure
```

## Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
beautifulsoup4==4.15.0
certifi==2026.6.17
charset-normalizer==3.4.7
colorama==0.4.6
idna==3.18
lxml==6.1.1
requests==2.34.2
soupsieve==2.8.4
typing_extensions==4.15.0
urllib3==2.7.0
```

## Usage

```bash
python3 src/main.py
```

You'll be asked how large a pool to randomize from (e.g. top 300). AniScraper fetches just the one page your random pick lands on, parses it, and prints the result. Enter a new number to roll again, or type `q` to quit.

## How it works

1. You enter a number **N** - the size of the top-ranked pool to pick from (e.g. top 300).
2. AniScraper picks a random rank between 1 and N.
3. It calculates which MyAnimeList results page that rank falls on (MAL lists 50 anime per page) and fetches **only that page**.
4. It parses just the single row matching your random rank out of that page's HTML - title, rank, score, type, episode count, air dates, and member count - using BeautifulSoup.
5. The result is printed to your terminal, color-coded for readability.
6. You can roll again immediately, or quit.

This approach means AniScraper never needs to download or parse the entire ranked list just to give you one pick - only the page containing your random result is ever fetched.

## Disclaimer

This project is for personal/educational use only. Please be respectful of MyAnimeList's terms of service and rate limits when scraping.
