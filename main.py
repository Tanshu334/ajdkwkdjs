import re
import requests
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://gateway.platoboost.com/a/8?id=1631533348")
    page.wait_for_timeout(7000)
    page.get_by_role("button", name="Continue").click(force=True)
    page.wait_for_url(re.compile(r"^https://linkvertise\.com"))
    response = requests.get(f"https://ancient-dew-2472.fly.dev/api?url={page.url}")
    
    browser.close()