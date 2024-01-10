import re
import requests
import sys
import random
from flask import Flask, render_template, jsonify, request, redirect
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def index():
    return redirect('https://yxubot.vercel.app/')

@app.route("/bypasskey/system/delta", methods=["GET"])
def delta():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            frames = page.frames

            link = request.args.get("link")
            if not link or "id=" not in link:
                return jsonify({"status": "error", "message": "MethodNotAllowed"}), 400

            id = link.split("id=")[1]

            page.goto(link)
            for frame in frames:
                if re.match(r"^https://challenges.cloudflare.com/cdn-cgi", frame.url):
                    element = frame.locator('.mark')
                    page.wait_for_timeout(3000)
                    element.check()
                    break
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
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occured on line {sys.exc_info()[-1].tb_lineno}:\n{e}"})
    
@app.route("api/v1/Bypass/hydrogen")
def hydrogen():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        link = request.args.get("link")

        if not link or not "method" in link:
            return jsonify({"status": "error", "message": "Forbidden Method"})
        
        page.wait_for_selector("button:text('Get Key')")
        page.get_by_role("button", name="Get Key").click()
        page.wait_for_url(re.compile(r"^https://linkvertise\.com"))
        page.wait_for_timeout(1000)
        page.go_back()

        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=25585)