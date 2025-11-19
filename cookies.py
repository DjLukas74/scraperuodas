from playwright.sync_api import sync_playwright
import json
import time

URL = "https://www.aruodas.lt/butai/vilniuje/"

def save_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)   # <- visible browser
        context = browser.new_context()

        page = context.new_page()
        page.goto(URL)

        print("\n=== Solve CAPTCHA manually ===")
        print("Leave this window open until the page fully loads.")
        print("When listings appear, close the browser window.\n")

        # Wait until user closes the browser manually
        # (Playwright throws an exception, so we just catch it)
        try:
            while True:
                time.sleep(1)
        except:
            pass

        # Save cookies
        cookies = context.cookies()
        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=4)

        print("Cookies saved to cookies.json")


if __name__ == "__main__":
    save_cookies()