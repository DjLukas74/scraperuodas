# scraperuodas

Scraper for aruodas.lt listings (e.g. `/butai/vilniuje/`) using Playwright and BeautifulSoup.

## Requirements
- Python 3.8+
- Internet access
- The following Python packages:
  - playwright
  - beautifulsoup4
  - lxml

## Setup

### Local Python
Install dependencies:
```bash
python3 -m pip install playwright beautifulsoup4 lxml
python3 -m playwright install chromium
```

### Docker
Build and run the container (recommended for headless scraping):
```bash
docker build -t scraperuodas .
docker run --rm scraperuodas
```

## Usage

- By default, the scraper fetches `/butai/vilniuje/` and parses all listings.
- It uses Playwright to render the page and BeautifulSoup to extract listing data.
- Results are saved to `aruodas_listings.json` and `aruodas_listings.csv`.
- Cookie support: If a `cookies.json` file is present, it will be loaded for authentication/session reuse.

## Output
- Listings are exported to:
  - `aruodas_listings.json` (full data)
  - `aruodas_listings.csv` (tabular data)

## Notes
- The scraper loops through all result pages until all listings are collected.
- If the site blocks requests, Playwright will solve most JS challenges.
- Respect robots.txt and site terms before scraping.

## Example
```bash
python3 main.py
```

Or with Docker:
```bash
docker build -t scraperuodas .
docker run --rm scraperuodas
```

---
web scraper for aruodas NT page
