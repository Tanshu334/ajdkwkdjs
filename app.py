#API made by very.tuff.no.cap (display name: very tuff cat) on discord.
import re
import requests
import sys
import os
from flask import Flask, jsonify, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)
browser = None
context = None
with sync_playwright() as p: #launching the browser and creating a context to save time.
    browser = p.chromium.launch()
    context = browser.new_context()

@app.route("/")
def index():
    return "You aren't supposed to be here. Go away :("

@app.route("/bypasskey/system/delta", methods=["GET"])
def delta():
    try:
        page = context.new_page()
        link = request.args.get("link")
        if not link or "id=" not in link:
            return jsonify({"status": "Error", "message": "MethodNotAllowed"}), 404

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

        return jsonify({"status": "success", "key": data["key"]}), 200
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"An error occurred in {fname} on line {exc_tb.tb_lineno}: {e}")
        return jsonify({"status": "fail", "message": "An error has occured. The developer has been notified and he will fix it ASAP."}), 400
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")