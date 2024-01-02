import re
import requests
from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello Niggers!"

def create_app():
    return app

@app.route("/bypasskey/system/delta", methods=["GET"])
def delta():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        link = request.args.get("link")
        if not link or "id=" not in link:
            return jsonify({"status": "⚠️Error", "message": "MethodNotAllowed"}), 400

        id = link.split("id=")[1]

        page.goto(link)
        page.wait_for_selector("button:text('Continue')")
        page.get_by_role("button", name="Continue").click(force=True)
        page.wait_for_url(re.compile(r"^https://linkvertise\.com"))
        url = page.url()

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
        
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)