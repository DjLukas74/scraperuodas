from playwright.sync_api import sync_playwright

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
        page.goto(url, wait_until="domcontentloaded")   # more reliable
        page.wait_for_timeout(3000)                     # let JS run a bit

        html = page.content()
        browser.close()
        return html

if __name__ == "__main__":
    html = fetch_page("https://www.aruodas.lt/butai/vilniuje/")
    print(html)
