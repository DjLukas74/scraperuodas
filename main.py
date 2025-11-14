from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        html = page.content()
        browser.close()
        return html

def extract_search_block(html):
    soup = BeautifulSoup(html, "html.parser")
    block = soup.find("div", class_="list-search-v2")
    return block


def parse_entries(block):
    entries = []

    # Each listing lives inside a div.list-row-v2 (sometimes multiple classes)
    rows = block.find_all("div", class_="list-row-v2")

    for row in rows:
        entry = {}

        # price
        price_el = row.select_one(".list-item-price-v2")
        entry["price"] = price_el.get_text(strip=True) if price_el else None

        # price €/m²
        price_m2_el = row.select_one(".price-pm-v2")
        entry["price_m2"] = price_m2_el.get_text(strip=True) if price_m2_el else None

        # area (m²)
        area_el = row.select_one(".list-AreaOverall-v2")
        entry["area_m2"] = area_el.get_text(strip=True) if area_el else None

        # address + URL
        addr_link = row.select_one(".list-adress-v2 h3 a")
        if addr_link:
            entry["address"] = addr_link.get_text(" ", strip=True)
            entry["url"] = addr_link.get("href")
        else:
            entry["address"] = None
            entry["url"] = None

        entries.append(entry)

    return entries

if __name__ == "__main__":
    url = "https://www.aruodas.lt/butai/vilniuje/"
    html = fetch_page(url)
    search_block = extract_search_block(html)
    entries = parse_entries(search_block)

    for e in entries:
        print(e)
