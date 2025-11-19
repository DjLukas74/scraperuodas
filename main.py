from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import csv
import os

COOKIE_FILE = "cookies.json"


def fetch_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Load cookies if available
        if os.path.exists(COOKIE_FILE):
            try:
                with open(COOKIE_FILE, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                context.add_cookies(cookies)
                print("[INFO] Loaded cookies.json")
            except Exception as e:
                print("[WARN] Failed to load cookies.json:", e)
        else:
            print("[INFO] No cookies.json found → scraping without cookies")

        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        html = page.content()
        browser.close()
        return html


def extract_search_block(html):
    soup = BeautifulSoup(html, "html.parser")
    block = soup.find("div", class_="list-search-v2")

    if not block:
        return None, 0

    num_el_html = block.select_one(".search-mark-v2 .number")
    if num_el_html:
        num_el_txt = num_el_html.get_text(strip=True).strip("()")
        total = int(num_el_txt)
    else:
        total = None

    return block, total


def parse_entries(block):
    entries = []

    if not block:
        return entries

    rows = block.find_all("div", class_="list-row-v2")
    for row in rows:
        entry = {}

        price_el = row.select_one(".list-item-price-v2")
        entry["price"] = price_el.get_text(strip=True) if price_el else None

        price_m2_el = row.select_one(".price-pm-v2")
        entry["price_m2"] = price_m2_el.get_text(strip=True) if price_m2_el else None

        area_el = row.select_one(".list-AreaOverall-v2")
        entry["area_m2"] = area_el.get_text(strip=True) if area_el else None

        addr_link = row.select_one(".list-adress-v2 h3 a")
        entry["address"] = addr_link.get_text(" ", strip=True) if addr_link else None
        entry["url"] = addr_link.get("href") if addr_link else None

        entries.append(entry)

    return entries


def export(entries):

    # --------------------------------------------------------
    # REMOVE EXACT DUPLICATES
    # --------------------------------------------------------
    seen = set()
    unique_entries = []

    for entry in all_entries:
        # convert dict to a tuple of sorted items for hashing
        t = tuple(sorted(entry.items()))
        if t not in seen:
            seen.add(t)
            unique_entries.append(entry)

    all_entries = unique_entries

    # --------------------------------------------------------
    # EXPORT: JSON
    # --------------------------------------------------------
    with open("aruodas_listings.json", "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=4)
        print("Saved: aruodas_listings.json")

    # --------------------------------------------------------
    # EXPORT: CSV
    # --------------------------------------------------------
    csv_fields = ["price", "price_m2", "area_m2", "address", "url"]
    
    with open("aruodas_listings.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(all_entries)
        print("Saved: aruodas_listings.csv")


# --------------------------------------------------------
# MULTI-PAGE LOOP
# --------------------------------------------------------

if __name__ == "__main__":
    base_url = "https://www.aruodas.lt/butai/vilniuje/"
    page_url = base_url

    html = fetch_page(page_url)
    if not html:
        print("Failed to fetch the initial page.")
        exit(1)
    block, total_entries = extract_search_block(html)

    all_entries = []
    all_entries.extend(parse_entries(block))

    print(f"Page 1 done. Parsed {len(all_entries)} / {total_entries}")

    current_page = 2

    # Loop until we collect all entries
    while len(all_entries) < total_entries:
        page_url = f"{base_url}puslapis/{current_page}/"
        print(f"Fetching page {current_page}: {page_url}")

        html = fetch_page(page_url)
        block, _ = extract_search_block(html)   # total not needed anymore
        entries = parse_entries(block)

        if not entries:
            print("No more entries found. Stopping.")
            break

        all_entries.extend(entries)
        print(f"Page {current_page} done. Parsed {len(all_entries)} / {total_entries}")

        current_page += 1

    print(f"\nFinished. Parsed {len(all_entries)} entries.")
    export(all_entries)
