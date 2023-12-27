import re
from playwright.sync_api import Page, expect

def test_main(page: Page):
    page.goto()