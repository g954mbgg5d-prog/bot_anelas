
# test_cdp.py

from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.connect_over_cdp(
        "http://127.0.0.1:9222"
    )

    print("Conectado")

    print(browser.contexts)

    for ctx in browser.contexts:
        for page in ctx.pages:
            print(page.title())
            print(page.url)
