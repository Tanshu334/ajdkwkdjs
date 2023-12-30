import re
import requests
from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/bypasskey/system/delta")
def delta():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        link = "https://gateway.platoboost.com/a/8?id=4231523548"
        id = link.split("id=")[1]
        page.goto(link)
        page.wait_for_selector("button:text('Continue')")
        page.get_by_role("button", name="Continue").click(force=True)
        page.wait_for_url(re.compile(r"^https://linkvertise\.com"))
        url = page.url
        page.goto("https://adlinkbypass.com/")
        page.get_by_role("textbox").fill(url)
        page.get_by_role("button", name="Bypass").click()
        page.get_by_role("button", name="Copy").click()
        elements = page.query_selector_all("div")
        for element in elements:
            text = element.inner_text()
            if "https://gateway.platoboost.com" in text:
                url2 = text
        page.goto(url2)
        page.wait_for_selector("button:text('Continue')")
        page.get_by_role("button", name="Continue").click(force=True)
        page.wait_for_timeout(3000)
        response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        data = response.json()
        browser.close()
        return jsonify({"status": "success", "key": data["key"]}), 200